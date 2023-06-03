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
    st.subheader("Configurar parámetros")
    arrival_rate = st.slider(
        "Intervalo entre llegadas de clientes `(min)`",
        0.0, 100.0, (25.0, 75.0)
    )
    service_rate = st.slider(
        "Intervalo de tiempo de servicio `(min)`",
        0.0, 100.0, (25.0, 75.0)
    )
    simulation_time = st.number_input(
        "Duración de la simulación `(min)`",
        min_value=1.00
    )
    distribution = st.radio(
    "Distribución a usar para generar los números aleatorios",
    ('uniform', 'gaussian'))

st.markdown(
    """
    # Situación I
    ## Descripción
    - Obedece al problema n° 1
    - Clientes que llegan individualmente en intervalos aleatorios
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempos de prestación de servicios de intervalo aleatorios
    - El servidor no abandona el puesto de servicio

    ## Uso
    - Configure parámetros usando la **👈 barra lateral** para dar valores
    - Presione el botón **'Simular'** para mostrar la tabla de simulación generada
    """
)

def mm1_simulation(arrival_rate, service_rate, simulation_time):
    clock = 0
    queue = 0
    total_customers_served = 0
    total_waiting_time = 0

    st.text("Iteration\tClock\tQueue\tTotal Served\tWaiting Time")
    iteration = 1

    while clock < simulation_time:
        inter_arrival_time = 1 / arrival_rate
        clock += inter_arrival_time

        if clock >= simulation_time:
            break

        total_customers_served += 1

        if queue == 0:
            service_time = 1 / service_rate
            total_waiting_time += service_time
            departure_time = clock + service_time
        else:
            queue -= 1
            service_time = 1 / service_rate
            total_waiting_time += service_time
            departure_time = clock + service_time

        queue += 1

        st.text(f"{iteration}\t\t{clock:.2f}\t{queue}\t{total_customers_served}\t\t{total_waiting_time:.2f}")
        iteration += 1

    average_waiting_time = total_waiting_time / total_customers_served
    return average_waiting_time

# Example usage
arrival_rate = 5  # average arrival rate of 5 customers per unit of time
service_rate = 7  # average service rate of 7 customers per unit of time
simulation_time = 1000

if st.button('Simular'):
    average_waiting_time = mm1_simulation(arrival_rate, service_rate, simulation_time)
    st.text("\nAverage waiting time:", average_waiting_time)