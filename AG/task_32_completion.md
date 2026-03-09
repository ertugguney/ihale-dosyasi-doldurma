# Görev 32: Mal Alımı Mali Teklif Formu Örnek Placeholder Temizliği

## Yapılan İşlem
Mal Alımı İhaleleri İçin MALİ TEKLİF FORMU (EK:4b) "Yayın referansı" alanında yer alan `<Örnek: TR21-23-İKT-XX/01>` metninin çıktı dökümanda kesinlikle görünmemesi sağlanmış ve doğrulanmıştır.

## Teknik Detaylar
1. **Global Temizlik Kuralı**: Döküman jeneratöründe (`doc_generator.py`) bulunan merkezi talimat temizleme listesine ilgili örnek placeholder metinleri eklenmiştir.
2. **Kapsam**: Bu kural EK:4a (Hizmet) ile ortak çalışmakta olup, EK:4b (Mal) formunun döküman yapısındaki ilgili paragrafı da otomatik olarak temizlemektedir.
3. **Regex Desteği**: Metin içerisinde tırnak karakterleri (`‘`, `’`, `'`) veya büyük/küçük harf varyasyonları olsa dahi merkezi filtreleme ile ayıklama yapılmaktadır.

## Doğrulama
`test_gen.py` çalıştırılarak üretilen dökümanın EK:4b bölümü incelenmiştir.
- **Döküman İçeriği**: `Yayın referansı : TR21-23-IKT-01/01` (Sadece girilen veri görünmekte, örnek metin tamamen silinmiş).
- **Sonuç**: Beklenen temizlik sağlanmıştır.

**Hesaplanan İşlem Süresi**: 7.62 saniye
**Sonuç Dosyası**: `2026-03-06_result.csv` güncellendi.
