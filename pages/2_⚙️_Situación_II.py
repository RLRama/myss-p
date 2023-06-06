import simpy
import pandas as pd
import numpy as np
import streamlit as st
import random

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
    - Tiempo de llegadas de cliente aleatorio (dentro de un intervalo dado)
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempo de prestación de servicio aleatorio (dentro de un intervalo dado)
    - El servidor abandona el puesto de servicio

    ### Uso
    1. Configure parámetros usando la **👈 barra lateral**
    2. Haga clic el botón **'Simular'** para generar la tabla de simulación
    """
)

# Mostrar parámetros en la barra lateral
with st.sidebar:
    st.header("⌨️")
    st.subheader("Parámetros")
    
    # Slider para el intervalo entre llegadas de clientes
    arrival_rate = st.slider(
        "Intervalo de tiempo entre llegadas (seg)",
        1, 100, (25, 75)
    )
    # Slider para el tiempo de trabajo
    service_rate = st.slider(
        "Intervalo de tiempo de servicio (seg)",
        1, 100, (25, 75)
    )
    # Entrada para la cant. de interrupciones
    interruption_rate = st.number_input(
        "Interrupciones por segundo",
        value=0.5,
        min_value=0.01
    )
    #S
    interruption_interval = st.slider(
        "Intervalo de duración de interrupción (seg)",
        1, 100, (25, 75)
    )
    # Entrada para la duración de simulación
    sim_time = st.number_input(
        "Tiempo de simulación (seg)",
        min_value=1, value=20
    )

    

def generate_random_number(interval):
    """Genera un número al azar dentro del intervalo dado"""
    lower_bound = interval[0]
    upper_bound = interval[1]
    return random.randint(lower_bound, upper_bound)

def customer(env, server, arrival_rate, service_rate, interruption_rate, queue_size):
    while True:
        # Evento de llegada de cliente
        yield env.timeout(generate_random_number(arrival_rate))
        arrival_time = env.now
        data.append([arrival_time, 'Llegada de cliente', queue_size.count])
        
        with server.request() as req:
            # Esperar a que el servidor esté libre
            yield req
            #Tiempo de servicio
            yield env.timeout(generate_random_number(service_rate))
            
        # Evento de interrupción
        if np.random.rand() < interruption_rate:
            interruption_duration = generate_random_number(interruption_interval)
            interruption_start = env.now
            data.append([interruption_start, 'Inicio de interrupción', queue_size.count])
            yield env.timeout(interruption_duration)
            interruption_end = env.now
            data.append([interruption_end, 'Fin de interrupción', queue_size.count])
        
        # Grabar evento de fin de servicio
        data.append([env.now, 'Fin de servicio', queue_size.count])

def queue_size(env, server):
    while True:
        # Actualizar tamaño de cola
        queue_size.count = len(server.queue)
        yield env.timeout(1)

def simulate_m_m_1_queue(arrival_rate, service_rate, interruption_rate, sim_time):
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=1)
    
    global data
    data = [['Hora actual', 'Tipo de evento', 'Tamaño de cola']]
    
    # Iniciar procesos de cliente y tamaño de cola
    env.process(customer(env, server, arrival_rate, service_rate, interruption_rate, server))
    env.process(queue_size(env, server))
    
    # Ejecutar la simulación hasta sim_time
    env.run(until=sim_time)
    
    # Convertir la lista de datos a un dataframe
    df = pd.DataFrame(data[1:], columns=data[0])
    df['Hora actual'] = pd.to_datetime(df['Hora actual'], unit='s')
    df['Hora actual'] = df['Hora actual'].dt.strftime('%H:%M:%S')
    return df

# Realizar simulación
if st.button('Simular'):
    df = simulate_m_m_1_queue(arrival_rate, service_rate, interruption_rate, sim_time)
    st.dataframe(df)