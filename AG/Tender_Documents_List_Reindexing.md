# Görev 44 (Görev 17): Madde 17 İhale Dosyası Belgeleri Re-İndeksleme

## Amaç
"İSTEKLİLERE TALİMATLAR" (Madde 6/17) altındaki doküman listesinin, seçilen **İhale Usulü**ne (Açık/Pazarlık) göre dinamik olarak düzenlenmesi, silinen maddeler sonrası indekslerin (a, b) otomatik kaydırılması ve gereksiz parantezlerin temizlenmesi.

## Yapılan İşlemler
1. **Pazarlık Usulü Yapılandırması**:
   - `a) İhaleye davet mektubu` satırı korunur.
   - Satır sonundaki `(Sadece Pazarlık Usulü İhalelerde kullanılacaktır.)` talimatı ve her türlü parantez tamamen silinir.
   - `b) Teklif Dosyası (...)` satırı korunur.

2. **Açık İhale Usulü Yapılandırması**:
   - `İhaleye davet mektubu` satırı dökümandan tamamen kaldırılır.
   - Normalde `b)` olan `Teklif Dosyası` satırı, otomatik olarak `a)` bendine çekilir (Re-indexing).

3. **Format Temizliği**:
   - Satırların yeniden inşasında `para.text = ""` ve `add_run()` yöntemleri kullanılarak, Word'ün otomatik numaralandırma (auto-numbering) özelliklerinden kaynaklı mizanpaj hatalarının ve "bir önceki düzeltmede kalan boş parantezlerin" önüne geçilmiştir.
   - Tüm prefixler (`a)`, `b)`) standart ve temiz bir şekilde uygulanmıştır.

4. **Teknik Uygulama**:
   - `doc_generator.py` içindeki ana döngüde, ilgili paragraflar anahtar kelimelerle ("İhaleye davet mektubu", "Teklif Dosyası") saptanıp, `ihale_usulu` değişkenine göre koşullu olarak yeniden yazılmaktadır.
   - `continue` ifadesi ile bu paragrafların genel run işleme sürecinden ayrıştırılması sağlanmıştır.

## Sonuç
`test_fix_17.py` ile yapılan kapsamlı testlerde;
- **Pazarlık Usulü**'nde a ve b maddelerinin hatasız listelendiği,
- **Açık İhale Usulü**'nde davet mektubu satırının silindiği ve teklif dosyasının başarıyla `a)` bendine kaydırıldığı,
doğrulanmıştır.

---
**Durum:** ✅ Tamamlandı
**Tarih:** 12.03.2026
