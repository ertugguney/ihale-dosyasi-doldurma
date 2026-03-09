# İhale Konusu Alım Kalemlerinin Dinamik Listelenmesi Düzeltmesi

## Problem
İhale dökümanının "İHALEYE DAVET MEKTUBU" bölümünde, ihale konusunun kalem kalem (i, ii, iii vb.) listelenmesi gereken bir yapı bulunmaktaydı. Ancak önceki sistemde "İhale Konusu" tek bir metin alanı (textarea) olarak tasarlandığı için, bu kalemleri şablondaki (i), (ii) satırlarına sırayla dağıtmak teknik olarak zordu ve kullanıcı deneyimi açısından verimsizdi.

## Çözüm
- **Dinamik Liste Girişi**: `field_config.py` içinde `ihale_konusu` alan tipi `list` olarak güncellendi.
- **Modern Arayüz**: `app.py` dosyasına `list` tipi desteği eklendi. Kullanıcı artık arayüzde kalemleri tek tek girebilmekte ve "➕ Yeni Kalem Ekle" butonuyla dilediği kadar girdi satırı oluşturabilmektedir.
- **Akıllı Dağıtım (Davet Mektubu)**: `doc_generator.py` içindeki `_process_paragraph_runs` fonksiyonu, davet mektubu sayfasındaki (i), (ii), (iii) işaretleyicilerini tespit ederek formdan gelen liste kalemlerini buralara sırasıyla yerleştirir. Eğer girilen kalem sayısı şablondaki yerden azsa, fazla satırlar otomatik temizlenir.
- **Otomatik Birleştirme**: Belgenin diğer tüm bölümlerinde (ihale ilanı, sözleşme başlığı vb.), bu liste kalemleri programatik olarak virgülle (", ") birleştirilerek tek bir akıcı metin haline getirilir.

## Test ve Doğrulama
- `test_gen.py` ve mevcut CSV datasıyla üretim denemesi yapıldı.
- Çıktı belgesi incelendiğinde:
    - Davet mektubunda kalemlerin alt alta madde madde dizildiği,
    - Diğer bölümlerde ise kalemlerin yan yana virgülle dizildiği,
  teyit edildi. Sistem hatasız çalışmaktadır.
