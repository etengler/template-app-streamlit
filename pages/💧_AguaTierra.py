import streamlit as st
#import geemap
import geemap.foliumap as geemap
import geemap.colormaps as cm
import ee
import os
import json
import datetime
#import leafmap.foliumap as leafmap

import folium
from shapely.geometry import Polygon
import warnings
import fiona
import geopandas as gpd


st.set_page_config(layout="wide")


#ee.Authenticate()
#ee.Initialize(project='ACA_VA_EL_NOMBRE_DEL_PROYECTO') #ESTA LINEA SE DEBE MODIFICAR
#ee.Initialize(project='ee-dig-aplicaciones') 




# Acceder a la clave del servicio desde los secretos
gcp_service_account = os.getenv('GCP_SERVICE_ACCOUNT')

if gcp_service_account:
    try:
        credentials = json.loads(gcp_service_account)
        ee.Initialize(credentials)
    except json.JSONDecodeError as e:
        st.error(f"Error al decodificar el JSON: {e}")
        st.error(f"Contenido de gcp_service_account: {gcp_service_account}")
else:
    st.error("No se pudo encontrar la clave del servicio. Asegúrate de que esté configurada correctamente.")






logo = "LogoIgn.png"
markdown = """
Aplicaciones web desarrolladas en la Dirección de Información Geoespacial del IGN
"""
st.sidebar.title("Detección Agua-Tierra")
st.sidebar.info(markdown)


st.title("Aplicación Agua-Tierra")
st.markdown("Esta aplicación permite...")
#user_input = st.text_input("Escriba aqui el nombre del proyecto GEE...")



  

#ee.Authenticate()
#ee.Initialize(project='ee-dig-aplicaciones')


#GEEMAP
#Map = geemap.Map(center=(-40, -64), zoom=4) #crear el mapa inetrcativo con coordenadas especificas
#Map.add_basemap('HYBRID')
#Map.to_streamlit(height=700)

#LEAFMAP
#Map = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
#Map = leafmap.Map(draw_control=False)
#Map.add_basemap('HYBRID')


# FOLIUM
#Map = folium.Map(location=[-39.50287042904495, -60.60134429509489], zoom_start=4)

Map = geemap.Map(
            basemap="HYBRID",
            plugin_Draw=True,
            Draw_export=True,
            locate_control=True,
            plugin_LatLngPopup=False,
        )



#Map.st_draw_features()


data = st.file_uploader(
            "Upload a GeoJSON file to use as an ROI. Customize timelapse parameters and then click the Submit button 😇👇",
            type=["geojson", "kml", "zip"],
        )





col1, col2 = st.columns([5,2]) 
####################################################################################################### VARIABLES GLOBALES
global classified_b
global extencion

classified_b = None
extencion = None

geometria_seleccionada = None


global geometria_dibujada 
geometria_dibujada = None

# Crear un contenedor para guardar las geometrías
geometries = []

####################################################################################################### ETIQUETAS



####################################################################################################### RECURSOS
cartas = ee.FeatureCollection("projects/ee-dig-aplicaciones/assets/AguaTierra/Cartas_50000")
valoresCarac_ = cartas.aggregate_array("carac").distinct().getInfo()# Obtener los valores únicos de la columna "carac"
valoresCarac = [None] + valoresCarac_  # Crear una lista de valores, incluyendo una opción nula



####################################################################################################### 

with col2:
    #selected_value = st.sidebar.selectbox('Selecciona una carta: ', valoresCarac)
    #st.sidebar.date_input('Fecha inicial:', datetime.date(2023, 1, 1))
    #st.sidebar.date_input('Fecha final:')
    selected_value = st.selectbox('Selecciona una carta: ', valoresCarac)
    fecha_inicial = st.date_input('Fecha inicial:', datetime.date(2023, 1, 1))
    fecha_final = st.date_input('Fecha final:')

if selected_value is not None:  # Evitar el procesamiento si se selecciona la opción nula
    geometria_seleccionada = cartas.filter(ee.Filter.eq("carac", selected_value))
    Map.addLayer(geometria_seleccionada, {}, 'Geometría seleccionada')
    



####################################################################################################### FUNCIONES
def obtenerFecha():
    time_interval = None

    # Obtener las fechas seleccionadas
    fecha_inicio = fecha_inicial
    fecha_fin = fecha_final

    # Convertir las fechas al formato deseado ('YYYY-MM-DD')
    fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
    fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')

    # Convertir las fechas en objetos ee.Date
    fecha_inicio_ee = ee.Date(fecha_inicio_str)
    fecha_fin_ee = ee.Date(fecha_fin_str)

    # Calcular la diferencia en milisegundos
    diferencia = fecha_inicio_ee.difference(fecha_fin_ee, 'days')

    # Verificar si la diferencia es negativa
    if diferencia.getInfo() >= 0:
        #etiqueta_mensaje_clasif.value='La fecha final no puede ser mayor o igual que la fecha inicial'
        st.sidebar.write('La fecha final no puede ser mayor o igual que la fecha inicial')
        # Puedes manejar el error de la manera que desees, por ejemplo, mostrar un mensaje de error.
    else:
        # Utilizar las fechas convertidas en el parámetro time_interval
        time_interval = (fecha_inicio_ee, fecha_fin_ee)

        # Retornar el resultado
    return time_interval



@st.cache_data
def uploaded_file_to_gdf(data):
    import tempfile
    import os
    import uuid

    _, file_extension = os.path.splitext(data.name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(data.getbuffer())

    if file_path.lower().endswith(".kml"):
        fiona.drvsupport.supported_drivers["KML"] = "rw"
        gdf = gpd.read_file(file_path, driver="KML")
    else:
        gdf = gpd.read_file(file_path)

    return gdf


if data:
    gdf = uploaded_file_to_gdf(data)
    try:
        st.session_state["roi"] = geemap.gdf_to_ee(gdf, geodesic=False)
        Map.add_gdf(gdf, "ROI")
    except Exception as e:
        st.error(e)
        st.error("Please draw another ROI and try again.")
    #Map.add_gdf(gdf, "ROI")
    
       
with col1:
    Map.to_streamlit()
    
 
 


