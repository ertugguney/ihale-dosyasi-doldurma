# Görev 31: Mali Teklif Formu Proje Adı Koruması (Mal Alımı)

## Yapılan İşlem
Mal Alımı İhaleleri İçin MALİ TEKLİF FORMU (Söz. EK:4b) bölümünde karşılaşılan "Projesi Projesi" kelime tekrarı sorunu kalıcı olarak çözülmüştür.

## Teknik Detaylar
1. **RegEx Temizliği**: `src/doc_generator.py` içerisindeki `proje_adi` alanı işlenirken, metnin sonunda yer alan "Projesi" kelimesi (büyük/küçük harf duyarsız) otomatik olarak temizlenmektedir.
2. **Kod Paylaşımı**: Bu özellik Görev 29 (Hizmet Alımı) ile paylaşılan merkezi bir kuraldır (`re.sub(r'(?i)\s+projesi$', '', str(value))`). 
3. **Kapsamlı Koruma**: Şablon içerisinde statik olarak gelen " Projesi için Mal Alımı" gibi ifadelerle kullanıcının girdiği "Edirne Altyapi Gelistirme Projesi" verisi çakışmaz; sonuç her zaman tekil "Projesi" şeklinde oluşur.

## Doğrulama
`test_gen.py` çalıştırılarak `İhale_Dosyası_Edirne_Belediye_Baskanligi_20260306_165729.docx` dökümanı incelenmiştir.
- **Döküman İçeriği**: `Sözleşme başlığı :Edirne Altyapi Gelistirme Projesi için Mal Alımı Temini`
- **Sonuç**: Tekrar (Projesi Projesi) engellenmiş ve gramer hatası giderilmiştir.

**Hesaplanan İşlem Süresi**: 7.62 saniye
**Sonuç Dosyası**: `2026-03-06_result.csv` güncellendi.
