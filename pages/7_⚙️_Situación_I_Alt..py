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

class MM1Queue:
    def __init__(self, arrival_rate, service_rate, num_customers):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.num_customers = num_customers
        self.queue = []
        self.iteration_data = []

    def run_simulation(self):
        arrival_time = 0
        for i in range(self.num_customers):
            interarrival_time = random.expovariate(self.arrival_rate)
            arrival_time += interarrival_time

            if len(self.queue) > 0:
                waiting_time = max(0, self.queue[-1] - arrival_time)
                self.iteration_data.append((i+1, arrival_time, waiting_time))

            self.queue.append(arrival_time)
            service_time = random.expovariate(self.service_rate)
            departure_time = arrival_time + service_time
            self.queue = [x for x in self.queue if x > departure_time]

        df = pd.DataFrame(self.iteration_data, columns=["Customer", "Arrival Time", "Waiting Time"])
        return df

# Parameters for the simulation
arrival_rate = 0.2
service_rate = 0.3
num_customers = 1000

# Create MM1Queue instance and run the simulation
mm1_queue = MM1Queue(arrival_rate, service_rate, num_customers)
df = mm1_queue.run_simulation()

# Print the dataframe
if st.button('Simular'):
    st.dataframe(df)