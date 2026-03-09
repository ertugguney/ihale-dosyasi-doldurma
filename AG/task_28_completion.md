# Görev 28: Adli Sicil Kaydı Yıl Girişi

## Yapılan İşlem
Yapım işi ihaleleri için teknik teklif formunda (Söz. EK: 3c) yer alan "Adli Sicil Kaydı Son <rakam girin> yıl içerisinde..." ifadesinin dinamik hale getirilmesi sağlanmıştır.

## Teknik Detaylar
1. **Field Config Güncellemesi**: `src/field_config.py` içerisine `dava_gecmisi_yili` ID'si ile yeni bir sayısal alan eklenmiştir.
   - **Başlık**: "Kaç yıl geriye doğru Adli Sicil Kaydı İstenecek"
   - **Eşleştirme**: `<rakam girin>` placeholder'ı bu alanla eşlenmiştir.
2. **Kategori**: "Sözleşme Bilgileri" kategorisi altında konumlandırılmıştır.
3. **Validasyon**: 1 ile 20 yaş arasında bir değer girilmesi zorunlu tutulmamış ancak varsayılan olarak desteklenmiştir.

## Doğrulama
`test_gen.py` çalıştırılarak döküman üretilmiş ve döküman içeriğinde "Son 1 yıl içerisinde..." (test verisindeki değer) ifadesinin doğru şekilde yer aldığı teyit edilmiştir.

**Hesaplanan İşlem Süresi**: 7.62 saniye (Döküman üretimi ve PDF dönüşümü dahil)
**Sonuç Dosyası**: `2026-03-06_result.csv` oluşturuldu.
