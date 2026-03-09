# Madde 8 İhalenin Yabancı İsteklilere Açıklığı Düzenlemesi

## Problem
Dökümanın "İSTEKLİLERE TALİMATLAR" (Madde 8) bölümünde, ihalenin kimlere açık olduğunu belirten iki seçenekli bir yapı bulunmaktaydı:
`<Sözleşme Makamı tarafından gerçekleştirilecek ihaleler yerli yabancı tüm isteklilere açıktır. / Sözleşme Makamı tarafından gerçekleştirilecek ihaleler sadece yerli isteklilere açıktır.(Uygun olanı seçiniz)>`
Bu yapı hem okunaklılığı bozmakta hem de manuel müdahale gerektirmekteydi.

## Çözüm
- `doc_generator.py` dosyasına Madde 8 için özel bir bağlamsal tarama mantığı eklendi.
- **Seçim Yerleştirme**: Formda "İstekli Kapsamı" açılır menüsünden seçilen seçenek otomatik olarak saptanır.
- **Dinamik Değişim**: Şablon üzerindeki ikili seçenek yapısı tamamen silinir ve sadece kullanıcının seçtiği ifade (Örn: **Sözleşme Makamı tarafından gerçekleştirilecek ihaleler sadece yerli isteklilere açıktır.**) yerleştirilir.
- **Talimat Temizliği**: Metnin sonundaki "(Uygun olanı seçiniz)>" gibi kılavuz ibareler tamamen ayıklanır.
- **Biçimlendirme**: Yeni metin, dökümana kalın (**Bold**) yazı tipiyle yansıtılarak vurgulanır.

## Test ve Doğrulama
- Mevcut CSV verisi ("Sadece yerli isteklilere açıktır" seçili) ile üretim yapıldı.
- Çıktı belgesinde Madde 8 içeriğinin tam olarak seçilen opsiyonu barındırdığı ve gereksiz ok (`>`) veya parantez işaretlerini içermediği doğrulanmıştır.
