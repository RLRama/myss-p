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
    # Situación II
    ## Descripción
    - Obedece al problema n° 2
    - Clientes que llegan individualmente en intervalos aleatorios
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempos de prestación de servicios de intervalo aleatorios
    - El servidor abandona el puesto de servicio con intervalos aleatorios de tiempo

    ## Uso
    - Configure parámetros usando la **👈 barra lateral** para dar valores
    - Presione el botón **'Simular'** para mostrar la tabla de simulación generada
    """
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
    break_rate = st.slider(
        "Intervalo de tiempo de descanso `(min)`",
        0.0, 100.0, (25.0, 75.0)
    )
    simulation_time = st.number_input(
        "Duración de la simulación `(min)`",
        min_value=1.00
    )
    distribution = st.radio(
    "Distribución a usar para generar los números aleatorios",
    ('uniform', 'gaussian'))

    return_rate = st.slider(
        "Intervalo de tiempo de regreso `(min)`",
        0.0, 100.0, (25.0, 75.0)
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
    time = pd.to_timedelta(float_minutes, unit='m')
    formatted_time = str(time)

    if '.' in formatted_time:
        formatted_time = formatted_time[:-3]

    return formatted_time

class Event:
    def __init__(self, time, arrival):
        self.time = time
        self.arrival = arrival

    def __lt__(self, other):
        return self.time < other.time

def mm1_queue_simulation(arrival_rate, service_rate, break_rate, return_rate, simulation_time):
    event_queue = []
    data = []

    clock = 0
    num_jobs = 0
    num_completed_jobs = 0
    total_response_time = 0
    previous_event_time = 0
    queue_size = 0
    server_state = "Idle"
    next_break_time = None
    return_to_work_time = None
    current_service_end_time = None

    while clock < simulation_time:
        if server_state == "Idle":
            if next_break_time is None:
                next_break_time = clock + generate_random_numbers(break_rate)
            if return_to_work_time is None:
                return_to_work_time = clock + generate_random_numbers(return_rate)

            if next_break_time <= return_to_work_time:
                event_queue.append(Event(next_break_time, False))
                server_state = "Break"
            else:
                event_queue.append(Event(return_to_work_time, False))
                server_state = "Idle"
                next_break_time = None
                return_to_work_time = None
        else:
            event_queue.append(Event(clock + generate_random_numbers(arrival_rate), True))

        event_queue.sort()
        current_event = event_queue.pop(0)
        clock = current_event.time

        next_arrival_time = event_queue[0].time if event_queue else None

        next_departure_time = None
        if queue_size > 0 and server_state == "Idle":
            next_departure_time = clock + generate_random_numbers(service_rate)

        data.append({
            "Event Type": "Arrival" if current_event.arrival else "Departure",
            "Current Time": clock,
            "Next Arrival Time": next_arrival_time,
            "Next Departure Time": next_departure_time,
            "Queue Size": queue_size,
            "Server State": server_state,
            "Next Break Time": next_break_time if server_state == "Idle" else None,
            "Return to Work Time": return_to_work_time if server_state == "Break" else None
        })

        if current_event.arrival:
            num_jobs += 1
            service_time = generate_random_numbers(service_rate)
            total_response_time += clock - previous_event_time
            previous_event_time = clock

            if queue_size == 0 and server_state == "Idle":
                event_queue.append(Event(clock + service_time, False))
            
            queue_size += 1
        else:
            num_completed_jobs += 1
            queue_size -= 1

            if queue_size > 0 and server_state == "Idle":
                service_time = generate_random_numbers(service_rate)
                event_queue.append(Event(clock + service_time, False))
            elif queue_size == 0 and server_state == "Break":
                server_state = "Idle"
                next_break_time = None
                return_to_work_time = None

    average_response_time = total_response_time / num_completed_jobs
    utilization = num_completed_jobs / clock

    average_response_time = total_response_time / num_completed_jobs
    utilization = num_completed_jobs / clock

    df = pd.DataFrame(data)

    st.write("### Resultados de la simulación:")
    st.write("- Tiempo de simulación:", format_float_as_time(simulation_time))
    st.write("- Servicios completados:", num_completed_jobs)
    st.write("- Tiempo de respuesta promedio (tiempo total de respuesta / trabajos completados):", format(average_response_time))
    st.write("- Utilización (trabajos completados / reloj):", utilization)

    return df

st.checkbox("Usar ancho total de la página", value=False, key="use_container_width")

if st.button ('Simular'):
    df = mm1_queue_simulation(arrival_rate, service_rate, break_rate, return_rate, simulation_time)
    st.dataframe(df, use_container_width=st.session_state.use_container_width)