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

def verify_teklif_sunum_fix(docx_path, expected_code):
    doc = Document(docx_path)
    in_section = False
    found = False
    for i, para in enumerate(doc.paragraphs):
        if "Teklif Sunum Formu" in para.text:
            in_section = True
            print(f"Teklif Sunum Formu bölmü saptandı: P{i}")
            
        if in_section:
            if "Yayın Referansı" in para.text:
                print(f"P{i} Yayın Referansı satırı: '{para.text}'")
                if expected_code in para.text and "<sözleşme no" not in para.text:
                    found = True
                    is_bold = any(r.bold for r in para.runs if expected_code in r.text)
                    print(f"BAŞARILI: Kod bulundu ({expected_code}), talimat temizlendi. Bold: {is_bold}")
                    break
            # Eğer başka bir bölüme geçildiyse arama alanını daraltabiliriz ama şimdilik gerek yok
            
    return found

if __name__ == "__main__":
    csv_path = r"C:\Users\eguney\Desktop\ihale\output\ihale_form_verileri_20260225.csv"
    template_path = r"Taslak İhale Dosyası.docx"
    output_dir = r"C:\Users\eguney\Desktop\ihale\output\test_out_teklif_sunum"
    
    print("--- Teklif Sunum Formu Yayın Referansı Doğrulama Başlatıldı ---")
    
    if not os.path.exists(csv_path):
        print(f"HATA: CSV dosyası bulunamadı: {csv_path}")
        sys.exit(1)
        
    data = load_test_data(csv_path)
    expected_code = data.get("sozlesme_kodu", "TR21-23-IKT-01")
    
    result = generate_filled_document(template_path, data, output_dir=output_dir)
    docx_path = result['docx']
    
    if verify_teklif_sunum_fix(docx_path, expected_code):
        print("--- TEST BAŞARILI ---")
    else:
        print("--- TEST BAŞARISIZ! ---")
