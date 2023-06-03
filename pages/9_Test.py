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
    - Tiempo de llegadas de cliente aleatorio (dentro de un intervalo dado)
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempo de prestación de servicio aleatorio (dentro de un intervalo dado)
    - El servidor no abandona el puesto de servicio

    ### Uso
    1. Configure parámetros usando la **👈 barra lateral**
    2. Haga clic el botón **'Simular'** para generar la tabla de simulación
    """
)

import random
import pandas as pd

def simulate_mm1_queue(arrival_rate, service_rate, simulation_time):
  """
  Simulates an M/M/1 queue.

  Args:
    arrival_rate: The arrival rate of customers.
    service_rate: The service rate of the server.
    simulation_time: The length of the simulation.

  Returns:
    A Pandas DataFrame containing the following columns:
      iteration: The iteration number.
      arrival_time: The time at which each customer arrives.
      service_time: The time it takes to serve each customer.
      wait_time: The time each customer waits in the queue.
  """

  # Initialize the simulation state.
  clock = 0
  queue = []
  customers = []

  # Simulate the arrival of customers.
  for i in range(int(simulation_time / arrival_rate)):
    arrival_time = clock + random.expovariate(arrival_rate)
    clock += arrival_time
    customers.append({
      'iteration': i,
      'arrival_time': arrival_time
    })

  # Simulate the service of customers.
  while customers:
    service_time = random.expovariate(service_rate)
    clock += service_time
    customers.pop(0)

    # Calculate the wait time for the customer.
    if queue:
      wait_time = clock - queue.pop(0)['arrival_time']
    else:
      wait_time = 0

    # Add the customer's data to the DataFrame.
    customers.append({
      'iteration': i,
      'arrival_time': arrival_time,
      'service_time': service_time,
      'wait_time': wait_time
    })

  # Return the DataFrame.
  return pd.DataFrame(customers)

if __name__ == '__main__':
  # Set the arrival rate and service rate.
  arrival_rate = 1.0 / 10.0
  service_rate = 1.0 / 5.0

  # Set the simulation time.
  simulation_time = 100.0

  # Simulate the queue and print the results to a DataFrame.
if st.button('Simular'):
  df = simulate_mm1_queue(arrival_rate, service_rate, simulation_time)
  print(df)

# 