# Görev 33: İstekli Adı İmza Alanı Koruması (Mali Teklif)

## Yapılan İşlem
Mal Alımı ve Hizmet Alımı İhaleleri İçin MALİ TEKLİF FORMLARI (Söz. EK:4a, 4b) içerisinde yer alan "İsteklinin adı : … … … … … … … … …" kısımlarının form verileriyle doldurulması engellenmiş, bu alanların imza için boş kalması (noktalı mizanpaj) sağlanmıştır.

## Teknik Detaylar
1. **İstisna Tanımı**: `doc_generator.py` döküman işleme döngüsünde, sarı vurgulu alanlar dahi olsa, paragraf içerisinde "İsteklinin adı" ifadesi geçtiğinde doldurma işlemi atlanır.
2. **Büyük/Küçük Harf Duyarlılığı**: Arama işlemi büyük/küçük harf duyarsız (case-insensitive) hale getirilerek farklı yazım biçimlerinin de yakalanması sağlanmıştır (`lower_para = para.text.lower()`).
3. **Mizanpaj Koruması**: Varsa mevcut sarı vurgular dökümandan kaldırılır (`highlight_color = None`) ancak orijinal noktalı metin (`… … … … … … … … …`) değiştirilmeden bırakılır.

## Doğrulama
`test_gen.py` ve `ihale_form_verileri_20260225.csv` ile yapılan üretimde EK:4a ve EK:4b bölümleri doğrulanmıştır.
- EK: 4a (P1086): `İsteklinin adı : … … … … … … … … …` (Dots preserved)
- EK: 4b (P1129): `İsteklinin adı : … … … … … … … … …` (Dots preserved)

**Hesaplanan İşlem Süresi**: 7.62 saniye
**Sonuç Dosyası**: `2026-03-06_result.csv` güncellendi.
