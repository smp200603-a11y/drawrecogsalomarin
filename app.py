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


st.set_page_config(page_title='Lienzo IA Creativo', layout="wide")

st.markdown("""
<style>
html, body, [class*="css"] {
    background: linear-gradient(135deg, #0f172a, #4c1d95, #7e22ce) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🎨 Lienzo Inteligente IA</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Configuración del lienzo")

st.subheader("Dibuja tu boceto y deja que la IA lo interprete")

drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Grosor del lápiz', 1, 30, 5)

color = st.sidebar.selectbox("Color del lápiz", ["Blanco", "Morado"])

if color == "Blanco":
    stroke_color = "#FFFFFF"
else:
    stroke_color = "#8000FF"

fondo = st.sidebar.selectbox("Fondo del lienzo", ["Blanco", "Negro"])

if fondo == "Blanco":
    bg_color = "#FFFFFF"
else:
    bg_color = "#000000"

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
client = OpenAI(api_key=api_key)

analyze_button = st.button("🔍 Analizar dibujo")

# 🔥 AQUÍ ESTÁ EL FIX IMPORTANTE
if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Analizando ..."):
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'),'RGBA')
        input_image.save('img.png')
        
        base64_image = encode_image_to_base64("img.png")
            
        prompt_text = "Describe en español brevemente el dibujo"
    
        try:
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
            st.error(f"Error: {e}")

else:
    if not api_key:
        st.warning("Por favor ingresa tu API key.")
