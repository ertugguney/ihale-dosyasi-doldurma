# Görev 49: Taahhütname İhale Türü Uyarlaması

## Amaç
"Teklif Sunum Formu"ndaki Taahhütname bölümünde yer alan çoklu seçenekli placeholder'ın, seçilen ihale türüne (Mal/Hizmet/Yapım) göre otomatik olarak ayarlanması ve talimatların temizlenmesi.

## Yapılan İşlemler
1. **Dinamik Metin Seçimi**:
   - Taahhütname paragrafı ("imza atmaya yetkili kişisi olarak...") saptandı.
   - İhale Türü "Mal Alımı" ise: "**malları tedarik etmeyi**"
   - İhale Türü "Hizmet Alımı" ise: "**hizmetleri sağlamayı**"
   - İhale Türü "Yapım İşi" ise: "**yapım işini üstlenmeyi**"
   ifadelerinden uygun olanı otomatik olarak seçilip placeholder ( < > ) yerine yerleştirildi.

2. **Gelişmiş Placeholder Temizliği**:
   - `_replace_text_across_runs` fonksiyonu güçlendirilerek, farklı "run" yapılarına bölünmüş olsa dahi `<hizmetleri sağlamayı / malları tedarik etmeyi / yapım işini üstlenmeyi>` bloğunun tamamı başarıyla temizlendi.

3. **Talimat Ayıklama**:
   - Paragraf sonundaki "(Yararlanıcı ihale konusu... silmelidir.)" şeklindeki rehber metin dökümandan kaldırıldı.

## Sonuç
`test_taahhutname.py` scripti ile yapılan testlerde;
- İhale türüne göre doğru fiil grubunun yerleştiği,
- Placeholder parantezlerinin ( < > ) ve eğik çizgilerin ( / ) tamamen temizlendiği,
- Talimat metninin silindiği,
doğrulanmıştır.

---
**Durum:** ✅ Tamamlandı
**Tarih:** 13.03.2026
