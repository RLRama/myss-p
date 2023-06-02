import streamlit as st
import datetime as dt
import random

# Función para simular la llegada de clientes
def generar_llegada(ps, q, hora_actual, delta_llegadas):
    hora_proxima_llegada = hora_actual + dt.timedelta(seconds=delta_llegadas)
    t_llegada = random.randint(1, 10)  # Generar tiempo de llegada aleatorio

    if ps == 0:
        ps = 1
    else:
        q += 1

    return ps, q, hora_actual, hora_proxima_llegada


# Función para simular el fin de servicio
def fin_servicio(ps, q, hora_actual, hora_proxima_llegada, delta_fs):
    if q > 0:
        ps = 1
        q -= 1
        hora_proximo_fin_servicio = hora_actual + dt.timedelta(seconds=delta_fs)
    else:
        ps = 0
        hora_proximo_fin_servicio = None

    return ps, q, hora_actual, hora_proxima_llegada, hora_proximo_fin_servicio


# Configuración de la interfaz de Streamlit
st.title('Simulación de Sistema de Colas')
st.write('Ingrese las condiciones iniciales para iniciar la simulación')

# Entrada manual de las condiciones iniciales
inicio_simulacion = st.text_input('Ingrese la hora de inicio de la simulación (HH:MM)', value='08:00')
hora_actual = dt.datetime.strptime(inicio_simulacion, '%H:%M')

ps_estado = st.radio('¿El puesto de servicio está ocupado al inicio de la simulación?', ('Sí', 'No'))
ps = 1 if ps_estado == 'Sí' else 0

delta_llegadas = st.slider('Intervalo de llegada de clientes (segundos)', min_value=1, max_value=60, value=45)
delta_fs = st.slider('Duración del servicio (segundos)', min_value=1, max_value=60, value=40)

# Simulación del sistema de colas
results = []
iterations = st.number_input('Ingrese la cantidad de iteraciones de simulación', value=10, min_value=1, step=1)
for _ in range(iterations):
    ps, q, hora_actual, hora_proxima_llegada = generar_llegada(ps, q, hora_actual, delta_llegadas)

    # Guardar los resultados de cada iteración en una lista
    results.append((hora_actual, hora_proxima_llegada, q, 'Ocupado' if ps == 1 else 'Desocupado'))

    if hora_proxima_llegada is not None and (hora_proximo_fin_servicio is None or hora_proxima_llegada <= hora_proximo_fin_servicio):
        hora_actual = hora_proxima_llegada
    else:
        ps, q, hora_actual, hora_proxima_llegada, hora_proximo_fin_servicio = fin_servicio(ps, q, hora_actual, hora_proxima_llegada, delta_fs)
        hora_actual = hora_proximo_fin_servicio

# Muestra Resultados
st.header('Resultados de la simulación')
st.write('Hora Actual | Hora Próxima Llegada | Cantidad de Clientes en Cola | Estado del Puesto de Servicio')
for result in results:
    st.write(result)
