# İhale Dosyası Doldurma Sistemi - Proje Detayları

## 📌 Amaç
Trakya Kalkınma Ajansı'nın mali destek programı kapsamında, yararlanıcıların ihale
dosyalarını hazırlaması sürecini dijitalleştirmek ve kolaylaştırmak.

## 📋 Ne Yapıldı?

### 1. Problem Tanımı
Yararlanıcılar, ihale dosyasını (Taslak İhale Dosyası) doldururken şu sorunlarla
karşılaşmaktaydı:
- **Sarı vurgulu alanlar** Word dosyasında 140+ yerde bulunuyor
- Aynı bilgi (örn: kurum adı) **6-7 farklı yerde** tekrar ediliyor
- Seçimlik alanlar (`/` ile ayrılmış seçenekler) kafa karışıklığı yaratıyor
- Tarih formatları tutarsız olabiliyor
- Yanlışlıkla şablon metni değiştirilebiliyor

### 2. Çözüm
Streamlit tabanlı web formu ile:
- **140+ sarı alan** analiz edildi
- **30+ benzersiz form alanı** türetildi (tekrar edenler birleştirildi)
- **7 kategori** altında organize edildi
- Kullanıcı **bir kere doldurur**, sistem **tüm yerlere otomatik yerleştirir**
- Şablon metni **hiçbir şekilde değişmez**

### 3. Benzersiz Alan Eşleştirme Mantığı

Belgede aynı bilgi farklı isimlerle isteniyor. Örneğin:

| Belgede Geçen İfade | Benzersiz Alan ID |
|---------------------|-------------------|
| Mali Destek Yararlanıcısın İsmi | `kurum_adi` |
| Sözleşme Makamı (Mali Destek Yararlanıcısı) | `kurum_adi` |
| Sözleşme Makamının anteti | `kurum_adi` |
| a) Adı/Ünvanı :………… | `kurum_adi` |
| proje adı | `proje_adi` |
| Proje adı (6 farklı yerde) | `proje_adi` |
| sözleşme no/ihale no (5 farklı yerde) | `ihale_referans_no` |

### 4. Alan Kategorileri ve Tipleri

| Kategori | Alan Sayısı | Zorunlu |
|----------|------------|---------|
| Kurum Bilgileri | 7 | 5 |
| Proje Bilgileri | 4 | 4 |
| İhale Bilgileri | 7 | 6 |
| Yer Bilgileri | 4 | 4 |
| Tarih ve Saat | 3 | 2 |
| Teminat ve Ödeme | 6 | 4 |
| Sözleşme Bilgileri | 7 | 4 |

### 5. Seçimlik Alanlar
Belgede `/` ile ayrılmış seçenekler form üzerinde açılır menü (selectbox) olarak 
sunulur:

- **İhale Türü**: Mal Alımı / Hizmet Alımı / Yapım İşi
- **İhale Usulü**: Pazarlık Usulü / Açık İhale Usulü
- **Teklif Esası**: Götürü Bedel / Birim Fiyat
- **Geçici Teminat**: İSTENMEKTEDİR / İSTENMEMEKTEDİR
- **Kesin Teminat**: İSTENMEKTEDİR / İSTENMEMEKTEDİR
- **Ön Ödeme**: Yapılacaktır / Yapılmayacaktır
- **Sigorta**: Aranacaktır / Aranmayacaktır
- **İstekli Kapsamı**: Yerli-yabancı / Sadece yerli

### 6. Talimat/Açıklama Alanları (Çıktıdan Siliniyor)
Belgede sarı vurgulu olup, yardımcı bilgi/talimat niteliğinde olan alanlar 
(örn: "Bu beyanın metni değiştirilemez", "(Yalnızca pazarlık usülü ihaleler için kullanılacaktır)")
form alanı olarak sunulmaz ve **çıktı Word/PDF dosyalarından tamamen silinir**.
Bu sayede nihai belge yalnızca doldurulmuş gerçek verileri içerir.

## 🖥️ Nasıl Erişilir?

### 🌐 Canlı Uygulama (Herkes Erişebilir):
**https://ihale-dosyasi-doldurma-bcrhaxb5oh5kglecegvmns.streamlit.app/**

### 💻 Lokal Çalıştırma (Geliştirici) ve Terminal Komutları:
Uygulamayı başlatmak ve tüm süreci tek bir terminal komutuyla yürütmek için aşağıdaki kod bloğunu kullanabilirsiniz:

```powershell
cd c:\Users\eguney\Desktop\ihale ; $start_time = Get-Date ; streamlit run app.py ; $end_time = Get-Date ; Write-Host "Toplam Yürütme Süresi: $(($end_time - $start_time).TotalSeconds) saniye" 
```

### 📦 GitHub Reposu:
https://github.com/ertugguney/ihale-dosyasi-doldurma

### Gereksinimler:
```bash
pip install streamlit python-docx pywin32
```

## 🔧 Teknik Detaylar

### Sarı Alan Tespit Yöntemi
```
WD_COLOR_INDEX.YELLOW = 7
```
python-docx kütüphanesi ile her paragraf ve tablodaki run'ların 
`font.highlight_color` özelliği kontrol edilir.

### Run Birleştirme
Word dosyalarında aynı paragraftaki metin farklı "run"lara bölünebilir.
Ardışık sarı run'lar birleştirilerek tek bir metin olarak işlenir:
```python
# Birleştirme: [run1:"proje "] + [run2:"adı"] → "proje adı"
```

### Dosya Çıktı Formatları
- **Word (.docx)**: python-docx ile doğrudan oluşturulur
- **PDF**: pywin32 veya LibreOffice ile Microsoft Word üzerinden dönüştürülür
- **CSV**: Form verileri (tarihli) CSV dosyasına kaydedilir ve güncel logları tutar.

### Uygulanan Dil Kuralları ve Biçim:
Çıktı Word dosyasına otomatik bold yazım uygulanmakta, ek olarak etraftaki `<` ve `>` işaretleri dinamik döngüler (ileri ve geri run taraması) yardımıyla metni bozmadan temizlenmektedir. İl/ilçe için yer (bulunma) ekleri ve saat verileri için yönelme ekleri Türkçe dil bilgisi kurallarına göre ('de/'da, 'te/'ta, 'e/'a, 'ye/'ya vb.) otomatik hesaplanarak aynı zamanda şablon içindeki tipografik kıvrık veya düz (', ’, ‘) kesme işaretleri ayırt edilerek şablona yansıtılmaktadır. Bu sayede "saat ...'ne" gibi ifadeler girilen saate göre (örn: 10:00'a) dinamik olarak düzeltilmektedir. Ek olarak şablon metninde yer alan noktalama eksiklikleri (örneğin "..." yerine ":") python-docx ile dinamik düzeltilmektedir. Yayın Referansı gibi alanlardaki `<Örnek: ...>` metinleri, Word içindeki farklı `run` yapılarına bölünmüş olsalar dahi `_replace_text_across_runs` algoritması ile dökümandan tamamen temizlenmektedir.

### Akıllı Form Özellikleri:
İdari Uygunluk Değerlendirme Tablosu ve Sözleşme Adı gibi bölümlerdeki birleşik alanlar (`[Proje Adı] Projesi için [İhale Türü]`) paragraf düzeyinde yakalanarak, proje adındaki "Projesi" mükerrerlikleri giderilmiş ve tam uyumlu (kalın yazılmış) sonuçlar üretilmektedir. Mükerrer "Projesi Projesi" veya "Programı Programı" gibi metin yanlışlıklarının önüne geçecek regex temizleyiciler kullanılmıştır. Bu temizleyici, özellikle Mali Teklif Formu (EK:4a) ve Teknik Teklif başlıklarında proje adının döküman akışıyla mükemmel uyum sağlamasını garantiler. Çevresel talimat izlerinin tamamı (açılıp kapanan < > vb. ayraçlar) gelişmiş loop fonksiyonlarıyla sıyrılmakta ve çıktı kusursuzlaştırılmaktadır. Ayrıca, şablonda hem tarih hem saat bilgisinin bir arada istendiği paragraflar otomatik tespit edilerek, formdaki ayrı tarih ve saat girdileri bu alanlarda "GG/AA/YYYY SS:DD" formatında birleştirilerek sunulmaktadır. İhale genel tarih placeholder'ları ile davet mektubu tarihleri arasındaki fark programatik olarak ayırt edilerek davet mektubu bölümündeki tarihler bağımsız bir girdiden beslenmektedir. Davet mektubu üzerindeki "Sayın: ____________" gibi kısımlar istisna listesine alınarak, bunların form verileriyle (örn: yararlanıcı adı) yanlışlıkla ezilmesinin önüne geçilmiş, şablonun orijinal yapısı korunmuştur. Yeni eklenen özellikle, İhaleye Davet Mektubu sayfasında "Sayın:" altında bulunan 16 alt çizgilik `________________` alanı `YELLOW_TO_UNIQUE_MAP` içerisinden çıkarılarak `INSTRUCTION_FIELDS` kapsamına alınmış ve sarı vurgusu kaldırılıp düz metni bozulmadan korunmuştur. "İhale Konusu" alanı artık dinamik bir liste yapısındadır; kullanıcı her bir alımı ayrı kalemler olarak sisteme girer, bu kalemler davet mektubunda (i, ii, iii) formatında otomatik listelenirken belgenin diğer kısımlarında akıllıca virgül ile birleştirilir. Son olarak, Davet Mektubu'ndaki değerlendirme kriterleri ihale türüne (Mal/Hizmet/Yapım) göre otomatik seçilir; "Mal Alımı/Yapım İşi" durumunda "a" şıkkı, "Hizmet Alımı" durumunda ise "b" şıkkı dökümanda bırakılır. Bu işlem sırasında başlıkta bulunan parantez içi talimatlar silinirken prefix yapısı (örn: (ii)) korunur ve madde işaretleri (a, b) standart hale getirilir. Madde 15 gibi noktalama hatası olan ("...") alanlar otomatik olarak düzgün formata (":") çevrilerek formdan gelen e-posta adresi (kalın yazılmış şekilde) sisteme dahil edilir ve profesyonel standart sağlanır. Teklif formlarındaki (Teknik, Mali, Sunum ve Kilit Uzman Taahhütnameleri) "Yayın Referansı" alanları, kılavuz ve örnek metinlerden arındırılarak doğrudan "Sözleşme Kodu" verisiyle kalın (bold) olarak doldurulur; bu işlem sırasında `YAyın referansı`, `Yayin Referansi` gibi büyük/küçük harf varyasyonları ve `<sözleşme no/ihale no/lot no>` gibi tüm placeholder yapıları tek bir akıllı, case-insensitive mantıkla temizlenir. "İSTEKLİLERE TALİMATLAR" bölümündeki "Sözleşme kodu:" satırı, formdaki sözleşme kodu verisiyle otomatik doldurulur ve kılavuz metinler temizlenir. İhale usulü (Açık/Pazarlık) seçimine göre belge listesi otomatik yeniden indekslenir (b -> a geçişleri) ve usule uygun olmayan maddeler talimatlarıyla birlikte temizlenir. Madde 17 altındaki Geçici Teminat ve Kesin Teminat seçenekleri form verilerine göre dinamik olarak temizlenir ve sadece seçilen opsiyon dökümanda şık bir şekilde bırakılır; ayrıca seçime bağlı olarak oransal giriş alanları arayüzden otomatik olarak gizlenir. Madde 8 altındaki "Yerli/Yabancı İstekli" tercihi, şablondaki ikili seçeneklerin yerine formdan gelen tekil verinin yerleştirilmesiyle dökümana yansıtılır. Madde 18 altındaki Teklif Esası seçimine, şablon akışına uygunluğu sağlamak adına otomatik olarak "esaslı" soneki eklenmektedir. Teklif teslim yöntemleri (posta/elden) içeren satırlarda, formdaki teslimat adresi otomatik olarak yerleştirilmekte ve cümleyi tamamlayan "Adresine" ifadesi eklenmektedir. Sözleşme başlıkları ihale türüne göre tam büyük harf ve kalın olarak yazılırken, "Teklif Sunum Formu" içerisindeki taahhütname gibi resmi metinler seçilen ihale türüne göre gramatik olarak otomatik yeniden kurgulanmaktadır (Örn: Mal Alımı için "malları tedarik etmeyi", Hizmet Alımı için "hizmetleri sağlamayı", Yapım İşi için "yapım işini üstlenmeyi"). Bu süreçte dökümana gömülü placeholderlar `< >` akıllı algoritmalarla tespit edilip temizlenirken, paragraf sonlarındaki "(Yararlanıcı ihale konusu...)" gibi yönlendirici talimatlar dökümandan tamamen ayıklanarak resmi bir döküman yapısı korunmaktadır. Ön ödeme seçeneklerinde "Yapılacaktır" tercih edildiğinde yasal tüm alt metinler dökümana eklenirken, "Yapılmayacaktır" durumunda bu kısımlar otomatik olarak ayıklanmaktadır. İstekli imza alanlarındaki noktalı mizanpaj korunmuş ve gereksiz Lot Numarası bilgileri tablolardan ayıklanmıştır. Son olarak, Adli Sicil Kaydı için istenen yıl sayısı artık form üzerinden dinamik olarak belirlenebilmektedir.

---
 
**Proje Başlatma Komutu:**
```powershell
streamlit run app.py
```

## 📊 Eşik Değerleri ve Kısıtlamalar

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| Kesin Teminat Min. Oranı | %6 | Satabileşme bedelinin en az %6'sı |
| Ön Ödeme Max. Oranı | %50 | Sözleşme bedelinin en fazla %50'si |
| Uygulama Süresi | 1-60 ay | Sözleşme uygulama süresi |
| Benzer İş Deneyimi | 1-20 yıl | Değerlendirme süresi |
