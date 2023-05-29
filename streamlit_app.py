import streamlit as st
import random as rnd
import simpy

# Barra lateral
with st.sidebar:
    st.header("Descripción")
    st.markdown(
        """
    - Cumplimenta con las distintas consignas y requisitos impuestos por las guías prácticas de '45: Modelos y Simulación de Sistemas'
    - Permite la operación paramétrica de una simulación de sistema de colas
    - Año 2023
    """
    )
    
    st.header("Académico")
    st.markdown(
        """
    - Universidad Nacional de La Rioja
    - Departamento Académico de Ciencias Exactas, Físicas y Naturales
    - Ingeniería en Sistemas de Información
    - 45: Modelos y Simulación de Sistemas
    """
    )
    
    st.header("Nosotros")
    st.markdown(
        """
    - Cano Angel Rodrigo | EISI-821
    - Dominguez Sotomayor Santiago Ismael | EISI-782
    - Rios Lopez Ramiro Ignacio | EISI-801    
    """
    )

    st.header("Herramientas utilizadas")
    st.markdown(
        """
    - Python
    - Streamlit
    - SimPy
    """
    )

# Parámetros
st.image("https://em-content.zobj.net/thumbs/120/apple/354/level-slider_1f39a-fe0f.png")
