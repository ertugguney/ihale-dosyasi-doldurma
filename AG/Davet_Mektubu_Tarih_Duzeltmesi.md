# Davet Mektubu Tarih Alanının Bağlamsal Düzeltmesi

## Problem
İhale şablonunun en başında yer alan "İHALEYE DAVET MEKTUBU" bölümündeki tarih placeholder'ı (`…./…./20…`), genel ihale tarihini (`06/03/2026`) temsil eden bir etiketle eşleşiyordu. Bu durum, davet mektubu tarihinin (`26/02/2026`) basılması gereken yere, gelecekteki bir tarih olan ihale tarihinin basılmasına neden oluyordu.

## Çözüm
- `doc_generator.py` dosyasına bağlamsal bir geçersiz kılma (override) mantığı uygulandı.
- Sistem belgeyi işlerken "İHALEYE DAVET MEKTUBU" ibaresini gördüğünde bir bayrak (`in_davet_mektubu = True`) kaldırır.
- Bu bayrak aktifken saptanan tarih placeholder'ları, global haritadaki karşılığı ne olursa olsun programatik olarak `davet_tarihi` inputuna yönlendirilir.
- Algoritma, şablondaki nokta farklılıklarını tolere etmek için regex (`re.search(r'\d{4}|…', combined_text)`) temelli bir saptama kullanır.

## Test ve Doğrulama
- Mevcut test verisi (`ihale_form_verileri_20260225.csv`) ile `test_gen.py` üzerinden doğrulama yapıldı.
- Çıktı belgesi (`test_out` klasörü) incelendiğinde:
    - Davet mektubu tarihinın: **26/02/2026** (Davet Tarihi)
    - Teklif teslim tarihinin: **06/03/2026** (İhale Tarihi)
  olduğu ve her birinin ait olduğu bağlamda doğru şekilde basıldığı kesinleştirildi.
