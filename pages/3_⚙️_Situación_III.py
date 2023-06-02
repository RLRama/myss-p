import streamlit as st
import datetime as dt
import random

# Función para simular la llegada de clientes
def llegadas(ps, q, horaActual, deltaLLegadas):
    horaProximaLlegada = horaActual + dt.timedelta(seconds=deltaLLegadas)
    t_llegada = random.randint(1, 10)  # Generar tiempo de llegada aleatorio

    # Calcular el próximo fin de servicio si el puesto de servicio está libre
    if ps == 0:
        t_s = random.randint(1, 10)  # Generar tiempo de servicio aleatorio
        horaProximoFinServicio = horaActual + dt.timedelta(seconds=t_s)
    else:
        t_s = 0
        horaProximoFinServicio = None

    return horaProximaLlegada, horaProximoFinServicio, t_llegada, t_s


# Función para simular el fin de servicio
def finservicio(ps, q, horaActual, deltaFS):
    if q > 0:
        ps = 1
        q -= 1
        t_s = random.randint(1, 10)  # Generar tiempo de servicio aleatorio
        horaProximoFinServicio = horaActual + dt.timedelta(seconds=t_s)
    else:
        ps = 0
        t_s = 0
        horaProximoFinServicio = None

    return horaProximoFinServicio, t_s


# Configuración de la interfaz de Streamlit
st.title('Simulación de Sistema de Colas')
st.write('Ingrese las condiciones iniciales para iniciar la simulación')

# Entrada manual de las condiciones iniciales
inicio_simulacion = st.text_input('Ingrese la hora de inicio de la simulación (HH:MM:SS)', value='08:00:00')
horaActual = dt.datetime.strptime(inicio_simulacion, '%H:%M:%S')

ps_estado = st.radio('¿El puesto de servicio está ocupado al inicio de la simulación?', ('Sí', 'No'))
ps = 1 if ps_estado == 'Sí' else 0

deltaLLegadas = st.slider('Intervalo de llegada de clientes (segundos)', min_value=1, max_value=60, value=45)
deltaFS = st.slider('Duración del servicio (segundos)', min_value=1, max_value=60, value=40)

# Simulación del sistema de colas
results = []
for _ in range(10):  # Realizar 10 iteraciones de simulación
    horaProximaLlegada, horaProximoFinServicio, t_llegada, t_s = llegadas(ps, q, horaActual, deltaLLegadas)

    # Guardar los resultados de cada iteración en una lista
    results.append((horaActual.strftime('%H:%M:%S'), horaProximaLlegada.strftime('%H:%M:%S'),
                    horaProximoFinServicio.strftime('%H:%M:%S') if horaProximoFinServicio else None,
                    q, 'Ocupado' if ps == 1 else 'Desocupado'))

    # Actualizar las variables para la siguiente iteración
    horaActual = horaProximaLlegada

    if horaProximoFinServicio and horaProximoFinServicio <= horaActual:
        horaProximoFinServicio, t_s = finservicio(ps, q, horaActual, deltaFS)
        horaActual = horaProximoFinServicio

# Muestra Resultados
st.header('Resultados de la simulación')
st.write('Hora Actual | Hora Próxima Llegada | Hora Próximo Fin de Servicio | Cantidad de Clientes en Cola | Estado del Puesto de Servicio')
for result in results:
    st.write(result)
