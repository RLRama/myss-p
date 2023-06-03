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
    arr_interval = st.slider(
        "Intervalo entre llegadas de clientes `(min)`",
        0.0, 100.0, (25.0, 75.0)
    )
    serv_interval = st.slider(
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

import numpy as np
import pandas as pd

def mm1_simulation(arrival_rate, service_rate, simulation_time):
    interarrival_times = np.random.exponential(scale=1 / arrival_rate)
    service_times = np.random.exponential(scale=1 / service_rate)

    arrival_times = [interarrival_times]
    service_starts = [arrival_times[0]]
    wait_times = [0]
    departure_times = [service_starts[0] + service_times]

    while departure_times[-1] < simulation_time:
        interarrival_times = np.random.exponential(scale=1 / arrival_rate)
        service_times = np.random.exponential(scale=1 / service_rate)

        arrival_times.append(arrival_times[-1] + interarrival_times)
        service_starts.append(max(arrival_times[-1], departure_times[-1]))
        wait_times.append(service_starts[-1] - arrival_times[-1])
        departure_times.append(service_starts[-1] + service_times)

    data = {
        'Iteration': range(len(arrival_times)),
        'Interarrival Time': np.diff([0] + arrival_times),
        'Arrival Time': arrival_times[:-1],
        'Service Time': service_times,
        'Service Start': service_starts[:-1],
        'Wait Time': wait_times[:-1],
        'Departure Time': departure_times[:-1]
    }

    df = pd.DataFrame(data)
    return df


# Example usage
arrival_rate = 0.5
service_rate = 0.6
simulation_time = 10.0

if st.button('Simular'):
    simulation_df = mm1_simulation(arrival_rate, service_rate, simulation_time)
    st.dataframe(simulation_df)