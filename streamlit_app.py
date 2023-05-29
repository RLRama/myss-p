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
Definición de variables para el tratamiento de la simulación propuesta
"""
)
st.subheader("Cliente")
customers = st.number_input("Cantidad de clientes que llegan",min_value=1)
st.markdown(
    """
    Intervalo de tiempo de llegada
"""
)
customersMinArrTime = st.number_input("Límite inferior de tiempo de llegada")
customersMaxArrTime = st.number_input("Límite superior de tiempo de llegada")
customersArrTimeDistr = st.radio(
    "Distribución de probabilidad de tiempo de llegada",
    ('Normal', 'Uniforme')
    )

st.divider()
st.subheader("Servidor")
st.markdown(
    """
    Intervalo de tiempo de servicio
"""
)
serverMinWorkTime = st.number_input("Límite inferior de tiempo de servicio")
serverMaxWorkTime = st.number_input("Límite superior de tiempo de servicio")
serverWorkTimeDistr = st.radio(
    "Distribución de probabilidad de tiempo de servicio",
    ('Normal', 'Uniforme')
    )
serverLeaves = st.checkbox('¿El servidor abandona la cola?')
st.caption("Ignorar si el servidor no abandona la cola")
serverMinLeaveTime = st.number_input("Límite inferior de tiempo de abandono")
serverMaxLeaveTime = st.number_input("Límite superior de tiempo de abandono")
serverLeaveTimeDistr = st.radio(
    "Distribución de probabilidad de tiempo de abandono",
    ('Normal', 'Uniforme')
    )