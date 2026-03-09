# Kesin Teminat Seçimi ve Dinamik Form Yönetimi

## Problem
Dökümanın "İSTEKLİLERE TALİMATLAR" (Madde 17) h fıkrasında, kesin teminata dair kullanıcıyı yönlendiren ham seçenekler ve talimatlar yer almaktaydı:
`h) İstenmesi halinde... kesin teminat (İSTENMEKTEDİR / İSTENMEMEKTEDİR.) <uygun olan seçeneği seçiniz>`
Ayrıca, kesin teminat istenmediği durumlarda arayüzde "Kesin Teminat Oranı" alanının görünmeye devam etmesi veri girişi sırasında kafa karışıklığına yol açabiliyordu.

## Çözüm
- **Belge Dinamizmi**: `doc_generator.py` içine Madde 17 h bendi için özel temizleme mantığı eklendi. Formdan gelen seçim (**İSTENMEKTEDİR** / **İSTENMEMEKTEDİR**) madde metnine eklenir ve profesyonel olmayan tüm parantez içi talimatlar dökümandan ayıklanır.
- **Arayüz Koşulları (UI Logic)**: `app.py` üzerinde "Kesin Teminat" açılır menüsü ile "Kesin Teminat Oranı (%)" alanı arasında bir bağımlılık (matching) kuruldu.
    - Eğer kullanıcı **İSTENMEMEKTEDİR** seçimini yaparsa, oran giriş alanı arayüzden anında gizlenir.
    - Eğer **İSTENMEKTEDİR** seçilirse, alan görünür hale gelir ve veri girişine izin verir.
- **Standardizasyon**: Dökümandaki seçimler bold (kalın) ve sonuna nokta eklenmiş şekilde profesyonel mizaçla basılır.

## Test ve Doğrulama
- Mevcut CSV datası (Kesin Teminat istenmeyen senaryo) kullanılarak üretim yapıldı.
- Belgede Madde 17 h fıkrasının sadece **"h) İstenmesi halinde... kesin teminat İSTENMEMEKTEDİR."** şeklinde tertemiz çıktığı ve formda ilgili oran alanının gizlendiği doğrulanmıştır.
