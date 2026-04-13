# İhale Dosyası Doldurma Sistemi

## 📋 Proje Açıklaması
Trakya Kalkınma Ajansı mali destek yararlanıcılarının ihale dosyalarını kolayca doldurmasını sağlayan Streamlit tabanlı web uygulaması.

## 🚀 Hızlı Başlangıç

### Tek Komutla Başlatma:
```bash
cd c:\Users\eguney\Desktop\ihale && streamlit run app.py
```

### Gereksinimler:
```bash
pip install streamlit python-docx
```
*Not: PDF dönüşümü için Windows'ta MS Word veya tüm sistemlerde LibreOffice yüklü olmalıdır.*

## 📁 Proje Yapısı
```
ihale/
├── app.py                          # Ana Streamlit uygulaması
├── src/
│   ├── field_config.py             # Form alanları yapılandırması
│   └── doc_generator.py            # Word belge oluşturucu
├── data/
│   └── draft.json                  # Kaydedilen taslak veriler
├── output/                         # Oluşturulan dosyalar
├── docs/
│   ├── roadmap.md                  # Geliştirme yol haritası
│   └── project_details.md          # Proje detayları
├── .agent/
│   └── skills/
│       └── instructions.md         # Agent talimatları
├── Taslak İhale Dosyası.doc        # Orijinal şablon
├── Taslak İhale Dosyası.docx       # Dönüştürülmüş şablon
└── README.md                       # Bu dosya
```

## 🔧 Özellikler
- **Sarı Alan Tespiti**: Word belgesindeki sarı vurgulu alanları otomatik tespit eder
- **Benzersiz Alan Eşleştirmesi**: 140+ sarı alandan 30+ benzersiz form alanı türetilir
- **Kategorize Form**: 7 kategoride organize edilmiş form alanları
- **Seçimlik Alanlar**: Açılır menü ile kolay seçim
- **Tarih/Saat Seçici**: Tarih ve saat alanları için özel giriş bileşenleri
- **Önizleme**: Doldurulmadan önce verilerin kontrol edilmesi
- **Word Çıktı**: Doldurulmuş .docx dosyası oluşturma
- **PDF Çıktı**: Otomatik PDF dönüşümü
- **CSV Kayıt**: Form verileri CSV olarak kaydedilir
- **Taslak Kayıt/Yükleme**: Yarım kalan formlar kaydedilip yüklenebilir

## ☁️ Streamlit Cloud Yayını
Bu uygulamayı Streamlit Cloud üzerinde yayınlamak için:
1. Kodları GitHub deponuza yükleyin.
2. [share.streamlit.io](https://share.streamlit.io) adresinden GitHub hesabınızla giriş yapın.
3. "New app" butonuna tıklayıp bu depoyu ve `app.py` dosyasını seçin.
4. "Advanced settings" kısmında Python sürümünün 3.9+ olduğundan emin olun.
5. Deploy butonuna basın.

**Not:** Streamlit Cloud üzerinde PDF dönüşümü için `packages.txt` dosyasındaki `libreoffice` paketi otomatik olarak yüklenecektir.
