r"""
Görev 38 Doğrulama Scripti.

Bu script, C:\Users\eguney\Desktop\ihale\output\ihale_form_verileri_20260225.csv
dosyasındaki verileri kullanarak döküman oluşturur ve düzeltmeleri kontrol eder.
"""

import os
import sys
import csv
import time
from datetime import datetime

# Proje kök dizinini ekle
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

def main():
    start_time = time.time()
    
    csv_input = os.path.join(base_dir, "output", "ihale_form_verileri_20260225.csv")
    template_path = os.path.join(base_dir, "Taslak İhale Dosyası.docx")
    output_dir = os.path.join(base_dir, "output", "test_out_38")
    
    print(f"--- Görev 38 Doğrulama Başlatıldı ---")
    print(f"Girdi Dosyası: {csv_input}")
    
    form_data = load_csv_data(csv_input)
    if not form_data:
        return
        
    # Test verisini uygula
    result = generate_filled_document(template_path, form_data, output_dir=output_dir)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"\n--- Sonuçlar ---")
    print(f"Oluşturulan Word: {result.get('docx')}")
    if result.get('pdf'):
        print(f"Oluşturulan PDF: {result.get('pdf')}")
    
    print(f"\nİstatistikler:")
    for k, v in result.get('stats', {}).items():
        print(f"  {k}: {v}")
        
    print(f"\nToplam Yürütme Süresi: {elapsed:.2f} saniye")
    
    # Kural gereği sonuç CSV oluştur (farklı isimle)
    today = datetime.now().strftime("%Y-%m-%d")
    result_csv = os.path.join(base_dir, f"{today}_task38_result.csv")
    with open(result_csv, "w", encoding="utf-8") as f:
        f.write(f"Tarih;Sure;Durum\n")
        f.write(f"{today};{elapsed:.2f};Tamamlandi\n")
    
    print(f"Sonuç raporu oluşturuldu: {result_csv}")

if __name__ == "__main__":
    main()
