import os
import sys
import csv
from docx import Document

# src klasörünü path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from doc_generator import generate_filled_document

def load_test_data(csv_path):
    data = {}
    with open(csv_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            data[row['Alan ID']] = row['Değer']
    return data

def verify_kilit_uzman_ref_fix(docx_path, expected_code):
    doc = Document(docx_path)
    found_title = False
    found_ref = False
    
    for i, para in enumerate(doc.paragraphs):
        if "Kilit Uzmanlar İçin Münhasırlık ve Müsaitlik Taahhüdü" in para.text:
            found_title = True
            print(f"Başlık bulundu: P{i}")
            
        if found_title and not found_ref:
            if "Yayın Referansı" in para.text or "YAyın referansı" in para.text or "yayın referansı" in para.text.lower():
                print(f"Yayın Referansı satırı bulundu: P{i} -> '{para.text}'")
                if expected_code in para.text and "<sözleşme no" not in para.text.lower():
                    found_ref = True
                    is_bold = any(r.bold for r in para.runs if expected_code in r.text)
                    print(f"BAŞARILI: Kod bulundu ({expected_code}), talimat temizlendi. Bold: {is_bold}")
                    break
    
    return found_ref

if __name__ == "__main__":
    csv_path = r"C:\Users\eguney\Desktop\ihale\output\ihale_form_verileri_20260225.csv"
    template_path = r"Taslak İhale Dosyası.docx"
    output_dir = r"C:\Users\eguney\Desktop\ihale\output\test_out_kilit_uzman"
    
    print("--- Kilit Uzmanlar Taahhüdü Yayın Referansı Doğrulama Başlatıldı ---")
    
    if not os.path.exists(csv_path):
        print(f"HATA: CSV dosyası bulunamadı: {csv_path}")
        sys.exit(1)
        
    data = load_test_data(csv_path)
    expected_code = data.get("sozlesme_kodu", "TR21-23-IKT-01")
    
    # İhale türünü Hizmet Alımı yapalım ki bu kısım anlamlı olsun (gerçi dökümanda hep var)
    data["ihale_turu"] = "Hizmet Alımı"
    
    result = generate_filled_document(template_path, data, output_dir=output_dir)
    docx_path = result['docx']
    
    if verify_kilit_uzman_ref_fix(docx_path, expected_code):
        print("--- TEST BAŞARILI ---")
    else:
        print("--- TEST BAŞARISIZ! ---")
