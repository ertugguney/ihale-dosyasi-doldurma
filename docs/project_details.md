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

### 6. Talimat/Açıklama Alanları (Form Dışı)
Belgede sarı vurgulu olup, yardımcı bilgi/talimat niteliğinde olan alanlar 
(örn: "Bu beyanın metni değiştirilemez") form alanı olarak sunulmaz, 
belgenin orijinal halinde kalır.

## 🖥️ Nasıl Erişilir?

### 🌐 Canlı Uygulama (Herkes Erişebilir):
**https://ihale-dosyasi-doldurma-bcrhaxb5oh5kglecegvmns.streamlit.app/**

### 💻 Lokal Çalıştırma (Geliştirici):
```bash
cd c:\Users\eguney\Desktop\ihale && streamlit run app.py
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
- **PDF**: pywin32 ile Microsoft Word üzerinden dönüştürülür
- **CSV**: Form verileri tarihli CSV dosyasına kaydedilir

## 📊 Eşik Değerleri ve Kısıtlamalar

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| Kesin Teminat Min. Oranı | %6 | Satabileşme bedelinin en az %6'sı |
| Ön Ödeme Max. Oranı | %50 | Sözleşme bedelinin en fazla %50'si |
| Uygulama Süresi | 1-60 ay | Sözleşme uygulama süresi |
| Benzer İş Deneyimi | 1-20 yıl | Değerlendirme süresi |
