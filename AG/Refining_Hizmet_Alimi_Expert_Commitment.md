# AG: Hizmet Alımı Expert Commitment Refinement

Bu döküman, Görev 40 kapsamında "Hizmet Alımı İhalelerinde Kilit Uzmanlar İçin Münhasırlık ve Müsaitlik Taahhüdü" sayfasındaki "Yayın Referansı" örneğinin temizlenmesini sağlayan süreci ve kod yapılarını içerir.

## Uygulanan Değişiklikler

1. **Mapping Güncellemesi**: `field_config.py` içerisinde `SÖZLEŞME NO/İHALE NO` anahtarı eklenerek form verisiyle eşleştirildi.
2. **Cleaning List**: `doc_generator.py` içindeki temizleme listesine `<ÖRNEK: TR21-23-İKT-XX/01>` ve varyasyonları eklendi.
3. **Robust Processing**: `_replace_text_across_runs` yardımcısı ile bölünmüş Word run'ları üzerinde temizlik garantilendi.

## Doğrulama Komutu
```powershell
python src/test_fix_38.py
```

## Sonuç
Döküman çıktılarında Yayın Referansı yanındaki parantez içi örnekler başarıyla temizlenmiştir.
