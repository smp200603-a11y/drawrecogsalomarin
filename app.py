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


# Streamlit 
st.set_page_config(page_title='Tablero Inteligente', layout="wide")

st.markdown("<h1 style='text-align:center;'>🎨 Lienzo Inteligente IA</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Acerca de:")
    st.subheader("La IA interpreta tu dibujo")

st.subheader("Dibuja y analiza tu boceto")

drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)

# colores
color = st.sidebar.selectbox("Color del lápiz", ["Blanco", "Morado"])
stroke_color = "#FFFFFF" if color == "Blanco" else "#8000FF"

fondo = st.sidebar.selectbox("Fondo", ["Blanco", "Negro"])
bg_color = "#FFFFFF" if fondo == "Blanco" else "#000000"

# canvas grande
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0.1)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=500,
    width=800,
    drawing_mode=drawing_mode,
    key="canvas",
)

ke = st.text_input('Ingresa tu Clave')
os.environ['OPENAI_API_KEY'] = ke

api_key = os.environ['OPENAI_API_KEY']

analyze_button = st.button("Analiza la imagen")

# 🔥 MISMA LÓGICA ORIGINAL (solo fix imagen)
if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Analizando ..."):
        
        input_numpy_array = np.array(canvas_result.image_data)

        # ✅ FIX: quitar transparencia (esto era el problema real)
        image_rgb = input_numpy_array[:, :, :3]
        input_image = Image.fromarray(image_rgb.astype('uint8'), 'RGB')
        input_image.save('img.png')
        
        base64_image = encode_image_to_base64("img.png")
            
        prompt_text = "Describe en español brevemente el dibujo"
    
        try:
            full_response = ""
            message_placeholder = st.empty()

            # ✅ EXACTAMENTE COMO TU ORIGINAL (esto sí funcionaba)
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
              max_tokens=300,
            )

            if response.choices[0].message.content is not None:
                full_response += response.choices[0].message.content
                message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Error: {e}")

else:
    if not api_key:
        st.warning("Por favor ingresa tu API key.")
