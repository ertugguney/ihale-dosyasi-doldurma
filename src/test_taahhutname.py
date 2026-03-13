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

def verify_taahhutname_fix(docx_path, ihale_turu):
    doc = Document(docx_path)
    expected_phrases = {
        "Mal Alımı": "malları tedarik etmeyi",
        "Hizmet Alımı": "hizmetleri sağlamayı",
        "Yapım İşi": "yapım işini üstlenmeyi"
    }
    expected = expected_phrases.get(ihale_turu, "")
    found = False
    
    for para in doc.paragraphs:
        if "imza atmaya yetkili kişisi olarak" in para.text:
            print(f"Taahhütname paragrafı bulundu: '{para.text[:100]}...'")
            if expected in para.text and "<hizmetleri" not in para.text:
                found = True
                print(f"BAŞARILI: '{expected}' ifadesi bulundu.")
            else:
                print(f"HATA: Beklenen '{expected}' bulunamadı veya placeholder temizlenmedi.")
                print(f"Mevcut Metin: '{para.text}'")
    
    return found

if __name__ == "__main__":
    csv_path = r"C:\Users\eguney\Desktop\ihale\output\ihale_form_verileri_20260225.csv"
    template_path = r"Taslak İhale Dosyası.docx"
    output_dir = r"C:\Users\eguney\Desktop\ihale\output\test_out_taahhutname"
    
    print("--- Taahhütname İhale Türü Uyarlama Doğrulama Başlatıldı ---")
    
    data = load_test_data(csv_path)
    # Test verisinde ihale_turu "Mal Alımı" (csv'den kontrol etmem gerekebilir ama genelde öyle)
    ihale_turu = data.get("ihale_turu", "Mal Alımı")
    print(f"Test verisi İhale Türü: {ihale_turu}")
    
    result = generate_filled_document(template_path, data, output_dir=output_dir)
    docx_path = result['docx']
    
    if verify_taahhutname_fix(docx_path, ihale_turu):
        print("--- TEST BAŞARILI ---")
    else:
        print("--- TEST BAŞARISIZ! ---")
