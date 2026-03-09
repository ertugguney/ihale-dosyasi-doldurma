# Ön Ödeme Şartları ve Dinamik Cümle Düzenlemesi

## Problem
Dökümanın "SÖZLEŞME VE ÖZEL KOŞULLAR" bölümünde ön ödemeye dair talimatlar karmaşık bir yapıdaydı:
`<yapılmayacaktır/yapılacaktır(uygun olanı seçiniz)>. <Ön ödeme miktarı... %50’den yüksek...>`
Bu metnin hem profesyonelce temizlenmesi hem de seçilen ön ödeme durumuna göre genişleyen/daralan bir yapıya kavuşması gerekiyordu.

## Çözüm
- **Belge Dinamizmi**: `doc_generator.py` içinde ön ödeme paragrafı için tam metin rekonstrüksiyon mantığı güncellendi.
- **Koşullu Metin Akışı**: 
    - **Yapılmayacaktır** seçildiğinde: Sadece "Sözleşme kapsamında ön ödeme **yapılmayacaktır.**" cümlesi kalır.
    - **Yapılacaktır** seçildiğinde: Cümle otomatik olarak genişler ve "Ön ödeme miktarı sözleşme bedelinin % **[Oran]**’sı olan..." şeklindeki tam yasal ibareleri barındırır.
- **Küçük Harf ve Bold**: Kullanıcının seçimi cümleye küçük harfle başlanarak dahil edilir ve seçim ile oran bilgisi kalın (**Bold**) olarak vurgulanır.
- **Arayüz Kontrolü**: `app.py` üzerinde, kullanıcı "Yapılmayacaktır" dediği anda oransal giriş alanı (input) gizlenerek hatalı veri girişinin önüne geçilir.

## Test ve Doğrulama
- Farklı ön ödeme senaryoları ile `test_gen.py` üzerinden doğrulamalar yapıldı.
- Çıktıda noktalama işaretlerinin (nokta biter bitmez başlayan yeni cümleler) tam olduğu ve metnin akışkan bir profesyonellikte olduğu teyit edilmiştir.
