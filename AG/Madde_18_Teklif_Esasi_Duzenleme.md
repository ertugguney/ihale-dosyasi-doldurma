# Madde 18 Teklif ve Sözleşme Türü Düzenlemesi

## Problem
Dökümanın "İSTEKLİLERE TALİMATLAR" (Madde 18) bölümünde, tekliflerin hangi esasa göre sunulacağı belirtilirken şablonda ham seçenekler ve talimatlar yer almaktaydı:
`Teklifler, götürü bedel / birim fiyat esaslı (her lot için uygun olan yöntem seçilecek ve belirtilecektir) olarak sunulmalıdır.`
Buradaki parantez içi talimat dökümanda kalmakta ve seçilen esasa (Götürü Bedel/Birim Fiyat) "esaslı" eki kullanıcı tarafından manuel eklenmek durumunda kalınmaktaydı.

## Çözüm
- `doc_generator.py` dosyasına Madde 18 için özel metin işleme mantığı eklendi.
- **Sonek Entegrasyonu**: Formdaki "Teklif Esası" seçiminin sonuna otomatik olarak " **esaslı**" kelimesi eklenir (Örn: **Birim Fiyat esaslı**).
- **Talimat Temizliği**: Paragraf içerisinde yer alan `(her lot için uygun olan yöntem seçilecek ve belirtilecektir)` ibaresi tamamen kaldırıldı.
- **Dinamik Değişim**: Şablon üzerindeki "götürü bedel / birim fiyat esaslı" kalıbı, kullanıcının seçimiyle akıllıca değiştirilir.
- **Biçimlendirme**: Seçilen esas metni dökümana kalın (**Bold**) olarak yansıtılarak vurgulanır.

## Test ve Doğrulama
- Mevcut CSV verisi ("Birim Fiyat" seçili) ile üretim yapıldı.
- Çıktı belgesinde Madde 18 içeriğinin tam olarak **"Teklifler, Birim Fiyat esaslı olarak sunulmalıdır."** şeklinde (talimatsız ve ekli) çıktığı doğrulanmıştır.
