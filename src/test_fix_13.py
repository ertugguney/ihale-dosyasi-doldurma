r"""
Görev 13 Doğrulama Scripti.

C:\Users\eguney\Desktop\ihale\output\ihale_form_verileri_20260225.csv
dosyasındaki verileri kullanarak döküman oluşturur ve "DEĞERLENDİRME" bölümündeki
madde seçimini (a veya b) kontrol eder.
"""

import os
import sys
import csv
import time
from datetime import datetime

base_dir = r"c:\Users\eguney\Desktop\ihale"
sys.path.insert(0, os.path.join(base_dir, "src"))

from doc_generator import generate_filled_document

def load_csv_data(csv_path):
    data = {}
    if not os.path.exists(csv_path):
        print(f"Hata: {csv_path} bulunamadı.")
        return None
        
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            field_id = row.get("Alan ID")
            value = row.get("Değer", "")
            if field_id:
                data[field_id] = value
    return data

def check_docx_evaluation(docx_path, ihale_turu):
    import docx
    try:
        doc = docx.Document(docx_path)
        print(f"\nİhale Türü: {ihale_turu}")
        
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        
        found_eval = False
        incorrect_removal = False
        
        for i, text in enumerate(paragraphs):
            # 'TEKNİK DEĞERLENDİRME TABLOSU' başlığını görmezden gel, gerçek değerlendirme başlığını seç
            if "DEĞERLENDİRME" in text.upper() and ("UYGUN" in text.upper() or len(text) < 50) and "TABLOSU" not in text.upper():
                found_eval = True
                print(f"Başlık bulundu: '{text}'")
                if "(" in text and "uygun ise" in text.lower():
                    print("HATA: Başlıktaki talimat parantezi silinmemiş!")
                else:
                    print("BAŞARILI: Başlık temizlenmiş.")
                
                # Mal Alımı / Yapım İşi ise a) şıkkı olmalı
                if ihale_turu in ["Mal Alımı", "Yapım İşi"]:
                    # Sonraki paragrafta a) olmalı
                    found_a = False
                    for j in range(1, 4):
                        if i+j < len(paragraphs):
                            para_text = paragraphs[i+j]
                            if para_text.strip().startswith("a)"):
                                print(f"BAŞARILI: a) şıkkı korundu: '{para_text[:50]}...'")
                                found_a = True
                                break
                            if para_text.strip().startswith("b)"):
                                print(f"HATA: b) şıkkı silinmemiş! İçerik: {para_text[:30]}")
                    if not found_a:
                        print("HATA: a) şıkkı bulunamadı!")
                
                # Hizmet Alımı ise b) şıkkı olmalı
                elif ihale_turu == "Hizmet Alımı":
                    found_b = False
                    for j in range(1, 4):
                        if i+j < len(paragraphs):
                            para_text = paragraphs[i+j]
                            if para_text.strip().startswith("b)"):
                                print(f"BAŞARILI: b) şıkkı korundu: '{para_text[:50]}...'")
                                found_b = True
                                break
                            if para_text.strip().startswith("a)"):
                                print(f"HATA: a) şıkkı silinmemiş! İçerik: {para_text[:30]}")
                    if not found_b:
                        print("HATA: b) şıkkı bulunamadı!")
        
        if not found_eval:
            print("HATA: DEĞERLENDİRME başlığı bulunamadı!")
            
    except Exception as e:
        print(f"Docx okuma hatası: {e}")

def main():
    start_time = time.time()
    
    csv_input = os.path.join(base_dir, "output", "ihale_form_verileri_20260225.csv")
    template_path = os.path.join(base_dir, "Taslak İhale Dosyası.docx")
    output_dir = os.path.join(base_dir, "output", "test_out_13")
    
    print(f"--- Görev 13 Doğrulama Başlatıldı ---")
    
    form_data = load_csv_data(csv_input)
    if not form_data:
        return
        
    ihale_turu = form_data.get("ihale_turu")
    result = generate_filled_document(template_path, form_data, output_dir=output_dir)
    docx_file = result.get('docx')
    
    if docx_file and os.path.exists(docx_file):
        check_docx_evaluation(docx_file, ihale_turu)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"\nToplam Yürütme Süresi: {elapsed:.2f} saniye")
    
    today = datetime.now().strftime("%Y-%m-%d")
    result_csv = os.path.join(base_dir, f"{today}_task13_result.csv")
    with open(result_csv, "w", encoding="utf-8") as f:
        f.write(f"Tarih,Sure,Durum\n")
        f.write(f"{today},{elapsed:.2f},Tamamlandi\n")
    
if __name__ == "__main__":
    main()
