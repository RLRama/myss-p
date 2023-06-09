import streamlit as st
import random
import pandas as pd

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
    ## Situación Parcial
    ### Descripción
    - Tiempo de llegadas de piezas aleatorio (dentro de un intervalo dado) [10-20 Segundos]
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempo de prestación de servicio 10 Segundos
    - El servidor abandona el servicio cada 1 hora y toma descanso de 5 minutos

    ### Uso
    1. Configure parámetros usando la **👈 barra lateral**
    2. Haga clic el botón **'Simular'** para generar la tabla de simulación
    """
)

# Mostrar parámetros en la barra lateral
import random
import pandas as pd
import streamlit as st

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

    # Entrada para la duración de simulación
    queue_duration = st.number_input(
        "Tiempo de simulación (seg)",
        min_value=1, value=20
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
        return ''
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# Crea una lista de diccionarios para los eventos de la cola
queue_events = []

# Definir función para manejar llegadas
def handle_arrival(time, queue):
    """Añade un cliente a la cola cuando el evento es de llegada."""
    queue.append(time)
    queue_events.append({
        "Hora actual": time,
        "Evento": "Llegada",
        "Clientes en cola": len(queue),
        "Hora sig. llegada": "",
        "Hora sig. fin de servicio": ""
    })


# Definir función para manejar salidas
def handle_departure(time, queue):
    """Quita un cliente de la cola cuando el evento es de salida."""
    if len(queue) > 0:
        queue.pop(0)
    queue_events.append({
        "Hora actual": time,
        "Evento": "Fin de servicio",
        "Clientes en cola": len(queue),
        "Hora sig. llegada": "",
        "Hora sig. fin de servicio": ""
    })


# Simula los eventos de cola
queue = []

# Inicializa la cola con el tamaño inicial
queue.extend([0] * initial_queue_size)
queue_events.append({
    "Hora actual": 0,
    "Evento": "",
    "Clientes en cola": len(queue),
    "Hora sig. llegada": "",
    "Hora sig. fin de servicio": ""
})

next_arrival = generate_random_number(arr_interval)
next_departure = generate_random_number(serv_interval)

# Variable para seguir el tiempo continuo de serv.
continuous_service_time = 0

# Variable para almacenar duración de interrupciones
interruption_duration = 300  # 5 minutos en segundos

# Bucle principal de la simulación
for t in range(1, queue_duration + 1):  # Salta la primera fila
    if t == next_arrival:
        handle_arrival(t, queue)
        next_arrival += generate_random_number(arr_interval)

    if t == next_departure:
        continuous_service_time += 1  # Incrementar el contador de t. continuo
        handle_departure(t, queue)

        if continuous_service_time >= 3600:  # Comprobar si el tiempo continuo llego a 3600 s (1 h.)
            continuous_service_time = 0  # Reiniciar contador de tiempo continuo de operación
            interruption_time = t + interruption_duration  # Calcular tiempo de interrupción
            queue_events.append({
                "Hora actual": interruption_time,
                "Evento": "Interrupción",
                "Clientes en cola": len(queue),
                "Hora sig. llegada": "",
                "Hora sig. fin de servicio": ""
            })
            next_departure = interruption_time + generate_random_number(serv_interval)  # Programar siguiente salida tras interrupción
        else:
            next_departure += generate_random_number(serv_interval)  # Schedule next departure as usual

            if continuous_service_time % 3600 == 0:  # Revisar si tiempo continuo es multiplo de 1 hora
                interruption_time = t + interruption_duration  # Calcular tiempo de interrupción
                queue_events.append({
                    "Hora actual": interruption_time,
                    "Evento": "Interrupción",
                    "Clientes en cola": len(queue),
                    "Hora sig. llegada": "",
                    "Hora sig. fin de servicio": ""
                })
                next_departure = interruption_time + generate_random_number(serv_interval)  # Programar siguiente salida tras interrupción

    else:
        continuous_service_time = 0  # Reiniciar contador de tiempo continuo de operación

    # Actualiza los tiempos de salida y llegada en el último evento de la cola
    queue_events[-1]["Hora sig. llegada"] = format_time(next_arrival) if t < next_arrival else ""
    queue_events[-1]["Hora sig. fin de servicio"] = format_time(next_departure) if t < next_departure else ""

# Crea el dataframe a partir de la lista de diccionarios
queue_df = pd.DataFrame(queue_events)

# Reinicia el índice del dataframe
queue_df.reset_index(drop=True, inplace=True)

# Aplica la función de formateo de tiempo a las columnas de tiempo
time_columns = ["Hora actual", "Hora sig. llegada", "Hora sig. fin de servicio"]
queue_df[time_columns] = queue_df[time_columns].applymap(format_time)

# Muestra el dataframe cuando se hace clic al botón
if st.button('Simular'):
    st.dataframe(queue_df)
