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

def single_server_queue_simulation(num_iterations, arrival_time, service_time):
    # Initialize the dataframe
    df = pd.DataFrame(columns=['Iteration', 'Arrival Time', 'Service Start Time', 'Service End Time', 'Waiting Time'])

    # Set the initial values
    arrival = 0
    service_start = 0
    service_end = 0
    waiting_time = 0

    for i in range(num_iterations):
        # Calculate the arrival time
        arrival += arrival_time

        # Calculate the service start time
        service_start = max(arrival, service_end)

        # Calculate the service end time
        service_end = service_start + service_time

        # Calculate the waiting time
        waiting_time = service_start - arrival

        # Append the iteration to the dataframe
        df = df.append({'Iteration': i + 1, 'Arrival Time': arrival, 'Service Start Time': service_start,
                        'Service End Time': service_end, 'Waiting Time': waiting_time}, ignore_index=True)

    return df

# Set the parameters
num_iterations = 10
arrival_time = 2
service_time = 3

# Run the simulation
simulation_df = single_server_queue_simulation(num_iterations, arrival_time, service_time)



# Print the dataframe
if st.button('Simular'):
    st.dataframe(simulation_df)