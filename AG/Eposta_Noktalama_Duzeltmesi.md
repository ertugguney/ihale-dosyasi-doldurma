# E-Posta Satırı Noktalama Düzeltmesi

## Problem
Dökümanın "İSTEKLİLERE TALİMATLAR" (Madde 15) maddesinde, "e) Elektronik posta adresi..." ifadesi yer almaktadır. Buradaki üç nokta (`...`) kullanımı, resmi bir belgede olması gereken iki nokta (`:`) standardına uymamaktadır.

## Çözüm
- `doc_generator.py` içindeki `_process_paragraph_runs` fonksiyonuna ilgili satırı tespit eden bir mantık eklendi.
- Satır içeriğinde "e) " ve "Elektronik posta adresi" ibareleri bir arada geçtiğinde, metin içindeki `...` (geleneksel üç nokta) ve `…` (Word özel elips karakteri) işaretleri otomatik olarak `:` karakterine dönüştürülür.
- Değişim `r.text.replace("...", ":")` metoduyla her bir run bazında güvence altına alınmıştır.

## Test ve Doğrulama
- Mevcut test verisi ile üretim yapıldı.
- Çıktı incelendiğinde Madde 15'in e fıkrasının artık **"e) Elektronik posta adresi:"** şeklinde göründüğü teyit edilmiştir.
