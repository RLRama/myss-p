import streamlit as st
import random
import simpy
import pandas as pd

# Configurar página
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
    st.subheader("Configurar parámetros")
    INTERVAL_CUSTOMERS = st.number_input(
        "Tiempo promedio entre llegadas de clientes `(min)`",
        min_value=1.00
    )
    t_serv = st.number_input(
        "Tiempo promedio de servicio `(min)`",
        min_value=1.00
    )
    NEW_CUSTOMERS = st.number_input(
        "Clientes generados",
        min_value=1
    )
    t = st.number_input(
        "Duración de la simulación `(min)`",
        min_value=1.00
    )
    RANDOM_SEED = st.number_input(
        "Semilla para generar números aleatorios",
        value=9999, min_value=1
    )

MIN_PATIENCE = 9999999999
MAX_PATIENCE = 9999999999

st.markdown(
    """
    # Situación I
    ## Descripción
    - Obedece al problema n° 1
    - Clientes que llegan individualmente en intervalos aleatorios
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempos de prestación de servicios aleatorios
    - El servidor no abandona el puesto de servicio

    ## Uso
    - Configure parámetros usando la **👈 barra lateral** para dar valores
    - Presione el botón **'Simular'** para mostrar la tabla de simulación generada
    """
)

def source(env, number, interval, counter, results):
    """Source generates customers randomly"""
    for i in range(number):
        c = customer(env, 'Cliente %04d' % i, counter, time_in_bank=12.0, results=results)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)

def customer(env, name, counter, time_in_bank, results):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    results.append((arrive, name, 'Evento de llegada'))

    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        # Esperar al contador o terminar el proceso
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            # Contador
            results.append((env.now, name, 'Esperó %04.2f min' % wait))

            tib = random.expovariate(1.0 / time_in_bank)
            yield env.timeout(tib)
            results.append((env.now, name, 'Fin de servicio'))

        else:
            # No se usa porque no hay abandono
            results.append((env.now, name, 'RENEGED after %6.3f' % wait))

# Configurar e iniciar simulación
random.seed(RANDOM_SEED)
env = simpy.Environment()

if st.button('Simular'):
    # Iniciar procesos y ejecutar
    results = []
    counter = simpy.Resource(env, capacity=1)
    env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter, results))
    env.run()

    # Mostrar resultados en una tabla
    df = pd.DataFrame(results, columns=['Tiempo', 'N° de cliente', 'Detalle de evento'])
    st.table(df)
else:
    st.text('')
