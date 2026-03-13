import os
import sys
import csv
from docx import Document
from datetime import datetime

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

def verify_contract_code_fix(docx_path, expected_code):
    doc = Document(docx_path)
    found = False
    for para in doc.paragraphs:
        if "Sözleşme kodu:" in para.text:
            print(f"Bulunan satır: '{para.text}'")
            if expected_code in para.text and "<Ajans ile Yararlanıcı" not in para.text:
                found = True
                is_bold = any(r.bold for r in para.runs if expected_code in r.text)
                if is_bold:
                    print(f"BAŞARILI: Sözleşme kodu bulundu ({expected_code}) ve kalın (bold) işaretlenmiş.")
                else:
                    print("HATA: Sözleşme kodu bulundu ama kalın değil!")
            elif "<Ajans ile Yararlanıcı" in para.text:
                print("HATA: Talimat metni hala duruyor!")
    return found

if __name__ == "__main__":
    csv_path = r"C:\Users\eguney\Desktop\ihale\output\ihale_form_verileri_20260225.csv"
    template_path = r"Taslak İhale Dosyası.docx"
    output_dir = r"C:\Users\eguney\Desktop\ihale\output\test_out_16"
    
    print("--- Görev 16 Doğrulama Başlatıldı ---")
    
    if not os.path.exists(csv_path):
        print(f"HATA: CSV dosyası bulunamadı: {csv_path}")
        sys.exit(1)
        
    data = load_test_data(csv_path)
    # sozlesme_kodu'nu al (csv'de Alan ID=sozlesme_kodu)
    expected_code = data.get("sozlesme_kodu", "TR21-23-İKT-XX")
    print(f"Beklenen Sözleşme Kodu: {expected_code}")
    
    result = generate_filled_document(template_path, data, output_dir=output_dir)
    docx_path = result['docx']
    
    if verify_contract_code_fix(docx_path, expected_code):
        print("--- TEST BAŞARILI ---")
    else:
        print("--- TEST BAŞARISIZ: Sözleşme kodu alanı bulunamadı veya hatalı! ---")
