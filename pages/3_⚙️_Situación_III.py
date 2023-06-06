import streamlit as st
import random as np
import pandas as pd
import simpy
import numpy as np
from datetime import datetime

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
    ## Situación III
    ### Descripción
    - Problema III
    - Tiempo de llegadas de cliente aleatorio (dentro de un intervalo dado)
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempo de prestación de servicio aleatorio (dentro de un intervalo dado)
    - El servidor no abandona el puesto de servicio
    - Los clientes abandonan la cola cuando esperan demasiado tiempo

    ### Uso
    1. Configure parámetros usando la **👈 barra lateral**
    2. Haga clic el botón **'Simular'** para generar la tabla de simulación
    """
)

# Mostrar parámetros en la barra lateral
with st.sidebar:
    st.header("⌨️")
    st.subheader("Parámetros")
    st.caption('La distribución para la generación de números aleatorios es exponencial')
    # Entrada para el intervalo entre llegadas de clientes
    arrival_rate = st.number_input(
        "Promedio de clientes que llegan por segundo",
        min_value=0.01, value=1.00
    )    
    # Entrada para el tiempo de trabajo
    service_rate = st.number_input(
        "Promedio de servicios completados por segundo",
        min_value=0.01, value=1.00
    )    
    # Entrada para clientes que abandonan
    abandonment_rate = st.number_input(
        "Promedio de clientes que abandonan por segundo",
        min_value=0.01, value=1.00
    ) 
    # Entrada para la duración de simulación
    simulation_time = st.number_input(
        "Tiempo de simulación (seg)",
        min_value=1, value=20
    )

class MM1Queue:
    def __init__(self, env, arrival_rate, service_rate, abandonment_rate):
        self.env = env
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.abandonment_rate = abandonment_rate
        self.queue_length = 0
        self.total_customers = 0
        self.total_wait_time = 0.0
        self.events = []  # List to store events
    
    def customer_arrival(self):
        while True:
            yield self.env.timeout(np.random.exponential(1 / self.arrival_rate))
            self.total_customers += 1
            customer = self.total_customers
            self.queue_length += 1
            self.events.append(('Arrival', self.env.now, customer, self.queue_length))
            self.env.process(self.serve_customer(customer))
    
    def serve_customer(self, customer):
        yield self.env.timeout(np.random.exponential(1 / self.service_rate))
        self.queue_length = max(0, self.queue_length - 1)  # Ensure queue length is non-negative
        self.total_wait_time += self.env.now
        self.events.append(('Service Completion', self.env.now, customer, self.queue_length))
    
    def customer_abandonment(self):
        while True:
            yield self.env.timeout(np.random.exponential(1 / self.abandonment_rate))
            if self.queue_length > 0:
                self.queue_length = max(0, self.queue_length - 1)  # Ensure queue length is non-negative
                self.events.append(('Abandonment', self.env.now, None, self.queue_length))
    
    def run_simulation(self, sim_time):
        self.env.process(self.customer_arrival())
        self.env.process(self.customer_abandonment())
        self.env.run(until=sim_time)
        
        avg_wait_time = self.total_wait_time / self.total_customers
        print("Simulation Results")
        print("Average Wait Time: {:.2f}".format(avg_wait_time))
        print("Total Customers Served: {}".format(self.total_customers))
        print("Queue Length: {}".format(self.queue_length))
        
        # Create dataframe from events
        df = pd.DataFrame(self.events, columns=['Event', 'Time', 'Customer', 'Queue Length'])
        df['Time'] = df['Time'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%H:%M:%S'))
        
        print("\nEvent Log:")
        st.dataframe(df)

# Create and run the simulation
if st.button('Simular'):
    env = simpy.Environment()
    queue = MM1Queue(env, arrival_rate, service_rate, abandonment_rate)
    queue.run_simulation(simulation_time)