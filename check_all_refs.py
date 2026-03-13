import os
import glob
from docx import Document

files = glob.glob(r'output/test_out_teklif_sunum/*.docx')
if not files:
    print("No files found")
    exit(1)

latest_file = max(files, key=os.path.getmtime)
print(f"Checking file: {latest_file}")
doc = Document(latest_file)

count = 0
for i, p in enumerate(doc.paragraphs):
    if "Yayın Referansı" in p.text:
        count += 1
        print(f"Match {count} at P{i}: '{p.text}'")
        if "<sözleşme no" in p.text:
            print("  HATA: Placeholder hala duruyor!")
        else:
            print("  TEMİZ: Placeholder temizlenmiş.")
