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

# Mostrar parámetros en la barra lateral
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

# Crea un dataframe vacío para los eventos de la cola
queue_df = pd.DataFrame(columns=["Hora actual", "Evento", "Clientes en cola", "Hora sig. llegada", "Hora sig. fin de servicio"])

# Definir función para manejar llegadas
def handle_arrival(time, queue, arrival_interval):
    """Añade un cliente a la cola cuando el evento es de llegada."""
    queue.append(time)
    queue_df.loc[len(queue_df)] = [time, "Llegada", len(queue), "", ""]

# Definir función para manejar salidas
def handle_departure(time, queue, departure_interval):
    """Quita un cliente de la cola cuando el evento es de salida."""
    if len(queue) > 0:
        queue.pop(0)
    queue_df.loc[len(queue_df)] = [time, "Fin de servicio", len(queue), "", ""]

# Simula los eventos de cola
queue = []

# Inicializa la cola con el tamaño inicial
queue.extend([0] * initial_queue_size)
queue_df.loc[len(queue_df)] = [0, "", len(queue), "", ""]

next_arrival = generate_random_number(arr_interval)
next_departure = generate_random_number(serv_interval)

# Bucle principal de la simulación
for t in range(1, queue_duration + 1):  # Salta la primera fila
    if t == next_arrival:
        handle_arrival(t, queue, next_arrival)
        next_arrival += generate_random_number(arr_interval)
    if t == next_departure:
        handle_departure(t, queue, next_departure)
        next_departure += generate_random_number(serv_interval)

    # Actualiza los tiempos de salida y llegada en el dataframe
    queue_df.loc[len(queue_df) - 1, "Hora sig. llegada"] = next_arrival if t < next_arrival else ""
    queue_df.loc[len(queue_df) - 1, "Hora sig. fin de servicio"] = next_departure if t < next_departure else ""

# Reinicia el índice del dataframe
queue_df.reset_index(drop=True, inplace=True)

# Convierte las columnas del dataframe a ints, y se encarga de los strings vacíos
queue_df["Hora actual"] = queue_df["Hora actual"].astype(int)
queue_df["Hora sig. llegada"] = queue_df["Hora sig. llegada"].apply(lambda x: int(x) if x else '')
queue_df["Hora sig. fin de servicio"] = queue_df["Hora sig. fin de servicio"].apply(lambda x: int(x) if x else '')

# Aplica la función de formateo de tiempo a las columnas de tiempo
queue_df["Hora actual"] = queue_df["Hora actual"].apply(format_time)
queue_df["Hora sig. llegada"] = queue_df["Hora sig. llegada"].apply(format_time)
queue_df["Hora sig. fin de servicio"] = queue_df["Hora sig. fin de servicio"].apply(format_time)

# Muestra el dataframe cuando se hace clic al botón
if st.button('Simular'):
    st.dataframe(queue_df)