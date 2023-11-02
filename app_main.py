# Importación de librerías
import streamlit as st

# Función para definir espacios en la app de streamlit (en la barra lateral)
def space_sidebar(num_lines=1):
    """Función para añadir espacios para la app de streamlit"""
    for _ in range(num_lines):
        st.sidebar.write("")

# Importación de aplicaciones
import app_exploracion
import app_prediccion


# Icono de aplicación
icono = "https://s.tcdn.co/5d5/c45/5d5c458f-3e3c-344c-aa5a-75ed839162ae/1.png"

# Configuración de la página (icono, usar toda la página, nombre)
st.set_page_config(
    layout = "wide", 
    page_icon = icono, 
    page_title = "App - Predicción valores bursátiles"
    )

# Páginas de la app
PAGES = {
    "Exploración de valores bursátiles.": app_exploracion,
    "Predicciones con Prophet.": app_prediccion
}

# Imágenes para sidebar
imagen_ws = """
<center><img src="https://s.tcdn.co/5d5/c45/5d5c458f-3e3c-344c-aa5a-75ed839162ae/1.png" style="width:200px;height:200px;"><center>
"""

imagen_ld = """
<center><img src="https://d1zlsjfa8g4s5.cloudfront.net/wp-content/uploads/2015/04/Icon-OptimisePM-WoB-220px.png" style="width:200px;height:310px;"><center>
"""

# Texto y páginas en la sidebar
st.sidebar.markdown("<i><b><u><center><font face='WildWest' size='5' >Exploración y predicción de cotizaciones bursátiles</font><br /></center></u></b></i>", unsafe_allow_html=True)
space_sidebar()
selection = st.sidebar.radio("Ir a:", list(PAGES.keys()))
page = PAGES[selection]
space_sidebar(20)
st.sidebar.markdown(imagen_ws, unsafe_allow_html=True)  
page.app()