import os
import streamlit as st
import base64
from openai import OpenAI
import openai
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_drawable_canvas import st_canvas

Expert=" "
profile_imgenh=" "
    
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."


# ⚠️ IMPORTANTE: esto ayuda a forzar cambios visuales
st.set_page_config(page_title='Lienzo IA PRO', layout="wide")

# 🔥 CSS QUE SÍ FUNCIONA EN STREAMLIT
st.markdown("""
<style>
html, body, [class*="css"] {
    background: linear-gradient(135deg, #0f172a, #4c1d95, #7e22ce) !important;
    color: white !important;
}

/* Título */
.titulo-grande {
    font-size: 40px;
    text-align: center;
    font-weight: bold;
    margin-bottom: 10px;
}

/* Subtexto */
.subtexto {
    text-align: center;
    font-size: 18px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# 🔥 TÍTULO FORZADO
st.markdown('<div class="titulo-grande">🎨 Lienzo Inteligente IA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtexto">Dibuja algo y deja que la IA lo interprete</div>', unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Configuración")
    st.write("Ajusta tu lápiz")

# CONFIGURACIÓN
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Grosor del lápiz', 1, 30, 6)

# 🔥 COLOR FUNCIONAL
color = st.sidebar.selectbox("Color del lápiz", ["Blanco", "Morado"])

if color == "Blanco":
    stroke_color = "#FFFFFF"
else:
    stroke_color = "#9b5de5"  # morado más visible

# 🔥 FONDO DEL CANVAS
bg_color = "#000000"

# 🔥 CANVAS MÁS GRANDE (AQUÍ ESTÁ EL CAMBIO REAL)
canvas_result = st_canvas(
    fill_color="rgba(255,255,255,0.1)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=550,   # más grande
    width=900,    # mucho más ancho
    drawing_mode=drawing_mode,
    key="canvas",
)

# API KEY
ke = st.text_input('Ingresa tu Clave')
os.environ['OPENAI_API_KEY'] = ke

api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)

analyze_button = st.button("🔍 Analizar dibujo")

# 🔒 LÓGICA ORIGINAL (NO TOCADA)
if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Analizando ..."):
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'),'RGBA')
        input_image.save('img.png')
        
        base64_image = encode_image_to_base64("img.png")
            
        prompt_text = (f"Describe in spanish briefly the image")
    
        try:
            full_response = ""
            message_placeholder = st.empty()
            response = openai.chat.completions.create(
              model="gpt-4o-mini",
              messages=[
                {
                   "role": "user",
                   "content": [
                     {"type": "text", "text": prompt_text},
                     {
                       "type": "image_url",
                       "image_url": {
                         "url": f"data:image/png;base64,{base64_image}",
                       },
                     },
                   ],
                  }
                ],
              max_tokens=500,
              )

            if response.choices[0].message.content is not None:
                full_response += response.choices[0].message.content
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

            if Expert== profile_imgenh:
               st.session_state.mi_respuesta= response.choices[0].message.content
    
        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    if not api_key:
        st.warning("Por favor ingresa tu API key.")
