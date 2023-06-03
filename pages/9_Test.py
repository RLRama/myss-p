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
    ## Situación I
    ### Descripción
    - Problema n° 1
    - Tiempos de llegadas de clientes aleatorios (dentro de un intervalo dado)
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempos de prestación de servicios aleatorios (dentro de un intervalo dado)
    - El servidor no abandona el puesto de servicio

    ### Uso
    1. Configure parámetros usando la **👈 barra lateral**
    2. Haga clic el botón **'Simular'** para generar la tabla de simulación
    """
)

def simulate_queue(arrival_time, departure_time, num_iterations):
    queue = []
    df = pd.DataFrame(columns=['Iteration', 'Arrival', 'Departure', 'Queue'])
    
    for i in range(num_iterations):
        if not queue:
            departure = arrival_time + departure_time
        else:
            departure = max(queue) + departure_time
        
        queue.append(departure)
        df.loc[i] = [i+1, arrival_time, departure, len(queue)]
        
        arrival_time += arrival_time
    
    return df

# Example usage
iterations = 20
arrival_time = 2
departure_time = 3

df = simulate_queue(arrival_time, departure_time, iterations)

# Print the dataframe
if st.button('Simular'):
    st.dataframe(df)