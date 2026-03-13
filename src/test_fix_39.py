r"""
Görev 39 Doğrulama Scripti.

C:\Users\eguney\Desktop\ihale\output\ihale_form_verileri_20260225.csv
dosyasındaki verileri kullanarak döküman oluşturur ve "Sayın: " bölümünün altının 
doldurulmadığını (________________ olarak kaldığını) test eder.
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

def check_docx_content(docx_path):
    import docx
    try:
        doc = docx.Document(docx_path)
        found_sayin = False
        sayin_line_index = -1
        
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        
        for i, text in enumerate(paragraphs):
            if text.strip() == "Sayın:":
                print(f"\nTespit edilen Sayın: satırı: '{text}'")
                found_sayin = True
                success = False
                
                for j in range(1, 4):
                    if i + j < len(paragraphs):
                        next_line = paragraphs[i+j]
                        print(f"Sonraki satır {j}: '{next_line}'")
                        if "___________" in next_line:
                            print("BAŞARILI: '_____' satırı korunmuş.")
                            success = True
                
                if success:
                    return True
        
        if not found_sayin:
            print("Uyarı: 'Sayın:' satırı bulunamadı!")
            
        print("GÖREV BAŞARISIZ: Altında boş çizgi korunmamış veya değiştirilmiş.")
        return False
    except Exception as e:
        print(f"Docx okuma hatası: {e}")
        return False

def main():
    start_time = time.time()
    
    csv_input = os.path.join(base_dir, "output", "ihale_form_verileri_20260225.csv")
    template_path = os.path.join(base_dir, "Taslak İhale Dosyası.docx")
    output_dir = os.path.join(base_dir, "output", "test_out_39")
    
    print(f"--- Görev 39 Doğrulama Başlatıldı ---")
    
    form_data = load_csv_data(csv_input)
    if not form_data:
        return
        
    result = generate_filled_document(template_path, form_data, output_dir=output_dir)
    docx_file = result.get('docx')
    
    if docx_file and os.path.exists(docx_file):
        check_docx_content(docx_file)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"\nToplam Yürütme Süresi: {elapsed:.2f} saniye")
    
    today = datetime.now().strftime("%Y-%m-%d")
    result_csv = os.path.join(base_dir, f"{today}_task39_result.csv")
    with open(result_csv, "w", encoding="utf-8") as f:
        f.write(f"Tarih,Sure,Durum\n")
        f.write(f"{today},{elapsed:.2f},Tamamlandi\n")
    
if __name__ == "__main__":
    main()
