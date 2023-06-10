import simpy
import random
import pandas as pd
import streamlit as st

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
    ## Situación V
    ### Descripción
    - Problema V
    - Tiempo de llegadas de cliente aleatorio (dentro de un intervalo dado)
    - Colas FIFO (los clientes son atendidos en el orden que llegan)
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
    # Entrada para el intervalo de retraso por la zona de seguridad
    delay_mean = st.slider(
        "Intervalo de de retraso por la zona de seguridad (seg)",
        1, 100, (25, 75)
    )
    # Entrada para el tiempo de trabajo
    service_time_mean = st.slider(
        "Intervalo de tiempo de trabajo (seg)",
        1, 100, (25, 75)
    )
    # Entrada para el número de clientes
    num_customers = st.number_input(
        "Número de clientes",
        min_value=1, value=20
    )

def generate_random_number(interval):
    """Genera un número al azar dentro del intervalo dado"""
    lower_bound = interval[0]
    upper_bound = interval[1]
    return random.randint(lower_bound, upper_bound)

class Customer:
    def __init__(self, env, name, service_time):
        self.env = env
        self.name = name
        self.service_time = service_time

def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'

def customer_generator(env, server, delay_mean, service_time_mean, num_customers, df):
    for i in range(num_customers):
        customer = Customer(env, f'Cliente {i}', generate_random_number(service_time_mean))
        env.process(customer_arrival(env, server, customer, df))
        yield env.timeout(generate_random_number(delay_mean))

def customer_arrival(env, server, customer, df):
    arrival_time = env.now
    df.loc[len(df)] = [customer.name, 'Llegada', seconds_to_hms(arrival_time), None]

    with server.request() as req:
        yield req

        wait_time = env.now - arrival_time
        df.loc[len(df)] = [customer.name, 'Inicio de servicio', seconds_to_hms(env.now), seconds_to_hms(wait_time)]

        yield env.timeout(customer.service_time)
        df.loc[len(df)] = [customer.name, 'Fin de servicio', seconds_to_hms(env.now), None]

# Crear el entorno de simulación, recuros de servidor y dataframe
env = simpy.Environment()
server = simpy.Resource(env, capacity=1)
df = pd.DataFrame(columns=['Cliente', 'Tipo de evento', 'Hora actual', 'Tiempo de espera'])

# Iniciar el proceso de generador de clientes
env.process(customer_generator(env, server, delay_mean, service_time_mean, num_customers, df))

# Mostrar el dataframe
if st.button('Simular'):
    # Ejecutar la simulación
    env.run()
    st.dataframe(df)