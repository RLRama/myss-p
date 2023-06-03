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
    ## Situación II
    ### Descripción
    - Problema II
    - Similar al problema anterior
    - Tiempo de llegadas de cliente aleatorio (dentro de un intervalo dado)
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempo de prestación de servicio aleatorio (dentro de un intervalo dado)
    - El servidor abandona el puesto de servicio durante ciertos periodos
    - Lo hace incluso con un servicio en curso, el cual termina al regresar

    ### Uso
    1. Configure parámetros usando la **👈 barra lateral**
    2. Haga clic el botón **'Simular'** para generar la tabla de simulación
    """
)

with st.sidebar:
    st.header("⌨️")
    st.subheader("Parámetros")

    # Slider para el intervalo entre llegadas de clientes
    arr_interval = st.slider(
        "Intervalo de tiempo entre llegadas (seg)",
        1, 100, (25, 75)
    )

    # Slider para el tiempo de trabajo
    serv_interval = st.slider(
        "Intervalo de tiempo de servicio (seg)",
        1, 100, (25, 75)
    )

    # Slider para el tiempo de descanso del servidor
    break_interval = st.slider(
        "Intervalo de tiempo de descanso del servidor (seg)",
        1, 100, (10, 30)
    )

    # Entrada para la duración de simulación
    queue_duration = st.number_input(
        "Tiempo de simulación (seg)",
        min_value=1
    )

    # Entrada para tamaño inicial de cola
    initial_queue_size = st.number_input(
        "Tamaño inicial de cola",
        min_value=0
    )


def generate_random_number(interval):
    """Genera un número al azar dentro del intervalo dado"""
    lower_bound = interval[0]
    upper_bound = interval[1]
    return random.randint(lower_bound, upper_bound)


def format_time(seconds):
    """Pasa de segundos a formato HH:MM:SS"""
    if not seconds:
        return ""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# Crea un dataframe vacío para los eventos de la cola
queue_df = pd.DataFrame(
    columns=["Hora actual", "Evento", "Clientes en cola", "Hora sig. llegada", "Hora sig. fin de servicio"]
)

# Definir función para manejar llegadas
def handle_arrival(time, queue, arrival_interval, departure_interval):
    """Añade un cliente a la cola cuando el evento es de llegada."""
    queue.append(time)
    queue_df.loc[len(queue_df)] = [time, "Llegada", len(queue), "", ""]

    # Si no hay un servicio en curso, programar el próximo evento de salida
    if len(queue) == 1:
        next_departure = time + generate_random_number(departure_interval)
        queue_df.loc[len(queue_df) - 1, "Hora sig. fin de servicio"] = next_departure


# Definir función para manejar salidas
def handle_departure(time, queue, departure_interval, break_interval):
    """Quita un cliente de la cola cuando el evento es de salida."""
    if len(queue) > 0:
        queue.pop(0)
    queue_df.loc[len(queue_df)] = [time, "Fin de servicio", len(queue), "", ""]

    # Si hay más clientes en la cola, programar el próximo evento de salida
    if len(queue) > 0:
        next_departure = time + generate_random_number(departure_interval)
        queue_df.loc[len(queue_df) - 1, "Hora sig. fin de servicio"] = next_departure
    else:
        # Si la cola está vacía, el servidor puede tomar un descanso
        break_time = time + generate_random_number(break_interval)
        queue_df.loc[len(queue_df) - 1, "Hora sig. fin de servicio"] = break_time


# Simula los eventos de cola
queue = []

# Inicializa la cola con el tamaño inicial
queue.extend([0] * initial_queue_size)
queue_df.loc[len(queue_df)] = [0, "", len(queue), "", ""]

next_arrival = generate_random_number(arr_interval)
next_departure = float("inf")  # Inicialmente no hay servicio en curso
on_break = False  # Inicialmente el servidor no está en descanso

# Bucle principal de la simulación
for t in range(1, queue_duration + 1):
    if t == next_arrival:
        handle_arrival(t, queue, arr_interval, serv_interval)
        next_arrival += generate_random_number(arr_interval)

        # Si no hay un servicio en curso, programar el próximo evento de salida
        if next_departure == float("inf"):
            next_departure = t + generate_random_number(serv_interval)
            queue_df.loc[len(queue_df) - 1, "Hora sig. fin de servicio"] = next_departure

    if t == next_departure and not on_break:
        handle_departure(t, queue, serv_interval, break_interval)

        # El servidor retoma el servicio después del descanso
        if t >= next_departure:
            next_departure = float("inf")
            on_break = False

    # Actualiza los tiempos de llegada en el dataframe
    queue_df.loc[len(queue_df) - 1, "Hora sig. llegada"] = next_arrival if t < next_arrival else ""

# Reinicia el índice del dataframe
queue_df.reset_index(drop=True, inplace=True)

# Convierte las columnas del dataframe a ints, y se encarga de los strings vacíos
queue_df["Hora actual"] = queue_df["Hora actual"].astype(int)
queue_df["Hora sig. llegada"] = queue_df["Hora sig. llegada"].apply(lambda x: int(x) if x else "")
queue_df["Hora sig. fin de servicio"] = queue_df["Hora sig. fin de servicio"].apply(lambda x: int(x) if x else "")

# Aplica la función de formateo de tiempo a las columnas de tiempo
queue_df["Hora actual"] = queue_df["Hora actual"].apply(format_time)
queue_df["Hora sig. llegada"] = queue_df["Hora sig. llegada"].apply(format_time)
queue_df["Hora sig. fin de servicio"] = queue_df["Hora sig. fin de servicio"].apply(format_time)

# Muestra el dataframe cuando se hace clic al botón
if st.button("Simular"):
    st.dataframe(queue_df)