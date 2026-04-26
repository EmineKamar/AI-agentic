import streamlit as st
from lama_search import search_text_files, search_image_files  # Fonksiyonların bulunduğu dosya

st.set_page_config(page_title="AI File Search", layout="wide")
st.title("📁 AI File Search App")
st.write("PDF, TXT ve görsel dosyalarda anahtar kelime arayabilirsiniz.")

# Kullanıcıdan arama kelimesi al
keyword = st.text_input("Aramak istediğiniz kelimeyi girin:")

if st.button("Ara"):
    if keyword.strip() == "":
        st.warning("Lütfen bir anahtar kelime girin.")
    else:
        with st.spinner("Dosyalar aranıyor..."):
            # Metin dosyalarını ara
            text_result = search_text_files(keyword)
            
            # Görsel dosyalarını ara
            image_result = search_image_files(keyword)

        # Metin dosyası sonucu
        if text_result != "None":
            st.success(f"Metin dosyasında bulundu: `{text_result}`")
        else:
            st.info("Metin dosyasında bulunamadı.")

        # Görsel dosyası sonucu
        if image_result != "None":
            st.success(f"Görsel dosyada bulundu: `{image_result}`")
            st.image(image_result, caption=image_result)
        else:
            st.info("Görsel dosyada bulunamadı.")
