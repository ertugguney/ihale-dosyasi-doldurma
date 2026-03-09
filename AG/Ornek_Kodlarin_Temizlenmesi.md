# Örnek Sözleşme Kodlarının Temizlenmesi

## Problem
Taslak dökümanın "İSTEKLİLERE TALİMATLAR" bölümünde, girdi alanlarının nasıl doldurulacağını göstermek amacıyla yer alan `<Örnek: TR21-11-İKT-1-XX>` gibi kılavuz metinler, dökümanın son çıktısında kalabalık oluşturmakta ve profesyonel olmayan bir görüntüye sebep olmaktadır.

## Çözüm
- `doc_generator.py` dosyasındaki `_process_paragraph_runs` fonksiyonu içerisinde yer alan "Gereksiz talimat metinlerini temizle" listesine bu örnek kod yapıları da eklendi.
- Sistem; `<Örnek: TR21-11-İKT-1-XX>`, `Örnek: TR21-11-İKT-1-XX`, `<Örnek: TR21-23-İKT-XX/01>` gibi varyasyonları tarayarak döküman üretim aşamasında bunları siler.
- Temizlik işlemi `r.text.replace(old_txt, "")` metoduyla gerçekleştirilir.

## Test ve Doğrulama
- `test_gen.py` üzerinden mock üretim tetiklendi.
- Çıktı dökümanı incelendiğinde, Sözleşme Kodu alanında sadece kullanıcının girdiği `TR21-23-IKT-01` verisinin kaldığı, yanındaki parantez içi örnek kısmın başarıyla silindiği doğrulanmıştır.
