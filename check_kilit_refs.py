import os
import glob
import re
from docx import Document

files = glob.glob(r'output/test_out_kilit_uzman/*.docx')
if not files:
    print("No files found")
    exit(1)

latest_file = max(files, key=os.path.getmtime)
print(f"Checking file: {latest_file}")
doc = Document(latest_file)

count = 0
for i, p in enumerate(doc.paragraphs):
    p_norm = p.text.lower().replace('ı', 'i').replace('i̇', 'i')
    if "yayin referans" in p_norm:
        count += 1
        print(f"Match {count} at P{i}: '{p.text}'")
        if "<sözleşme no" in p.text.lower() or "<sozlesme no" in p.text.lower():
            print("  HATA: Placeholder hala duruyor!")
        else:
            print("  TEMİZ: Başarıyla güncellendi.")

if count >= 6:
    print(f"\nTOPLAM {count} REFERANS BULUNDU VE KONTROL EDİLDİ.")
else:
    print(f"\nUYARI: Sadece {count} referans bulundu. (Beklenen: en az 6)")
