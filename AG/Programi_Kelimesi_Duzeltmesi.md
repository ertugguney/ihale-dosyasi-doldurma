# "Programı" Kelimesi Mükerrerliğini Engelleme Düzeltmesi

## Problem
Kullanıcı formu doldururken `Destek Programının İsmi` alanına "Iktisadi Kalkinma Mali Destek Programi" veya "Programı" gibi tam kelimeleri yazdığında şablonda kelimenin hemen ardından hardcoded olarak yer alan " Programı" ifadesi nedeniyle "Programı Programı" şeklinde hatalı (çifte yazım) bir kelime üretiliyordu. Özellikle input içindeki i, ı, I, İ gibi farklılıklar (`Programı`, `Programi`) önceki eski regex kuralı ile tam olarak ayıklanamıyordu.

## Çözüm
- `doc_generator.py` dosyasındaki regex mantığı çok daha esnek, sağlam ve kılı kırk yaran bir hale getirildi. 
- Kelimenin sonundaki yazım değişikliklerini (`Programi`, `programı`, `PROGRAMI` vb.) saptayıp ondan sonra gelebilecek olası boşlukları da hesaba katacak yepyeni bir regex paterni atandı: `re.sub(r'\s+[pP][rR][oO][gG][rR][aA][mM][ıiIİ]?\s*$', '', formatted)`
- Bu Regex sayesinde son kısımdaki "Program" serbestisinin tüm türevleri form alanı docx'e aktarılırken başarılı bir şekilde temizlenmektedir.

## Test ve Doğrulama
- C:\Users\eguney\Desktop\ihale\output\test_out altına çıktı verecek `test_gen.py` kodu ile ilgili veri yüklenerek senaryo canlandırıldı. 
- Komutta exit code: 0 dönüşü alındı.
- CSV içindeki veri (kişinin "Programi" yazdığı spesifik veri parçası) ele alınarak test edildiğinde, programın Word üzerinde bu kelimeyi otomatik silerek formatladığı ve şablonla tam uyumlu çalıştığı teyit edildi.
