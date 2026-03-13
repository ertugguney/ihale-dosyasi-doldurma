# Görev 47 (Görev 32): Mal Alımı Mali Teklif Formu Yayın Referansı Otomatik Doldurma

## Amaç
"Mal Alımı İhaleleri İçin MALİ TEKLİF FORMU" (Söz. EK:4a) bölümünde yer alan "Yayın Referansı" bilgisinin, formda girilen "Sözleşme Kodu" ile otomatik olarak doldurulması ve kılavuz metinlerin temizlenmesi.

## Yapılan İşlemler
1. **Esnek Placeholder Kontrolü**:
   - `doc_generator.py` içindeki mantık, döküman genelindeki tüm Yayın Referansı placeholder varyasyonlarını (`<sözleşme no/ihale no>`, `<sözleşme no/ihale no/lot no>` vb.) saptayacak şekilde genişletildi.
   - Bu sayede 27, 30 ve 32 numaralı görevler tek bir merkezi fonksiyonla çözüldü.

2. **Dinamik Veri Entegrasyonu**:
   - Formdaki `sozlesme_kodu` verisi, ilgili alanlara kalın (**bold**) olarak yerleştirildi.

3. **Placeholder ve Örnek Temizliği**:
   - Döküman genelindeki tüm `<...>` şeklindeki placeholderlar ve örnek format metinleri (`<Örnek: ...>`) dökümandan ayıklandı.

## Sonuç
`test_fix_32.py` ile yapılan doğrulamada, döküman içerisindeki tüm (toplam 3 adet) Yayın Referansı alanının başarıyla güncellendiği teyit edilmiştir.

---
**Durum:** ✅ Tamamlandı
**Tarih:** 12.03.2026
