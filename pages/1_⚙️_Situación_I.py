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

# Example usage
arrival_rate = 0.2
service_rate = 0.3
simulation_time = 100

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

def generate_random_numbers(interval, distribution):
    lower_bound = interval[0]
    upper_bound = interval[1]

    if distribution == 'uniform':
        return random.uniform(lower_bound, upper_bound)
    elif distribution == 'gaussian':
        mu = (lower_bound + upper_bound) / 2
        sigma = (upper_bound - lower_bound) / 6
        return np.random.normal(mu, sigma)
    else:
        raise ValueError("Distribución inválida")
    
def format_float_as_time(float_minutes):
    hours = int(float_minutes // 60)
    minutes = int(float_minutes % 60)
    seconds = int((float_minutes * 60) % 60)

    formatted_time = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return formatted_time

class Event:
    def __init__(self, time, arrival):
        self.time = time
        self.arrival = arrival

    def __lt__(self, other):
        return self.time < other.time

def mm1_queue_simulation(arrival_rate, service_rate, simulation_time):
    event_queue = []
    data = []
    clock = 0
    num_jobs = 0
    num_completed_jobs = 0
    total_response_time = 0
    previous_event_time = 0
    queue_size = 0

    while clock < simulation_time:
        event_queue.append(Event(clock + generate_random_numbers(arrival_rate, distribution), True))

        event_queue.sort()
        current_event = event_queue.pop(0)
        clock = current_event.time

        next_arrival_time = event_queue[0].time if event_queue else None

        next_departure_time = None
        if queue_size > 0:
            next_departure_time = clock + generate_random_numbers(service_rate, distribution)

        formatted_clock = format_float_as_time(clock)

        data.append({
            "Evento": "Llegada" if current_event.arrival else "Fin de servicio",
            "Hora": clock,
            "Siguiente llegada": next_arrival_time,
            "Siguiente fin de servicio": next_departure_time,
            "Clientes en cola": queue_size,
            "Servidor": "Ocupado" if queue_size > 0 else "Libre"
        })

        if current_event.arrival:
            num_jobs += 1
            service_time = generate_random_numbers(service_rate, distribution)
            total_response_time += clock - previous_event_time
            previous_event_time = clock

            if queue_size == 0:
                event_queue.append(Event(clock + service_time, False))
            
            queue_size += 1
        else:
            num_completed_jobs += 1
            queue_size -= 1

            if queue_size > 0:
                service_time = generate_random_numbers(service_rate, distribution)
                event_queue.append(Event(clock + service_time, False))

    average_response_time = total_response_time / num_completed_jobs
    utilization = num_completed_jobs / clock

    df = pd.DataFrame(data)

    st.write("### Resultados de la simulación:")
    st.write("- Tiempo de simulación:", simulation_time)
    st.write("- Servicios completados:", num_completed_jobs)
    st.write("- Tiempo de respuesta promedio (tiempo total de respuesta / trabajos completados):", (average_response_time))
    st.write("- Utilización (trabajos completados / reloj):", utilization)

    return df

st.checkbox("Usar ancho total de la página", value=False, key="use_container_width")

if st.button ('Simular'):
    df = mm1_queue_simulation(arrival_rate, service_rate, simulation_time)
    st.dataframe(df, use_container_width=st.session_state.use_container_width)