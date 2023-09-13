import streamlit as st
from PIL import Image
import folium
import base64
import tempfile


def obtener_coordenadas(foto_path):
    with Image.open(foto_path) as img:
        exif_data = img._getexif()
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


def obtener_orientacion(foto_path):
    with Image.open(foto_path) as img:
        exif_data = img._getexif()
        if 34853 in exif_data:
            gps_info = exif_data[34853]
            return gps_info.get(17, None)  # 17 es el tag para GPSImgDirection
    return None




def encode_image_to_base64(image_path):
    """Codificar la imagen en base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def apply_exif_orientation(image):
    """
    Ajustar la imagen de acuerdo a la orientación EXIF, si está presente.
    """
    orientation_tag = 274  # Código del tag de orientación EXIF
   
    # No hacer nada si no hay datos EXIF
    if not hasattr(image, '_getexif') or image._getexif() is None:
        return image
   
    exif = dict(image._getexif().items())
    orientation = exif.get(orientation_tag, 1)
   
    # Ajustar la imagen según la orientación
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


def create_thumbnail(image_path, folder_path, base_width=300):
    """Crear y guardar una versión en miniatura de la imagen."""
    img = Image.open(image_path)
    img = apply_exif_orientation(img)
   
    w_percent = base_width / float(img.size[0])
    h_size = int(float(img.size[1]) * float(w_percent))
    img = img.resize((base_width, h_size), Image.LANCZOS)
   
    temp_dir = os.path.join(folder_path, "temp_thumbnails")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
   
    thumbnail_filename = "temp_thumbnail.jpg"
    thumbnail_path = os.path.join(temp_dir, thumbnail_filename)
    img.save(thumbnail_path)
   
    return thumbnail_path




# Streamlit App
def main():
    st.title("Karten-Generator für Fotos mit Koordinaten")

    uploaded_files = st.file_uploader("Laden Sie Ihre Fotos hoch", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

    if uploaded_files:
        # Solicitar al usuario que seleccione la carpeta con las fotos
        optionen = {
            "280 (empfohlen für Handys)": 280,
            "400 (empfohlen für Tablets)": 400,
            "600 (empfohlen für Computer)": 600
        }
        thumbnail_groesse = st.selectbox("Wählen Sie die Thumbnail-Größe:", list(optionen.keys()))

        if st.button("Karte erstellen"):
            # Proceso principal
            coordenadas_nombres = []

            for uploaded_file in uploaded_files:
                # Usar un objeto temporal para obtener la ruta del archivo
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    foto_path = temp_file.name
                    coordenadas = obtener_coordenadas(foto_path)
                    if coordenadas:
                        coordenadas_nombres.append((coordenadas, uploaded_file.name))


                # Calcular el centro promedio de las coordenadas
                lat_promedio = sum(coord[0] for coord, _ in coordenadas_nombres) / len(coordenadas_nombres)
                lon_promedio = sum(coord[1] for coord, _ in coordenadas_nombres) / len(coordenadas_nombres)
                centro = (lat_promedio, lon_promedio)


                # Creamos un mapa centrado en el promedio de las coordenadas con un zoom inicial
                m = folium.Map(location=centro, zoom_start=17)


                # Agregamos los marcadores al mapa con el nombre de la foto y una vista preliminar de la foto como popup
                for coord, foto_nombre in coordenadas_nombres:
                    foto_path = os.path.join(folder_path, foto_nombre)
                   
                    # Creamos una miniatura y la codificamos en base64
                    thumbnail_path = create_thumbnail(foto_path, folder_path)


                    encoded_image = encode_image_to_base64(thumbnail_path)
                   
                    # Extraer la orientación y usarla para agregar un icono de dirección
                    orientacion = obtener_orientacion(foto_path)
                    if orientacion:
                        icon = folium.CustomIcon(icon_image='path_a_icono_de_flecha.png', angle=orientacion)
                        folium.Marker(coord, icon=icon).add_to(m)
                   
                    popup_content = f'<p>{foto_nombre}</p><img src="data:image/jpeg;base64,{encoded_image}" width="300">'
                    popup = folium.Popup(popup_content, max_width=400)
                    folium.Marker(coord, popup=popup).add_to(m)


            # Guardar el mapa en un archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
                m.save(temp_file.name)
                temp_html_path = temp_file.name

            # Proporcionar un enlace de descarga
            with open(temp_html_path, "rb") as f:
                bytes_html = f.read()
                b64_html = base64.b64encode(bytes_html).decode()
                href = f'<a download="mapa_fotos.html" href="data:text/html;base64,{b64_html}">Download Map</a>'
                st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

