# Görev 45 (Görev 27): Teknik Teklif Formu Yayın Referansı Otomatik Doldurma

## Amaç
"TEKNİK TEKLİF FORMU" (Söz. EK: 3b) ve benzeri eklerde yer alan "Yayın Referansı" bilgisinin, formda girilen "Sözleşme Kodu" ile otomatik olarak doldurulması, kılavuz/örnek metinlerin temizlenmesi ve profesyonel görünüm sağlanması.

## Yapılan İşlemler
1. **Dinamik Veri Aktarımı**:
   - Döküman genelindeki "Yayın Referansı" satırları tespit edildi.
   - Formdan gelen `sozlesme_kodu` verisi bu alanlara otomatik olarak aktarıldı.

2. **Talimat ve Örnek Temizliği**:
   - `<sözleşme no/ihale no>` ve `<sözleşme no/ihale no/lot no>` şeklindeki placeholderlar tamamen kaldırıldı.
   - Satır yanındaki `<Örnek: TR21-23-İKT-XX/01>` gibi açıklayıcı metinler dökümandan ayıklandı.

3. **Görsel Biçimlendirme**:
   - Eklenen sözleşme kodu metni döküman içerisinde **kalın (bold)** olarak işaretlendi.
   - `para.add_run()` yöntemiyle format bütünlüğü korundu.

4. **Kapsamlı Uygulama**:
   - Sadece Mal Alımı değil, döküman içerisinde bu placeholderı içeren tüm bölümler (Hizmet vb.) tek bir mantıkla güncellendi.

## Sonuç
`test_fix_27.py` scripti ile yapılan testlerde;
- Tüm "Yayın Referansı" alanlarının boşaltılıp form verisiyle doldurulduğu,
- Eski talimat izlerinin kalmadığı,
- Verinin kalın basıldığı,
doğrulanmıştır.

---
**Durum:** ✅ Tamamlandı
**Tarih:** 12.03.2026
