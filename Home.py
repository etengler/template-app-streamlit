import streamlit as st

st.set_page_config(layout="wide")

markdown = """
Aplicaciones web desarrolladas en la Dirección de Información Geoespacial del IGN
"""
logo = "LogoIgn.png"

st.sidebar.image(logo)
st.title("Agua-Tierra App")
st.sidebar.title("Aplicaciones web:  DIG - IGN")
st.sidebar.info(markdown)

# Customize page title
st.title("Aplicaciones web DIG - IGN")

st.markdown(
    """
    Aplicaciones web desarrolladas en el departamento de Ciencia de Datos Geoespaciales de la Dirección de Información Geoespacial del IGN.
    """
)

st.header("Instrucciones")

markdown = """
1. For the [GitHub repository](https://github.com/opengeos/streamlit-map-template) or [use it as a template](https://github.com/opengeos/streamlit-map-template/generate) for your own project.
2. Customize the sidebar by changing the sidebar text and logo in each Python files.
3. Find your favorite emoji from https://emojipedia.org.
4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.

"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)


