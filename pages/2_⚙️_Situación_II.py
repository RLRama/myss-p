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
    ## Situación II
    ### Descripción
    - Problema II
    - Similar al problema anterior
    - Tiempo de llegadas de cliente aleatorio (dentro de un intervalo dado)
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempo de prestación de servicio aleatorio (dentro de un intervalo dado)
    - El servidor abandona el puesto de servicio durante ciertos periodos
    - Lo hace incluso con un servicio en curso, el cual termina al regresar

    ### Uso
    1. Configure parámetros usando la **👈 barra lateral**
    2. Haga clic el botón **'Simular'** para generar la tabla de simulación
    """
)

def add_breaks(queue_df, break_interval, service_interval, break_duration):
    """Adds breaks to the queue dataframe based on the break interval and break duration."""
    break_start = break_interval  # Start the first break after the break interval
    while break_start < len(queue_df):
        break_end = min(break_start + break_duration, len(queue_df))
        for i in range(break_start, break_end):
            queue_df.loc[i, "Evento"] = "Descanso"
            queue_df.loc[i, "Clientes en cola"] = len(queue_df) - (i + 1)
            queue_df.loc[i, "Hora sig. llegada"] = ""
            queue_df.loc[i, "Hora sig. fin de servicio"] = ""

        service_start = break_end
        service_end = min(service_start + generate_random_number(service_interval), len(queue_df))
        for i in range(service_start, service_end):
            queue_df.loc[i, "Evento"] = "Servicio antes de descanso"
            queue_df.loc[i, "Clientes en cola"] = len(queue_df) - (i + 1)
            queue_df.loc[i, "Hora sig. llegada"] = ""
            queue_df.loc[i, "Hora sig. fin de servicio"] = ""

        break_start = service_end + generate_random_number(service_interval)
    return queue_df



with st.sidebar:
    st.header("⌨️")
    st.subheader("Parámetros")

    # Slider para el intervalo entre llegadas de clientes
    arr_interval = st.slider(
        "Intervalo de tiempo entre llegadas (seg)",
        1, 100, (25, 75)
    )

    # Slider para el tiempo de trabajo
    serv_interval = st.slider(
        "Intervalo de tiempo de servicio (seg)",
        1, 100, (25, 75)
    )

    # Slider para el intervalo entre descansos
    break_interval = st.slider(
        "Intervalo entre descansos",
        1, 10, 1
    )

    # Slider para la duración del descanso
    break_duration = st.slider(
        "Duración del descanso",
        1, 10, 1
    )

    # Entrada para la duración de simulación
    queue_duration = st.number_input(
        "Tiempo de simulación (seg)",
        min_value=1
    )

    # Entrada para tamaño inicial de cola
    initial_queue_size = st.number_input(
        "Tamaño inicial de cola",
        min_value=0
    )

def generate_random_number(interval):
    """Generates a random number within the given interval."""
    lower_bound = interval[0]
    upper_bound = interval[1]
    return random.randint(lower_bound, upper_bound)

def format_time(seconds):
    """Converts seconds to HH:MM:SS format."""
    if not seconds:
        return ''
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Create an empty dataframe for queue events
queue_df = pd.DataFrame(columns=["Hora actual", "Evento", "Clientes en cola", "Hora sig. llegada", "Hora sig. fin de servicio"])

# Define function to handle arrivals
def handle_arrival(time, queue, arrival_interval):
    """Adds a customer to the queue when the event is an arrival."""
    queue.append(time)
    queue_df.loc[len(queue_df)] = [time, "Llegada", len(queue), "", ""]

# Define function to handle departures
def handle_departure(time, queue, departure_interval):
    """Removes a customer from the queue when the event is a departure."""
    if len(queue) > 0:
        queue.pop(0)
    queue_df.loc[len(queue_df)] = [time, "Fin de servicio", len(queue), "", ""]

# Simulate queue events
queue = []

# Initialize the queue with the initial size
queue.extend([0] * initial_queue_size)
queue_df.loc[len(queue_df)] = [0, "", len(queue), "", ""]

next_arrival = generate_random_number(arr_interval)
next_departure = generate_random_number(serv_interval)

# Main simulation loop
for t in range(1, queue_duration + 1):  # Skip the first row
    if t == next_arrival:
        handle_arrival(t, queue, next_arrival)
        next_arrival += generate_random_number(arr_interval)
    if t == next_departure:
        handle_departure(t, queue, next_departure)
        next_departure += generate_random_number(serv_interval)

    # Update the next arrival and departure times in the dataframe
    queue_df.loc[len(queue_df) - 1, "Hora sig. llegada"] = next_arrival if t < next_arrival else ""
    queue_df.loc[len(queue_df) - 1, "Hora sig. fin de servicio"] = next_departure if t < next_departure else ""

# Add breaks to the queue dataframe
queue_df = add_breaks(queue_df, break_interval, serv_interval, break_duration)

# Reset the dataframe index
queue_df.reset_index(drop=True, inplace=True)

# Convert the dataframe columns to ints and handle empty strings
queue_df["Hora actual"] = queue_df["Hora actual"].astype(int)
queue_df["Hora sig. llegada"] = queue_df["Hora sig. llegada"].apply(lambda x: int(x) if x else '')
queue_df["Hora sig. fin de servicio"] = queue_df["Hora sig. fin de servicio"].apply(lambda x: int(x) if x else '')

# Apply the time formatting function to the time columns
queue_df["Hora actual"] = queue_df["Hora actual"].apply(format_time)
queue_df["Hora sig. llegada"] = queue_df["Hora sig. llegada"].apply(format_time)
queue_df["Hora sig. fin de servicio"] = queue_df["Hora sig. fin de servicio"].apply(format_time)

# Display the dataframe when the "Simular" button is clicked
if st.button('Simular'):
    st.dataframe(queue_df)
