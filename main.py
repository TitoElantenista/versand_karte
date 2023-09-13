import streamlit as st
from PIL import Image
import folium
import base64
from io import BytesIO
import tempfile

def obtener_coordenadas(image_obj):
    exif_data = image_obj._getexif()
    gps_info = exif_data.get(34853, None)
    if gps_info:
        lat = gps_info.get(2, None)
        lon = gps_info.get(4, None)
        if lat and lon:
            lat_val = lat[0] + lat[1] / 60.0 + lat[2] / 3600.0
            lon_val = lon[0] + lon[1] / 60.0 + lon[2] / 3600.0
            if gps_info.get(1) == 'S':
                lat_val = -lat_val
            if gps_info.get(3) == 'W':
                lon_val = -lon_val
            return lat_val, lon_val
    return None

def obtener_orientacion(image_obj):
    exif_data = image_obj._getexif()
    if 34853 in exif_data:
        gps_info = exif_data[34853]
        return gps_info.get(17, None)
    return None

def encode_image_to_base64(image_io):
    """Codificar la imagen en base64 desde un objeto IO."""
    return base64.b64encode(image_io.getvalue()).decode()

def apply_exif_orientation(image):
    orientation_tag = 274
    if not hasattr(image, '_getexif') or image._getexif() is None:
        return image
    exif = dict(image._getexif().items())
    orientation = exif.get(orientation_tag, 1)
    if orientation == 2:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation == 3:
        image = image.rotate(180)
    elif orientation == 4:
        image = image.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation == 5:
        image = image.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation == 6:
        image = image.rotate(-90, expand=True)
    elif orientation == 7:
        image = image.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation == 8:
        image = image.rotate(90, expand=True)
    return image

def create_thumbnail(image_obj, base_width=300):
    img = apply_exif_orientation(image_obj)
    w_percent = base_width / float(img.size[0])
    h_size = int(float(img.size[1]) * float(w_percent))
    img = img.resize((base_width, h_size), Image.LANCZOS)
    thumbnail_io = BytesIO()
    img.save(thumbnail_io, format="JPEG")
    thumbnail_io.seek(0)
    return thumbnail_io

def main():
    st.title("Karten-Generator für Fotos mit Koordinaten")
    uploaded_files = st.file_uploader("Laden Sie Ihre Fotos hoch", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

    if uploaded_files:
        optionen = {
            "280 (empfohlen für Handys)": 280,
            "400 (empfohlen für Tablets)": 400,
            "600 (empfohlen für Computer)": 600
        }
        thumbnail_groesse = st.selectbox("Wählen Sie die Thumbnail-Größe:", list(optionen.keys()))

        if st.button("Karte erstellen"):
            coordenadas_nombres = []

            for uploaded_file in uploaded_files:
                image_obj = Image.open(uploaded_file)
                coordenadas = obtener_coordenadas(image_obj)
                if coordenadas:
                    coordenadas_nombres.append((coordenadas, uploaded_file.name))

            lat_promedio = sum(coord[0] for coord, _ in coordenadas_nombres) / len(coordenadas_nombres)
            lon_promedio = sum(coord[1] for coord, _ in coordenadas_nombres) / len(coordenadas_nombres)
            centro = (lat_promedio, lon_promedio)
            m = folium.Map(location=centro, zoom_start=17)

            for coord, foto_nombre in coordenadas_nombres:
                image_obj = Image.open(uploaded_file)
                thumbnail_io = create_thumbnail(image_obj)
                encoded_image = encode_image_to_base64(thumbnail_io)
                popup_content = f'<p>{foto_nombre}</p><img src="data:image/jpeg;base64,{encoded_image}" width="300">'
                popup = folium.Popup(popup_content, max_width=400)
                folium.Marker(coord, popup=popup).add_to(m)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
                m.save(temp_file.name)
                temp_html_path = temp_file.name

            with open(temp_html_path, "rb") as f:
                bytes_html = f.read()
                b64_html = base64.b64encode(bytes_html).decode()
                href = f'<a download="mapa_fotos.html" href="data:text/html;base64,{b64_html}">Download Map</a>'
                st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
