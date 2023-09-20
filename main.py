import streamlit as st
from PIL import Image
import folium
import base64
from io import BytesIO
import tempfile
import streamlit_folium
import folium.plugins
from folium.plugins import PolyLineTextPath
from geopy.distance import geodesic
from folium.plugins import MiniMap
from folium.plugins import MousePosition
from folium.plugins import AntPath

def obtener_coordenadas(image_obj):
    exif_data = image_obj._getexif()
    if not exif_data:
        return None
   
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




def primeros_dos_puntos_distantes(coords, min_dist=20):
    """
    Devuelve los dos primeros puntos que estén al menos a 'min_dist' metros de distancia entre sí.
    """
    if len(coords) < 2:
        return coords




    punto_inicial = coords[0]
    for punto in coords[1:]:
        if geodesic(punto_inicial, punto).meters >= min_dist:
            return [punto_inicial, punto]




    return [punto_inicial]




def obtener_fecha_hora(image_obj):
    exif_data = image_obj._getexif()
    if 36867 in exif_data:
        return exif_data[36867]
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




def generar_mapa(coordenadas_nombres, comentarios, optionen, thumbnail_groesse, centro, uploaded_files, foto_destacada=None):
    m = folium.Map(location=centro, zoom_start=17)
    minimap = MiniMap(fixedZoom=True, zoomLevelFixed=12)
    m.add_child(minimap)


    MousePosition().add_to(m)
    # Creamos un MarkerCluster
    marker_cluster = folium.plugins.MarkerCluster().add_to(m)
   
    # Ordenar las fotos por fecha y hora
    coordenadas_nombres_fecha = []
    for coord, foto_nombre in coordenadas_nombres:
        for u_file in uploaded_files:
            if u_file.name == foto_nombre:
                fecha_hora = obtener_fecha_hora(Image.open(u_file))
                coordenadas_nombres_fecha.append((coord, foto_nombre, fecha_hora))
                break
    coordenadas_nombres_fecha.sort(key=lambda x: x[2])  # Ordenar por fecha y hora
   
    for coord, foto_nombre, _ in coordenadas_nombres_fecha:
        for u_file in uploaded_files:
            if u_file.name == foto_nombre:
                image_obj = Image.open(u_file)
                thumbnail_io = create_thumbnail(image_obj, optionen[thumbnail_groesse])
                encoded_image = encode_image_to_base64(thumbnail_io)
                comentario_usuario = comentarios.get(foto_nombre, "")
               
                # Aquí agregamos la fecha y hora al contenido emergente
                popup_content = f'<p>{foto_nombre}</p>'
                fecha_hora = obtener_fecha_hora(image_obj)
                if fecha_hora:
                    popup_content += f'<p>Datum und Uhrzeit: {fecha_hora}</p>'
                popup_content += f'<p>{comentario_usuario}</p><img src="data:image/jpeg;base64,{encoded_image}" width="280">'
               
                # Cambia el color del marcador si es la foto destacada
                if foto_nombre == foto_destacada:
                    marker_color = "red"
                elif comentario_usuario:  # Si tiene comentario, color negro
                    marker_color = "black"
                else:
                    marker_color = "blue"




                folium.Marker(coord, popup=popup_content, icon=folium.Icon(icon="circle", color=marker_color)).add_to(marker_cluster)
                break
   
    # Dibujar una polilínea en el mapa
    coords_linea = [coord for coord, _, _ in coordenadas_nombres_fecha]
    AntPath(coords_linea, color="blue", weight=2.5, opacity=0.7, delay=1000).add_to(m)  # 1000 milisegundos es igual a 1 segundo
   
    return m


def main():
    st.title("Karten-Generator für Fotos mit Koordinaten")
    st.markdown("""---""")
    if 'uploaded_images' not in st.session_state:
        st.session_state.uploaded_images = []
   
    new_uploaded_files = st.file_uploader("Laden Sie Ihre Fotos hoch...", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    if new_uploaded_files:
        current_file_names = [f.name for f in st.session_state.uploaded_images]
        for file in new_uploaded_files:
            if file.name not in current_file_names:
                st.session_state.uploaded_images.append(file)




    if st.session_state.uploaded_images:
        optionen = {
            "280 (empfohlen für Handys)": 280,
            "400 (empfohlen für Tablets)": 400,
            "600 (empfohlen für Computer)": 600
        }
        thumbnail_groesse = st.selectbox("Wählen Sie die Thumbnail-Größe:", list(optionen.keys()))




        coordenadas_nombres = []
        fotos_ignoradas = 0
        comentarios = {}




        # Inicializar st.session_state.comentarios si aún no existe
        if 'comentarios' not in st.session_state:
            st.session_state.comentarios = {}
        # Usa el estado guardado para inicializar 'comentarios'
        comentarios = st.session_state.comentarios
        for uploaded_file in st.session_state.uploaded_images:
            image_obj = Image.open(uploaded_file)
            coordenadas = obtener_coordenadas(image_obj)
            if coordenadas:
                coordenadas_nombres.append((coordenadas, uploaded_file.name))
               
                # Si la foto no tiene un comentario en session_state, asignarle un valor vacío.
                if uploaded_file.name not in st.session_state.comentarios:
                    comentarios[uploaded_file.name] = ""
            else:
                fotos_ignoradas += 1


        if not coordenadas_nombres:
            st.error("Kein hochgeladenes Foto enthält GPS-Koordinaten.")
            return




        lat_promedio = sum(coord[0] for coord, _ in coordenadas_nombres) / len(coordenadas_nombres)
        lon_promedio = sum(coord[1] for coord, _ in coordenadas_nombres) / len(coordenadas_nombres)
        centro = (lat_promedio, lon_promedio)




        foto_seleccionada = st.selectbox("Seleccione una foto para agregar un comentario:", [nombre for _, nombre in coordenadas_nombres])
        comentario = st.text_area(f"Comentario para {foto_seleccionada}", value=comentarios[foto_seleccionada])




        # Reserva un espacio para el mapa
        mapa_placeholder = st.empty()
        boton_presionado = False




        if st.button("Agregar comentario"):
            st.session_state.comentarios[foto_seleccionada] = comentario
            comentarios[foto_seleccionada] = comentario
           
            boton_presionado = True
            m = generar_mapa(coordenadas_nombres, comentarios, optionen, thumbnail_groesse, centro, st.session_state.uploaded_images, foto_seleccionada)
            mapa_placeholder.empty()
            streamlit_folium.folium_static(m)




        if not boton_presionado:
            m = generar_mapa(coordenadas_nombres, comentarios, optionen, thumbnail_groesse, centro, st.session_state.uploaded_images, foto_seleccionada)
            streamlit_folium.folium_static(m)
        if st.button("Karte herunterladen"):
            m = generar_mapa(coordenadas_nombres, comentarios, optionen, thumbnail_groesse, centro, st.session_state.uploaded_images)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
                m.save(temp_file.name)
                temp_html_path = temp_file.name




            with open(temp_html_path, "rb") as f:
                bytes_html = f.read()
                b64_html = base64.b64encode(bytes_html).decode()
                href = f'<a download="mapa_fotos.html" href="data:text/html;base64,{b64_html}">Karte herunterladen</a>'
                st.markdown(href, unsafe_allow_html=True)
           
            st.info(f"{len(coordenadas_nombres)} Fotos mit Koordinaten verarbeitet. {fotos_ignoradas} Fotos wurden aufgrund fehlender Koordinaten ignoriert.")




if __name__ == "__main__":
    main()
