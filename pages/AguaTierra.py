import streamlit as st
import geemap
import ee

markdown = """
Aplicaciones web desarrolladas en la Dirección de Información Geoespacial del IGN
"""
logo = "LogoIgn.png"

st.title("Agua-Tierra App")
st.markdown("Esta aplicación permite...")
user_input = st.text_input("Escriba aqui el nombre del proyecto GEE...")

st.sidebar.title("Detección Agua-Tierra")
st.sidebar.info(markdown)

ee.Authenticate()
ee.Initialize(project='ee-dig-aplicaciones')

Map = geemap.Map(center=(-40, -64), zoom=4) #crear el mapa inetrcativo con coordenadas especificas
Map.add_basemap('HYBRID')
Map.to_streamlit(height=700)
