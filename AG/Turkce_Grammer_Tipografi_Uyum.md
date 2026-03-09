# Türkçe Bulunma/Yönelme Ekleri ve Tipografik Uyumlandırma Düzeltmesi

## Problem
Form alanları üzerinden örneğin "Edirne / Keşan" girildiğinde çıktı aşamasında son ekin Türkçe karakter ve hece uyum kurallarına (Örn: 'da, 'de, 'ta, 'te) göre otomatik tespitini yapan algoritma mevcuttu, fakat şablon içinden gelen tek tırnak yapısının farklı Word versiyonlarından dolayı düz kesme işareti (`'`) ya da kıvrık (tipografik) kesme işareti (`’`) olabilme durumu Regex paterni ile (`r'^(\'[a-zçğıöşü]+)(.*)'`) tam karşılanamıyordu. Bu yüzden şablon içerisinde `’` (kıvrık olanı) ile başlayan `<'de>` gibi yapılardaki ek değişimi hiç gerçekleşemeyip "Edirne / Keşan’de" şeklinde hatalı Türkçe yazımı olarak kalabiliyor veya patlıyordu.

## Çözüm
- `doc_generator.py` dosyasında `is_yeri_il_ilce` (il, ilçe) parametreleri ve `ihale_saati` parametrelerindeki Regex gruplamaları `r'^([\'’][a-zçğıöşü]+)(.*)'` şeklinde revize edildi. 
- Bu sayede Word dosyası o bölgede hangi tip tırnak işaretini barındırıyorsa o spesifik karakter değişkene atanarak (quote), ardından `suffix[1:]` kuralıyla doğru olan harf değişimine tabi tutularak şablona geri enjekte edildi. Bu sayede format bozulması önlenmiş oldu.

## Test ve Doğrulama
- C:\Users\eguney\Desktop\ihale\output\test_out altına çıktı verecek `test_gen.py` kodu ile "Edirne / Keşan" verisi tekrar işlenerek senaryo canlandırıldı. 
- Komut exit code 0 ile doğru dönüşü verdi.
- Çıktı Word belgesindeki spesifik cümlenin "...Edirne / Keşan'da ve Saat: 10:00'a" formatını tamamen hatasız şekilde kazandığı görüldü.
