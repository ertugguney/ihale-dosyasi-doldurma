# İhale Tarih ve Saat Bilgilerinin Birleştirilmesi Düzeltmesi

## Problem
İhale şablonu içerisinde bazı alanlarda (örneğin "Teklif teslimi için son tarih ve saati") hem tarih hem de saat bilgisinin yan yana olması bekleniyordu. Ancak sistem, formdaki `ihale_tarihi` ve `ihale_saati` alanlarını iki ayrı veri olarak gördüğü için bu tip birleşim noktalarında sadece tarih bilgisini (`06/03/2026`) yazdırıyor, saat bilgisi eksik kalıyordu.

## Çözüm
- `doc_generator.py` dosyasına akıllı bir "bağlamsal birleştirme" mantığı eklendi.
- `ihale_tarihi` alanı bir paragrafa yerleştirilirken, sistem ilgili paragrafın metni içinde "tarih" ve "saat" kelimelerinin (küçük harfe duyarsız olarak) aynı anda geçip geçmediğini kontrol eder.
- Eğer her iki kelime de bulunuyorsa (örn: "son tarih ve saati"), sistem otomatik olarak `ihale_tarihi` bilgisinin yanına bir boşluk ekleyerek `ihale_saati` bilgisini de iliştirir.
- Birleştirme kuralı: `{tarih} {saat}` (Örn: `06/03/2026 10:00`) şeklinde uygulanır.

## Test ve Doğrulama
- Mevcut test verisi (`ihale_form_verileri_20260225.csv`) ile `test_gen.py` üzerinden mock üretim yapıldı.
- Üretilen Word ve PDF belgeleri incelendiğinde, ilgili maddenin `<06/03/2026 10:00>` şeklinde (ayraçlar bir önceki görevde kalktığı için `06/03/2026 10:00` şeklinde) tam veri ile dolduğu teyit edildi.
- İşlem başarıyla tamamlandı (Exit code: 0).
