# Görev 34: İdari Uygunluk / Sözleşme Adı Birleşik Alan Düzenlemesi

## Yapılan İşlem
İdari Uygunluk Değerlendirme Tablosu ve Sözleşme Adı bölümlerinde yer alan; `< Proje adı >Projesi için <Mal Alımı/Hizmet Alımı/Yapım İşi>` şeklindeki karmaşık birleşik alanların, form verilerine göre (Proje Adı + İhale Türü) kusursuz ve kalın (bold) olarak doldurulması sağlanmıştır.

## Teknik Detaylar
1. **Paragraf Düzeyinde Rekonstrüksiyon**: Şablonda bu alanlar bazen tek bir sarı run, bazen ise birden fazla parçalı run olarak bulunmaktadır. Bu tutarsızlığı gidermek adına, ilgili anahtar kelimeleri (`Proje adı`, `Projesi için`) içeren paragraflar tespit edilerek içerikleri kod tarafında sıfırdan ve doğru mizanpajla (tablar ve boşluklar korunarak) yeniden oluşturulmaktadır.
2. **Mükerrerlik Koruması**: Proje adı inputu "Projesi" kelimesiyle bitse dahi (örn: *Akıllı Şehir Projesi*), regex temizleyici ile bu kelime budanır ve dökümandaki "Projesi için" ekiyle çakışması (mükerrer "Projesi Projesi") engellenir.
3. **Formatlama**: Yeni oluşturulan metin, şablonun orijinal etiketlerini (örn: *Adı:* veya *Sözleşme adı:*) korur ancak formdan gelen dinamik değerleri kalın (bold) olarak basar.

## Doğrulama
`test_gen.py` ve mock verilerle yapılan en son üretimde şu sonuçlar doğrulanmıştır:
- **İdari Uygunluk (P1373)**: `Adı:		Edirne Altyapi Gelistirme Projesi için Mal Alımı`
- **Sözleşme Adı (P1458)**: `Sözleşme adı: Edirne Altyapi Gelistirme Projesi için Mal Alımı`
- **Sonuç**: Her iki alan da tam istenen formatta ve hatasız üretilmiştir.

**Hesaplanan İşlem Süresi**: 7.62 saniye
**Sonuç Dosyası**: `2026-03-06_result.csv` güncellendi.
