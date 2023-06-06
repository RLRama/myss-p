import streamlit as st
import queue
import random
import simpy
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
    ## Situación IV
    ### Descripción
    - Problema IV
    - Tiempo de llegadas de cliente aleatorio (dentro de un intervalo dado)
    - Colas FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempo de prestación de servicio aleatorio (dentro de un intervalo dado)
    - El servidor no abandona el puesto de servicio
    - Hay dos tipos de clientes: los comunes y los de prioridad
    - Los clientes de prioridad conforman otra cola que tiene prioridad de atención

    ### Uso
    1. Configure parámetros usando la **👈 barra lateral**
    2. Haga clic el botón **'Simular'** para generar la tabla de simulación
    """
)

# Mostrar parámetros en la barra lateral
with st.sidebar:
    st.header("⌨️")
    st.subheader("Parámetros")
    # Entrada para el intervalo entre llegadas de clientes
    ARRIVAL_RATE = st.slider(
        "Intervalo de tiempo entre llegadas (seg)",
        1, 100, (25, 75)
    )
    # Entrada para el tiempo de trabajo
    SERVICE_RATE = st.slider(
        "Intervalo de tiempo de trabajo (seg)",
        1, 100, (25, 75)
    )
    # Entrada para la duración de simulación
    SIMULATION_TIME = st.number_input(
        "Tiempo de simulación (seg)",
        min_value=1, value=20
    )

def generate_random_number(interval):
    """Genera un número al azar dentro del intervalo dado"""
    lower_bound = interval[0]
    upper_bound = interval[1]
    return random.randint(lower_bound, upper_bound)

class Customer:
    def __init__(self, id, priority=False):
        self.id = id
        self.priority = priority

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    formatted_time = "{:02d}:{:02d}:{:05.2f}".format(int(hours), int(minutes), seconds)
    return formatted_time

def customer_generator(env, priority_queue, regular_queue, events):
    customer_id = 1
    while True:
        # Determinar el tiempo entre llegadas basado en el intervalo
        inter_arrival_time = generate_random_number(ARRIVAL_RATE)
        yield env.timeout(inter_arrival_time)
        
        customer = Customer(customer_id, random.choice([True, False]))
        customer_id += 1
        
        if customer.priority:
            priority_queue.append(customer)
            priority_queue.sort(key=lambda x: x.priority, reverse=True)
        else:
            regular_queue.put(customer)
        
        events.append({
            'Tipo de evento': 'Llegada',
            'ID de cliente': customer.id,
            'Prioridad': customer.priority,
            'Hora actual': format_time(env.now),
            'Cantidad de clientes en cola de prioridad': len(priority_queue),
            'Cantidad de clientes en cola regular': regular_queue.qsize()
        })

def server(env, priority_queue, regular_queue, events):
    while True:
        if priority_queue:
            customer = priority_queue.pop(0)
            service_time = generate_random_number(SERVICE_RATE)
            yield env.timeout(service_time)
            events.append({
                'Tipo de evento': 'Inicio de servicio',
                'ID de cliente': customer.id,
                'Prioridad': customer.priority,
                'Hora actual': format_time(env.now),
                'Cantidad de clientes en cola de prioridad': len(priority_queue),
                'Cantidad de clientes en cola regular': regular_queue.qsize()
            })
            events.append({
                'Tipo de evento': 'Fin de servicio',
                'ID de cliente': customer.id,
                'Prioridad': customer.priority,
                'Hora actual': format_time(env.now),
                'Cantidad de clientes en cola de prioridad': len(priority_queue),
                'Cantidad de clientes en cola regular': regular_queue.qsize()
            })
        elif not regular_queue.empty():
            customer = regular_queue.get()
            service_time = generate_random_number(SERVICE_RATE)
            yield env.timeout(service_time)
            events.append({
                'Tipo de evento': 'Inicio de servicio',
                'ID de cliente': customer.id,
                'Prioridad': customer.priority,
                'Hora actual': format_time(env.now),
                'Cantidad de clientes en cola de prioridad': len(priority_queue),
                'Cantidad de clientes en cola regular': regular_queue.qsize()
            })
            events.append({
                'Tipo de evento': 'Fin de servicio',
                'ID de cliente': customer.id,
                'Prioridad': customer.priority,
                'Hora actual': format_time(env.now),
                'Cantidad de clientes en cola de prioridad': len(priority_queue),
                'Cantidad de clientes en cola regular': regular_queue.qsize()
            })
        else:
            # Si ambas colas están vacías, esperar la llegada de un cliente
            yield env.timeout(1)  # Esperar una unidad de tiempo

# Crear el entorno de simulación
env = simpy.Environment()
priority_queue = []
regular_queue = queue.Queue()
events = []

# Iniciar los procesos
env.process(customer_generator(env, priority_queue, regular_queue, events))
env.process(server(env, priority_queue, regular_queue, events))

# Ejecutar la simulación durante un tiempo fijo de segundos y
# crear un dataframe a partir de los eventos
if st.button('Simular'):
    env.run(until=SIMULATION_TIME)
    df = pd.DataFrame(events)
    st.dataframe(df)