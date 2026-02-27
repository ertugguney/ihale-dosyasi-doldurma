"""
İhale Dosyası Form Alanları Yapılandırması.

Bu modül, ihale dosyasındaki sarı vurgulu alanları benzersiz (unique) form
alanlarına eşleştirir. Birden fazla yerde geçen aynı bilgi tek bir form
alanından doldurulur ve otomatik olarak tüm ilgili yerlere yerleştirilir.

Alan Türleri:
    - text: Serbest metin girişi (örn: kurum adı, adres)
    - select: Açılır menüden seçim (örn: ihale türü)
    - date: Tarih seçici
    - time: Saat seçici
    - number: Sayısal giriş
    - textarea: Uzun metin girişi
    - phone: Telefon numarası
    - email: E-posta adresi
"""

# =============================================================================
# BENZERSİZ FORM ALANLARI TANIMLAMASI
# =============================================================================

UNIQUE_FIELDS = {
    # =========================================================================
    # BÖLÜM 1: KURUM / SÖZLEŞME MAKAMI BİLGİLERİ
    # =========================================================================
    "kurum_adi": {
        "label": "Sözleşme Makamı (Yararlanıcı) Adı / Ünvanı",
        "type": "text",
        "placeholder": "Örn: ABC Belediye Başkanlığı",
        "help": "Mali Destek Yararlanıcısının / Sözleşme Makamının resmi adı veya ünvanı. "
                "Bu bilgi ihale ilanı, davet mektubu, sözleşme ve tüm belgelerde kullanılır.",
        "required": True,
        "category": "Kurum Bilgileri",
        "order": 1,
    },
    "kurum_adresi": {
        "label": "Sözleşme Makamı Adresi",
        "type": "textarea",
        "placeholder": "Örn: Merkez Mah. Cumhuriyet Cad. No:1, Edirne",
        "help": "Sözleşme Makamının açık adresi. Tekliflerin sunulacağı adres olarak da kullanılır.",
        "required": True,
        "category": "Kurum Bilgileri",
        "order": 2,
    },
    "kurum_telefon": {
        "label": "Telefon Numarası",
        "type": "phone",
        "placeholder": "Örn: 0284 XXX XX XX",
        "help": "Sözleşme Makamının telefon numarası.",
        "required": True,
        "category": "Kurum Bilgileri",
        "order": 3,
    },
    "kurum_faks": {
        "label": "Faks Numarası",
        "type": "phone",
        "placeholder": "Örn: 0284 XXX XX XX",
        "help": "Sözleşme Makamının faks numarası.",
        "required": False,
        "category": "Kurum Bilgileri",
        "order": 4,
    },
    "kurum_eposta": {
        "label": "Elektronik Posta Adresi",
        "type": "email",
        "placeholder": "Örn: info@kurum.gov.tr",
        "help": "Sözleşme Makamının e-posta adresi.",
        "required": True,
        "category": "Kurum Bilgileri",
        "order": 5,
    },
    "kurum_ilgili_personel": {
        "label": "İlgili Personelin Adı-Soyadı / Ünvanı",
        "type": "text",
        "placeholder": "Örn: Ahmet YILMAZ / Proje Koordinatörü",
        "help": "İhale ile ilgili irtibat personeli.",
        "required": True,
        "category": "Kurum Bilgileri",
        "order": 6,
    },
    "kurum_internet_sitesi": {
        "label": "Yararlanıcının İnternet Sitesi",
        "type": "text",
        "placeholder": "Örn: www.kurum.gov.tr",
        "help": "İhale dosyasının yayınlanacağı internet sitesi adresi.",
        "required": False,
        "category": "Kurum Bilgileri",
        "order": 7,
    },

    # =========================================================================
    # BÖLÜM 2: PROJE BİLGİLERİ
    # =========================================================================
    "proje_adi": {
        "label": "Proje Adı",
        "type": "text",
        "placeholder": "Örn: Trakya Bölgesi Altyapı Geliştirme Projesi",
        "help": "Projenin tam adı. Sözleşme başlığı, teklifler ve tüm belgelerde kullanılır.",
        "required": True,
        "category": "Proje Bilgileri",
        "order": 10,
    },
    "destek_programi_adi": {
        "label": "Destek Programının İsmi",
        "type": "text",
        "placeholder": "Örn: İktisadi Kalkınma Mali Destek Programı",
        "help": "Trakya Kalkınma Ajansı tarafından yürütülen destek programının adı.",
        "required": True,
        "category": "Proje Bilgileri",
        "order": 11,
    },
    "sozlesme_kodu": {
        "label": "Sözleşme Kodu",
        "type": "text",
        "placeholder": "Örn: TR21-23-İKT-XX",
        "help": "Ajans ile Yararlanıcı arasında imzalanan mali destek sözleşmesinin kodu.",
        "required": True,
        "category": "Proje Bilgileri",
        "order": 12,
    },
    "ihale_referans_no": {
        "label": "İhale / Yayın Referans Numarası",
        "type": "text",
        "placeholder": "Örn: TR21-23-İKT-XX/01",
        "help": "Sözleşme no/ihale no/lot no formatında referans numarası.",
        "required": True,
        "category": "Proje Bilgileri",
        "order": 13,
    },

    # =========================================================================
    # BÖLÜM 3: İHALE BİLGİLERİ
    # =========================================================================
    "ihale_turu": {
        "label": "İhale Türü",
        "type": "select",
        "options": ["Mal Alımı", "Hizmet Alımı", "Yapım İşi"],
        "help": "İhale konusu alımın türünü seçiniz. Birden fazla seçilebilir.",
        "required": True,
        "category": "İhale Bilgileri",
        "order": 20,
    },
    "ihale_konusu": {
        "label": "İhale Konusu (Alım Sözleşmesinin Tanımı)",
        "type": "textarea",
        "placeholder": "Örn: Ofis mobilyası ve bilgisayar ekipmanları temini\n(Birden fazla kalem varsa her birini klavyede 'Enter' tuşuna basarak yeni bir satıra yazınız.)",
        "help": "İhaleye konu olan alım sözleşmesinin kısa tanımı. Birden fazla alım kalemi (i, ii, iii vb.) varsa lütfen her birini ayrı bir satıra yazınız.",
        "required": True,
        "category": "İhale Bilgileri",
        "order": 21,
    },
    "ihale_usulu": {
        "label": "İhale Usulü",
        "type": "select",
        "options": ["Pazarlık Usulü", "Açık İhale Usulü"],
        "help": "Uygulanacak ihale usulünü seçiniz.",
        "required": True,
        "category": "İhale Bilgileri",
        "order": 22,
    },
    "teklif_esasi": {
        "label": "Teklif Esası",
        "type": "select",
        "options": ["Götürü Bedel", "Birim Fiyat"],
        "help": "Tekliflerin sunulacağı fiyatlandırma yöntemini seçiniz.",
        "required": True,
        "category": "İhale Bilgileri",
        "order": 23,
    },
    "para_birimi": {
        "label": "Para Birimi",
        "type": "select",
        "options": ["TL", "EUR", "USD"],
        "help": "Teklif ve ödemelerde geçerli para birimi.",
        "required": True,
        "category": "İhale Bilgileri",
        "order": 24,
        "default": "TL",
    },
    "istekli_kapsamı": {
        "label": "İstekli Kapsamı",
        "type": "select",
        "options": [
            "Sözleşme Makamı tarafından gerçekleştirilecek ihaleler yerli yabancı tüm isteklilere açıktır.",
            "Sözleşme Makamı tarafından gerçekleştirilecek ihaleler sadece yerli isteklilere açıktır."
        ],
        "help": "İhalenin yerli/yabancı isteklilere açık olma durumunu seçiniz.",
        "required": True,
        "category": "İhale Bilgileri",
        "order": 25,
    },
    "fiziki_miktar_ve_tur": {
        "label": "Fiziki Miktarı ve Türü",
        "type": "textarea",
        "placeholder": "Örn: 100 adet bilgisayar, 50 adet masa – Mal Alımı",
        "help": "İhale için ayrılan miktar ve alım türünü belirtiniz.",
        "required": True,
        "category": "İhale Bilgileri",
        "order": 26,
    },

    # =========================================================================
    # BÖLÜM 4: YER BİLGİLERİ
    # =========================================================================
    "is_yeri_il_ilce": {
        "label": "İşin Yapılacağı İl / İlçe",
        "type": "text",
        "placeholder": "Örn: Edirne / Keşan",
        "help": "İhale konusu işin yapılacağı il ve ilçe bilgisi.",
        "required": True,
        "category": "Yer Bilgileri",
        "order": 30,
    },
    "teslim_yeri": {
        "label": "İşin/Teslimin Gerçekleştirileceği Yer",
        "type": "textarea",
        "placeholder": "Örn: Keşan Belediyesi, Merkez Mah. No:5, Keşan/Edirne",
        "help": "Yapım İşlerinde işin yapılacağı, hizmet alımlarında hizmetin gerçekleştirileceği, "
                "mal alımlarında malın teslim edileceği yeri belirtiniz.",
        "required": True,
        "category": "Yer Bilgileri",
        "order": 31,
    },
    "ihale_yapilacak_adres": {
        "label": "İhalenin Yapılacağı Adres",
        "type": "textarea",
        "placeholder": "Örn: Keşan Belediyesi Toplantı Salonu, Merkez Mah. No:5",
        "help": "İhalenin gerçekleştirileceği yerin açık adresi.",
        "required": True,
        "category": "Yer Bilgileri",
        "order": 32,
    },
    "mahkeme_il": {
        "label": "Uyuşmazlık Mahkeme İli",
        "type": "text",
        "placeholder": "Örn: Edirne",
        "help": "Sözleşmeden doğan uyuşmazlıklarda yetkili mahkemenin bulunduğu il.",
        "required": True,
        "category": "Yer Bilgileri",
        "order": 33,
    },

    # =========================================================================
    # BÖLÜM 5: TARİH VE SAAT BİLGİLERİ
    # =========================================================================
    "ihale_tarihi": {
        "label": "İhale Tarihi",
        "type": "date",
        "help": "Son teklif verme tarihi (ihale tarihi).",
        "required": True,
        "category": "Tarih ve Saat",
        "order": 40,
    },
    "ihale_saati": {
        "label": "İhale Saati",
        "type": "time",
        "help": "Son teklif verme saati (ihale saati).",
        "required": True,
        "category": "Tarih ve Saat",
        "order": 41,
    },
    "davet_tarihi": {
        "label": "Davet Tarihi",
        "type": "date",
        "help": "İhaleye davet mektubu tarihi (Pazarlık usulünde).",
        "required": False,
        "category": "Tarih ve Saat",
        "order": 42,
    },

    # =========================================================================
    # BÖLÜM 6: TEMİNAT VE ÖDEME BİLGİLERİ
    # =========================================================================
    "gecici_teminat": {
        "label": "Geçici Teminat",
        "type": "select",
        "options": ["İSTENMEKTEDİR", "İSTENMEMEKTEDİR"],
        "help": "Md. 26'daki koşullara uygun geçici teminat istenip istenmediğini seçiniz.",
        "required": True,
        "category": "Teminat ve Ödeme",
        "order": 50,
    },
    "kesin_teminat": {
        "label": "Kesin Teminat",
        "type": "select",
        "options": ["İSTENMEKTEDİR", "İSTENMEMEKTEDİR"],
        "help": "Sözleşme imzalama aşamasında kesin teminat istenip istenmediğini seçiniz.",
        "required": True,
        "category": "Teminat ve Ödeme",
        "order": 51,
    },
    "kesin_teminat_orani": {
        "label": "Kesin Teminat Oranı (%)",
        "type": "number",
        "placeholder": "Örn: 6",
        "help": "Kesin teminat tutarı sözleşme bedelinin yüzde kaçı olacağını giriniz. "
                "%6'dan az bir oran belirlenemez.",
        "required": False,
        "category": "Teminat ve Ödeme",
        "order": 52,
        "min_value": 6,
        "max_value": 100,
    },
    "on_odeme": {
        "label": "Ön Ödeme",
        "type": "select",
        "options": ["Yapılacaktır", "Yapılmayacaktır"],
        "help": "Sözleşme kapsamında ön ödeme yapılıp yapılmayacağını seçiniz.",
        "required": True,
        "category": "Teminat ve Ödeme",
        "order": 53,
    },
    "on_odeme_orani": {
        "label": "Ön Ödeme Oranı (%)",
        "type": "number",
        "placeholder": "Örn: 30",
        "help": "Ön ödeme miktarının sözleşme bedelinin yüzde kaçı olacağını giriniz. "
                "%50'den yüksek bir oran yazılamaz.",
        "required": False,
        "category": "Teminat ve Ödeme",
        "order": 54,
        "min_value": 1,
        "max_value": 50,
    },
    "sigorta": {
        "label": "Sigorta Koşulu",
        "type": "select",
        "options": ["Aranacaktır", "Aranmayacaktır"],
        "help": "Mal ve Hizmet alımlarında sigorta şartı aranıp aranmayacağını seçiniz. "
                "Yapım işleri için sigorta koşulu sağlanmalıdır.",
        "required": True,
        "category": "Teminat ve Ödeme",
        "order": 55,
    },

    # =========================================================================
    # BÖLÜM 7: SÖZLEŞME BİLGİLERİ
    # =========================================================================
    "sozlesme_baslangic": {
        "label": "Sözleşme Başlangıç Şekli",
        "type": "select",
        "options": [
            "Sözleşmenin her iki tarafça imzalandığı tarih",
            "Belirli bir tarih"
        ],
        "help": "Uygulamaya başlama tarihinin nasıl belirleneceğini seçiniz.",
        "required": True,
        "category": "Sözleşme Bilgileri",
        "order": 60,
    },
    "sozlesme_baslangic_tarihi": {
        "label": "Sözleşme Başlangıç Tarihi (Belirli tarih seçildiyse)",
        "type": "date",
        "help": "Belirli bir tarih seçildiyse başlangıç tarihini giriniz.",
        "required": False,
        "category": "Sözleşme Bilgileri",
        "order": 61,
    },
    "uygulama_suresi_ay": {
        "label": "Uygulama Süresi (Ay)",
        "type": "number",
        "placeholder": "Örn: 6",
        "help": "Sözleşmenin uygulama süresini ay olarak giriniz.",
        "required": True,
        "category": "Sözleşme Bilgileri",
        "order": 62,
        "min_value": 1,
        "max_value": 60,
    },
    "lot_numarasi": {
        "label": "Lot Numarası",
        "type": "text",
        "placeholder": "Örn: Lot 1",
        "help": "İhale lotlara bölünmüşse lot numarasını giriniz. Bölünmemişse boş bırakınız.",
        "required": False,
        "category": "Sözleşme Bilgileri",
        "order": 63,
    },
    "diger_bilgiler": {
        "label": "Alıma Ait Diğer Bilgiler",
        "type": "textarea",
        "placeholder": "Varsa ek bilgileri giriniz...",
        "help": "Alıma ait varsa diğer bilgiler.",
        "required": False,
        "category": "Sözleşme Bilgileri",
        "order": 64,
    },
    "yeterlik_degerlendirme": {
        "label": "Yeterlik Değerlendirmesinde Kullanılacak Bilgi/Belgeler",
        "type": "textarea",
        "placeholder": "Örn: İş deneyim belgeleri, bilanço, iş hacmini gösteren belgeler...",
        "help": "İhale konusu işin niteliğine göre istenen bilgi ve/veya belgelerden hangilerinin "
                "yeterlik değerlendirmesinde kullanılacağını belirtiniz.",
        "required": True,
        "category": "Sözleşme Bilgileri",
        "order": 65,
    },
    "benzer_is_yili": {
        "label": "Benzer İş Deneyimi Yıl Sayısı",
        "type": "number",
        "placeholder": "Örn: 5",
        "help": "Son kaç yıl içerisinde tamamlanan benzer nitelikteki işlerin değerlendirileceğini giriniz.",
        "required": True,
        "category": "Sözleşme Bilgileri",
        "order": 66,
        "min_value": 1,
        "max_value": 20,
    },
    "dava_gecmisi_yili": {
        "label": "Kaç yıl geriye doğru Adli Sicil Kaydı İstenecek",
        "type": "number",
        "placeholder": "Örn: 5",
        "help": "Son kaç yıl içerisinde yürütülen sözleşmelerden kaynaklanan dava/tahkim geçmişinin "
                "sorgulanacağı yıl sayısını giriniz.",
        "required": False,
        "category": "Sözleşme Bilgileri",
        "order": 67,
        "min_value": 1,
        "max_value": 20,
    },
}

# =============================================================================
# ALAN KATEGORİLERİ VE SIRALAMA
# =============================================================================

FIELD_CATEGORIES = [
    "Kurum Bilgileri",
    "Proje Bilgileri",
    "İhale Bilgileri",
    "Yer Bilgileri",
    "Tarih ve Saat",
    "Teminat ve Ödeme",
    "Sözleşme Bilgileri",
]

# =============================================================================
# SARI ALANLARIN BENZERSİZ ALANLARA EŞLEŞTİRMESİ
# =============================================================================
# Her sarı alan, hangi unique field'a karşılık geldiğini belirtir.
# "None" olanlar doğrudan bilgi/talimat metinleridir, form alanı değildir.

YELLOW_TO_UNIQUE_MAP = {
    # Kurum bilgileri
    "Mali Destek Yararlanıcısın İsmi": "kurum_adi",
    "Sözleşme Makamının (Mali Destek Yararlanıcısının) resmi adı ve adresi": "kurum_adi",
    "Sözleşme Makamı (Yararlanıcı)nın ismi ve adresi": "kurum_adi",
    "Sözleşme Makamının anteti": "kurum_adi",
    "…………………………………………………………………………": "kurum_adi",
    "________________": "kurum_adi",
    
    "yararlanıcı adresi": "kurum_adresi",
    "..............................................................................................................................": "kurum_adresi",
    "Sözleşme Makamının Adresi": "kurum_adresi",
    "mali destek yararlanıcısının belirleyeceği adres": "kurum_adresi",
    "……………………….(sözleşme makamının adresi)": "kurum_adresi",
    
    ".............................................................................................................": "kurum_telefon",
    "____________": "kurum_telefon",
    
    "..................................................................................................................": "kurum_faks",
    "______________": "kurum_faks",
    
    "……………………………………….....……………………": "kurum_eposta",
    
    "................................................................................": "kurum_ilgili_personel",
    
    "yararlanıcının internet sitesi": "kurum_internet_sitesi",
    "Destek Yararlanıcısın internet adresi": "kurum_internet_sitesi",
    
    # Proje bilgileri
    "proje adı": "proje_adi",
    "Proje adı": "proje_adi",
    "............................................................................................................": "proje_adi",
    
    "Destek Programının İsmi": "destek_programi_adi",
    
    "Ajans ile Yararlanıcı arasında imzalanan mali destek sözleşmesinin kodunu yazınız": "sozlesme_kodu",
    
    "sözleşme no/ihale no": "ihale_referans_no",
    "sözleşme no/ihale no>": "ihale_referans_no",
    
    # İhale bilgileri
    "Mal Alımı/Hizmet Alımı/Yapım İşi (uygun olan(lar) seçilecek)": "ihale_turu",
    "mal alımı/hizmet alımı/yapım işi (uygun olan(lar) seçilecek)": "ihale_turu",
    "MAL ALIMI/HİZMET ALIMI/YAPIM İŞİ": "ihale_turu",
    "Mal Alımı/Hizmet Alımı/Yapım İşi": "ihale_turu",
    "Mal Alımı/Yapım İşi": "ihale_turu",
    "hizmet /mal/ yapım işi": "ihale_turu",
    "hizmetleri sağlamayı / malları tedarik etmeyi / yapım işini üstlenmeyi": "ihale_turu",
    
    "ihaleye konu olan alım sözleşmesinin tanımı": "ihale_konusu",
    "İhale konusu": "ihale_konusu",
    "Sözleşme Başlığı": "ihale_konusu",
    
    "Pazarlık Usulü / Açık İhale Usulü(uygun olanı seçiniz)": "ihale_usulu",
    
    "götürü bedel / birim fiyat esaslı (her lot için uygun olan yöntem seçilecek ve belirtilecektir)": "teklif_esasi",
    
    "TL": "para_birimi",
    
    "ihale için ayrılan miktarı ve alım türünü (mal alımı, hizmet alımı, yapım işi) belirtiniz": "fiziki_miktar_ve_tur",
    
    # Yer bilgileri
    "Yerin ismi": "is_yeri_il_ilce",
    "il/ilçe": "is_yeri_il_ilce",
    "İlçe/İl": "is_yeri_il_ilce",
    
    "Yapım İşlerinde işin yapılacağı, hizmet alımlarında hizmetin gerçekleştirileceği, mal alımlarında malın teslim edileceği yeri belirtiniz": "teslim_yeri",
    
    "İhalenin yapılacağı yerin açık adresi yazılmalıdır": "ihale_yapilacak_adres",
    
    "yer adı (ihale makamının faaliyet gösterdiği il)": "mahkeme_il",
    
    # Tarih ve Saat
    "<…./…/20…": "ihale_tarihi",
    "<…. /…./20….>": "ihale_tarihi",
    "…./…./20…": "ihale_tarihi",
    "…./…./…..(ihale tarihi)": "ihale_tarihi",
    "Son başvuru tarihi bu duyurunun yayın tarihinden en az 20 gün sonra olmalıdır": "ihale_tarihi",
    
    "… : ..>": "ihale_saati",
    ": <… : …>": "ihale_saati",
    "<… : …>": "ihale_saati",
    "……(ihale saati)": "ihale_saati",
    
    "< Davet tarihi (ihaleye davet mektubu alınmışsa)>": "davet_tarihi",
    
    # Teminat ve Ödeme
    "yapılmayacaktır/yapılacaktır(uygun olanı seçiniz)": "on_odeme",
    
    "aranmayacaktır/aranacaktır": "sigorta",
    
    "tarih / sözleşmenin her iki tarafça imzalandığı tarih(uygun olanı seçiniz)": "sozlesme_baslangic",
    
    "sayı (uygulama süresini giriniz": "uygulama_suresi_ay",
    
    "Lot No, ihale lotlara bölünmüş ise": "lot_numarasi",
    
    "......................................": "diger_bilgiler",
    
    "rakam": "benzer_is_yili",
    "<rakam girin>": "dava_gecmisi_yili",
    
    "İhale konusu işin niteliğine göre istenen bilgi ve/veya belgelerden": "yeterlik_degerlendirme",
}

# Talimat / açıklama niteliğindeki sarı alanlar (form alanı değil, bilgilendirme amaçlı)
INSTRUCTION_FIELDS = [
    "Lot Numarası",
    "Aşağıda yer alan maddeler içerisindeki boş yerler",
    "İhalenize aşağıdaki ifadelerden hangisi uygun ise onu seçiniz",
    "Sözleşme Makamı ihale yöntemini belirlediğinde",
    "Birim fiyat esasında ihale yapılmakta ise",
    "Götürü bedel ihalelerde",
    "Önerilen teknik kriterler ve ağırlıkları",
    "Değerlendirme Komitesinin başkan ve üyeleri",
    "Bu beyanın metni değiştirilemez",
    "Azami 3 sayfa + 3 sayfa ek",
    "Yapım işi alımlarında ihale kapsamında talep edilmiş ise",
    "İhaleye ortak girişim ya da konsorsiyum olarak teklif sunulacaksa",
    "Serbest formatta aşağıdaki bilgileri içeren",
    "Tüzel kişiliğin antetli kağıdına yazılarak sunulacaktır",
    "mali kimlik formu, tüzel kişilik formu",
    "İstekliler teknik tekliflerini Teknik Şartname doğrultusunda",
    "İhale kapsamında tekliflerin sunulması aşamasında",
    "Toplam teklif fiyatı ile ilgili bütçe dökümü",
    "Yalnızca pazarlık usülü ihaleler için kullanılacaktır",
    "Sadece Pazarlık Usulü İhalelerde kullanılacaktır",
    "Pazarlık Usulü uygulanacak ihalelerde Değerlendirme Komitesi",
    "Not: İhalenin geçerli olması için en az 5 adayın",
    "Yararlanıcı ihale konusu ile ilgili olmayan",
    "İstenmesi halinde;",
    "Yapım işleri için sigorta koşulu sağlanmalıdır",
    "Eğer ihale lotlara ayrıldıysa uygulama süresini",
    "Hizmet Alımlarında Organizasyon ve Metodoloji",
    "İhale teklifi sırasında herhangi bir bedel yazılmamalıdır",
    "Ön ödeme miktarı sözleşme bedelinin",
    "%6'dan az bir oran belirlenemez",
    "Okudum, kabul ediyorum",
    "İmza",
    "Teklif Veren (Yetkili imzası/imzaları ve kaşe)",
    "Tarih",
    "<Örnek:",
    "İsteklinin Antedi",
    "Tüzel kişiliğin ad(lar)ı",
    "liderliği tarafımızca üstlenilmiş olarak / bireysel olarak",
    "Tüzel kişiliğin yetkili temsilcisinin imzası",
    "Tüzel kişiliğin yetkili temsilcisinin adı ve ünvanı",
    "isteklinin adı",
    "Tedarikçinin/Hizmet Sunucusunun/Yapım Müteahhidinin Tam Resmi Adı",
    "Hukuki statüsü / ünvanı",
    "Resmi tescil numarası",
    "Açık resmi-tebligat adresi",
    "Vergi dairesi ve numarası",
    "Kesin teminat tutarı sözleşme bedelinin",
    "uygun olan seçeneği seçiniz",
]


def get_fields_by_category():
    """Alanları kategorilere göre gruplar ve sıralı olarak döndürür."""
    categorized = {}
    for cat in FIELD_CATEGORIES:
        categorized[cat] = []

    for field_id, field_info in UNIQUE_FIELDS.items():
        cat = field_info["category"]
        if cat in categorized:
            categorized[cat].append((field_id, field_info))

    # Her kategori içinde sırala
    for cat in categorized:
        categorized[cat].sort(key=lambda x: x[1].get("order", 999))

    return categorized


def get_all_required_fields():
    """Zorunlu alanları döndürür."""
    return {
        fid: finfo for fid, finfo in UNIQUE_FIELDS.items()
        if finfo.get("required", False)
    }
