# Dinamik "<" ve ">" Temizleme İşlemi

## Problem
Kullanıcı formu doldurduktan sonra şablonda oluşturulan belge içerisinde, girilen yeni değerlerin sağında ve solunda kalan `<` ve `>` (açısal ayraç) işaretleri, bazı durumlarda ya hiç temizlenmiyor ya da eksik silinerek word belgesinde kalıyordu. Önceki koddaki temizleme mantığı, sadece yerleştirilen hedefin tam olarak bir yanındaki (`i-1` veya `i+1`) "run"ları baz aldığı için, arada boşluk olan durumlarda veya talimat silme işlemlerinde bu ayracı saptayamıyordu.

## Çözüm
- `doc_generator.py` dosyasındaki temizleme mantığı tamamen değiştirildi.
- Hem sarı alanlara atanan değer the hem de output'a yansımayacak olan (instruction text) saptanan değerler için güçlü bir "backward (geriye dönük)" ve "forward (ileriye dönük)" tarama döngüsü (loop algoritması) yazıldı.
- Her iki durumda da metin konulan `run` üzerinden geriye dönük loopa girilip ilk `<` karakterine rastlandığında bu karakter yok ediliyor, ve eğer karakterli (boş olmayan) bir text run'a gelinirse daha fazla gidişatı durdurarak (break) döngü sonlandırılıyor.
- Aynı işlem sağ kısımdaki `>` işaretleri için ileriye dönük (forward loop) taranıp uygulanıyor.

## Test ve Doğrulama
Bunu testetmek amacıyla lokalde `test_gen.py` scripti yazılıp `run_command` ile çalıştırılarak `C:\Users\eguney\Desktop\ihale\output\ihale_form_verileri_20260225.csv` datası mock kullanılarak belgenin render olması tetiklendi. Komut başarıyla eksiksiz 0 exit code ile çalıştırıldı ve `<...>` gibi ayraçların çıktıda tamamıyla giderildiği teyit edildi. Çıktı süre istatistikleri ve pdf çıktısı elde edildi. C:\Users\eguney\Desktop\ihale\output\test_out altına `20260305...` dosyası olarak düştü.
