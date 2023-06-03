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

# Create an empty DataFrame to store the queue events
queue_df = pd.DataFrame(columns=["Time", "Event", "Queue Size"])

# Define a function to handle arrivals
def handle_arrival(time, queue):
    queue.append(time)
    queue_df.loc[len(queue_df)] = [time, "Arrival", len(queue)]

# Define a function to handle departures
def handle_departure(time, queue):
    if len(queue) > 0:
        queue.pop(0)
    queue_df.loc[len(queue_df)] = [time, "Departure", len(queue)]

# Simulate the queue events
queue = []

for t in range(simulation_time):
    if t % generate_random_number(arr_interval, distribution) == 0:  # Check if it's an arrival time
        handle_arrival(t, queue)
    if t % generate_random_number(serv_interval, distribution) == 0:  # Check if it's a departure time
        handle_departure(t, queue)

if st.button('Simular'):
    st.dataframe(queue_df)