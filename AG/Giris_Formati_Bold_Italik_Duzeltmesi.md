# Veri Girdilerinin (Input) Görünüm Ayarı Düzeltmesi

## Problem
Kullanıcı tarafından forma girilen bilgilerin bazen şablonun orijinal stilinden (italik vb.) etkilenmesi veya programatik olarak (kodla) yeniden oluşturulan paragraflarda (Ön Ödeme, Kesin Teminat vb.) standart stilde kalması söz konusuydu. Kullanıcı, tüm girdi verilerinin istisnasız **koyu (bold)** yazılmasını ve asla **italik (eğik)** olmamasını talep etti.

## Çözüm
- `doc_generator.py` içindeki tüm veri yerleştirme noktaları (`_process_paragraph_runs`) revize edildi.
- Değer atanan her `run` objesi için `font.bold = True` ve `font.italic = False` kesin olarak atandı.
- Kod tarafından baştan yazılan (add_run metodu kullanılan) "Ön Ödeme" ve "Kesin Teminat" paragraflarında da değişkenlerin (oranlar vb.) üzerine bu stil kuralları tek tek uygulandı.
- Davet mektubu içerisindeki mal listesi/ihale konusu gibi maddelere de (`r.font.italic = False`) kuralı eklendi.

## Test ve Doğrulama
- `test_gen.py` üzerinden `C:\Users\eguney\Desktop\ihale\output\ihale_form_verileri_20260225.csv` datasıyla üretim tetiklendi.
- Çıktı Word belgesi ve PDF kontrol edildiğinde; girilen kurum adlarından, tarihlere, sayısal oranlardan, yer bilgilerine kadar tüm form verilerinin belgede **Kalın (Bold)** ve **Düz (İtalik Değil)** olarak başarıyla basıldığı teyit edildi.
- İşlem süresi: ~2.5 saniye (Lokal üretim).
