import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# 🎨 Estética Mágica Medieval
st.markdown("""
    <style>
    .stApp {
        background-color: #1e1b14;
        color: #e3c565;
        font-family: 'Courier New', monospace;
    }
    h1, h2, h3 {
        color: #f9d423;
        text-shadow: 0 0 10px #c0a300;
    }
    .stButton>button, .stCameraInput>div>button {
        background-color: #3c2f1f;
        color: #f9e6a1;
        border: 2px solid #bfa14d;
        padding: 0.5em 1em;
        font-size: 18px;
        transition: 0.3s;
    }
    .stButton>button:hover, .stCameraInput>div>button:hover {
        background-color: #6e552e;
        border-color: #ffdd57;
    }
    .stRadio label {
        color: #e8c872;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📜 Hechizo de Revelación de Escrituras")
st.markdown("**Usa tu dispositivo mágico para capturar un pergamino y revelar el mensaje oculto...**")

img_file_buffer = st.camera_input("📸 Invoca el Ojo de Visión (Cámara)")

with st.sidebar:
    filtro = st.radio("🧪 ¿Aplicar encantamiento visual?", ('✨ Activar Filtro Mágico', '🚫 Sin Encantamiento'))

if img_file_buffer is not None:
    st.markdown("🔮 Procesando imagen mágica...")

    # Leer la imagen
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == '✨ Activar Filtro Mágico':
        cv2_img = cv2.bitwise_not(cv2_img)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)

    st.markdown("### 📖 Escrituras Reveladas:")
    st.code(text, language='markdown')
