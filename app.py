import streamlit as st
from PIL import Image
import requests
import io
import time
import json

# 1. Sahifa sozlamalari
st.set_page_config(page_title="ANVARBEK AI", page_icon="🌿", layout="wide")

# 2. Til tanlash (Oddiy interfeys uchun)
language = st.sidebar.selectbox("🌐 Tilni tanlang / Choose language:", ["O'zbek", "Русский", "English"])

# Tilga qarab matnlarni o'zgartirish
if language == "O'zbek":
    app_title = "🌿 ANVARBEK AI"
    sub_title = "O'simlik dunyosini kashf eting"
    camera_btn = "📷 Kamera bilan suratga olish"
    upload_btn = "🖼️ Galereyadan tanlash"
    research_btn = "🔬 Tadqiqot rejimi"
    game_btn = "🎮 O'yin rejimi"
    model_btn = "🧊 3D Model"
    offline_status = "📴 Holat: Ofline"
    online_status = "📶 Holat: Online"
    result_text = "🔎 Aniqlangan o'simlik:"
    wait_text = "⏳ Rasm tahlil qilinmoqda..."
elif language == "Русский":
    app_title = "🌿 ANVARBEK AI"
    sub_title = "Откройте мир растений"
    camera_btn = "📷 Снять на камеру"
    upload_btn = "🖼️ Выбрать из галереи"
    research_btn = "🔬 Режим исследования"
    game_btn = "🎮 Игровой режим"
    model_btn = "🧊 3D модель"
    offline_status = "📴 Статус: Офлайн"
    online_status = "📶 Статус: Онлайн"
    result_text = "🔎 Определенное растение:"
    wait_text = "⏳ Анализ изображения..."
else:
    app_title = "🌿 ANVARBEK AI"
    sub_title = "Discover the plant world"
    camera_btn = "📷 Take a picture"
    upload_btn = "🖼️ Upload from gallery"
    research_btn = "🔬 Research Mode"
    game_btn = "🎮 Game Mode"
    model_btn = "🧊 3D Model"
    offline_status = "📴 Status: Offline"
    online_status = "📶 Status: Online"
    result_text = "🔎 Detected Plant:"
    wait_text = "⏳ Analyzing image..."

# 3. Asosiy sarlavha
st.title(app_title)
st.caption(sub_title)

# 4. Offline / Online rejim statusi (Internet bor yoki yo'qligini tekshirish)
try:
    requests.get("https://www.google.com", timeout=2)
    status_online = True
    st.sidebar.success(online_status)
except:
    status_online = False
    st.sidebar.warning(offline_status)

# 5. Tezkor kirish (Quick Access) — Katta interfeys tugmalari
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(camera_btn, use_container_width=True):
        st.info("📷 Kamera qurilmangiz tomonidan ochiladi (Web kameraga ruxsat bering).")
        # Bu yerda kamera kodini qo'shish mumkin, hozircha UI ko'rinishi uchun qo'yildi.
        
with col2:
    if st.button(model_btn, use_container_width=True):
        st.warning("🧊 3D Model hozircha ishlab chiqilmoqda (Beta versiya).")

with col3:
    if st.button(game_btn, use_container_width=True):
        st.success("🎮 O'yin rejimi: O'simlik rasmini toping! (Tez orada!)")

with col4:
    if st.button(research_btn, use_container_width=True):
        st.balloons()  # Chiroyli animatsiya
        st.write("🔬 Ilmiy tadqiqot ma'lumotlari yuklanmoqda...")

# 6. Rasm yuklash / Kamera bo'limi
st.divider()
uploaded_file = st.file_uploader(f"📷 {sub_title}", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Rasmni ko'rsatish
    st.image(image, caption="Yuklangan rasm", use_container_width=True)
    
    # 7. Koordinatalarni aniqlash (GPS)
    # Real GPS brauzer ruxsatisiz olinmaydi, lekin biz test uchun mavjud API dan foydalanamiz
    try:
        # Bu yerda IP orqali taxminiy lokatsiya olamiz
        geo_response = requests.get("https://ipapi.co/json/", timeout=3)
        geo_data = geo_response.json()
        lat = geo_data.get("latitude", "Noma'lum")
        lon = geo_data.get("longitude", "Noma'lum")
        st.caption(f"📍 Taxminiy koordinatalar: {lat}, {lon}")
    except:
        st.caption("📍 Koordinata aniqlanmadi (Internet uzilgan).")
    
# 8. AI Aniqlash jarayoni
    # 8. AI Aniqlash jarayoni
if st.button("🔍 O'simlikni aniqlash"):

    with st.spinner("🌿 O'simlik aniqlanmoqda..."):

        try:
            PLANT_ID_API_KEY = st.secrets["PLANT_ID_API_KEY"].strip()

            API_URL = "https://api.plant.id/v3/identification"

            image = Image.open(uploaded_file).convert("RGB")

            image_buffer = io.BytesIO()
            image.save(
                image_buffer,
                format="JPEG",
                quality=90
            )

            image_bytes = image_buffer.getvalue()

            import base64

            image_base64 = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            headers = {
                "Api-Key": PLANT_ID_API_KEY,
                "Content-Type": "application/json"
            }

            payload = {
                "images": [
                    image_base64
                ],
                "similar_images": True
            }

            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:

                result = response.json()

                suggestions = result.get(
                    "result",
                    {}
                ).get(
                    "classification",
                    {}
                ).get(
                    "suggestions",
                    []
                )

                st.subheader("🌿 AI natijasi")

                if suggestions:

                    best = suggestions[0]

                    name = best.get(
                        "name",
                        "Noma'lum"
                    )

                    probability = best.get(
                        "probability",
                        0
                    )

                    st.success(
                        f"🌱 O'simlik: **{name}**"
                    )

                    st.write(
                        f"📊 Ishonchlilik: "
                        f"**{probability * 100:.2f}%**"
                    )

                else:

                    st.warning(
                        "⚠️ O'simlik aniqlanmadi."
                    )
            elif response.status_code == 401:
                    
                    st.error("❌ Plant.id API 401 — autentifikatsiya xatosi.")
                    
                    st.write("API javobi:")
                    
                    st.code(response.text)
            
            elif response.status_code == 402:

                st.error(
                    "💳 Plant.id kreditlari tugagan "
                    "yoki API keyga kredit biriktirilmagan."
                )

            elif response.status_code == 429:

                st.error(
                    "⏳ API so'rovlar limiti tugagan."
                )

            else:

                st.error(
                    f"❌ Plant.id API xatosi: "
                    f"{response.status_code}"
                )

                st.code(response.text)

        except KeyError:

            st.error(
                "❌ Streamlit Secrets ichida "
                "PLANT_ID_API_KEY topilmadi."
            )

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ Plant.id javobi juda uzoq davom etdi."
            )

        except Exception as e:

            st.error(
                f"❌ Xatolik: {e}"
            )
