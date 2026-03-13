# Davet Mektubu "Sayın: ________________" Satırının Korunması (Görev 39)

Bu görevde İhaleye Davet Mektubu sayfasında yer alan "Sayın:" metninin hemen altında ve sarı vurgulu olan "________________" satırının, Kurum Adı form verisi ile gereksiz yere ezilmesini engelledik.

## Yapılan İşlemler:
1. `field_config.py` içerisindeki `YELLOW_TO_UNIQUE_MAP` sözlüğünden "________________" çıkarıldı, böylece sistemin buraya Kurum Adı verisini basması önlendi.
2. Ancak sistem eşleşmeyen alanların metinlerini (sarı vurgulu ise) doğrudan sildiği için bu satır tamamen kayboluyordu. Bunu önlemek adına "________________" metni `INSTRUCTION_FIELDS` listesine (Talimatlar) eklendi.
3. Ancak `INSTRUCTION_FIELDS` içerisinde olan metinler de çıktı temizliği aşamasında görünmez yapılıyordu. Bu duruma özel olarak `doc_generator.py` içindeki mantığa müdahale edildi. Sadece alt çizgi karakterlerinden (`___`) oluşan talimat satırlarının **metinleri silinmedi**, yalnızca sarı vurgularının temizlenmesi sağlandı (`yr.font.highlight_color = None`).
4. Görevin doğrulaması için özel bir Python test scripti (`test_fix_39.py`) yazıldı ve `C:\Users\eguney\Desktop\ihale\output\ihale_form_verileri_20260225.csv` giriş verisiyle başarılı bir biçimde test edildi.
5. `docs/roadmap.md` ve `docs/project_details.md` belgelerine ilgili log kayıtları şeffaf bir nedensellik çerçevesinde eklendi.

Sistem başarıyla test edilmiş ve ilgili satır (________________) çıktı belge üzerinde güvence altına alınmıştır.
