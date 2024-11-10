import streamlit as st
import requests
from io import BytesIO
from zipfile import ZipFile
from PIL import Image

API_URL = "https://string-art-api.azurewebsites.net/processimage"

st.title("String Art Image Generator")
st.write("Upload an image, select the size, and generate string art coordinates.")

# Subir la imagen
uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

# Mostrar vista previa de la imagen cargada
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image Preview", use_container_width=True)

# Configurar el tamaño con un slider
size = st.slider("Select Image Size", min_value=3, max_value=90, value=20)

# Procesar la imagen al hacer clic en el botón
if uploaded_file and st.button("Generate"):
    files = {'image': ('image.png', uploaded_file, 'image/png')}
    data = {'size': str(size)}

    with st.spinner("Processing..."):
        response = requests.post(API_URL, files=files, data=data)

        if response.status_code == 200 and 'application/zip' in response.headers.get('Content-Type', ''):
            zip_buffer = BytesIO(response.content)
            with ZipFile(zip_buffer, 'r') as zip_file:
                processed_image_data = zip_file.read('processed_image.png')
                coordinates_data = zip_file.read('coordinates.csv')

            # Mostrar la imagen procesada
            st.image(Image.open(BytesIO(processed_image_data)), caption="Processed Image", use_container_width=True)

            # Descargar el archivo CSV
            st.download_button(
                label="Download Coordinates CSV",
                data=coordinates_data,
                file_name="coordinates.csv",
                mime="text/csv"
            )
        else:
            st.error("Error processing image. Please try again.")