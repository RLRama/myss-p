import streamlit as st
import random as rnd
import simpy as sp
import numpy as np
import pandas as pd

# Configurar página
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
    st.subheader("Configurar parámetros")
    t_arr = st.number_input(
        "Tiempo promedio entre llegadas de clientes `(min)`",
        min_value=1.00
    )
    t_serv = st.number_input(
        "Tiempo promedio de servicio `(min)`",
        min_value=1.00
    )
    n = st.number_input(
        "Clientes generados",
        min_value=1
    )
    t = st.number_input(
        "Duración de la simulación `(min)`",
        min_value=1.00
    )
    seed = st.number_input(
        "Semilla para generar números aleatorios",
        value=9999, min_value=1
    )

st.markdown(
    """
    # Situación I
    ## Descripción
    - Obedece al problema n° 1
    - Clientes que llegan individualmente en intervalos aleatorios
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempos de prestación de servicios aleatorios
    - El servidor no abandona el puesto de servicio

    ## Uso
    - Configure parámetros usando la **👈 barra lateral** para dar valores
    - Presione el botón **'Simular'** para mostrar la tabla de simulación generada
    """
)

