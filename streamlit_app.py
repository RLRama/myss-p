import streamlit as st
import random as rnd
import simpy as sp
import numpy as np
import pandas as pd

# Configurar página
st.set_page_config(
    page_title="Simulación de colas",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "MySS - 2023 - UNLaR"
    }
)

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
st.header("Parámetros de simulación")
st.markdown(
    """
- Definición de variables para el tratamiento de la simulación propuesta
"""
)
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Cliente")
    customerN = st.number_input(label='Número de clientes',min_value=1)
    randArrTime = st.checkbox('Tiempo de llegada aleatorio de clientes')
    arrTime = st.number_input(label="Tiempo entre llegadas",min_value=1.00)
    arrTimeDistr = st.radio(
        "Distribución",
        ('Normal', 'Uniforme')
    )
    arrTimeSpread = st.number_input(label="Dispersión",min_value=1.00)
    if randArrTime:
        arr

    st.subheader("Simulación")
    maxTime = st.number_input(label="Tiempo máximo",min_value=1)

