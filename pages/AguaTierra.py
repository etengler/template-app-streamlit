import streamlit as st
import geemap

markdown = """
Aplicaciones web desarrolladas en la Dirección de Información Geoespacial del IGN
"""
logo = "LogoIgn.png"

st.sidebar.image(logo)
st.sidebar.title("Aplicaciones web:  DIG - IGN")
st.sidebar.info(markdown)

st.title("Agua-Tierra App")
st.markdown("Esta aplicación permite...")

user_input = st.text_input("Escriba aqui el nombre del proyecto GEE...")


