import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator

# 🔮 Estética mágica medieval
st.markdown("""
    <style>
    .stApp {
        background-color: #1d1b16;
        color: #e2c96d;
        font-family: 'Courier New', monospace;
    }
    h1, h2, h3 {
        color: #ffdd88;
        text-shadow: 0 0 15px #bfae5e;
    }
    .stButton>button, .stCameraInput>div>button, .stFileUploader>div>button {
        background-color: #3c2e1f;
        color: #f1dc8e;
        border: 2px solid #a3873a;
        font-size: 18px;
        padding: 0.5em 1em;
        transition: all 0.3s;
    }
    .stButton>button:hover, .stCameraInput>div>button:hover {
        background-color: #6a522e;
        border-color: #ffe17d;
    }
    .stRadio label, .stSelectbox label, .stCheckbox label {
        color: #f5e3a1;
    }
    </style>
""", unsafe_allow_html=True)

text = " "

# 📜 Conjuro de traducción mágica
def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

# 🧹 Limpiar archivos antiguos
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if mp3_files:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)

st.title("📖 Grimorio del Texto Encantado")
st.subheader("Elige la fuente del pergamino: puedes usar el Ojo del Vidente (cámara) o subir una imagen sagrada.")

cam_ = st.checkbox("👁️ Usar Ojo del Vidente")

if cam_:
    img_file_buffer = st.camera_input("Invoca el Ojo del Vidente")
else:
    img_file_buffer = None

with st.sidebar:
    st.subheader("🔧 Encantamientos de Imagen")
    filtro = st.radio("Aplicar encantamiento visual", ('Sí', 'No'))

bg_image = st.file_uploader("🗂️ Cargar pergamino:", type=["png", "jpg"])
if bg_image is not None:
    uploaded_file = bg_image
    st.image(uploaded_file, caption='🖼️ Pergamino cargado.', use_column_width=True)

    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())

    img_cv = cv2.imread(uploaded_file.name)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.markdown("### 🧾 Escrituras Reveladas del Grimorio:")
    st.code(text)

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Sí':
        cv2_img = cv2.bitwise_not(cv2_img)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.markdown("### 🧾 Escrituras Reveladas del Hechizo Visual:")
    st.code(text)

with st.sidebar:
    st.subheader("🌍 Parámetros del Conjuro de Traducción")
    try:
        os.mkdir("temp")
    except:
        pass

    translator = Translator()

    in_lang = st.selectbox("Lenguaje del pergamino original", ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"))
    input_language = {"Inglés": "en", "Español": "es", "Bengali": "bn", "Coreano": "ko", "Mandarín": "zh-cn", "Japonés": "ja"}[in_lang]

    out_lang = st.selectbox("Lenguaje del encantamiento hablado", ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"))
    output_language = {"Inglés": "en", "Español": "es", "Bengali": "bn", "Coreano": "ko", "Mandarín": "zh-cn", "Japonés": "ja"}[out_lang]

    english_accent = st.selectbox("Tono del conjuro (acento)", ("Default", "India", "Reino Unido", "Estados Unidos", "Canadá", "Australia", "Irlanda", "Sudáfrica"))
    tld = {"Default": "com", "India": "co.in", "Reino Unido": "co.uk", "Estados Unidos": "com", "Canadá": "ca", "Australia": "com.au", "Irlanda": "ie", "Sudáfrica": "co.za"}[english_accent]

    display_output_text = st.checkbox("📜 Mostrar traducción escrita")

    if st.button("🗣️ Invocar hechizo de voz"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("### 🔊 Conjuro Recitado:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown("### 📖 Traducción Hechizada:")
            st.write(output_text)
