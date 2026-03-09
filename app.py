"""
İhale Dosyası Doldurma Uygulaması - Ana Streamlit Modülü.

Trakya Kalkınma Ajansı mali destek yararlanıcılarının ihale dosyalarını
kolayca doldurmasını sağlayan web tabanlı form uygulaması.

Özellikler:
    - Sarı vurgulu alanları otomatik tespit
    - Benzersiz (unique) alan eşleştirmesi ile tekrar eden bilgilerin tek seferde girişi
    - Seçimlik alanlar için açılır menü desteği
    - Doldurulmuş Word (.docx) ve PDF çıktısı oluşturma
    - Form verilerini CSV olarak kaydetme

Kullanım:
    streamlit run app.py
"""

import streamlit as st
import os
import sys
import json
import csv
import time as time_module
from datetime import datetime, date, time

# Proje modülleri
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from field_config import (
    UNIQUE_FIELDS,
    FIELD_CATEGORIES,
    get_fields_by_category,
    get_all_required_fields,
)
from doc_generator import generate_filled_document, validate_form_data

# =============================================================================
# SAYFA YAPILANDIRMASI
# =============================================================================
st.set_page_config(
    page_title="İhale Dosyası Doldurma Sistemi",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# ÖZEL CSS STİLLERİ
# =============================================================================
st.markdown("""
<style>
    /* Ana tema */
    :root {
        --primary: #1B4F72;
        --primary-light: #2E86C1;
        --secondary: #F39C12;
        --success: #27AE60;
        --danger: #E74C3C;
        --bg-dark: #0E1117;
        --bg-card: #1A1D23;
        --text-primary: #FAFAFA;
        --text-secondary: #B3B8C3;
    }

    /* Başlık stili */
    .main-header {
        background: linear-gradient(135deg, #1B4F72 0%, #2E86C1 50%, #3498DB 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(46, 134, 193, 0.3);
        text-align: center;
    }
    .main-header h1 {
        color: white !important;
        font-size: 2rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .main-header p {
        color: rgba(255, 255, 255, 0.85);
        font-size: 1.05rem;
        margin: 0;
    }

    /* Kategori başlık kartı */
    .category-header {
        background: linear-gradient(135deg, #1A1D23 0%, #2D3436 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #F39C12;
        margin: 1.5rem 0 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .category-header h3 {
        color: #F39C12 !important;
        font-weight: 600;
        margin: 0 !important;
        font-size: 1.2rem;
    }
    .category-header p {
        color: #B3B8C3;
        font-size: 0.85rem;
        margin: 0.3rem 0 0 0;
    }

    /* Form alanı kartı */
    .field-card {
        background: #1A1D23;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
    }
    .field-card:hover {
        border-color: rgba(46, 134, 193, 0.3);
        box-shadow: 0 4px 16px rgba(46, 134, 193, 0.1);
    }

    /* İstatistik kartı */
    .stat-card {
        background: linear-gradient(135deg, #1A1D23, #2D3436);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .stat-card h2 {
        color: #3498DB !important;
        font-size: 2rem;
        margin: 0;
    }
    .stat-card p {
        color: #B3B8C3;
        font-size: 0.85rem;
        margin: 0.3rem 0 0 0;
    }

    /* Başarı mesajı */
    .success-box {
        background: linear-gradient(135deg, rgba(39, 174, 96, 0.15), rgba(39, 174, 96, 0.05));
        border: 1px solid rgba(39, 174, 96, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    /* Sidebar stili */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E1117 0%, #1A1D23 100%);
    }

    /* Progress bar */
    .progress-bar-container {
        background: #2D3436;
        border-radius: 20px;
        padding: 3px;
        margin: 0.5rem 0;
    }
    .progress-bar-fill {
        height: 12px;
        border-radius: 20px;
        transition: width 0.5s ease;
    }

    /* Buton stili */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 2rem;
        transition: all 0.3s ease;
    }

    /* Zorunlu alan işareti */
    .required-mark {
        color: #E74C3C;
        font-weight: bold;
    }

    /* Tab stili */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# SESSION STATE BAŞLATMA
# =============================================================================
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

if "page" not in st.session_state:
    st.session_state.page = "form"

if "generation_result" not in st.session_state:
    st.session_state.generation_result = None


def get_template_path():
    """Şablon .docx dosyasının yolunu döndürür."""
    candidates = [
        os.path.join(os.path.dirname(__file__), "Taslak İhale Dosyası.docx"),
        os.path.join(os.path.dirname(__file__), "data", "Taslak İhale Dosyası.docx"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def render_header():
    """Ana başlık bölümünü oluşturur."""
    st.markdown("""
    <div class="main-header">
        <h1>📋 İhale Dosyası Doldurma Sistemi</h1>
        <p>Trakya Kalkınma Ajansı Mali Destek Programı – İhale Dosyası Hazırlama Formu</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Yan menüyü oluşturur."""
    with st.sidebar:
        st.markdown("### 🏛️ Trakya Kalkınma Ajansı")
        st.markdown("---")

        # İlerleme bilgisi
        total = len(UNIQUE_FIELDS)
        filled = sum(
            1 for fid in UNIQUE_FIELDS
            if st.session_state.form_data.get(fid)
            and st.session_state.form_data[fid] != ""
        )
        required_total = len(get_all_required_fields())
        required_filled = sum(
            1 for fid, finfo in UNIQUE_FIELDS.items()
            if finfo.get("required") and st.session_state.form_data.get(fid)
            and st.session_state.form_data[fid] != ""
        )

        pct = int((filled / total) * 100) if total > 0 else 0
        req_pct = int((required_filled / required_total) * 100) if required_total > 0 else 0

        # Güzel progress gösterimi
        st.markdown("#### 📊 Doluluk Durumu")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Doldurulan", f"{filled}/{total}")
        with col2:
            st.metric("Zorunlu", f"{required_filled}/{required_total}")

        # Progress bar
        if req_pct == 100:
            bar_color = "#27AE60"
        elif req_pct >= 50:
            bar_color = "#F39C12"
        else:
            bar_color = "#E74C3C"

        st.markdown(f"""
        <div class="progress-bar-container">
            <div class="progress-bar-fill" style="width: {req_pct}%; background: {bar_color};"></div>
        </div>
        <p style="text-align:center; color: {bar_color}; font-weight:600;">
            Zorunlu Alanlar: %{req_pct}
        </p>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Kategori navigasyonu
        st.markdown("#### 🗂️ Bölümler")
        for i, cat in enumerate(FIELD_CATEGORIES, 1):
            cat_fields = [
                fid for fid, fi in UNIQUE_FIELDS.items()
                if fi["category"] == cat
            ]
            cat_filled = sum(
                1 for fid in cat_fields
                if st.session_state.form_data.get(fid)
                and st.session_state.form_data[fid] != ""
            )
            icon = "✅" if cat_filled == len(cat_fields) else "📝"
            st.markdown(f"{icon} **{i}. {cat}** ({cat_filled}/{len(cat_fields)})")

        st.markdown("---")

        # Hızlı işlemler
        st.markdown("#### ⚡ Hızlı İşlemler")
        if st.button("🗑️ Formu Temizle", use_container_width=True):
            st.session_state.form_data = {}
            st.session_state.generation_result = None
            st.rerun()

        if st.button("💾 Taslak Kaydet", use_container_width=True):
            _save_draft()

        if st.button("📂 Taslak Yükle", use_container_width=True):
            _load_draft()

        st.markdown("---")
        st.markdown(
            "<p style='text-align:center; color:#666; font-size:0.75rem;'>"
            "v1.0 | Trakya Kalkınma Ajansı<br>"
            f"Tarih: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>",
            unsafe_allow_html=True,
        )


def render_form_field(field_id, field_info):
    """Tek bir form alanını oluşturur."""
    field_type = field_info["type"]
    label = field_info["label"]
    required = field_info.get("required", False)
    help_text = field_info.get("help", "")
    placeholder = field_info.get("placeholder", "")

    # Zorunlu alan işareti
    if required:
        label = f"{label} *"

    current_value = st.session_state.form_data.get(field_id, "")

    if field_type == "text":
        value = st.text_input(
            label,
            value=current_value or "",
            placeholder=placeholder,
            help=help_text,
            key=f"field_{field_id}",
        )

    elif field_type == "textarea":
        value = st.text_area(
            label,
            value=current_value or "",
            placeholder=placeholder,
            help=help_text,
            height=100,
            key=f"field_{field_id}",
        )

    elif field_type == "select":
        options = field_info.get("options", [])
        all_options = ["-- Seçiniz --"] + options
        current_idx = 0
        if current_value in options:
            current_idx = options.index(current_value) + 1

        selected = st.selectbox(
            label,
            options=all_options,
            index=current_idx,
            help=help_text,
            key=f"field_{field_id}",
        )
        value = selected if selected != "-- Seçiniz --" else ""

    elif field_type == "date":
        if isinstance(current_value, date):
            default_date = current_value
        elif isinstance(current_value, str) and current_value:
            try:
                default_date = datetime.strptime(current_value, "%d/%m/%Y").date()
            except ValueError:
                default_date = date.today()
        else:
            default_date = date.today()

        value = st.date_input(
            label,
            value=default_date,
            help=help_text,
            key=f"field_{field_id}",
            format="DD/MM/YYYY",
        )

    elif field_type == "time":
        if isinstance(current_value, time):
            default_time = current_value
        elif isinstance(current_value, str) and current_value:
            try:
                parts = current_value.split(":")
                default_time = time(int(parts[0]), int(parts[1]))
            except (ValueError, IndexError):
                default_time = time(10, 0)
        else:
            default_time = time(10, 0)

        value = st.time_input(
            label,
            value=default_time,
            help=help_text,
            key=f"field_{field_id}",
        )

    elif field_type == "number":
        min_val = field_info.get("min_value", 0)
        max_val = field_info.get("max_value", 1000)

        if isinstance(current_value, (int, float)):
            default_val = int(current_value)
        elif isinstance(current_value, str) and current_value:
            try:
                default_val = int(current_value)
            except ValueError:
                default_val = min_val
        else:
            default_val = min_val

        value = st.number_input(
            label,
            min_value=min_val,
            max_value=max_val,
            value=default_val,
            help=help_text,
            key=f"field_{field_id}",
        )

    elif field_type == "list":
        # Dinamik Çoklu Satır Girişi
        st.write(f"**{label}**")
        if help_text:
            st.caption(help_text)
            
        # Mevcut değerleri listeye çevir (CSV'den string gelmiş olabilir)
        if isinstance(current_value, str):
            items = [i.strip() for i in current_value.splitlines() if i.strip()]
        elif isinstance(current_value, list):
            items = current_value
        else:
            items = []
            
        # En az 1 boş satır olsun
        if not items:
            items = [""]
            
        new_items = []
        for i, item in enumerate(items):
            input_val = st.text_input(
                f"Kalem {i+1}",
                value=item,
                placeholder=placeholder,
                key=f"field_{field_id}_{i}"
            )
            new_items.append(input_val)
            
        # Yeni satır ekleme butonu
        if st.button("➕ Yeni Kalem Ekle", key=f"btn_add_{field_id}"):
            new_items.append("")
            st.rerun()
            
        value = [i.strip() for i in new_items if i.strip()]

    elif field_type in ("phone", "email"):
        value = st.text_input(
            label,
            value=current_value or "",
            placeholder=placeholder,
            help=help_text,
            key=f"field_{field_id}",
        )

    else:
        value = st.text_input(
            label,
            value=current_value or "",
            placeholder=placeholder,
            help=help_text,
            key=f"field_{field_id}",
        )

    # Değeri session state'e kaydet
    st.session_state.form_data[field_id] = value


def render_form():
    """Ana form bölümünü oluşturur."""
    categorized = get_fields_by_category()

    # Tab'lar ile kategorileri göster
    tabs = st.tabs([f"📌 {cat}" for cat in FIELD_CATEGORIES])

    for tab, cat in zip(tabs, FIELD_CATEGORIES):
        with tab:
            # Kategori başlığı
            category_descriptions = {
                "Kurum Bilgileri": "Sözleşme Makamı / Mali Destek Yararlanıcısının temel bilgileri",
                "Proje Bilgileri": "Proje adı, sözleşme kodu ve referans numaraları",
                "İhale Bilgileri": "İhale türü, usulü ve kapsamına ilişkin bilgiler",
                "Yer Bilgileri": "İşin yapılacağı yer, ihale adresi ve mahkeme ili",
                "Tarih ve Saat": "İhale tarihi, saati ve diğer tarih bilgileri",
                "Teminat ve Ödeme": "Geçici teminat, kesin teminat, ön ödeme bilgileri",
                "Sözleşme Bilgileri": "Sözleşme süresi, lot bilgileri ve diğer detaylar",
            }

            st.markdown(f"""
            <div class="category-header">
                <h3>{cat}</h3>
                <p>{category_descriptions.get(cat, '')}</p>
            </div>
            """, unsafe_allow_html=True)

            fields = categorized.get(cat, [])
            
            # Görünen alanları filtrele (Koşullu alanlar için)
            visible_fields = []
            for field_id, field_info in fields:
                # Kesin Teminat Oranı Gizleme
                if field_id == "kesin_teminat_orani":
                    if st.session_state.form_data.get("kesin_teminat") == "İSTENMEMEKTEDİR":
                        st.session_state.form_data[field_id] = ""
                        continue
                        
                # Ön Ödeme Oranı Gizleme
                if field_id == "on_odeme_orani":
                    if st.session_state.form_data.get("on_odeme") == "Yapılmayacaktır":
                        st.session_state.form_data[field_id] = ""
                        continue
                        
                visible_fields.append((field_id, field_info))

            # İki sütunlu düzen
            col1, col2 = st.columns(2)
            for i, (field_id, field_info) in enumerate(visible_fields):
                with col1 if i % 2 == 0 else col2:
                    render_form_field(field_id, field_info)


def render_preview():
    """Önizleme bölümünü oluşturur."""
    st.markdown("### 👁️ Form Verisi Önizleme")

    categorized = get_fields_by_category()
    has_data = False

    for cat in FIELD_CATEGORIES:
        fields = categorized.get(cat, [])
        filled_fields = [
            (fid, finfo) for fid, finfo in fields
            if st.session_state.form_data.get(fid)
            and st.session_state.form_data[fid] != ""
        ]

        if filled_fields:
            has_data = True
            st.markdown(f"**{cat}:**")
            for fid, finfo in filled_fields:
                value = st.session_state.form_data[fid]
                if isinstance(value, date):
                    value = value.strftime("%d/%m/%Y")
                elif isinstance(value, time):
                    value = value.strftime("%H:%M")
                st.markdown(f"- {finfo['label']}: `{value}`")

    if not has_data:
        st.info("Henüz veri girilmemiş. Lütfen formu doldurunuz.")


def render_generation():
    """Belge oluşturma bölümünü oluşturur."""
    st.markdown("""
    <div class="category-header">
        <h3>📄 Belge Oluşturma</h3>
        <p>Formu doldurup aşağıdaki butona tıklayarak ihale dosyanızı oluşturabilirsiniz.</p>
    </div>
    """, unsafe_allow_html=True)

    # Doğrulama
    is_valid, errors = validate_form_data(st.session_state.form_data)

    if errors:
        with st.expander("⚠️ Eksik / Hatalı Alanlar", expanded=True):
            for err in errors:
                st.warning(err)

    # İstatistikler
    total_fields = len(UNIQUE_FIELDS)
    filled = sum(
        1 for fid in UNIQUE_FIELDS
        if st.session_state.form_data.get(fid)
        and st.session_state.form_data[fid] != ""
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h2>{total_fields}</h2>
            <p>Toplam Alan</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h2>{filled}</h2>
            <p>Doldurulan</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        req_total = len(get_all_required_fields())
        req_filled = sum(
            1 for fid, fi in UNIQUE_FIELDS.items()
            if fi.get("required") and st.session_state.form_data.get(fid)
            and st.session_state.form_data[fid] != ""
        )
        st.markdown(f"""
        <div class="stat-card">
            <h2>{req_filled}/{req_total}</h2>
            <p>Zorunlu Alanlar</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        pct = int((filled / total_fields) * 100) if total_fields > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <h2>%{pct}</h2>
            <p>Tamamlanma</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Oluşturma butonu
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        generate_clicked = st.button(
            "🚀 İhale Dosyasını Oluştur",
            type="primary",
            use_container_width=True,
            disabled=not is_valid,
        )

    if generate_clicked:
        template_path = get_template_path()
        if not template_path:
            st.error("❌ Şablon dosyası bulunamadı! 'Taslak İhale Dosyası.docx' "
                     "dosyasının proje klasöründe olduğundan emin olunuz.")
            return

        start_time = time_module.time()

        with st.spinner("📄 İhale dosyası oluşturuluyor..."):
            try:
                output_dir = os.path.join(os.path.dirname(__file__), "output")
                result = generate_filled_document(
                    template_path,
                    st.session_state.form_data,
                    output_dir=output_dir,
                )

                elapsed = time_module.time() - start_time
                result["elapsed_time"] = elapsed

                st.session_state.generation_result = result

                # CSV kaydet
                _save_result_csv()

            except Exception as e:
                st.error(f"❌ Belge oluşturma hatası: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    # Sonuç gösterimi
    if st.session_state.generation_result:
        result = st.session_state.generation_result
        stats = result.get("stats", {})

        st.markdown("""
        <div class="success-box">
            <h3 style="color: #27AE60;">✅ İhale Dosyası Başarıyla Oluşturuldu!</h3>
        </div>
        """, unsafe_allow_html=True)

        # İstatistikler
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Toplam Sarı Alan", stats.get("total_yellow", 0))
        with col2:
            st.metric("Doldurulan", stats.get("filled", 0))
        with col3:
            st.metric("Talimat (Atlandı)", stats.get("instruction_skipped", 0))
        with col4:
            elapsed = result.get("elapsed_time", 0)
            st.metric("Süre", f"{elapsed:.2f} sn")

        # İndirme bağlantıları
        st.markdown("#### 📥 Dosyaları İndir")
        col_dl1, col_dl2 = st.columns(2)

        docx_path = result.get("docx")
        if docx_path and os.path.exists(docx_path):
            with col_dl1:
                with open(docx_path, "rb") as f:
                    st.download_button(
                        "📄 Word Dosyasını İndir (.docx)",
                        data=f.read(),
                        file_name=os.path.basename(docx_path),
                        mime="application/vnd.openxmlformats-officedocument"
                             ".wordprocessingml.document",
                        use_container_width=True,
                        type="primary",
                    )

        pdf_path = result.get("pdf")
        if pdf_path and os.path.exists(pdf_path):
            with col_dl2:
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "📑 PDF Dosyasını İndir (.pdf)",
                        data=f.read(),
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf",
                        use_container_width=True,
                    )
        elif result.get("pdf_error"):
            with col_dl2:
                st.warning(f"PDF oluşturulamadı: {result['pdf_error']}")


def _save_draft():
    """Form verilerini taslak olarak kaydeder."""
    draft_path = os.path.join(os.path.dirname(__file__), "data", "draft.json")
    os.makedirs(os.path.dirname(draft_path), exist_ok=True)

    # Serialize edilebilir hale getir
    serializable = {}
    for k, v in st.session_state.form_data.items():
        if isinstance(v, date):
            serializable[k] = v.strftime("%d/%m/%Y")
        elif isinstance(v, time):
            serializable[k] = v.strftime("%H:%M")
        else:
            serializable[k] = v

    with open(draft_path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)

    st.sidebar.success("✅ Taslak kaydedildi!")


def _load_draft():
    """Kayıtlı taslağı yükler."""
    draft_path = os.path.join(os.path.dirname(__file__), "data", "draft.json")
    if os.path.exists(draft_path):
        with open(draft_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        st.session_state.form_data = data
        st.sidebar.success("✅ Taslak yüklendi!")
        st.rerun()
    else:
        st.sidebar.warning("⚠️ Kayıtlı taslak bulunamadı.")


def _save_result_csv():
    """Sonuçları CSV olarak kaydeder."""
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    today = datetime.now().strftime("%Y%m%d")
    csv_path = os.path.join(output_dir, f"ihale_form_verileri_{today}.csv")

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Alan ID", "Alan Adı", "Kategori", "Değer", "Zorunlu", "Tarih"])

        for fid, finfo in UNIQUE_FIELDS.items():
            value = st.session_state.form_data.get(fid, "")
            if isinstance(value, date):
                value = value.strftime("%d/%m/%Y")
            elif isinstance(value, time):
                value = value.strftime("%H:%M")

            writer.writerow([
                fid,
                finfo["label"],
                finfo["category"],
                value,
                "Evet" if finfo.get("required") else "Hayır",
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            ])


# =============================================================================
# ANA UYGULAMA
# =============================================================================
def main():
    """Ana uygulama akışı."""
    render_header()
    render_sidebar()

    # Şablon dosyası kontrolü
    template_path = get_template_path()
    if not template_path:
        st.error(
            "⚠️ **Şablon dosyası bulunamadı!**\n\n"
            "Lütfen `Taslak İhale Dosyası.docx` dosyasının proje klasöründe "
            "olduğundan emin olunuz.\n\n"
            "`.doc` dosyanız varsa önce `.docx` formatına dönüştürünüz. "
            "Bunun için `analyze_doc.py` scriptini çalıştırabilirsiniz."
        )

    # Ana içerik
    main_tab1, main_tab2, main_tab3 = st.tabs([
        "📝 Form Doldurma",
        "👁️ Ön İzleme",
        "📄 Belge Oluştur",
    ])

    with main_tab1:
        render_form()

    with main_tab2:
        render_preview()

    with main_tab3:
        render_generation()


if __name__ == "__main__":
    main()
