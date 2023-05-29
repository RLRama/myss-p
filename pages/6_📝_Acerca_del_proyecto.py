import streamlit as st
import random as rnd
import simpy as sp
import numpy as np
import pandas as pd

# Configurar página
st.set_page_config(
    page_title="Información",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "MySS - 2023 - UNLaR"
    }
)

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
    - Pandas
    - NumPy
    """
    )