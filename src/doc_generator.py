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


def _normalize_text(text):
    """Metni karşılaştırma için normalize eder."""
    if not text:
        return ""
    return text.strip().replace("\u00a0", " ").replace("  ", " ")


def _match_yellow_to_field(yellow_text):
    """
    Sarı vurgulu metni benzersiz alan ID'sine eşleştirir.

    Args:
        yellow_text: Sarı vurgulu metin.

    Returns:
        Eşleşen benzersiz alan ID'si veya None.
    """
    normalized = _normalize_text(yellow_text)

    # Direkt eşleşme
    if normalized in YELLOW_TO_UNIQUE_MAP:
        return YELLOW_TO_UNIQUE_MAP[normalized]

    # Kısmi eşleşme (sarı metin bir map anahtarını içeriyorsa)
    for key, field_id in YELLOW_TO_UNIQUE_MAP.items():
        if key in normalized or normalized in key:
            return field_id

    # Talimat mı kontrol et
    for instruction in INSTRUCTION_FIELDS:
        if instruction in normalized or normalized in instruction:
            return None  # Talimat metni, form alanı değil

    return None


def _format_field_value(field_id, value):
    """
    Alan değerini Word'de gösterilecek formata dönüştürür.

    Args:
        field_id: Benzersiz alan ID'si.
        value: Kullanıcının girdiği değer.

    Returns:
        Formatlanmış metin.
    """
    if value is None or value == "":
        return ""

    field_info = UNIQUE_FIELDS.get(field_id, {})
    field_type = field_info.get("type", "text")

    if field_type == "date":
        if isinstance(value, date):
            return value.strftime("%d/%m/%Y")
        elif isinstance(value, str):
            return value
    elif field_type == "time":
        if isinstance(value, time):
            return value.strftime("%H:%M")
        elif isinstance(value, str):
            return value
    elif field_type == "number":
        return str(value)

    return str(value)


def generate_filled_document(template_path, form_data, output_dir="output"):
    """
    Şablon Word belgesini kullanıcı verileriyle doldurarak yeni belge oluşturur.

    Args:
        template_path: Orijinal .docx şablon dosyasının yolu.
        form_data: Kullanıcının form üzerinden girdiği veriler (dict).
                   Anahtar: benzersiz alan ID, Değer: girilen veri.
        output_dir: Çıktı dosyalarının kaydedileceği klasör.

    Returns:
        dict: Oluşturulan dosyaların yollarını içeren sözlük.
              {"docx": "path/to/file.docx", "pdf": "path/to/file.pdf"}
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

    # --- PARAGRAFLAR ---
    for para in doc.paragraphs:
        _process_paragraph_runs(para, form_data, stats)

    # --- TABLOLAR ---
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    _process_paragraph_runs(para, form_data, stats)

    # --- HEADER/FOOTER ---
    for section in doc.sections:
        for header in [section.header, section.first_page_header]:
            if header and header.is_linked_to_previous is False:
                for para in header.paragraphs:
                    _process_paragraph_runs(para, form_data, stats)
        for footer in [section.footer, section.first_page_footer]:
            if footer and footer.is_linked_to_previous is False:
                for para in footer.paragraphs:
                    _process_paragraph_runs(para, form_data, stats)

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


def _process_paragraph_runs(para, form_data, stats):
    """
    Bir paragraftaki sarı vurgulu run'ları işler ve kullanıcı verileriyle doldurur.

    Strateji:
        1. Ardışık sarı run'ları birleştirir
        2. Birleştirilmiş metni benzersiz alana eşleştirir
        3. Eşleşme varsa, ilk run'ın metnini günceller ve diğerlerini temizler
        4. Sarı vurguyu kaldırır
    """
    runs = list(para.runs)
    if not runs:
        return

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

            if field_id is not None:
                value = form_data.get(field_id, "")
                formatted_value = _format_field_value(field_id, value)

                if formatted_value:
                    # İlk run'a değeri yaz
                    yellow_runs[0].text = formatted_value
                    yellow_runs[0].font.highlight_color = None  # Sarıyı kaldır

                    # Geri kalan run'ları temizle
                    for extra_run in yellow_runs[1:]:
                        extra_run.text = ""
                        extra_run.font.highlight_color = None

                    stats["filled"] += 1
                else:
                    # Değer girilmemiş, sarıyı bırak ama sayıyı say
                    stats["unmatched"] += 1
            else:
                # Talimat veya eşleşmeyen alan
                is_instruction = False
                normalized = _normalize_text(combined_text)
                for instruction in INSTRUCTION_FIELDS:
                    if instruction in normalized or normalized in instruction:
                        is_instruction = True
                        break

                if is_instruction:
                    stats["instruction_skipped"] += 1
                else:
                    stats["unmatched"] += 1

            i = j
        else:
            i += 1


def _convert_to_pdf(docx_path):
    """
    Word dosyasını PDF'e dönüştürür.

    Platformdan bağımsız çalışır:
        - Linux (Streamlit Cloud): LibreOffice headless modu
        - Windows: pywin32 veya LibreOffice

    Args:
        docx_path: .docx dosyasının yolu.

    Returns:
        PDF dosyasının yolu veya None.
    """
    import subprocess
    import platform

    abs_docx = os.path.abspath(docx_path)
    output_dir = os.path.dirname(abs_docx)
    pdf_path = abs_docx.replace(".docx", ".pdf")

    # Yöntem 1: LibreOffice (Linux & Windows - platformdan bağımsız)
    try:
        libreoffice_cmd = "libreoffice"
        if platform.system() == "Windows":
            # Windows'ta LibreOffice yolu
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
    except Exception as e:
        print(f"LibreOffice PDF dönüşüm hatası: {e}")

    # Yöntem 2: pywin32 (yalnızca Windows, yüklüyse)
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
        except Exception as e:
            print(f"pywin32 PDF dönüşüm hatası: {e}")
            try:
                word.Quit()
            except Exception:
                pass

    print("PDF dönüşümü yapılamadı (LibreOffice veya pywin32 bulunamadı).")
    return None


def validate_form_data(form_data):
    """
    Form verilerini doğrular.

    Args:
        form_data: Kullanıcının girdiği veriler.

    Returns:
        (is_valid, errors): Doğrulama sonucu ve hata listesi.
    """
    errors = []

    for field_id, field_info in UNIQUE_FIELDS.items():
        if field_info.get("required", False):
            value = form_data.get(field_id)
            if value is None or value == "" or value == []:
                errors.append(
                    f"'{field_info['label']}' alanı zorunludur."
                )

        # Sayısal alan kontrolleri
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
