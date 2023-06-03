import streamlit as st
import random
import numpy as np
import pandas as pd
import math
import datetime

# Configurar página de Streamlit
st.set_page_config(
    page_title="Simulación de colas",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "MySS - 2023 - UNLaR"
    }
)

with st.sidebar:
    st.header("⌨️")
    st.subheader("Parámetros")
    arr_interval = st.slider(
        "Intervalo entre llegadas de clientes (seg)",
        1, 100, (25, 75)
    )
    serv_interval = st.slider(
        "Intervalo de tiempo de servicio (seg)",
        1, 100, (25, 75)
    )
    simulation_time = st.number_input(
        "Duración de la simulación (seg)",
        min_value=1
    )
    distribution = st.radio(
    "Distribución a usar para generar los números aleatorios",
    ('uniforme', 'gaussiana'))

st.markdown(
    """
    # Situación I
    ## Descripción
    - Problema n° 1
    - Tiempos de llegadas de clientes aleatorios (dentro de un intervalo dado)
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempos de prestación de servicios aleatorios (dentro de un intervalo dado)
    - El servidor no abandona el puesto de servicio

    ## Uso
    - Configure parámetros usando la **👈 barra lateral**
    - Presione el botón **'Simular'** para generar la tabla de simulación
    """
)
