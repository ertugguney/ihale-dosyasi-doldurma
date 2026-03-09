# Görev 36: Teknik Değerlendirme Tablosu Proje Adı Koruması

## Yapılan İşlem
TEKNİK DEĞERLENDİRME TABLOSU sayfasında yer alan; `<proje adı> Projesi için <Mal Alımı/Yapım İşi>` şeklindeki birleşik alanın, form verilerindeki "Projesi" kelimesiyle çakışarak oluşturduğu "Projesi Projesi" mükerrerlik hatası giderilmiştir.

## Teknik Detaylar
1. **Büyük/Küçük Harf Duyarsız Eşleşme**: Şablonda bu alan `proje adı` (küçük harf) olarak geçtiği için, eşleştirme algoritması tüm varyasyonları (büyük/küçük harf) kapsayacak şekilde güncellenmiştir.
2. **Merkezi Rekonstrüksiyon**: Paragraf, `doc_generator.py` içerisinde özel bir blokla (`Sözleşme başlı`) yakalanarak sıfırdan oluşturulur. `p_adi_clean` fonksiyonu ile inputtaki "Projesi" kelimesi budanır ve şablonun sabit "Projesi için" metniyle mükemmel uyum sağlanır.
3. **Formatlama**: Veriler dökümana **kalın (bold)** olarak işlenir ve etraftaki `< >` ayraçları tamamen temizlenir.

## Doğrulama
`test_gen.py` ve mock verilerle yapılan en son üretimde şu sonuç doğrulanmıştır:
- **Teknik Değerlendirme (P1427)**: `Sözleşme başlı	: Edirne Altyapi Gelistirme Projesi için Mal Alımı`
- **Sonuç**: "Projesi Projesi" tekrarı engellenmiş ve veri bold olarak dökümana işlenmiştir.

**Hesaplanan İşlem Süresi**: 7.62 saniye
**Sonuç Dosyasi**: `2026-03-06_result.csv` güncellendi.
