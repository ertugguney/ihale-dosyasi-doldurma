# Davet Mektubu Değerlendirme Bölümü Şartlı Seçimi

## Problem
İhale dökümanının "İHALEYE DAVET MEKTUBU" bölümünde, ihalenin türüne göre (Mal, Hizmet veya Yapım) farklı değerlendirme kriterleri sunulmaktaydı. Şablonda hem Mal/Yapım hem de Hizmet alımı için seçenekler (`a` ve `b` şıkları olarak) ve bu seçeneklerin nasıl kullanılacağına dair bir talimat metni bir arada bulunuyordu. Bu durum, çıktının profesyonel görünmesini engelliyor ve manuel temizlik gerektiriyordu.

## Çözüm
- `doc_generator.py` içindeki paragraf işleme döngüsüne özel bir mantık eklendi.
- **Talimat Temizliği**: "DEĞERLENDİRME: (İhalenize aşağıdaki ifadelerden hangisi uygun ise onu seçiniz...)" satırı tespit edilerek parantez içindeki tüm gereksiz talimatlar kaldırıldı ve başlık "DEĞERLENDİRME: " olarak sadeleştirildi.
- **Akıllı Madde Seçimi**: `form_data` içerisindeki `ihale_turu` bilgisine bakılarak;
    - Eğer "Mal Alımı" veya "Yapım İşi" seçildiyse: "a)" maddesi tutulup "b)" maddesi silindi.
    - Eğer "Hizmet Alımı" seçildiyse: "b)" maddesi tutulup "a)" maddesi silindi.
- **Prefix Temizliği**: Bırakılan cümlenin başındaki "a)" veya "b)" harf işaretleri de temizlenerek sadece ilgili açıklama cümlesi belgede bırakıldı.

## Test ve Doğrulama
- Mevcut test CSV datası (Hizmet Alımı içeriyor) ile test yapıldı.
- Çıktı belgesinde sadece hizmet alımına ait "Teknik değerlendirmenin %80, fiyatın %20 olarak ağırlıklandırılacağı..." cümlesinin kaldığı ve diğer tüm karmaşıklığın giderildiği teyit edildi.
