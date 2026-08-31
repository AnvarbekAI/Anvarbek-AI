import streamlit as st
from PIL import Image
import requests


st.set_page_config(
    page_title="ANVARBEK AI",
    page_icon="🌿",
    layout="centered"
)

st.title("🌿 ANVARBEK AI")
st.write("O‘simlik rasmini yuklang — AI uni aniqlashga harakat qiladi.")

uploaded_file = st.file_uploader(
    "📷 O‘simlik rasmini yuklang",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Yuklangan rasm", use_container_width=True)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Yuklangan rasm", use_container_width=True)
    
    # ... AI natijasi ...
    
    API_TOKEN = st.secrets["HF_TOKEN"]
    
    # ... keyingi AI chaqiruv kodlari ...
    # 🔍 O'simlikni aniqlash
if st.button("🔍 O'simlikni aniqlash"):

    with st.spinner("🌿 AI rasmni tahlil qilmoqda..."):

        API_URL = "https://router.huggingface.co/hf-inference/models/google/vit-base-patch16-224"

        headers = {
            "Authorization": f"Bearer {API_TOKEN}"
        }

        image_bytes = uploaded_file.getvalue()

        response = requests.post(
            API_URL,
            headers=headers,
            data=image_bytes,
            timeout=120
        )

        if response.status_code == 200:

            results = response.json()

            st.subheader("🔎 AI natijasi")

            if isinstance(results, list) and len(results) > 0:

                best = results[0]

                label = best.get("label", "Noma'lum")
                score = best.get("score", 0)

                st.write(f"🏷️ Aniqlangan obyekt: {label}")
                st.write(f"📊 Ishonchlilik: {score * 100:.2f}%")

            else:
                st.warning("⚠️ AI natija qaytarmadi.")

        else:

            st.error(f"❌ API xatosi: {response.status_code}")
            st.code(response.text)
