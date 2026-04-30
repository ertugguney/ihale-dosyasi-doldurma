import streamlit as st

if "form_data" not in st.session_state:
    st.session_state.form_data = {}

def render_form_field(field_id):
    st.write("Dinamik Liste Testi")
    
    current_value = st.session_state.form_data.get(field_id, "")
    
    if isinstance(current_value, list):
        items = current_value
    elif isinstance(current_value, str):
        items = [i.strip() for i in current_value.splitlines() if i.strip()]
    else:
        items = []
        
    if not items:
        items = [""]
        
    new_items = []
    for i, item in enumerate(items):
        input_val = st.text_input(
            f"Kalem {i+1}",
            value=item,
            key=f"field_input_{field_id}_{i}"
        )
        new_items.append(input_val)
        
    if st.button("➕ Yeni Kalem Ekle", key=f"btn_add_{field_id}"):
        if len(items) < 10:
            current_typed = []
            for j in range(len(items)):
                val = st.session_state.get(f"field_input_{field_id}_{j}", "")
                current_typed.append(val)
            
            st.session_state.form_data[field_id] = current_typed + [""]
            st.rerun()
        else:
            st.warning("⚠️ Maksimum 10 kalem eklenebilir!")
        
    value = new_items
    st.session_state.form_data[field_id] = value

render_form_field("ihale_konusu")
st.write(st.session_state.form_data)
