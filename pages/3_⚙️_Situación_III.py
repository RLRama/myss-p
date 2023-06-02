import streamlit as st
import datetime as dt
import random
import pandas as pd

# Función para simular la llegada de clientes
def llegada_cliente(puesto_servicio, cola_clientes, hora_actual):
    tiempo_llegada = random.randint(1, 10)  # Generar tiempo de llegada aleatorio
    hora_proxima_llegada = hora_actual + dt.timedelta(seconds=tiempo_llegada)

    # Verificar si el puesto de servicio está ocupado
    if puesto_servicio == "ocupado":
        # Agregar al cliente a la cola
        cola_clientes += 1
    else:
        # Atender al cliente inmediatamente
        tiempo_servicio = random.randint(1, 10)  # Generar tiempo de servicio aleatorio
        hora_proximo_fin_servicio = hora_actual + dt.timedelta(seconds=tiempo_servicio)
        puesto_servicio = "ocupado"

        # Mostrar evento de fin de servicio
        results.append((hora_actual, hora_proxima_llegada, hora_proximo_fin_servicio, cola_clientes, puesto_servicio))

        # Mostrar evento de fin de servicio en la tabla
        st.write(f"[{hora_actual.strftime('%H:%M:%S')}] Fin de servicio: Cliente atendido.")

    # Mostrar evento de llegada de cliente
    results.append((hora_actual, hora_proxima_llegada, None, cola_clientes, puesto_servicio))

    # Mostrar evento de llegada de cliente en la tabla
    st.write(f"[{hora_actual.strftime('%H:%M:%S')}] Llegada de cliente: Cliente llega al sistema.")

    return puesto_servicio, cola_clientes, hora_proxima_llegada

# Configuración de la interfaz de Streamlit
st.title('Simulación de Sistema de Colas')
st.write('Ingrese las condiciones iniciales para iniciar la simulación')

# Entrada manual de las condiciones iniciales
inicio_simulacion = st.text_input('Ingrese la hora de inicio de la simulación (HH:MM:SS)', value='08:00:00')
hora_actual = dt.datetime.strptime(inicio_simulacion, '%H:%M:%S')

puesto_servicio_estado = st.radio('¿El puesto de servicio está ocupado al inicio de la simulación?', ('Sí', 'No'))
puesto_servicio = "ocupado" if puesto_servicio_estado == 'Sí' else "desocupado"

cola_clientes = st.number_input('Ingrese la cantidad de clientes en cola', min_value=0, value=0, step=1)

num_iteraciones = st.number_input('Ingrese la cantidad de iteraciones de la simulación', min_value=1, value=10, step=1)

# Simulación del sistema de colas
results = []
for _ in range(num_iteraciones):
    puesto_servicio, cola_clientes, hora_proxima_llegada = llegada_cliente(puesto_servicio, cola_clientes, hora_actual)

    # Determinar la hora actual para la siguiente iteración
    if hora_proxima_llegada and hora_proxima_llegada < hora_actual:
        hora_actual = hora_proxima_llegada
    else:
        hora_actual += dt.timedelta(seconds=1)

# Convertir los resultados en un DataFrame
df_results = pd.DataFrame(results, columns=['Hora Actual', 'Hora Próxima Llegada', 'Hora Próximo Fin de Servicio',
                                             'Cantidad de Clientes en Cola', 'Estado del Puesto de Servicio'])

# Mostrar resultados en una tabla
st.header('Resultados de la simulación')
st.dataframe(df_results)
