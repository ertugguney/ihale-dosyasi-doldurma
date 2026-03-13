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

def verify_pub_ref_fix(docx_path, expected_code):
    doc = Document(docx_path)
    count = 0
    total_found = 0
    for para in doc.paragraphs:
        if "Yayın Referansı" in para.text:
            total_found += 1
            print(f"Bulunan satır: '{para.text}'")
            if expected_code in para.text and "<sözleşme no" not in para.text and "<Örnek:" not in para.text:
                count += 1
                is_bold = any(r.bold for r in para.runs if expected_code in r.text)
                if is_bold:
                    print(f"DOĞRULANDI: Yayın Referansı dolmuş ({expected_code}) ve kalın.")
                else:
                    print("HATA: Bold değil!")
            else:
                print("HATA: Beklenen kod bulunamadı veya talimat metni hala duruyor!")
    
    return count > 0

if __name__ == "__main__":
    csv_path = r"C:\Users\eguney\Desktop\ihale\output\ihale_form_verileri_20260225.csv"
    template_path = r"Taslak İhale Dosyası.docx"
    output_dir = r"C:\Users\eguney\Desktop\ihale\output\test_out_27"
    
    print("--- Görev 27 Doğrulama Başlatıldı ---")
    
    if not os.path.exists(csv_path):
        print(f"HATA: CSV bulunamadı: {csv_path}")
        sys.exit(1)
        
    data = load_test_data(csv_path)
    expected_code = data.get("sozlesme_kodu", "TR21-23-IKT-01")
    
    result = generate_filled_document(template_path, data, output_dir=output_dir)
    docx_path = result['docx']
    
    if verify_pub_ref_fix(docx_path, expected_code):
        print("--- TEST BAŞARILI ---")
    else:
        print("--- TEST BAŞARISIZ! ---")
