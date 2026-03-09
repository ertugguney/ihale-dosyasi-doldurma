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
        
    # Özel kural: Destek programı adı sonundaki "Programı" (veya Programi, PROGRAM vb.) kelimesini sil.
    if field_id == "destek_programi_adi":
        formatted = re.sub(r'\s+[pP][rR][oO][gG][rR][aA][mM][ıiIİ]?\s*$', '', formatted)
        
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
        if context.get("in_davet_mektubu"):
            text_norm = para.text.strip().lower()
            # Başlıktaki talimat metnini temizle
            if "değerlendirme:" in text_norm and "hangisi uygun ise onu seçiniz" in text_norm:
                para.text = "DEĞERLENDİRME: "
            
            # Seçeneğe göre filtreleme
            turu = form_data.get("ihale_turu")
            if text_norm.startswith("a)") and "mal alımı" in text_norm:
                if turu == "Hizmet Alımı":
                    paragraphs_to_remove.append(para)
                else:
                    # a) yazısını kaldır, sadece metni bırak (isteğe bağlı ama "cümle bırakılacaktır" dediği için temizleyelim)
                    para.text = para.text.replace("a)", "").strip()
            elif text_norm.startswith("b)") and "hizmet alımlarında" in text_norm:
                if turu in ["Mal Alımı", "Yapım İşi"]:
                    paragraphs_to_remove.append(para)
                else:
                    # b) yazısını kaldır, sadece metni bırak
                    para.text = para.text.replace("b)", "").strip()
                    
        # Madde 14: İSTEKLİLERE TALİMATLAR "Aşağıda yer alan maddeler..." silimi
        if "Aşağıda yer alan maddeler içerisindeki boş yerler" in para.text and "Diğer metinleri hiçbir şekilde değiştirmeyiniz" in para.text:
            paragraphs_to_remove.append(para)

        # Madde 8: İhalenin yabancı isteklilere açıklığı
        if "İhalenin yabancı isteklilere açıklığı" in para.text or "İhaleye yabancı isteklilere açıklığı" in para.text:
            # Bir sonraki paragrafları kontrol et (Çünkü başlık ayrı paragraf olabilir)
            context["in_madde_8"] = True
            continue
            
        if context.get("in_madde_8") and ("yerli yabancı tüm isteklilere açıktır" in para.text or "sadece yerli isteklilere açıktır" in para.text):
            val = form_data.get("istekli_kapsamı")
            if val:
                para.text = str(val)
                # Koyu yazım uygulaması yapalım genel kurala uymak için
                for r in para.runs:
                    r.font.bold = True
                    r.font.italic = False
            context["in_madde_8"] = False # İşlem tamam
            continue

        # Madde 18: Teklif ve sözleşme türü
        if "Teklif ve sözleşme türü" in para.text and "esaslı" in para.text:
            val = form_data.get("teklif_esasi")
            if val:
                # Talimatı temizle
                instruct = "(her lot için uygun olan yöntem seçilecek ve belirtilecektir)"
                for r in para.runs:
                    if instruct in r.text:
                        r.text = r.text.replace(instruct, "")
                
                # Esas metni ve "esaslı" ekini ayarla
                target = "götürü bedel / birim fiyat esaslı"
                if target in para.text:
                    for r in para.runs:
                        if target in r.text:
                            r.text = r.text.replace(target, f"{val} esaslı")
                            r.font.bold = True
                else:
                     # "götürü bedel / birim fiyat" ifadesini bul ve "esaslı" ekini koru/ekle
                     for r in para.runs:
                         if "götürü bedel / birim fiyat" in r.text:
                             r.text = r.text.replace("götürü bedel / birim fiyat", val)
                             r.font.bold = True
                             if "esaslı" not in r.text and "esaslı" not in para.text:
                                 r.text += " esaslı"
            continue
            
            
        # Madde 22: Teslim Yeri ve "Adresine" Kelimesi Eklenmesi
        if "Taahhütlü posta / kargo servisi" in para.text or "Ya da Sözleşme Makamına doğrudan elden" in para.text:
            teslim_yeri = form_data.get("teslim_yeri", "")
            if teslim_yeri:
                target_1 = "Taahhütlü posta / kargo servisi) ile"
                target_2 = "Ya da Sözleşme Makamına doğrudan elden"
                
                if target_1 in para.text:
                    # Para text'ini temizleyip yeni yapıyı kuralım
                    old_text = para.text
                    para.text = ""
                    # "Taahhütlü posta / kargo servisi) ile" kısmına kadar olan yeri koru (eğer bir madde numarası varsa vb)
                    prefix = old_text.split(target_1)[0]
                    para.add_run(prefix + target_1 + " ")
                    r_val = para.add_run(f"{teslim_yeri}")
                    r_val.bold = True
                    para.add_run(" Adresine")
                    # Geri kalan metni de ekle (eğer varsa)
                    suffix = old_text.split(target_1)[-1]
                    if suffix and suffix != old_text:
                        para.add_run(suffix)
                    continue

                if target_2 in para.text:
                    old_text = para.text
                    para.text = ""
                    prefix = old_text.split(target_2)[0]
                    para.add_run(prefix + target_2 + " ")
                    r_val = para.add_run(f"{teslim_yeri}")
                    r_val.bold = True
                    para.add_run(" Adresine")
                    suffix = old_text.split(target_2)[-1]
                    if suffix and suffix != old_text:
                        para.add_run(suffix)
                    continue

        # Madde 17: İhale Usulü Kontrolü a) ve b) maddeleri
        if "İhaleye davet mektubu" in para.text:
            usul = form_data.get("ihale_usulu")
            if usul == "Açık İhale Usulü":
                paragraphs_to_remove.append(para)
            else: # Pazarlık Usulü
                # Talimat metnini temizle
                for old_txt in ["(Sadece Pazarlık Usulü İhalelerde kullanılacaktır.)", "Sadece Pazarlık Usulü İhalelerde kullanılacaktır."]:
                    if old_txt in para.text:
                        for r in para.runs:
                            r.text = r.text.replace(old_txt, "").strip()
            continue

        if "Teklif Dosyası" in para.text and "Sözleşme Taslağı" in para.text:
            if form_data.get("ihale_usulu") == "Açık İhale Usulü":
                # b) maddesini a) maddesine çevir
                if "b)" in para.text:
                    for r in para.runs:
                        r.text = r.text.replace("b)", "a)")
                elif para.text.strip().startswith("b"):
                    # Bazen tırnak/format farklılığı olabilir
                    for r in para.runs:
                        if r.text.strip().startswith("b"):
                            r.text = r.text.replace("b", "a", 1)
            continue

        # Madde 17 f) bendi: Geçici Teminat Seçimi
        if "f) İstenmesi halinde Md. 26" in para.text and "geçici teminat" in para.text:
            val = form_data.get("gecici_teminat")
            if val:
                para.text = ""
                para.add_run("f)\tİstenmesi halinde Md. 26’daki koşullara uygun sunulmuş geçici teminat ")
                r_val = para.add_run(f"{val}.")
                r_val.bold = True
                r_val.italic = False
                continue

        # Madde 17 h) bendi: Kesin Teminat Seçimi
        if "h) İstenmesi halinde Genel Koşullar md. 29" in para.text and "kesin teminat" in para.text:
            val = form_data.get("kesin_teminat")
            if val:
                para.text = ""
                para.add_run("h)\tİstenmesi halinde Genel Koşullar md. 29’da ve Taslak Sözleşme Özel Koşullar md. 8.1’de şartları tanımlanmış kesin teminat ")
                r_val = para.add_run(f"{val}.")
                r_val.bold = True
                r_val.italic = False
                continue

        # Madde 25: Sözleşme ve Özel Koşullar - Kesin Teminat Bölümü (Task 25)
        if "Yüklenici tarafından sözleşme imzalama aşamasında kesin teminat" in para.text:
            val = form_data.get("kesin_teminat")
            if val:
                # "Kesin teminat ve Sigorta" başlığı aynı paragrafta olabilir, koruyalım
                prefix = ""
                if "Kesin teminat ve Sigorta" in para.text:
                    prefix = "Kesin teminat ve Sigorta "
                
                para.text = ""
                para.add_run(f"{prefix}Bu sözleşme kapsamında işin ihale edildiği Yüklenici tarafından sözleşme imzalama aşamasında kesin teminat ")
                r_val = para.add_run(f"{val}")
                r_val.bold = True
                r_val.italic = False
                para.add_run(".")
                continue
                
        # Madde 24: Ön Ödeme Paragrafı Yeniden Yazımı (Task 24)
        if "Sözleşme kapsamında ön ödeme" in para.text:
            val = form_data.get("on_odeme")
            if val == "Yapılmayacaktır":
                para.text = ""
                para.add_run("Sözleşme kapsamında ön ödeme ")
                r_val = para.add_run("yapılmayacaktır")
                r_val.bold = True
                r_val.italic = False
                para.add_run(".")
            elif val == "Yapılacaktır":
                oran = form_data.get("on_odeme_orani", "")
                para.text = ""
                para.add_run("Sözleşme kapsamında ön ödeme ")
                r_val = para.add_run("yapılacaktır")
                r_val.bold = True
                r_val.italic = False
                para.add_run(". Ön ödeme miktarı sözleşme bedelinin % ")
                r_oran = para.add_run(f"{oran}")
                r_oran.bold = True
                r_oran.italic = False
                para.add_run("’sı olan ……………….. TL’dir. Ön ödeme, sözleşme imza tarihinden sonra 15 gün içerisinde belirlenen ön ödeme tutarı kadar avans teminat mektubunun sunulmasını takiben yapılacaktır.")
            continue
                        
        # Madde 25: Kesin Teminat Oranı İkinci Cümle
        if "Kesin teminat tutarı sözleşme bedelinin" in para.text and "olmalıdır" in para.text:
            val = form_data.get("kesin_teminat")
            if val == "İSTENMEMEKTEDİR":
                paragraphs_to_remove.append(para)
                continue
            elif val == "İSTENMEKTEDİR":
                oran = form_data.get("kesin_teminat_orani", "")
                para.text = ""
                para.add_run("Kesin teminat tutarı sözleşme bedelinin % ")
                r_oran = para.add_run(f"{oran}")
                r_oran.bold = True
                r_oran.italic = False
                para.add_run("’sı kadar olmalıdır.")
                continue

        # Madde 34, 36, 37: İdari Uygunluk / Sözleşme Adı / Teknik Tablo birleşik alan (< Proje adı >Projesi için...)
        p_text_lower = para.text.lower()
        if "proje ad" in p_text_lower and "projesi i" in p_text_lower and ("ad" in p_text_lower or "sözleşme" in p_text_lower):
            p_adi = str(form_data.get("proje_adi", ""))
            i_turu = str(form_data.get("ihale_turu", ""))
            p_adi_clean = re.sub(r'(?i)\s+projesi$', '', p_adi)
            
            # Label ve sekmeleri koru
            if "Sözleşme adı:" in para.text:
                label = "Sözleşme adı: "
            elif "Sözleşme başlı" in para.text:
                # Şablonda 'Sözleşme başlı	:' şeklinde (tab ile) geçiyor
                label = "Sözleşme başlı\t: "
            else:
                # 'Adı:' kısmında template'te \t\t var
                label = "Adı:\t\t"
            
            para.text = ""
            para.add_run(label)
            r_val = para.add_run(f"{p_adi_clean} Projesi için {i_turu}")
            r_val.bold = True
            r_val.italic = False
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
        ihale_konusu_val = form_data.get("ihale_konusu", "")
        if isinstance(ihale_konusu_val, list):
            lines = ihale_konusu_val
        else:
            lines = [line.strip() for line in str(ihale_konusu_val).splitlines() if line.strip()]
        
        for idx, marker in enumerate(["(i)", "(ii)", "(iii)"]):
            if marker in para.text:
                if idx < len(lines):
                    # Replace _________ with the line item
                    for r in runs:
                        r.text = r.text.replace("____________________", lines[idx])
                        r.text = r.text.replace("_________________", lines[idx])
                        r.font.bold = True
                        r.font.italic = False
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
        "< ÖRNEK: TR21-23-İKT-XX/01 >", "<ÖRNEK: TR21-23-İKT-XX/01 >",
        "<uygun olan seçeneği seçiniz >", "<uygun olan seçeneği seçiniz>",
        "uygun olan seçeneği seçiniz",
        "(Uygun olanı seçiniz)>", "(Uygun olanı seçiniz)", "Uygun olanı seçiniz"
    ]:
        if old_txt in para.text:
            _replace_text_across_runs(para, old_txt, "")

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
            if context.get("in_davet_mektubu") and field_id == "ihale_tarihi":
                # Davet mektubundaki tarih alanı genellikle …./…./20… formatındadır
                if re.search(r'\d{4}|…', combined_text):
                    field_id = "davet_tarihi"

            if field_id is not None:
                # Madde 34: Birleşik alan kontrolü (< Proje adı >Projesi için <Mal Alımı...>)
                if "Proje adı" in combined_text and "Projesi için" in combined_text:
                    p_adi = str(form_data.get("proje_adi", ""))
                    i_turu = str(form_data.get("ihale_turu", ""))
                    p_adi_clean = re.sub(r'(?i)\s+projesi$', '', p_adi)
                    value = f"{p_adi_clean} Projesi için {i_turu}"
                else:
                    value = form_data.get(field_id, "")
                
                # Özel Biçimlendirmeler:
                
                # İhale Konusu başka bir yerdeyse (tek satırda) virgülle birleştir
                if field_id == "ihale_konusu":
                    if isinstance(value, list):
                        value = ", ".join(value)
                    elif "\n" in str(value):
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
                if field_id == "ihale_tarihi":
                    text_lower = para.text.lower()
                    if "tarih" in text_lower and "saat" in text_lower:
                        ihale_saati = _format_field_value("ihale_saati", form_data.get("ihale_saati", ""))
                        if ihale_saati and ihale_saati not in str(value):
                            value = str(value) + " " + ihale_saati
                        
                # Madde 21: Teklif Esası -> "esaslı" ekle
                if field_id == "teklif_esasi":
                    value = str(value) + " esaslı"
                    
                # Madde 22: Taahhütlü Posta / Elden Teslim -> " Adresine" ekle
                if field_id == "teslim_yeri":
                    if "Taahhütlü posta" in para.text or "doğrudan elden" in para.text:
                        value = str(value) + " Adresine"
                        
                # Madde 27, 33: "İsteklinin adı" dots should remain dots (Signature lines)
                lower_para = para.text.lower()
                if "isteklinin" in lower_para and "ad" in lower_para:
                    stats["instruction_skipped"] += 1
                    yellow_runs[0].font.highlight_color = None
                    for extra_run in yellow_runs[1:]:
                        extra_run.font.highlight_color = None
                    i = j
                    continue

                # Madde 35: Lot Numarası alanını tamamen sil
                norm_combined = combined_text.lower().strip()
                if "lot numarası" in norm_combined or "lot numarasi" in norm_combined:
                    for r_item in yellow_runs:
                        r_item.text = ""
                        r_item.font.highlight_color = None
                    i = j
                    continue

                # Madde 23: Sözleşme başlığında İhale Türü BÜYÜK ve BOLD olmalı
                if field_id == "ihale_turu" and "SÖZLEŞMESİ" in para.text:
                    value = str(value).upper()
                    
                # Madde 26, 29, 31, 34, 36, 37: Proje adında 'Projesi' tekrarını önle
                if field_id == "proje_adi":
                    value = re.sub(r'(?i)\s+projesi$', '', str(value))
                    
                # Madde 39: Taahhütname cümlesi ihale türüne göre özel cümle ataması
                if field_id == "ihale_turu" and ("hizmetleri sağlamayı" in combined_text or "malları tedarik etmeyi" in combined_text):
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
                    
                    # Geriye dönük < sil
                    for prev_idx in range(i-1, -1, -1):
                        txt = runs[prev_idx].text
                        if '<' in txt:
                            runs[prev_idx].text = txt.replace('<', '')
                            break
                        if len(txt.strip()) > 0:
                            break

                    # İleriye dönük > sil ve son ekleri (suffix) akıllıca yakala
                    for next_idx in range(j, len(runs)):
                        txt = runs[next_idx].text
                        if not txt: continue
                        
                        original_was_just_marker = False
                        if '>' in txt:
                            if txt.strip() == '>':
                                original_was_just_marker = True
                            txt = txt.replace('>', '')
                            runs[next_idx].text = txt
                            
                        # Eğer bu run hala metin içeriyorsa veya sadece '>' değil idiyse (yani peşinden bir şey gelebilir)
                        # Suffix tespiti için sonraki birkaç run'ı birleştirerek kontrol et (bölünmüş run desteği)
                        if txt.strip() or original_was_just_marker:
                            combined_suffix = ""
                            suffix_runs = []
                            # Sonraki 5 run'ı birleştir (genelde suffix 2-3 run'a yayılır: ' | n | e)
                            for k in range(next_idx, min(next_idx + 5, len(runs))):
                                combined_suffix += runs[k].text
                                suffix_runs.append(runs[k])
                                if " " in runs[k].text: break # Boşluk gelirse kelime bitmiştir
                                
                            # Regex: Tırnak ile başlayan (opsiyonel boşluktan sonra) ve harflerle devam eden yapı
                            # (not: şablonda hem düz ('), hem kıvrık sağ (’) hem de kıvrık sol (‘) tırnaklar olabiliyor!)
                            m = re.match(r'^(\s*)([\'’‘][a-zçğıöşü]+)(.*)', combined_suffix, flags=re.IGNORECASE)
                            if m:
                                target_suffix = None
                                if field_id == "is_yeri_il_ilce":
                                    target_suffix = get_locative_suffix(formatted_value)
                                elif field_id == "ihale_saati":
                                    target_suffix = get_dative_suffix(formatted_value)
                                
                                if target_suffix:
                                    quote = m.group(2)[0]
                                    # Yeni eki oluştur (varsa baştaki boşluğu silerek yapıştırır)
                                    full_new = quote + target_suffix[1:] + m.group(3)
                                    suffix_runs[0].text = full_new
                                    # Diğer birleştirilen run'ları temizle
                                    for sr in suffix_runs[1:]:
                                        sr.text = ""
                                    break # Suffix işlendi
                            
                            if txt.strip(): # Eğer suffix değilse ama metin varsa aramayı durdur
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
                        
                    # Talimat çevresindeki < ve > işaretlerini temizle
                    for prev_idx in range(i-1, -1, -1):
                        txt = runs[prev_idx].text
                        if '<' in txt:
                            runs[prev_idx].text = txt.replace('<', '')
                            break
                        if len(txt.strip()) > 0:
                            break
                            
                    for next_idx in range(j, len(runs)):
                        txt = runs[next_idx].text
                        if '>' in txt:
                            runs[next_idx].text = txt.replace('>', '')
                            break
                        if len(txt.strip()) > 0:
                            break
                    
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


def _replace_text_across_runs(paragraph, old_text, new_text):
    """
    Paragraf içindeki metni (farklı run'lara bölünmüş olsa dahi) bulur ve değiştirir.
    """
    if old_text not in paragraph.text:
        return

    # Önce tekil run'larda dene
    for run in paragraph.runs:
        if old_text in run.text:
            run.text = run.text.replace(old_text, new_text)
            if old_text not in paragraph.text:
                return

    # Eğer hala metin varsa ve bu bir "Örnek" metni ise, 
    # format kaybını göze alarak paragraf düzeyinde siliyoruz.
    if old_text in paragraph.text and ("Örnek:" in old_text or "ÖRNEK:" in old_text):
        paragraph.text = paragraph.text.replace(old_text, new_text)
