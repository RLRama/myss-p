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

st.image("https://em-content.zobj.net/thumbs/120/apple/354/level-slider_1f39a-fe0f.png")
st.header("¡Hola! 👋")
st.markdown(
    """
    Aplicación web para `Modelos y Simulación de Sistemas` 
    
    **👈 Seleccione una página de la barra lateral** para ver el funcionamiento
"""
)