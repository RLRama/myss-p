import streamlit as st
import datetime as dt

# Función para simular la llegada de clientes
def generar_llegada(ps, q, hora_actual, delta_llegadas):
    if ps == 0:
        ps = 1
    else:
        q += 1

    # Generar horario de próxima llegada
    hora_proxima_llegada = hora_actual + dt.timedelta(seconds=delta_llegadas)
    
    return ps, q, hora_actual, hora_proxima_llegada

# Función para simular el fin de servicio
def fin_servicio(ps, q, hora_actual, delta_fs):
    if q > 0:
        ps = 1
        q -= 1
        # Calcular próximo fin de servicio
        hora_proximo_fin_servicio = hora_actual + dt.timedelta(seconds=delta_fs)
    else:
        ps = 0
        hora_proximo_fin_servicio = None
    
    return ps, q, hora_actual, hora_proximo_fin_servicio

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
iterations = st.number_input('Ingrese la cantidad de iteraciones de simulación', min_value=1, value=10, step=1)

for _ in range(iterations):
    ps, q, hora_actual, hora_proxima_llegada = generar_llegada(ps, q, hora_actual, delta_llegadas)
    results.append((hora_actual, hora_proxima_llegada, q, 'Ocupado' if ps == 1 else 'Desocupado'))
    
    if hora_proxima_llegada and (not hora_proximo_fin_servicio or hora_proxima_llegada < hora_proximo_fin_servicio):
        hora_actual = hora_proxima_llegada
    else:
        ps, q, hora_actual, hora_proximo_fin_servicio = fin_servicio(ps, q, hora_actual, delta_fs)
        hora_actual = hora_proximo_fin_servicio

# Mostrar resultados en una tabla
st.header('Resultados de la simulación')
st.write('Hora Actual | Hora Próxima Llegada | Cantidad de Clientes en Cola | Estado del Puesto de Servicio')
for result in results:
    st.write(result)
