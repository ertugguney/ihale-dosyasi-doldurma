# Madde 17 f) Bendi Geçici Teminat Seçimi Düzenlemesi

## Problem
Dökümanın "İSTEKLİLERE TALİMATLAR" (Madde 17) bölümündeki f fıkrasında, geçici teminata dair karmaşık bir yapı bulunmaktaydı:
`f) İstenmesi halinde Md. 26’daki koşullara uygun sunulmuş geçici teminat (İSTENMEKTEDİR / İSTENMEMEKTEDİR.) <uygun olan seçeneği seçiniz >`
Buradaki hem ham seçenekler hem de kılavuz metinler dökümanda kalıyor ve manuel silme gerektiriyordu.

## Çözüm
- `doc_generator.py` dosyasına Madde 17 f bendi için özel bir paragraf yeniden yazma mantığı eklendi.
- **Dinamik Seçim**: Formdaki "Geçici Teminat" açılır menüsünden seçilen veri (**İSTENMEKTEDİR** veya **İSTENMEMEKTEDİR**) programatik olarak alınır.
- **Talimat Temizliği**: Paragraf içeriği tamamen temizlenerek, sadece seçilen geçerli seçenek ve maddenin ana metni birleştirilir.
- **Biçimlendirme**: Seçilen seçenek sonuna nokta (`.`) eklenmiş ve profesyonel bir vurgu için kalın (**Bold**) yazı tipiyle dökümana yansıtılmıştır.

## Test ve Doğrulama
- `test_gen.py` ve mevcut CSV datası üzerinden üretim yapıldı.
- Çıktı belgesinin Madde 17 f fıkrasında artık sadece **"f) İstenmesi halinde Md. 26’daki koşullara uygun sunulmuş geçici teminat İSTENMEMEKTEDİR."** (veya seçim neyse o) yazdığı, parantezli karmaşanın ve uyarıların tamamen temizlendiği teyit edildi.
