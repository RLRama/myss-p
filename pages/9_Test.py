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

st.markdown(
    """
    ## Situación I
    ### Descripción
    - Problema I
    - Tiempo de llegadas de cliente aleatorio (dentro de un intervalo dado)
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempo de prestación de servicio aleatorio (dentro de un intervalo dado)
    - El servidor no abandona el puesto de servicio

    ### Uso
    1. Configure parámetros usando la **👈 barra lateral**
    2. Haga clic el botón **'Simular'** para generar la tabla de simulación
    """
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
    initial_queue_size = st.number_input(
        "Clientes en cola al inicio",
        min_value=0
    )
    distribution = st.radio(
    "Distribución para generación de números aleatorios",
    ('uniforme', 'gaussiana'))

def generate_random_number(interval, distribution):
    lower_bound = interval[0]
    upper_bound = interval[1]

    if distribution == 'uniforme':
        return random.uniform(lower_bound, upper_bound)
    elif distribution == 'gaussiana':
        mean = (lower_bound + upper_bound) / 2
        std_dev = (upper_bound - lower_bound) / 6  # Adjust the standard deviation based on the interval
        return np.random.normal(mean, std_dev)
    else:
        raise ValueError("Invalid distribution specified.")

def simulate_mm1_queue(arrival_rate, service_rate, simulation_time, initial_queue_size):
    event_list = []
    time = 0
    queue_size = initial_queue_size
    next_arrival_time = np.random.exponential(scale=1/arrival_rate)
    next_departure_time = np.inf

    while time < simulation_time:
        if next_arrival_time < next_departure_time:
            event_type = 'Arrival'
            time = next_arrival_time
            next_arrival_time += np.random.exponential(scale=1/arrival_rate)

            if queue_size == 0:
                next_departure_time = time + np.random.exponential(scale=1/service_rate)

            queue_size += 1
        else:
            event_type = 'Departure'
            time = next_departure_time
            next_departure_time = np.inf

            if queue_size > 0:
                queue_size -= 1

            if queue_size > 0:
                next_departure_time = time + np.random.exponential(scale=1/service_rate)

        event_list.append({
            'Time': time,
            'Event': event_type,
            'Queue Size': queue_size,
            'Next Arrival Time': next_arrival_time,
            'Next Departure Time': next_departure_time
        })

    df = pd.DataFrame(event_list)
    return df

if st.button('Simular'):
    df = simulate_mm1_queue(arr_interval, serv_interval, simulation_time, initial_queue_size)
    st.dataframe(df)