import streamlit as st
#import geemap
import geemap.foliumap as geemap
import ee
import os
import json


'''
# Lee las credenciales del archivo JSON LOCALMENTE
ruta_archivo = "C:/Users/etengler/Downloads/ee-dig-aplicaciones-774222ef12fc.json"
with open(ruta_archivo, 'r') as archivo_json:
    credenciales = json.load(archivo_json)

# Autenticación usando las credenciales en formato JSON
credentials = ee.ServiceAccountCredentials(credenciales['client_email'], ruta_archivo)
#ee.Initialize(credentials)

try:
    ee.Initialize(credentials)
    st.write("Earth Engine se ha inicializado correctamente")
except:
    st.error("Error inicializando Earth Engine")

'''
# Cargar las credenciales directamente (sólo para pruebas)
gcp_service_account = os.getenv("GCP_SERVICE_ACCOUNT")
if gcp_service_account:
    credenciales = json.loads(gcp_service_account)
    credentials = ee.ServiceAccountCredentials(credenciales['client_email'], credenciales['private_key'])
    ee.Initialize(credentials)
else:
    st.error("No se pudo acceder a las credenciales de Google Cloud.")

st.write(gcp_service_account)


markdown = """
Aplicaciones web desarrolladas en la Dirección de Información Geoespacial del IGN
"""
logo = "LogoIgn.png"

st.title("Agua-Tierra App")
st.markdown("Esta aplicación permite...")
user_input = st.text_input("Escriba aqui el nombre del proyecto GEE...")

st.sidebar.title("Detección Agua-Tierra")
st.sidebar.info(markdown)

#ee.Authenticate()
#ee.Initialize(project='ee-dig-aplicaciones')

Map = geemap.Map(center=(-40, -64), zoom=4) #crear el mapa inetrcativo con coordenadas especificas
Map.add_basemap('HYBRID')
#st.write(Map)

Map.to_streamlit(height=700)
#st.map(Map)