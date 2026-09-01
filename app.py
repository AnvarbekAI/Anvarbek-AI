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
    offline_status = "📴 Holat: Ofлайн"
    online_status = "📶 Holat: Onлайн"
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
    # 🔍 O'SIMLIKNI ANIQLASH
if st.button("🔍 Aniqlash", use_container_width=True):

    with st.spinner("🌿 O'simlik aniqlanmoqda..."):

        try:
            # Pl@ntNet API kaliti
            PLANTNET_API_KEY = st.secrets["PLANTNET_API_KEY"]

            # Pl@ntNet API
            API_URL = (
                "https://my-api.plantnet.org/v2/identify/all"
                f"?api-key={PLANTNET_API_KEY}"
                "&lang=en"
                "&nb-results=5"
            )

            # Yuklangan rasm
            image_bytes = uploaded_file.getvalue()

            # Rasmni multipart qilib yuborish
            files = {
                "images": (
                    uploaded_file.name,
                    image_bytes,
                    uploaded_file.type
                )
            }

            data = {
                "organs": "auto"
            }

            response = requests.post(
                API_URL,
                files=files,
                data=data,
                timeout=120
            )

            # Muvaffaqiyatli javob
            if response.status_code == 200:

                result = response.json()

                st.success("✅ O'simlik aniqlandi!")

                # Eng yaxshi natija
                best_match = result.get(
                    "bestMatch",
                    "Noma'lum"
                )

                st.subheader("🌿 Aniqlangan o'simlik")

                st.write(
                    f"### 🌱 {best_match}"
                )

                # Natijalar
                results = result.get("results", [])

                if results:

                    best = results[0]

                    score = best.get(
                        "score",
                        0
                    )

                    species = best.get(
                        "species",
                        {}
                    )

                    scientific_name = species.get(
                        "scientificNameWithoutAuthor",
                        best_match
                    )

                    common_names = species.get(
                        "commonNames",
                        []
                    )

                    genus = species.get(
                        "genus",
                        {}
                    ).get(
                        "scientificNameWithoutAuthor",
                        "Noma'lum"
                    )

                    family = species.get(
                        "family",
                        {}
                    ).get(
                        "scientificNameWithoutAuthor",
                        "Noma'lum"
                    )

                    # Ishonchlilik
                    st.metric(
                        "📊 Ishonchlilik",
                        f"{score * 100:.2f}%"
                    )

                    st.markdown("---")

                    # Asosiy ma'lumotlar
                    st.subheader("📋 O'simlik ma'lumotlari")

                    st.write(
                        f"🌿 **Nomi:** {best_match}"
                    )

                    st.write(
                        f"🔬 **Ilmiy nomi:** "
                        f"{scientific_name}"
                    )

                    if common_names:
                        st.write(
                            "🏷️ **Umumiy nomlari:** "
                            + ", ".join(common_names[:5])
                        )

                    st.write(
                        f"🌱 **Turkumi:** {genus}"
                    )

                    st.write(
                        f"🧬 **Oilasi:** {family}"
                    )

                    st.markdown("---")

                    # Boshqa ehtimoliy natijalar
                    st.subheader(
                        "🔎 Boshqa ehtimoliy natijalar"
                    )

                    for i, item in enumerate(
                        results[:5],
                        start=1
                    ):

                        item_species = item.get(
                            "species",
                            {}
                        )

                        item_name = item_species.get(
                            "scientificNameWithoutAuthor",
                            "Noma'lum"
                        )

                        item_score = item.get(
                            "score",
                            0
                        )

                        st.write(
                            f"**{i}. {item_name}** — "
                            f"{item_score * 100:.2f}%"
                        )

                    st.markdown("---")

                    # Parvarish
                    st.subheader(
                        "🌱 Parvarish bo'yicha umumiy tavsiyalar"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write("☀️ **Yorug'lik**")

                        st.write(
                            "Ko'pchilik o'simliklar uchun "
                            "yetarli tabiiy yorug'lik muhim. "
                            "Aniq talab turiga qarab farq qiladi."
                        )

                        st.write("💧 **Sug'orish**")

                        st.write(
                            "Sug'orish miqdori o'simlik "
                            "turiga va tuproq namligiga bog'liq. "
                            "Ortiqcha sug'orishdan saqlaning."
                        )

                    with col2:

                        st.write("🌱 **Tuproq**")

                        st.write(
                            "Yaxshi drenajga ega tuproq "
                            "ko'pchilik o'simliklar uchun ma'qul."
                        )

                        st.write("🌡️ **Harorat**")

                        st.write(
                            "Keskin sovuq yoki issiqdan "
                            "himoya qilish tavsiya etiladi."
                        )

                    st.info(
                        "ℹ️ Parvarish tavsiyalari umumiy. "
                        "Aniq parvarish o'simlik turiga qarab "
                        "farq qilishi mumkin."
                    )

            else:

                st.error(
                    f"❌ Pl@ntNet API xatosi: "
                    f"{response.status_code}"
                )

                st.code(
                    response.text
                )

        except KeyError:

            st.error(
                "❌ PLANTNET_API_KEY topilmadi!"
            )

            st.info(
                "Streamlit → Settings → Secrets "
                "ichiga PLANTNET_API_KEY qo'shing."
            )

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ Server javobi juda uzoq davom etdi. "
                "Qayta urinib ko'ring."
            )

        except Exception as e:

            st.error(
                "❌ Xatolik yuz berdi:"
            )

            st.code(
                str(e)
            )
