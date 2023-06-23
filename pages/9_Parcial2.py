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
    2. Haga clic en el botón **'Simular'** para generar la tabla de simulación
    """
)

# Mostrar parámetros en la barra lateral
with st.sidebar:
    st.header("⌨️")
    st.subheader("Parámetros")

    # Slider para el intervalo entre llegadas de clientes
    arrival_rate = st.slider(
        "Intervalo de tiempo entre llegadas de piezas (seg)",
        10, 20, (10, 20)
    )
    # Slider para el tiempo de producción de cada pieza
    service_rate = st.slider(
        "Tiempo de producción por pieza (seg)",
        1, 20, 10
    )
    # Slider para el intervalo de mantenimiento
    maintenance_interval = st.slider(
        "Intervalo de tiempo para el mantenimiento (seg)",
        300, 3600, 3600
    )
    # Duración del mantenimiento
    maintenance_duration = st.slider(
        "Duración del mantenimiento (seg)",
        60, 600, 300
    )
    # Entrada para la duración de simulación
    sim_time = st.number_input(
        "Tiempo de simulación (seg)",
        min_value=1, value=20
    )


def generar_intervalo_llegada(intervalo):
    """Genera un intervalo de llegada aleatorio dentro del intervalo dado"""
    return random.randint(intervalo[0], intervalo[1])


def llegada_pieza(env, server, intervalo_llegada, tiempo_produccion, tiempo_total, contador_piezas, tiempo_espera, piezas_producidas, data):
    while tiempo_total < sim_time:
        # Evento de llegada de pieza
        yield env.timeout(generar_intervalo_llegada(intervalo_llegada))
        intervalo_llegada = generar_intervalo_llegada(intervalo_llegada)
        tiempo_total += intervalo_llegada

        if tiempo_produccion == 0:
            tiempo_produccion = 10

            if contador_piezas > 0:
                contador_piezas -= 1
                tiempo_espera += tiempo_total - tiempo_espera
                piezas_producidas += 1
        else:
            contador_piezas += 1

        # Grabar evento de llegada de pieza en el DataFrame
        data.append([tiempo_total, 'Llegada de pieza', contador_piezas, tiempo_espera, piezas_producidas])

    # Completar el servicio de las piezas restantes
    while contador_piezas > 0:
        tiempo_total += 1

        if tiempo_produccion > 0:
            tiempo_produccion -= 1

        if tiempo_produccion == 0:
            contador_piezas -= 1
            tiempo_espera += tiempo_total - tiempo_espera
            piezas_producidas += 1

        # Grabar evento de fin de servicio en el DataFrame
        data.append([tiempo_total, 'Fin de servicio', contador_piezas, tiempo_espera, piezas_producidas])


def mantenimiento(env, server, tiempo_total, intervalo_mantenimiento, duracion_mantenimiento, data):
    while tiempo_total < sim_time:
        yield env.timeout(intervalo_mantenimiento)
        st.write("Realizando mantenimiento...")
        st.write(f"Número de piezas producidas hasta el momento: {data[-1][4]}")
        st.write("---------------------------------------")
        yield env.timeout(duracion_mantenimiento)
        st.write("¡Mantenimiento completado!")


def simulate_queue(arrival_rate, service_rate, maintenance_interval, maintenance_duration, sim_time):
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=1)

    data = [['Tiempo actual', 'Tipo de evento', 'Tamaño de cola', 'Tiempo de espera acumulado', 'Piezas producidas']]

    tiempo_total = 0
    intervalo_llegada = generar_intervalo_llegada(arrival_rate)
    tiempo_produccion = 0
    contador_piezas = 0
    tiempo_espera = 0
    piezas_producidas = 0

    # Proceso de llegada de piezas
    env.process(llegada_pieza(env, server, intervalo_llegada, tiempo_produccion, tiempo_total, contador_piezas, tiempo_espera, piezas_producidas, data))

    # Proceso de mantenimiento
    if maintenance_interval <= sim_time:
        env.process(mantenimiento(env, server, tiempo_total, maintenance_interval, maintenance_duration, data))

    # Ejecutar la simulación hasta sim_time
    env.run(until=sim_time)

    # Convertir la lista de datos a un DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    df['Tiempo actual'] = pd.to_datetime(df['Tiempo actual'], unit='s')
    df['Tiempo actual'] = df['Tiempo actual'].dt.strftime('%H:%M:%S')

    return df


# Realizar simulación
if st.button('Simular'):
    df = simulate_queue(arrival_rate, service_rate, maintenance_interval, maintenance_duration, sim_time)
    st.dataframe(df)
