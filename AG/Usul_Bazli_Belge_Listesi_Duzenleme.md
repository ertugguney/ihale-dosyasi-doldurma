# İhale Usulüne Göre Belge Listesi Düzenlemesi

## Problem
Dökümanın "İSTEKLİLERE TALİMATLAR" (Madde 17) bölümünde, ihale dosyasını oluşturan belgelerin listesi sunulmaktadır. Ancak bu liste, ihale usulüne (Pazarlık veya Açık) göre farklılık göstermeli ve döküman doldurma talimatlarını barındırmamalıdır.
1. Pazarlık Usulü'nde: Davet mektubu maddesi gelmeli ancak yanındaki parantez içi talimat silinmelidir.
2. Açık İhale Usulü'nde: Davet mektubu maddesi hiç gelmemeli ve sonraki maddeler (b -> a) şeklinde yeniden numaralandırılmalıdır.

## Çözüm
- `doc_generator.py` içindeki ana paragraf döngüsüne Madde 17 için özel bağlamsal kontrol eklendi.
- **Pazarlık Usulü Seçeneği**:
    - "İhaleye davet mektubu" içeren paragraf korunur.
    - `(Sadece Pazarlık Usulü İhalelerde kullanılacaktır.)` gibi talimat metinleri `replace` metoduyla run seviyesinde temizlenir.
- **Açık İhale Usulü Seçeneği**:
    - "İhaleye davet mektubu" maddesi `paragraphs_to_remove` listesine eklenerek tamamen silinir.
    - "Teklif Dosyası" maddesi (normalde b şıkkı) tespit edilerek, başındaki `b)` harfi programatik olarak `a)` harfi ile değiştirilir. Bu sayede liste sıralaması bozulmadan a'dan başlar.

## Test ve Doğrulama
- `test_gen.py` ile her iki usul senaryosu için üretim yapıldı.
- **Pazarlık çıktısında**: Davet mektubu maddesinin talimatsız basıldığı,
- **Açık ihale çıktısında**: Davet mektubu maddesinin silindiği ve listenin doğrudan "a) Teklif Dosyası" olarak başladığı,
teyit edilmiştir.
