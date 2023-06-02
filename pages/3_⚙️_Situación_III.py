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
        ps = 1  # Ocupar el puesto de servicio
    else:
        t_s = 0
        horaProximoFinServicio = None

    return horaProximaLlegada, horaProximoFinServicio, t_llegada, t_s, ps


# Función para simular el fin de servicio
def finservicio(ps, q, horaActual, deltaFS):
    if q > 0:
        q -= 1  # Atender al próximo cliente en cola
        t_s = random.randint(1, 10)  # Generar tiempo de servicio aleatorio
        horaProximoFinServicio = horaActual + dt.timedelta(seconds=t_s)
    else:
        ps = 0  # Liberar el puesto de servicio
        horaProximoFinServicio = None

    return horaProximoFinServicio, t_s, ps


# Configuración de la interfaz de Streamlit
st.title('Simulación de Sistema de Colas')
st.write('Ingrese las condiciones iniciales para iniciar la simulación')

# Entrada manual de las condiciones iniciales
inicio_simulacion = st.text_input('Ingrese la hora de inicio de la simulación (HH:MM:SS)', value='08:00:00')
horaActual = dt.datetime.strptime(inicio_simulacion, '%H:%M:%S')

ps_estado = st.radio('¿El puesto de servicio está ocupado al inicio de la simulación?', ('Sí', 'No'))
ps = 1 if ps_estado == 'Sí' else 0

q = st.number_input('Ingrese la cantidad de clientes en cola', min_value=0, value=0, step=1)

deltaLLegadas = st.slider('Intervalo de llegada de clientes (segundos)', min_value=1, max_value=60, value=45)
deltaFS = st.slider('Duración del servicio (segundos)', min_value=1, max_value=60, value=40)

num_iteraciones = st.number_input('Ingrese la cantidad de iteraciones de la simulación', min_value=1, value=10, step=1)

# Simulación del sistema de colas
results = []
for _ in range(num_iteraciones):  # Realizar las iteraciones de simulación especificadas
    horaProximaLlegada, horaProximoFinServicio, t_llegada, t_s, ps = llegadas(ps, q, horaActual, deltaLLegadas)

    # Guardar los resultados de cada iteración en una lista
    results.append((horaActual, horaProximaLlegada, horaProximoFinServicio, q, 'Ocupado' if ps == 1 else 'Desocupado'))

    # Determinar la hora actual para la siguiente iteración
    if horaProximaLlegada and horaProximoFinServicio:
        horaActual = min(horaProximaLlegada, horaProximoFinServicio)
    elif horaProximaLlegada:
        horaActual = horaProximaLlegada
    elif horaProximoFinServicio:
        horaActual = horaProximoFinServicio

    if horaProximoFinServicio and horaProximoFinServicio <= horaProximaLlegada:
        horaProximoFinServicio, t_s, ps = finservicio(ps, q, horaActual, deltaFS)
        horaActual = horaProximoFinServicio
        q += 1  # Añadir al cliente atendido a la cola

# Muestra Resultados
st.header('Resultados de la simulación')
st.write('Hora Actual | Hora Próxima Llegada | Hora Próximo Fin de Servicio | Cantidad de Clientes en Cola | Estado del Puesto de Servicio')

# Crear una lista de diccionarios para mostrar los resultados en forma de tabla
table_data = []
for result in results:
    table_data.append({
        'Hora Actual': result[0].strftime('%H:%M:%S'),
        'Hora Próxima Llegada': result[1].strftime('%H:%M:%S') if result[1] else '',
        'Hora Próximo Fin de Servicio': result[2].strftime('%H:%M:%S') if result[2] else '',
        'Cantidad de Clientes en Cola': result[3],
        'Estado del Puesto de Servicio': result[4]
    })

# Mostrar la tabla con los resultados
st.table(table_data)
