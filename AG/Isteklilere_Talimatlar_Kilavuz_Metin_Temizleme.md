# İsteklilere Talimatlar Bölümündeki Kılavuz Metnin Temizlenmesi

## Problem
Taslak dökümanın "İSTEKLİLERE TALİMATLAR" başlığı altında, dökümanı dolduran kuruma rehberlik etmesi amacıyla parantez içerisinde yer alan döküman doldurma talimatı ("Aşağıda yer alan maddeler içerisindeki boş yerler... siliniz. Diğer metinleri hiçbir şekilde değiştirmeyiniz.") dökümanın son halinden (çıktısından) profesyonel görünümün korunması için silinmelidir.

## Çözüm
- `doc_generator.py` dosyası içerisinde paragraf seviyesinde tarama yapan döngüye, bu kılavuz metni saptayan bir koşul eklendi.
- `if "Aşağıda yer alan maddeler içerisindeki boş yerler" in para.text and "Diğer metinleri hiçbir şekilde değiştirmeyiniz" in para.text:` kontrolü ile ilgili paragraf tespit edilir ve döküman nesnesinden (`paragraphs_to_remove`) tamamen silinir.
- Bu saptama yöntemi, yanlışlıkla başka içeriklerin silinmesini önlemek için her iki kritik cümlenin beraberliğini doğrular.

## Test ve Doğrulama
- Mevcut test verisi (`ihale_form_verileri_20260225.csv`) ile `test_gen.py` üzerinden doğrulama yapıldı.
- Üretilen belgenin "İSTEKLİLERE TALİMATLAR" bölümünde, doğrudan madde 1'e geçildiği ve aradaki parantezli rehberlik metninin dökümandan tamamen temizlendiği görülmüştür.
- Exit code: 0 ile işlem tamamlandı.
