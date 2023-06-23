import streamlit as st
import random
import datetime as dt

# import simpy
# import pandas as pd
# import numpy as np
# import streamlit as st
# import random
# import datetime as dt


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
    ## Situación Parcial
    ### Descripción
    - Tiempo de llegadas de piezas aleatorio (dentro de un intervalo dado) [10-20 Segundos]
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempo de prestación de servicio 10 Segundos
    - El servidor abandona el servicio cada 1 hora y toma descanso de 5 minutos

    ### Uso
    1. Configure parámetros usando la **👈 barra lateral**
    2. Haga clic el botón **'Simular'** para generar la tabla de simulación
    """
)

# Mostrar parámetros en la barra lateral
# with st.sidebar:
#     st.header("⌨️")
#     st.subheader("Parámetros")

#     # Slider para el intervalo entre llegadas de clientes
#     arrival_rate = st.slider(
#         "Intervalo de tiempo entre llegadas de piezas (seg)",
#         10, 20, (10, 20)
#     )
#     # Slider para el tiempo de producción de cada pieza
#     service_rate = st.slider(
#         "Tiempo de producción por pieza (seg)",
#         1, 20, 10
#     )
#     # Slider para el intervalo de mantenimiento
#     maintenance_interval = st.slider(
#         "Intervalo de tiempo para el mantenimiento (seg)",
#         300, 3600, 3600
#     )
#     # Duración del mantenimiento
#     maintenance_duration = st.slider(
#         "Duración del mantenimiento (seg)",
#         60, 600, 300
#     )
#     # Entrada para la duración de simulación
#     sim_time = st.number_input(
#         "Tiempo de simulación (seg)",
#         min_value=1, value=20
#     )


# def generar_intervalo_llegada(intervalo):
#     """Genera un intervalo de llegada aleatorio dentro del intervalo dado"""
#     lower_bound, upper_bound = intervalo
#     return random.randint(lower_bound, upper_bound)


# def llegada_pieza(env, server, intervalo_llegada, tiempo_produccion, tiempo_total, contador_piezas, tiempo_espera, piezas_producidas, data):
#     while tiempo_total < sim_time:
#         # Evento de llegada de pieza
#         yield env.timeout(generar_intervalo_llegada(intervalo_llegada))
#         intervalo_llegada = generar_intervalo_llegada(intervalo_llegada)
#         tiempo_total += intervalo_llegada

#         if tiempo_produccion == 0:
#             tiempo_produccion = 10

#             if contador_piezas > 0:
#                 contador_piezas -= 1
#                 tiempo_espera += tiempo_total - tiempo_espera
#                 piezas_producidas += 1
#         else:
#             contador_piezas += 1

#         # Grabar evento de llegada de pieza en el DataFrame
#         data.append([tiempo_total, 'Llegada de pieza', contador_piezas, tiempo_espera, piezas_producidas])

#         # Comenzar servicio si el servidor está disponible
#         if tiempo_produccion == 10 and server.count == 1:
#             tiempo_produccion -= 1
#             contador_piezas -= 1
#             tiempo_espera += tiempo_total - tiempo_espera
#             piezas_producidas += 1

#             # Grabar evento de inicio de servicio en el DataFrame
#             data.append([tiempo_total, 'Inicio de servicio', contador_piezas, tiempo_espera, piezas_producidas])

#             yield env.timeout(tiempo_produccion)

#             tiempo_total += tiempo_produccion
#             tiempo_produccion = 0

#             # Grabar evento de fin de servicio en el DataFrame
#             data.append([tiempo_total, 'Fin de servicio', contador_piezas, tiempo_espera, piezas_producidas])

#     # Completar el servicio de las piezas restantes
#     while contador_piezas > 0:
#         tiempo_total += 1

#         if tiempo_produccion > 0:
#             tiempo_produccion -= 1

#         if tiempo_produccion == 0:
#             contador_piezas -= 1
#             tiempo_espera += tiempo_total - tiempo_espera
#             piezas_producidas += 1

#         # Grabar evento de fin de servicio en el DataFrame
#         data.append([tiempo_total, 'Fin de servicio', contador_piezas, tiempo_espera, piezas_producidas])


# def mantenimiento(env, server, tiempo_total, intervalo_mantenimiento, duracion_mantenimiento, data):
#     while tiempo_total < sim_time:
#         yield env.timeout(intervalo_mantenimiento)
#         st.write("Realizando mantenimiento...")
#         st.write(f"Número de piezas producidas hasta el momento: {data[-1][4]}")
#         st.write("---------------------------------------")
#         yield env.timeout(duracion_mantenimiento)
#         st.write("¡Mantenimiento completado!")


# def simulate_queue(arrival_rate, service_rate, maintenance_interval, maintenance_duration, sim_time):
#     env = simpy.Environment()
#     server = simpy.Resource(env, capacity=1)

#     data = [['Tiempo actual', 'Tipo de evento', 'Tamaño de cola', 'Tiempo de espera acumulado', 'Piezas producidas']]

#     tiempo_total = 0
#     intervalo_llegada = [arrival_rate[0], arrival_rate[1]]
#     tiempo_produccion = 0
#     contador_piezas = 0
#     tiempo_espera = 0
#     piezas_producidas = 0

#     # Proceso de llegada de piezas
#     env.process(llegada_pieza(env, server, intervalo_llegada, tiempo_produccion, tiempo_total, contador_piezas,
#                               tiempo_espera, piezas_producidas, data))

#     # Proceso de mantenimiento
#     if maintenance_interval <= sim_time:
#         env.process(mantenimiento(env, server, tiempo_total, maintenance_interval, maintenance_duration, data))

#     # Ejecutar la simulación hasta sim_time
#     env.run(until=sim_time)

#     # Convertir la lista de datos a un DataFrame
#     df = pd.DataFrame(data[1:], columns=data[0])
#     df['Tiempo actual'] = pd.to_datetime(df['Tiempo actual'], unit='s')
#     df['Tiempo actual'] = df['Tiempo actual'].dt.strftime('%H:%M:%S')

#     return df


# # Simulación de la cola
# df = simulate_queue(arrival_rate, service_rate, maintenance_interval, maintenance_duration, sim_time)

# # Mostrar el DataFrame con los resultados
# st.subheader("Tabla de simulación")
# st.dataframe(df)

# QGral= QPrio= ZS= PS= T= caso= S= 0
# tLlegadaGrali= tLlegadaGralf= tLlegadaPrioi= tLlegadaPriof= tAtencióni= tAtenciónf= tDescansoi= tDescansof= tTrabajoi= tTrabajof= tAbandonoi= tAbandonof= tZS= contador= 0
# horaActual= horaFinal= SigFinServicio= SigFinZona= SigLlegadaGral= SigLlegadaPrio= SigLlegadaServ= SigSalidaServ= dt.datetime(2000,1,1,0,0,0)

# vAbandono = [horaFinal]
# def VectorInicial():
#     global QGral,PS, T, contador, tLlegadaGrali, tLlegadaGralf, tAtencióni, tAtenciónf ,S, tDescansoi, tDescansof, tTrabajoi, tTrabajof, SigFinServicio, SigLlegadaGral, SigLlegadaServ, SigSalidaServ, horaFinal, horaActual, tAbandonoi, tAbandonof, caso
#     print("Indique el tipo de simulación que quiere hacer:")
#     print("1 - Caso parcial")
#     caso = int(input("caso: "))

#     aux = dt.timedelta(hours=int(input("Ingrese hora de inicio de la simulación: ")))
#     horaActual = horaActual + aux
#     QGral = int(input("Ingrese la cantidad inicial de clientes en cola: "))
#     PS = int(input("Ingrese el estado inicial del puesto de trabajo (ocupado = 1; libre = 0): "))
#     T = int(input("Ingrese la duración de la simulación (en minutos): "))
#     horaFinal = horaActual + dt.timedelta(minutes=T)
#     SigFinServicio= SigFinZona= SigLlegadaGral= SigLlegadaPrio= SigLlegadaServ= SigSalidaServ= vAbandono[0]= horaFinal
    
#     print("Ingrese el intervalo que tarda el puesto de servicio en atender los clientes: ")
#     tAtencióni = int(input("Mínimo: "))
#     tAtenciónf = int(input("Máximo: "))

#     if caso == 1:
#         #-----------Ajuste de vatriables-----------
#         tAtencióni = 10
#         tAtenciónf = 10
#         tLlegadaGrali = 10
#         tLlegadaGralf = 20
#         tDescansoi = 5
#         tDescansof = 5
#         tTrabajoi = 60
#         tTrabajof = 60
#     else:
#         print("Error")

# def LlegadaCliente(case):
#     a=random.randint(tAtencióni, tAtenciónf)
#     global QGral, PS, horaActual, SigFinServicio, SigLlegadaGral, caso, vAbandono

#     if caso == 1:
#         #print("--------------------------------Llegada Caso 6--------------------------------")
#         #modificamos los minutos por segundos
#         b=random.randint(tLlegadaGrali, tLlegadaGralf)
#         if PS == 0 and S == 1:
#             PS = 1
#             SigFinServicio = horaActual + dt.timedelta(seconds=a)
#         else:
#             QGral = QGral + 1
#         SigLlegadaGral = horaActual + dt.timedelta(seconds=b)

# def FinServicio():
#     a=random.randint(tAtencióni, tAtenciónf)
#     global QGral, PS, SigFinServicio, caso, contador

#     if caso == 1:
#         #print("--------------------------------Fin serv Caso 6--------------------------------")
#         #cambiamos los min por segundos
#         contador = contador + 1
#         if QGral >= 1:
#             QGral = QGral - 1
#             SigFinServicio = horaActual + dt.timedelta(seconds=a)
#         else:
#             PS = 0
#             SigFinServicio = horaFinal

# def SalidaServidor():
#     global S, SigLlegadaServ, SigFinServicio, SigSalidaServ
#     a = random.randint(tDescansoi, tDescansof)
#     S = 0
#     SigLlegadaServ = horaActual + dt.timedelta(minutes=a)
#     if PS == 1:
#         SigFinServicio = SigFinServicio + dt.timedelta(minutes=a)
#     if SigFinServicio == SigSalidaServ:
#         FinServicio()
#     SigSalidaServ = horaFinal

# def LlegadaServidor():
#     a=random.randint(tTrabajoi, tTrabajof)
#     global S, SigSalidaServ, SigLlegadaServ
#     S = 1
#     SigSalidaServ = horaActual + dt.timedelta(minutes=a)
#     SigLlegadaServ = horaFinal

# def Simulacion():
#     global horaActual, PS, T, QGral, SigFinServicio, SigLlegadaGral, SigLlegadaServ, SigSalidaServ, S, contador
#     LlegadaCliente("Gral")

#     if caso == 1:
#         LlegadaServidor()
#         print("{:<13}{:<24}{:<21}{:<24}{:<25}{:<6}{:<3}{:<4}".format("Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "H.Prox Salida servidor", "H.Prox Llegada servidor", "QGral", "PS", "S"))
#         while True:
#             horaActual = min(SigFinServicio, SigLlegadaGral, SigLlegadaServ, SigSalidaServ)
#             if min(SigFinServicio, SigLlegadaGral, SigLlegadaServ, SigSalidaServ) == SigFinServicio:
#                 FinServicio()
#             elif min(SigFinServicio, SigLlegadaGral, SigLlegadaServ, SigSalidaServ) == SigLlegadaGral:
#                 LlegadaCliente("Gral")
#             elif min(SigFinServicio, SigLlegadaGral, SigLlegadaServ, SigSalidaServ) == SigLlegadaServ:
#                 LlegadaServidor()
#             elif min(SigFinServicio, SigLlegadaGral, SigLlegadaServ, SigSalidaServ) == SigSalidaServ:
#                 SalidaServidor()
#             elif SigFinServicio == SigLlegadaGral == SigLlegadaServ == SigSalidaServ:
#                 print ("Error")
#                 break
#             #"Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "H.Prox Salida servidor", "H.Prox Llegada servidor", "QGral", "PS", "S"
#             print("{:>2}{:<1}{:<10}{:>2}{:<1}{:<21}{:>2}{:<1}{:<18}{:>2}{:<1}{:<21}{:>2}{:<1}{:<22}{:<6}{:<3}{:<4}".format(horaActual.hour,":", horaActual.minute, SigLlegadaGral.hour,":", SigLlegadaGral.minute, SigFinServicio.hour,":", SigFinServicio.minute, SigSalidaServ.hour,":", SigSalidaServ.minute,  SigLlegadaServ.hour,":", SigLlegadaServ.minute, QGral, PS, S)) 
#             if horaActual >= horaFinal:
#                 print("-------------- Fin de la simulación -------------- ") 
#                 print("Cantidad de piezas producidas: ", contador)
#                 break
#     return

# VectorInicial()
# Simulacion()

import streamlit as st
import random
import datetime as dt

QGral= QPrio= ZS= PS= T= caso= S= 0
tLlegadaGrali= tLlegadaGralf= tLlegadaPrioi= tLlegadaPriof= tAtencióni= tAtenciónf= tDescansoi= tDescansof= tTrabajoi= tTrabajof= tAbandonoi= tAbandonof= tZS= contador= 0
horaActual= horaFinal= SigFinServicio= SigFinZona= SigLlegadaGral= SigLlegadaPrio= SigLlegadaServ= SigSalidaServ= dt.datetime(2000,1,1,0,0,0)

vAbandono = [horaFinal]

def VectorInicial():
    global QGral,PS, T, contador, tLlegadaGrali, tLlegadaGralf, tAtencióni, tAtenciónf ,S, tDescansoi, tDescansof, tTrabajoi, tTrabajof, SigFinServicio, SigLlegadaGral, SigLlegadaServ, SigSalidaServ, horaFinal, horaActual, tAbandonoi, tAbandonof, caso
    st.write("Indique el tipo de simulación que quiere hacer:")
    st.write("1 - Caso parcial")
    caso = st.number_input("caso: ", min_value=1, max_value=1, step=1)

    aux = dt.timedelta(hours=int(st.text_input("Ingrese hora de inicio de la simulación: ")))
    horaActual = horaActual + aux
    QGral = int(st.text_input("Ingrese la cantidad inicial de clientes en cola: "))
    PS = int(st.text_input("Ingrese el estado inicial del puesto de trabajo (ocupado = 1; libre = 0): "))
    T = int(st.text_input("Ingrese la duración de la simulación (en minutos): "))
    horaFinal = horaActual + dt.timedelta(minutes=T)
    SigFinServicio= SigFinZona= SigLlegadaGral= SigLlegadaPrio= SigLlegadaServ= SigSalidaServ= vAbandono[0]= horaFinal
    
    st.write("Ingrese el intervalo que tarda el puesto de servicio en atender los clientes: ")
    tAtencióni = int(st.text_input("Mínimo: "))
    tAtenciónf = int(st.text_input("Máximo: "))

    if caso == 1:
        #-----------Ajuste de vatriables-----------
        tAtencióni = 10
        tAtenciónf = 10
        tLlegadaGrali = 10
        tLlegadaGralf = 20
        tDescansoi = 5
        tDescansof = 5
        tTrabajoi = 60
        tTrabajof = 60
    else:
        st.write("Error")

def LlegadaCliente(case):
    a=random.randint(tAtencióni, tAtenciónf)
    global QGral, PS, horaActual, SigFinServicio, SigLlegadaGral, caso, vAbandono

    if caso == 1:
        b=random.randint(tLlegadaGrali, tLlegadaGralf)
        if PS == 0 and S == 1:
            PS = 1
            SigFinServicio = horaActual + dt.timedelta(seconds=a)
        else:
            QGral = QGral + 1
        SigLlegadaGral = horaActual + dt.timedelta(seconds=b)

def FinServicio():
    a=random.randint(tAtencióni, tAtenciónf)
    global QGral, PS, SigFinServicio, caso, contador

    if caso == 1:
        contador = contador + 1
        if QGral >= 1:
            QGral = QGral - 1
            SigFinServicio = horaActual + dt.timedelta(seconds=a)
        else:
            PS = 0
            SigFinServicio = horaFinal

def SalidaServidor():
    global S, SigLlegadaServ, SigFinServicio, SigSalidaServ
    a = random.randint(tDescansoi, tDescansof)
    S = 0
    SigLlegadaServ = horaActual + dt.timedelta(minutes=a)
    if PS == 1:
        SigFinServicio = SigFinServicio + dt.timedelta(minutes=a)
    if SigFinServicio == SigSalidaServ:
        FinServicio()
    SigSalidaServ = horaFinal

def LlegadaServidor():
    a=random.randint(tTrabajoi, tTrabajof)
    global S, SigSalidaServ, SigLlegadaServ
    S = 1
    SigSalidaServ = horaActual + dt.timedelta(minutes=a)
    SigLlegadaServ = horaFinal

def Simulacion():
    global horaActual, PS, T, QGral, SigFinServicio, SigLlegadaGral, SigLlegadaServ, SigSalidaServ, S, contador
    LlegadaCliente("Gral")

    if caso == 1:
        LlegadaServidor()
        st.write("{:<13}{:<24}{:<21}{:<24}{:<25}{:<6}{:<3}{:<4}".format("Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "H.Prox Salida servidor", "H.Prox Llegada servidor", "QGral", "PS", "S"))
        while True:
            horaActual = min(SigFinServicio, SigLlegadaGral, SigLlegadaServ, SigSalidaServ)
            if min(SigFinServicio, SigLlegadaGral, SigLlegadaServ, SigSalidaServ) == SigFinServicio:
                FinServicio()
            elif min(SigFinServicio, SigLlegadaGral, SigLlegadaServ, SigSalidaServ) == SigLlegadaGral:
                LlegadaCliente("Gral")
            elif min(SigFinServicio, SigLlegadaGral, SigLlegadaServ, SigSalidaServ) == SigLlegadaServ:
                LlegadaServidor()
            elif min(SigFinServicio, SigLlegadaGral, SigLlegadaServ, SigSalidaServ) == SigSalidaServ:
                SalidaServidor()
            elif SigFinServicio == SigLlegadaGral == SigLlegadaServ == SigSalidaServ:
                st.write("Error")
                break
            st.write("{:>2}{:<1}{:<10}{:>2}{:<1}{:<21}{:>2}{:<1}{:<18}{:>2}{:<1}{:<21}{:>2}{:<1}{:<22}{:<6}{:<3}{:<4}".format(horaActual.hour,":", horaActual.minute, SigLlegadaGral.hour,":", SigLlegadaGral.minute, SigFinServicio.hour,":", SigFinServicio.minute, SigSalidaServ.hour,":", SigSalidaServ.minute,  SigLlegadaServ.hour,":", SigLlegadaServ.minute, QGral, PS, S)) 
            if horaActual >= horaFinal:
                st.write("-------------- Fin de la simulación -------------- ") 
                st.write("Cantidad de piezas producidas: ", contador)
                break
    return

VectorInicial()
Simulacion()


