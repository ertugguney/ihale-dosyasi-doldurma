# Görev 30: Örnek Placeholder Temizliği

## Yapılan İşlem
Hizmet Alımı İhaleleri İçin MALİ TEKLİF FORMU (EK:4a) ve diğer ilgili bölümlerdeki "Yayın referansı" alanında bulunan `<Örnek: TR21-23-İKT-XX/01>` gibi placeholder metinlerin temizlenmesi işlemi doğrulanmıştır.

## Teknik Detaylar
1. **Dinamik Temizlik**: `src/doc_generator.py` içerisindeki `_process_paragraph_runs` fonksiyonu, döküman üzerindeki yellow-highlighted run'ları birleştirerek `combined_text` oluşturur.
2. **Talimat Algılama**: `combined_text` içerisinde `"<Örnek:"` ifadesi geçtiğinde, bu alan bir "instruction" (talimat) olarak kabul edilir ve dökümandan tamamen temizlenir.
3. **Manuel Filtreleme**: Alternatif bir önlem olarak, paragraf düzeyinde metin tabanlı temizleme listesine de ilgili string eklenmiştir.

## Doğrulama
`test_gen.py` çalıştırılarak üretilen dökümanlar (EK:4a, 4b, 4c) incelenmiş ve "Yayın referansı" satırında sadece formdan gelen gerçek değerin (örn: `TR21-23-IKT-01/01`) yer aldığı, örnek metinlerin ise tamamen yok edildiği teyit edilmiştir.

**Hesaplanan İşlem Süresi**: 7.62 saniye
**Sonuç Dosyası**: `2026-03-06_result.csv` güncellendi.
