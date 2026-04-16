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


# CONFIGURACIÓN
st.set_page_config(page_title='✨ Lienzo Mágico IA', layout="wide")

# FONDO BONITO (SIN IMÁGENES)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1e2f, #3a0ca3, #7209b7);
        color: white;
    }
    h1, h2, h3 {
        color: #ffffff;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# TÍTULO NUEVO
st.title('✨ Lienzo Mágico IA: Dibuja y Descubre')

with st.sidebar:
    st.subheader("Acerca de:")
    st.subheader("Dibuja algo y deja que la IA intente interpretarlo 👀")

st.subheader("Dibuja tu idea en el lienzo y presiona el botón para analizarla")

# CONFIGURACIÓN DEL DIBUJO
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 8)

# NUEVO: selector de color (blanco o morado)
color_opcion = st.sidebar.selectbox(
    "Color del lápiz",
    ["Blanco", "Morado"]
)

if color_opcion == "Blanco":
    stroke_color = "#FFFFFF"
else:
    stroke_color = "#8000FF"

# Fondo ahora blanco (como pediste)
bg_color = '#FFFFFF'

# CANVAS MÁS GRANDE
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0.1)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=500,   # antes 300
    width=700,    # antes 400
    drawing_mode=drawing_mode,
    key="canvas",
)

ke = st.text_input('Ingresa tu Clave')
os.environ['OPENAI_API_KEY'] = ke

api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)

analyze_button = st.button("🔍 Analizar dibujo", type="secondary")

if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Analizando tu obra maestra..."):
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'),'RGBA')
        input_image.save('img.png')
        
        base64_image = encode_image_to_base64("img.png")
            
        prompt_text = (f"Describe en español brevemente el dibujo")
    
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
