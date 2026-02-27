"""
İhale Dosyası Word Belge Oluşturucu.

Bu modül, kullanıcının form üzerinden girdiği bilgileri kullanarak
orijinal ihale dosyası şablonundaki sarı vurgulu alanları doldurur
ve yeni Word (.docx) ve PDF dosyaları oluşturur.

Temel İşlev:
    - Şablon .docx dosyasını okur
    - Sarı vurgulu run'ları tespit eder
    - Kullanıcı verilerini ilgili alanlara yerleştirir
    - Sarı vurguyu kaldırır (doldurulan alanlardan)
    - Yeni Word ve PDF dosyaları oluşturur
"""

import os
import sys
import re
import subprocess
import platform
from datetime import datetime, date, time
from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import Pt, RGBColor

# Modül yolunu ayarla (hem local hem cloud ortamında çalışması için)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field_config import UNIQUE_FIELDS, YELLOW_TO_UNIQUE_MAP, INSTRUCTION_FIELDS


def get_locative_suffix(word):
    """
    Kelimedeki son ünlüye ve ünsüze göre 'de/'da, 'te/'ta ekini döndürür.
    """
    if not word:
        return ""
    
    # Türkçe karakterleri destekle
    word_lower = word.strip().lower()
    
    # Son ünlü harfi bul
    vowels = "aeıioöuü"
    last_vowel = ""
    for char in reversed(word_lower):
        if char in vowels:
            last_vowel = char
            break
            
    if not last_vowel:
        return "'de" # varsayılan
        
    hard_consonants = "fstkçşhp"
    last_char = word_lower[-1]
    is_hard = last_char in hard_consonants
    
    if last_vowel in "aıou":
        return "'ta" if is_hard else "'da"
    else:
        return "'te" if is_hard else "'de"

def get_dative_suffix(time_str):
    """
    14:00 (on dört'e), 10:30 (otuz'a) vb. için yönelme (ismin -e hali) eki.
    """
    if not time_str:
        return "'e"
    
    # Saat 00 ile bitiyorsa saate bak, yoksa dakikaya bak
    parts = str(time_str).split(":")
    if len(parts) >= 2:
        hour = int(parts[0])
        minute = int(parts[1])
        if minute == 0:
            val = hour
        else:
            val = minute
            
        # Son rakamın okunuşuna göre ek
        last_digit = val % 10
        if val == 0: # sıfır -> a
            return "'a"
        if last_digit in [1, 2, 5, 7, 8]: # bir'e, iki'ye, beş'e, yedi'ye, sekiz'e -> e
            if last_digit == 2 or last_digit == 7:
                return "'ye"
            return "'e"
        elif last_digit in [3, 4, 0]: # üç'e, dört'e, (on'a, otuz'a, kırk'a, altmış'a) -> a/e
            if last_digit == 3 or last_digit == 4:
                return "'e"
            
            # 10, 30, 40, 50, 20
            if val == 10: return "'a" # on'a
            if val == 20: return "'ye" # yirmi'ye
            if val == 30: return "'a" # otuz'a
            if val == 40: return "'a" # kırk'a
            if val == 50: return "'ye" # elli'ye
            
            return "'a"
        elif last_digit in [6, 9]: # altı'ya, dokuz'a
            if last_digit == 6:
                return "'ya"
            return "'a"
            
    return "'e" # varsayılan


def _normalize_text(text):
    """Metni karşılaştırma için normalize eder."""
    if not text:
        return ""
    return text.strip().replace("\u00a0", " ").replace("  ", " ")


def _match_yellow_to_field(yellow_text):
    """
    Sarı vurgulu metni benzersiz alan ID'sine eşleştirir.
    """
    normalized = _normalize_text(yellow_text)

    # Direkt eşleşme
    if normalized in YELLOW_TO_UNIQUE_MAP:
        return YELLOW_TO_UNIQUE_MAP[normalized]

    # Talimat mı kontrol et (Kısmi eşleşmeden ÖNCE)
    for instruction in INSTRUCTION_FIELDS:
        if instruction in normalized or normalized in instruction:
            return None  # Talimat metni, form alanı değil

    # Kısmi eşleşme (sarı metin bir map anahtarını içeriyorsa)
    for key, field_id in YELLOW_TO_UNIQUE_MAP.items():
        if key in normalized or normalized in key:
            return field_id

    return None


def _format_field_value(field_id, value):
    """
    Alan değerini Word'de gösterilecek formata dönüştürür.
    """
    if value is None or value == "":
        return ""

    field_info = UNIQUE_FIELDS.get(field_id, {})
    field_type = field_info.get("type", "text")

    formatted = str(value)
    
    if field_type == "date":
        if isinstance(value, date):
            formatted = value.strftime("%d/%m/%Y")
        elif isinstance(value, str):
            formatted = value
    elif field_type == "time":
        if isinstance(value, time):
            formatted = value.strftime("%H:%M")
        elif isinstance(value, str):
            formatted = value
    elif field_type == "number":
        formatted = str(value)
        
    # Özel kural: Destek programı adı sonundaki "Programı" kelimesini sil.
    if field_id == "destek_programi_adi":
        formatted = re.sub(r'(?i)\s+programı$', '', formatted)
        
    return formatted


def generate_filled_document(template_path, form_data, output_dir="output"):
    """
    Şablon Word belgesini kullanıcı verileriyle doldurarak yeni belge oluşturur.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Şablonu aç
    doc = Document(template_path)

    # İstatistikler
    stats = {
        "total_yellow": 0,
        "filled": 0,
        "instruction_skipped": 0,
        "unmatched": 0,
    }

    # Context bilgileri
    context = {"in_davet_mektubu": False}

    # --- PARAGRAFLAR ---
    paragraphs_to_remove = []
    
    for para in doc.paragraphs:
        # Davet mektubu kontrolü
        if "İHALEYE DAVET MEKTUBU" in para.text:
            context["in_davet_mektubu"] = True
            
        # Değerlendirme paragrafı a)/b) kontrolü
        if context["in_davet_mektubu"]:
            text_norm = para.text.strip().lower()
            if text_norm.startswith("a)") and "mal alımı ve yapım" in text_norm:
                turu = form_data.get("ihale_turu")
                if turu == "Hizmet Alımı":
                    paragraphs_to_remove.append(para)
            elif text_norm.startswith("b)") and "hizmet alımlarında" in text_norm:
                turu = form_data.get("ihale_turu")
                if turu in ["Mal Alımı", "Yapım İşi"]:
                    paragraphs_to_remove.append(para)
                    
        # Madde 14: İSTEKLİLERE TALİMATLAR "Aşağıda yer alan maddeler..." silimi
        if "Aşağıda yer alan maddeler içerisindeki boş yerler" in para.text and "Diğer metinleri hiçbir şekilde değiştirmeyiniz" in para.text:
            paragraphs_to_remove.append(para)
            
        # Madde 17: İhale Usulü Kontrolü a) ve b) maddeleri
        if "İhaleye davet mektubu" in para.text and "Sadece Pazarlık Usulü" in para.text:
            if form_data.get("ihale_usulu") == "Açık İhale Usulü":
                paragraphs_to_remove.append(para)
                
        # Madde 24: Ön Ödeme Paragrafı Yeniden Yazımı
        if "Sözleşme kapsamında ön ödeme" in para.text:
            val = form_data.get("on_odeme")
            if val == "Yapılmayacaktır":
                para.text = "Sözleşme kapsamında ön ödeme yapılmayacaktır."
            elif val == "Yapılacaktır":
                oran = form_data.get("on_odeme_orani", "")
                para.text = f"Sözleşme kapsamında ön ödeme yapılacaktır. Ön ödeme miktarı sözleşme bedelinin % {oran}’sı olan ……………….. TL’dir. Ön ödeme, sözleşme imza tarihinden sonra 15 gün içerisinde belirlenen ön ödeme tutarı kadar avans teminat mektubunun sunulmasını takiben yapılacaktır."
            continue
            
        # Madde 25: Kesin Teminat Oranı İkinci Cümle
        if "Kesin teminat tutarı sözleşme bedelinin" in para.text and "olmalıdır" in para.text:
            val = form_data.get("kesin_teminat")
            if val == "İSTENMEMEKTEDİR":
                paragraphs_to_remove.append(para)
                continue
            elif val == "İSTENMEKTEDİR":
                oran = form_data.get("kesin_teminat_orani", "")
                para.text = f"Kesin teminat tutarı sözleşme bedelinin % {oran}’sı kadar olmalıdır."
                continue
        
        _process_paragraph_runs(para, form_data, stats, context)

    # Remove the explicitly deleted paragraphs correctly
    for p in paragraphs_to_remove:
        try:
            p1 = p._element
            p1.getparent().remove(p1)
            p._p = p._element = None
        except Exception:
            pass

    # --- TABLOLAR ---
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    _process_paragraph_runs(para, form_data, stats, context)

    # --- HEADER/FOOTER ---
    for section in doc.sections:
        for header in [section.header, section.first_page_header]:
            if header and header.is_linked_to_previous is False:
                for para in header.paragraphs:
                    _process_paragraph_runs(para, form_data, stats, context)
        for footer in [section.footer, section.first_page_footer]:
            if footer and footer.is_linked_to_previous is False:
                for para in footer.paragraphs:
                    _process_paragraph_runs(para, form_data, stats, context)

    # Dosya adı oluştur
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    kurum_adi = form_data.get("kurum_adi", "ihale")
    safe_name = re.sub(r'[^\w\s-]', '', kurum_adi).strip().replace(' ', '_')[:50]
    docx_filename = f"İhale_Dosyası_{safe_name}_{timestamp}.docx"
    docx_path = os.path.join(output_dir, docx_filename)

    # Kaydet
    doc.save(docx_path)

    result = {
        "docx": os.path.abspath(docx_path),
        "stats": stats,
    }

    # PDF dönüşümü dene
    try:
        pdf_path = _convert_to_pdf(docx_path)
        if pdf_path:
            result["pdf"] = pdf_path
    except Exception as e:
        result["pdf_error"] = str(e)

    return result


def _process_paragraph_runs(para, form_data, stats, context):
    runs = list(para.runs)
    if not runs:
        return

    # Önce "(i)", "(ii)", "(iii)" durumunu kontrol edelim (Davet mektubu mal listesi)
    if context.get("in_davet_mektubu") and any(m in para.text for m in ["(i)", "(ii)", "(iii)"]):
        # Eğer paragrafta sadece (i) ____________________ vb varsa
        ihale_konusu_text = form_data.get("ihale_konusu", "")
        lines = [line.strip() for line in ihale_konusu_text.splitlines() if line.strip()]
        
        for idx, marker in enumerate(["(i)", "(ii)", "(iii)"]):
            if marker in para.text:
                if idx < len(lines):
                    # Replace _________ with the line item
                    for r in runs:
                        r.text = r.text.replace("____________________", lines[idx])
                        r.text = r.text.replace("_________________", lines[idx])
                        r.font.bold = True
                else:
                    # Clear it completely if no item
                    for r in runs:
                        if marker in r.text or "_" in r.text:
                            r.text = ""

    # Madde 15: "e) Elektronik posta adresi…" -> ":"
    if "e) " in para.text and "Elektronik posta adresi" in para.text:
        for r in runs:
            r.text = r.text.replace("adresi…", "adresi:").replace("...", ":").replace("…", ":")
            
    # Madde 34: ">Projesi için" boşluk düzenlemesi
    for r in runs:
        if "Projesi için" in r.text:
            r.text = r.text.replace(">Projesi için", "> Projesi için").replace("Projesi için", " Projesi için").replace("  Projesi için", " Projesi için")

    # Madde 16, 18, 19, 20, 30, 38, 40: Gereksiz talimat metinlerini temizle
    for old_txt in [
        "<Örnek: TR21-11-İKT-1-XX>", "Örnek: TR21-11-İKT-1-XX",
        "<Örnek: TR21-23-İKT-XX/01>", "Örnek: TR21-23-İKT-XX/01",
        "<ÖRNEK: TR21-23-İKT-XX/01>", "ÖRNEK: TR21-23-İKT-XX/01",
        "<uygun olan seçeneği seçiniz >", "<uygun olan seçeneği seçiniz>",
        "uygun olan seçeneği seçiniz",
        "(Uygun olanı seçiniz)>", "(Uygun olanı seçiniz)", "Uygun olanı seçiniz",
        "(Sadece Pazarlık Usulü İhalelerde kullanılacaktır.)", "Sadece Pazarlık Usulü İhalelerde kullanılacaktır."
    ]:
        if old_txt in para.text:
            for r in runs:
                r.text = r.text.replace(old_txt, "")
                
    # Madde 17: Açık ihale ise "b) Teklif Dosyası" -> "a) Teklif Dosyası"
    if form_data.get("ihale_usulu") == "Açık İhale Usulü":
        if "Teklif Dosyası" in para.text and ("b)" in para.text or "b" in para.text):
            for r in runs:
                r.text = r.text.replace("b) Teklif Dosyası", "a) Teklif Dosyası")
                r.text = r.text.replace("b)\tTeklif Dosyası", "a)\tTeklif Dosyası")
                r.text = r.text.replace("b) ", "a) ")

    i = 0
    while i < len(runs):
        run = runs[i]

        # Sarı vurgulu mu?
        if run.font.highlight_color is not None and run.font.highlight_color == 7:
            stats["total_yellow"] += 1

            # Ardışık sarı run'ları birleştir
            combined_text = run.text
            j = i + 1
            yellow_runs = [run]

            while j < len(runs):
                next_run = runs[j]
                if (next_run.font.highlight_color is not None and
                        next_run.font.highlight_color == 7):
                    combined_text += next_run.text
                    yellow_runs.append(next_run)
                    stats["total_yellow"] += 1
                    j += 1
                else:
                    break

            # Eşleştir
            field_id = _match_yellow_to_field(combined_text)

            # Özel context geçersiz kılmaları:
            if context.get("in_davet_mektubu") and field_id == "ihale_tarihi" and combined_text.strip() == "…./…./20…":
                field_id = "davet_tarihi"

            if field_id is not None:
                value = form_data.get(field_id, "")
                
                # Özel Biçimlendirmeler:
                
                # İhale Konusu başka bir yerdeyse (tek satırda) virgülle birleştir
                if field_id == "ihale_konusu" and "\n" in str(value):
                    lines = [line.strip() for line in str(value).splitlines() if line.strip()]
                    value = ", ".join(lines)
                    
                # Yeterlik Değerlendirme (Davet mektubu teknik teklif paragrafında)
                if field_id == "yeterlik_degerlendirme":
                    if "\n" in str(value):
                        lines = [line.strip() for line in str(value).splitlines() if line.strip()]
                        value = ", ".join(lines)
                    if not str(value).endswith("yeterlik değerlendirmesinde kullanılacaktır."):
                        value = str(value).rstrip(".") + " yeterlik değerlendirmesinde kullanılacaktır."
                
                # Saat ise "Teklif teslimi..." gibi paragrafta isek tarih ile saati birleştirebiliriz
                if field_id == "ihale_tarihi" and "son tarih ve saati" in para.text:
                    ihale_saati = _format_field_value("ihale_saati", form_data.get("ihale_saati", ""))
                    if ihale_saati:
                        value = str(value) + " " + ihale_saati
                        
                # Madde 21: Teklif Esası -> "esaslı" ekle
                if field_id == "teklif_esasi":
                    value = str(value) + " esaslı"
                    
                # Madde 22: Taahhütlü Posta / Elden Teslim -> " Adresine" ekle
                if field_id == "teslim_yeri":
                    if "Taahhütlü posta" in para.text or "doğrudan elden" in para.text:
                        value = str(value) + " Adresine"
                        
                # Madde 23: Sözleşme başlığında İhale Türü BÜYÜK ve BOLD olmalı
                if field_id == "ihale_turu" and "SÖZLEŞMESİ" in para.text:
                    value = str(value).upper()
                    
                # Madde 26, 29, 31, 34, 36, 37: Proje adında 'Projesi' tekrarını önle
                if field_id == "proje_adi":
                    value = re.sub(r'(?i)\s+projesi$', '', str(value))
                    
                # Madde 39: Taahhütname cümlesi ihale türüne göre özel cümle ataması
                if field_id == "ihale_turu" and "hizmetleri sağlamayı" in combined_text:
                    if str(value) == "Mal Alımı": value = "malları tedarik etmeyi"
                    elif str(value) == "Hizmet Alımı": value = "hizmetleri sağlamayı"
                    elif str(value) == "Yapım İşi": value = "yapım işini üstlenmeyi"
                
                formatted_value = _format_field_value(field_id, value)

                if formatted_value:
                    # İlk run'a değeri yaz
                    yellow_runs[0].text = formatted_value
                    yellow_runs[0].font.highlight_color = None  # Sarıyı kaldır
                    
                    # Bold olmasını ve İtalik olmamasını sağla
                    yellow_runs[0].font.bold = True
                    yellow_runs[0].font.italic = False

                    # Geri kalan run'ları temizle
                    for extra_run in yellow_runs[1:]:
                        extra_run.text = ""
                        extra_run.font.highlight_color = None

                    # --- ETRAFIAKİ < > İŞARETLERİNİ VE EKLERİ TEMİZLE/DÜZELT ---
                    
                    # Öncesindeki run'ın son karakteri < ise sil
                    if i > 0 and runs[i-1].text.endswith("<"):
                        runs[i-1].text = runs[i-1].text[:-1]
                    if i > 0 and runs[i-1].text.endswith("< "):
                        runs[i-1].text = runs[i-1].text[:-2]
                        
                    for prev_idx in range(i-1, -1, -1):
                        if runs[prev_idx].text.strip() == '<':
                            runs[prev_idx].text = runs[prev_idx].text.replace('<', '')
                            break
                        if len(runs[prev_idx].text.strip()) > 0:
                            break

                    # Sonrasındaki run'ın ilk karakteri > ise sil
                    if j < len(runs) and runs[j].text.startswith(">"):
                        runs[j].text = runs[j].text[1:]
                    if j < len(runs) and runs[j].text.startswith(" >"):
                        runs[j].text = runs[j].text[2:]
                        
                    for next_idx in range(j, len(runs)):
                        if runs[next_idx].text.strip() == '>':
                            runs[next_idx].text = runs[next_idx].text.replace('>', '')
                            break
                        if len(runs[next_idx].text.strip()) > 0:
                            txt = runs[next_idx].text
                            
                            if field_id == "is_yeri_il_ilce":
                                m = re.match(r'^(\'[a-zçğıöşü]+)(.*)', txt, flags=re.IGNORECASE)
                                if m:
                                    suffix = get_locative_suffix(formatted_value)
                                    runs[next_idx].text = suffix + m.group(2)
                            
                            if field_id == "ihale_saati":
                                m = re.match(r'^(\'[a-zçğıöşü]+)(.*)', txt, flags=re.IGNORECASE)
                                if m:
                                    suffix = get_dative_suffix(formatted_value)
                                    runs[next_idx].text = suffix + m.group(2)
                                    
                            break

                    stats["filled"] += 1
                else:
                    stats["unmatched"] += 1
            else:
                is_instruction = False
                normalized = _normalize_text(combined_text)
                for instruction in INSTRUCTION_FIELDS:
                    if instruction in normalized or normalized in instruction:
                        is_instruction = True
                        break

                if is_instruction:
                    for yr in yellow_runs:
                        yr.text = ""
                        yr.font.highlight_color = None
                        
                    if i > 0 and runs[i-1].text.endswith("<"): runs[i-1].text = runs[i-1].text[:-1]
                    if j < len(runs) and runs[j].text.startswith(">"): runs[j].text = runs[j].text[1:]
                    
                    stats["instruction_skipped"] += 1
                else:
                    stats["unmatched"] += 1

            i = j
        else:
            i += 1


def _convert_to_pdf(docx_path):
    import subprocess
    import platform

    abs_docx = os.path.abspath(docx_path)
    output_dir = os.path.dirname(abs_docx)
    pdf_path = abs_docx.replace(".docx", ".pdf")

    try:
        libreoffice_cmd = "libreoffice"
        if platform.system() == "Windows":
            lo_paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            ]
            for lo_path in lo_paths:
                if os.path.exists(lo_path):
                    libreoffice_cmd = lo_path
                    break

        result = subprocess.run(
            [
                libreoffice_cmd,
                "--headless",
                "--convert-to", "pdf",
                "--outdir", output_dir,
                abs_docx,
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if os.path.exists(pdf_path):
            return pdf_path
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    except Exception:
        pass

    if platform.system() == "Windows":
        try:
            import win32com.client

            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            doc = word.Documents.Open(abs_docx)
            doc.SaveAs2(pdf_path, FileFormat=17)
            doc.Close()
            word.Quit()
            return pdf_path
        except ImportError:
            pass
        except Exception:
            try:
                word.Quit()
            except Exception:
                pass

    return None


def validate_form_data(form_data):
    errors = []

    for field_id, field_info in UNIQUE_FIELDS.items():
        if field_info.get("required", False):
            value = form_data.get(field_id)
            if value is None or value == "" or value == []:
                errors.append(
                    f"'{field_info['label']}' alanı zorunludur."
                )

        if field_info.get("type") == "number" and field_id in form_data:
            value = form_data[field_id]
            if value is not None and value != "":
                try:
                    num_val = float(value)
                    min_val = field_info.get("min_value")
                    max_val = field_info.get("max_value")
                    if min_val is not None and num_val < min_val:
                        errors.append(
                            f"'{field_info['label']}' en az {min_val} olmalıdır."
                        )
                    if max_val is not None and num_val > max_val:
                        errors.append(
                            f"'{field_info['label']}' en fazla {max_val} olmalıdır."
                        )
                except (ValueError, TypeError):
                    errors.append(
                        f"'{field_info['label']}' geçerli bir sayı olmalıdır."
                    )

    return len(errors) == 0, errors
