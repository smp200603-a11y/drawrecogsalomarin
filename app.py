import os
import streamlit as st
import base64
from openai import OpenAI
import tensorflow as tf
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_drawable_canvas import st_canvas

Expert=" "
profile_imgenh=" "
    
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except:
        return None


# CONFIG
st.set_page_config(page_title='Tablero Inteligente', layout="wide")

st.title('🎨 Lienzo Inteligente IA')

with st.sidebar:
    st.subheader("Acerca de:")
    st.subheader("La IA interpreta tu dibujo")

st.subheader("Dibuja el boceto y presiona el botón para analizarlo")

# DIBUJO
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)

color = st.sidebar.selectbox("Color del lápiz", ["Negro", "Morado", "Blanco"])
if color == "Negro":
    stroke_color = "#000000"
elif color == "Morado":
    stroke_color = "#8000FF"
else:
    stroke_color = "#FFFFFF"

fondo = st.sidebar.selectbox("Fondo", ["Blanco", "Negro"])
bg_color = "#FFFFFF" if fondo == "Blanco" else "#000000"

# CANVAS GRANDE
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

# API
ke = st.text_input('Ingresa tu Clave', type="password")
os.environ['OPENAI_API_KEY'] = ke

client = OpenAI(api_key=ke)

# BOTÓN
analyze_button = st.button("🔍 Analizar dibujo")

# ANÁLISIS
if canvas_result.image_data is not None and ke and analyze_button:

    with st.spinner("Analizando ..."):

        try:
            # 🔥 FIX IMPORTANTE (imagen correcta)
            img_array = np.array(canvas_result.image_data)
            img_rgb = img_array[:, :, :3]
            image = Image.fromarray(img_rgb.astype('uint8'), 'RGB')
            image.save("img.png")

            base64_image = encode_image_to_base64("img.png")

            prompt_text = "¿Qué es este dibujo? Responde en una frase corta en español."

            response = client.chat.completions.create(
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
                max_tokens=200,
            )

            resultado = response.choices[0].message.content

            st.success("Resultado:")
            st.write(resultado)

        except Exception as e:
            st.error(f"Error real: {e}")

else:
    if not ke:
        st.warning("Por favor ingresa tu API key.")
