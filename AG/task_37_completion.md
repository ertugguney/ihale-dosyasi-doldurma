# Görev 37: Teklif Sunum Formu Sözleşme Adı Mükerrerlik Koruma

## Yapılan İşlem
Teklif Sunum Formu sayfasında (P1458) yer alan `Sözleşme adı: < Proje adı >Projesi için <Mal Alımı/Hizmet Alımı/Yapım İşi>` birleşik alanı, mükerrerlik hatası ("Projesi Projesi") olmayacak şekilde ve kalın (bold) font ile otomatik doldurulmaktadır.

## Teknik Detaylar
1. **Dinamik Birleşim**: Şablon üzerindeki bu karmaşık yapı, `doc_generator.py` içerisindeki merkezi rekonstrüksiyon bloğu (Madde 34, 36, 37) tarafından yönetilir.
2. **Regex Filtreleme**: `proje_adi` inputundaki "Projesi" kelimesi, `re.sub(r'(?i)\s+projesi$', '', p_adi)` kuralıyla budanır. Boylece şablonun sabit parçası olan "Projesi için" metni ile birleştiğinde doğru ve tekil bir cümle yapısı oluşur.
3. **Mizanpaj**: `Sözleşme adı:` etiketi korunur ancak formdan beslenen değerler bold olarak basılır.

## Doğrulama
`test_gen.py` çalıştırılarak üretilen döküman incelenmiştir.
- **Bölüm D (Teklif Sunum Formu) - P1458**: `Sözleşme adı: Edirne Altyapi Gelistirme Projesi için Mal Alımı`
- **Sonuç**: Tekrar hatası giderilmiş, mizanpaj düzgün sekmeli ve kalın font ile tamamlanmıştır.

**Hesaplanan İşlem Süresi**: 7.62 saniye
**Sonuç Dosyası**: `2026-03-06_result.csv` güncellendi.
