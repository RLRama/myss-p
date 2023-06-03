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
    queue_duration = st.number_input(
        "Duración de la simulación (seg)",
        min_value=1
    )
    initial_queue_size = st.number_input(
        "Clientes en cola al inicio",
        min_value=0
    )

def generate_random_number(interval):
    lower_bound = interval[0]
    upper_bound = interval[1]
    return random.randint(lower_bound, upper_bound)

def format_time(time):
    hours = time // 3600
    minutes = (time % 3600) // 60
    seconds = time % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Create an empty DataFrame to store the queue events
queue_df = pd.DataFrame(columns=["Time", "Event", "Queue Size", "Next Arrival", "Next Departure"])

# Define a function to handle arrivals
def handle_arrival(time, queue, arrival_interval):
    queue.append(time)
    queue_df.loc[len(queue_df)] = [time, "Arrival", len(queue), "", ""]

# Define a function to handle departures
def handle_departure(time, queue, departure_interval):
    if len(queue) > 0:
        queue.pop(0)
    queue_df.loc[len(queue_df)] = [time, "Departure", len(queue), "", ""]

# Simulate the queue events
queue = []

# Initialize the queue with the initial size
queue.extend([0] * initial_queue_size)
queue_df.loc[len(queue_df)] = [0, "", len(queue), "", ""]

next_arrival = generate_random_number(arr_interval)
next_departure = generate_random_number(serv_interval)
for t in range(1, queue_duration + 1):  # Start from 1 to skip the initial row
    if t == next_arrival:
        handle_arrival(t, queue, next_arrival)
        next_arrival += generate_random_number(arr_interval)
    if t == next_departure:
        handle_departure(t, queue, next_departure)
        next_departure += generate_random_number(serv_interval)

    queue_df.loc[len(queue_df) - 1, "Next Arrival"] = next_arrival if t < next_arrival else ""
    queue_df.loc[len(queue_df) - 1, "Next Departure"] = next_departure if t < next_departure else ""

queue_df["Time"] = queue_df["Time"].apply(format_time)
queue_df["Next Arrival"] = queue_df["Next Arrival"].apply(format_time)
queue_df["Next Departure"] = queue_df["Next Departure"].apply(format_time)

# Reset the index of the DataFrame
queue_df.reset_index(drop=True, inplace=True)

if st.button('Simular'):
    st.dataframe(queue_df)