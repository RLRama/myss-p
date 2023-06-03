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

# Display parameters in the Streamlit sidebar
with st.sidebar:
    st.header("⌨️")
    st.subheader("Parameters")
    
    # Slider for interval between customer arrivals
    arr_interval = st.slider(
        "Interval between customer arrivals (sec)",
        1, 100, (25, 75)
    )
    
    # Slider for service time interval
    serv_interval = st.slider(
        "Service time interval (sec)",
        1, 100, (25, 75)
    )
    
    # Input field for simulation duration
    queue_duration = st.number_input(
        "Simulation duration (sec)",
        min_value=1
    )
    
    # Input field for initial number of customers in the queue
    initial_queue_size = st.number_input(
        "Initial number of customers in queue",
        min_value=0
    )

def generate_random_number(interval):
    """Generate a random number within the given interval."""
    lower_bound = interval[0]
    upper_bound = interval[1]
    return random.randint(lower_bound, upper_bound)

def format_time(seconds):
    """Format time from seconds to HH:MM:SS format."""
    if not seconds:
        return ''
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Create an empty DataFrame to store the queue events
queue_df = pd.DataFrame(columns=["Current Time", "Event", "Customers in Queue", "Next Arrival Time", "Next Service Completion Time"])

# Define a function to handle arrivals
def handle_arrival(time, queue, arrival_interval):
    """Handle an arrival event by adding a customer to the queue."""
    queue.append(time)
    queue_df.loc[len(queue_df)] = [time, "Arrival", len(queue), "", ""]

# Define a function to handle departures
def handle_departure(time, queue, departure_interval):
    """Handle a departure event by removing a customer from the queue."""
    if len(queue) > 0:
        queue.pop(0)
    queue_df.loc[len(queue_df)] = [time, "Service Completion", len(queue), "", ""]

# Simulate the queue events
queue = []

# Initialize the queue with the initial size
queue.extend([0] * initial_queue_size)
queue_df.loc[len(queue_df)] = [0, "", len(queue), "", ""]

next_arrival = generate_random_number(arr_interval)
next_departure = generate_random_number(serv_interval)

# Main simulation loop
for t in range(1, queue_duration + 1):  # Start from 1 to skip the initial row
    if t == next_arrival:
        handle_arrival(t, queue, next_arrival)
        next_arrival += generate_random_number(arr_interval)
    if t == next_departure:
        handle_departure(t, queue, next_departure)
        next_departure += generate_random_number(serv_interval)

    # Update the next arrival and departure times in the queue DataFrame
    queue_df.loc[len(queue_df) - 1, "Next Arrival Time"] = next_arrival if t < next_arrival else ""
    queue_df.loc[len(queue_df) - 1, "Next Service Completion Time"] = next_departure if t < next_departure else ""

# Reset the index of the DataFrame
queue_df.reset_index(drop=True, inplace=True)

# Convert the DataFrame columns to integers, handling empty strings
queue_df["Current Time"] = queue_df["Current Time"].astype(int)
queue_df["Next Arrival Time"] = queue_df["Next Arrival Time"].apply(lambda x: int(x) if x else '')
queue_df["Next Service Completion Time"] = queue_df["Next Service Completion Time"].apply(lambda x: int(x) if x else '')

# Apply the formatting function to the time columns
queue_df["Current Time"] = queue_df["Current Time"].apply(format_time)
queue_df["Next Arrival Time"] = queue_df["Next Arrival Time"].apply(format_time)
queue_df["Next Service Completion Time"] = queue_df["Next Service Completion Time"].apply(format_time)

# Display the queue DataFrame when the "Simulate" button is clicked
if st.button('Simulate'):
    st.dataframe(queue_df)
