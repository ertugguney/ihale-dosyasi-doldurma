# Teslimat Adresi ve "Adresine" İfadesi Düzenlemesi

## Problem
Dökümanın "İSTEKLİLERE TALİMATLAR" bölümünde, tekliflerin gönderileceği adreslerin belirtilmesi gereken satırlar ham metin olarak kalmaktaydı. Kullanıcının her ihalede bu adresleri manuel yazması gerekiyordu ve cümle sonu ("Adresine") eksikti.

## Çözüm
- `doc_generator.py` içerisindeki paragraf döngüsüne Madde 22/23 için özel bir kontrol eklendi.
- **Hedef Cümleler**: 
    1. "Taahhütlü posta / kargo servisi) ile"
    2. "Ya da Sözleşme Makamına doğrudan elden"
- **Dinamik Veri**: Formda girilen **İşin/Teslimin Gerçekleştirileceği Yer** (`teslim_yeri`) bilgisi bu cümlelerden hemen sonra otomatik olarak enjekte edilir.
- **Tamamlayıcı Metin**: Adres bilgisinden hemen sonra cümleyi makul bir Türkçe yapısına kavuşturan "**Adresine**" kelimesi eklenir.
- **Biçimlendirme**: Eklenen adres bilgisi kalın (**Bold**) yapılarak döküman içerisinde belirgin hale getirildi.

## Test ve Doğrulama
- Mevcut CSV datası ("Keşan Belediyesi..." adresi) ile üretim yapıldı.
- Çıktı belgesinde ilgili satırların tam olarak şu şekilde göründüğü doğrulandı:
    > "... kargo servisi) ile **Keşan Belediyesi, No: 5 Keşan / Edirne** Adresine"
    > "Ya da Sözleşme Makamına doğrudan elden **Keşan Belediyesi, No: 5 Keşan / Edirne** Adresine"
