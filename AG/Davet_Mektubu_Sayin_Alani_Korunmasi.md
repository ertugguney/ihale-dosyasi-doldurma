# Davet Mektubu "Sayın" Alanının Korunması Düzeltmesi

## Problem
İhale şablonunun "İHALEYE DAVET MEKTUBU" sayfasında bulunan `Sayın: ________________` alanı, alt tire karakterlerinin uzunluğundan dolayı sistem tarafından yanlışlıkla "Sözleşme Makamı Adı" (`kurum_adi`) alanı ile eşleştiriliyordu. Bu durum, davet edilecek firmanın adının yazılması gereken boşluğun, ihale makamının kendi adı ile dolmasına neden oluyordu.

## Çözüm
- `field_config.py` dosyasındaki `INSTRUCTION_FIELDS` (Talimat Alanları) listesine `Sayın: ________________` ifadesi eklendi.
- Bu değişiklik ile sistem, bu spesifik diziyi gördüğünde onu bir form girişi olarak değil, olduğu gibi bırakılması veya temizlenmesi gereken bir şablon parçası olarak tanımlar.
- Benzer bir risk taşıyan `Sözleşme Makamı (Yararlanıcı)nın ismi ve adresi` ifadesi de aynı listeye dahil edildi.

## Test ve Doğrulama
- `test_gen.py` üzerinden mock üretim yapıldı.
- Üretilen belgede davet mektubu sayfası incelendiğinde:
    - `Sayın: ________________` alanının artık dolmadığı ve **boş (şablon haliyle)** kaldığı doğrulandı.
- Üretim istatistiklerinde bir alanın daha "instruction_skipped" (talimat olarak atlandı) olarak sayıldığı ve toplam doluluk dengesinin düzeldiği görüldü.
