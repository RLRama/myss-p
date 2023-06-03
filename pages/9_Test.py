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

import numpy as np
import pandas as pd

def mm1_simulation(arrival_rate, service_rate, num_iterations):
    interarrival_times = np.random.exponential(scale=1 / arrival_rate, size=num_iterations)
    service_times = np.random.exponential(scale=1 / service_rate, size=num_iterations)

    arrival_times = np.cumsum(interarrival_times)
    service_starts = np.zeros(num_iterations)
    wait_times = np.zeros(num_iterations)
    departure_times = np.zeros(num_iterations)

    for i in range(1, num_iterations):
        service_starts[i] = max(arrival_times[i], departure_times[i-1])
        wait_times[i] = service_starts[i] - arrival_times[i]
        departure_times[i] = service_starts[i] + service_times[i]

    data = {
        'Iteration': range(num_iterations),
        'Interarrival Time': interarrival_times,
        'Arrival Time': arrival_times,
        'Service Time': service_times,
        'Service Start': service_starts,
        'Wait Time': wait_times,
        'Departure Time': departure_times
    }

    df = pd.DataFrame(data)
    return df


# Example usage
arrival_rate = 0.5
service_rate = 0.6
num_iterations = 10



if st.button('Simular'):
    simulation_df = mm1_simulation(arrival_rate, service_rate, num_iterations)
    st.dataframe(simulation_df)