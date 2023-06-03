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
    - Problema I
    - Tiempos de llegadas de clientes aleatorios (dentro de un intervalo dado)
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempos de prestación de servicios aleatorios (dentro de un intervalo dado)
    - El servidor no abandona el puesto de servicio

    ### Uso
    1. Configure parámetros usando la **👈 barra lateral**
    2. Haga clic el botón **'Simular'** para generar la tabla de simulación
    """
)

import pandas as pd

def single_server_queue_simulation(arrival_time, departure_time, num_iterations):
    queue = []
    wait_times = []
    arrival_times = []
    departure_times = []

    current_time = 0
    departure = departure_time
    num_customers = 0

    for i in range(num_iterations):
        if current_time == departure:
            num_customers -= 1
            if queue:
                departure = current_time + departure_time
                wait_times.append(current_time - queue.pop(0))
                departure_times.append(departure)
            else:
                departure = float('inf')
        if current_time == arrival_time:
            num_customers += 1
            if num_customers == 1:
                departure = current_time + departure_time
            queue.append(current_time)
            arrival_time += arrival_time

        current_time = min(arrival_time, departure)
        arrival_times.append(arrival_time)

    data = {
        'Iteration': list(range(1, num_iterations+1)),
        'Arrival Time': arrival_times,
        'Departure Time': departure_times,
        'Wait Time': wait_times
    }
    df = pd.DataFrame(data)
    return df

# Simulation parameters
arrival_time = 2
departure_time = 3
num_iterations = 10

# Run simulation and print dataframe


# Print the dataframe
if st.button('Simular'):
    simulation_df = single_server_queue_simulation(arrival_time, departure_time, num_iterations)
    st.dataframe(simulation_df)