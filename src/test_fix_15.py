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

def verify_email_fix(docx_path, expected_email):
    doc = Document(docx_path)
    found = False
    for para in doc.paragraphs:
        if "Elektronik posta adresi" in para.text:
            print(f"Bulunan satır: '{para.text}'")
            if expected_email in para.text and para.text.strip().startswith("e)"):
                found = True
                # Bold kontrolü (en az bir run bold olmalı)
                is_bold = any(r.bold for r in para.runs if expected_email in r.text)
                if is_bold:
                    print("BAŞARILI: Email bulundu ve kalın (bold) işaretlenmiş.")
                else:
                    print("HATA: Email bulundu ama kalın değil!")
    return found

if __name__ == "__main__":
    csv_path = r"C:\Users\eguney\Desktop\ihale\output\ihale_form_verileri_20260225.csv"
    template_path = r"Taslak İhale Dosyası.docx"
    output_dir = r"C:\Users\eguney\Desktop\ihale\output\test_out_15"
    
    print("--- Görev 15 Doğrulama Başlatıldı ---")
    
    if not os.path.exists(csv_path):
        print(f"HATA: CSV dosyası bulunamadı: {csv_path}")
        sys.exit(1)
        
    data = load_test_data(csv_path)
    expected_email = data.get("kurum_eposta", "info@edirne.bel.tr") # CSV'den oku
    print(f"Beklenen Email: {expected_email}")
    
    result = generate_filled_document(template_path, data, output_dir=output_dir)
    docx_path = result['docx']
    
    if verify_email_fix(docx_path, expected_email):
        print("--- TEST BAŞARILI ---")
    else:
        print("--- TEST BAŞARISIZ: E-posta alanı bulunamadı veya hatalı! ---")
