import streamlit as st
import datetime as dt

# Función para simular la llegada de clientes
def llegadas(ps, q, horaActual, deltaLLegadas):
    if ps == 0:
        ps = 1
    else:
        q += 1

    # Generar horario de próxima llegada
    horaProximaLlegada = horaActual + dt.timedelta(seconds=deltaLLegadas)
    
    return ps, q, horaActual, horaProximaLlegada

# Función para simular el fin de servicio
def finservicio(ps, q, horaActual, deltaFS):
    if q > 0:
        ps = 1
        q -= 1
        # Calcular próximo fin de servicio
        horaProximoFinServicio = horaActual + dt.timedelta(seconds=deltaFS)
    else:
        ps = 0
        horaProximoFinServicio = None
    
    return ps, q, horaActual, horaProximoFinServicio

# Configuración de la interfaz de Streamlit
st.title('Simulación de Sistema de Colas')
st.write('Ingrese las condiciones iniciales para iniciar la simulación')

# Entrada manual de las condiciones iniciales
inicio_simulacion = st.text_input('Ingrese la hora de inicio de la simulación (HH:MM)', value='08:00')
horaActual = dt.datetime.strptime(inicio_simulacion, '%H:%M')

ps_estado = st.radio('¿El puesto de servicio está ocupado al inicio de la simulación?', ('Sí', 'No'))
ps = 1 if ps_estado == 'Sí' else 0

deltaLLegadas = st.slider('Intervalo de llegada de clientes (segundos)', min_value=1, max_value=60, value=45)
deltaFS = st.slider('Duración del servicio (segundos)', min_value=1, max_value=60, value=40)

# Simulación del sistema de colas
results = []
iterations = st.number_input('Ingrese la cantidad de iteraciones de simulación', min_value=1, value=10, step=1)

for _ in range(iterations):
    ps, q, horaActual, horaProximaLlegada = llegadas(ps, q, horaActual, deltaLLegadas)
    results.append((horaActual, horaProximaLlegada, q, 'Ocupado' if ps == 1 else 'Desocupado'))
    
    if horaProximaLlegada and (not horaProximoFinServicio or horaProximaLlegada < horaProximoFinServicio):
        horaActual = horaProximaLlegada
    else:
        ps, q, horaActual, horaProximoFinServicio = finservicio(ps, q, horaActual, deltaFS)
        horaActual = horaProximoFinServicio

# Mostrar resultados en una tabla
st.header('Resultados de la simulación')
st.write('Hora Actual | Hora Próxima Llegada | Cantidad de Clientes en Cola | Estado del Puesto de Servicio')
for result in results:
    st.write(result)
