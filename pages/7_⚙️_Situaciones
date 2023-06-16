import random
import datetime as dt
import streamlit as st

QGral = QPrio = ZS = PS = T = caso = S = 0
tLlegadaGrali = tLlegadaGralf = tLlegadaPrioi = tLlegadaPriof = tAtencióni = tAtenciónf = tDescansoi = tDescansof = tTrabajoi = tTrabajof = tAbandonoi = tAbandonof = tZS = 0
horaActual = horaFinal = SigFinServicio = SigFinZona = SigLlegadaGral = SigLlegadaPrio = SigLlegadaServ = SigSalidaServ = dt.datetime(2000, 1, 1, 0, 0, 0)

vAbandono = [horaFinal]

def vector_inicial():
    global QGral, QPrio, PS, T, tLlegadaGrali, tLlegadaGralf, tLlegadaPrioi, tLlegadaPriof, tAtencióni, tAtenciónf, caso, S, tDescansoi, tDescansof, tTrabajoi, tTrabajof, SigFinServicio, SigLlegadaGral, SigLlegadaPrio, SigLlegadaServ, SigFinZona, SigSalidaServ, horaFinal, horaActual, tAbandonoi, tAbandonof, tZS
    st.write("Indique el tipo de simulación que quiere hacer:")
    caso = st.selectbox("caso", ["Caso Base, sin abandono de servidor, sin abandono de clientes",
                                "Caso con abandono de servidor",
                                "Caso con abandono de clientes",
                                "Caso con clientes con prioridad",
                                "Caso con zona de seguridad"])
    
    aux = dt.timedelta(hours=st.number_input("Ingrese hora de inicio de la simulación: ", value=0, step=1))
    horaActual = horaActual + aux
    QGral = st.number_input("Ingrese la cantidad inicial de clientes en cola: ", value=0, step=1)
    PS = st.number_input("Ingrese el estado inicial del puesto de trabajo (ocupado = 1; libre = 0): ", value=0, step=1)
    T = st.number_input("Ingrese la duración de la simulación (en minutos): ", value=0, step=1)
    horaFinal = horaActual + dt.timedelta(minutes=T)
    SigFinServicio = SigFinZona = SigLlegadaGral = SigLlegadaPrio = SigLlegadaServ = SigSalidaServ = vAbandono[0] = horaFinal
    
    st.write("Ingrese el intervalo que tarda el puesto de servicio en atender los clientes:")
    tAtencióni = st.number_input("Mínimo: ", value=0, step=1)
    tAtenciónf = st.number_input("Máximo: ", value=0, step=1)
    
    if caso == "Caso Base, sin abandono de servidor, sin abandono de clientes":
        st.write("--------------------------------Caso 1--------------------------------")
        st.write("Ingrese el intervalo que tarda un cliente general en llegar:")
        tLlegadaGrali = st.number_input("Mínimo: ", value=0, step=1)
        tLlegadaGralf = st.number_input("Máximo: ", value=0, step=1)
        return
    elif caso == "Caso con abandono de servidor":
        st.write("--------------------------------Caso 2--------------------------------")
        st.write("Ingrese el intervalo que tarda un cliente general en llegar:")
        tLlegadaGrali = st.number_input("Mínimo: ", value=0, step=1)
        tLlegadaGralf = st.number_input("Máximo: ", value=0, step=1)
        return
    elif caso == "Caso con abandono de clientes":
        st.write("--------------------------------Caso 3--------------------------------")
        st.write("Ingrese el intervalo que tarda un cliente general en llegar:")
        tLlegadaGrali = st.number_input("Mínimo: ", value=0, step=1)
        tLlegadaGralf = st.number_input("Máximo: ", value=0, step=1)
        return
    elif caso == "Caso con clientes con prioridad":
        st.write("--------------------------------Caso 4--------------------------------")
        st.write("Ingrese el intervalo que tarda un cliente general en llegar:")
        tLlegadaGrali = st.number_input("Mínimo: ", value=0, step=1)
        tLlegadaGralf = st.number_input("Máximo: ", value=0, step=1)
        st.write("Ingrese el intervalo que tarda un cliente con prioridad en llegar:")
        tLlegadaPrioi = st.number_input("Mínimo: ", value=0, step=1)
        tLlegadaPriof = st.number_input("Máximo: ", value=0, step=1)
        return
    elif caso == "Caso con zona de seguridad":
        st.write("--------------------------------Caso 5--------------------------------")
        st.write("Ingrese el intervalo que tarda un cliente general en llegar:")
        tLlegadaGrali = st.number_input("Mínimo: ", value=0, step=1)
        tLlegadaGralf = st.number_input("Máximo: ", value=0, step=1)
        tZS = st.number_input("Ingrese la duración de la zona de seguridad (en minutos): ", value=0, step=1)
        return

def genera_tiempo_llegada(intervalo_min, intervalo_max):
    return horaActual + dt.timedelta(minutes=random.uniform(intervalo_min, intervalo_max))

def generar_tiempo_atencion(intervalo_min, intervalo_max):
    return dt.timedelta(minutes=random.uniform(intervalo_min, intervalo_max))

def llegada_general():
    global QGral, SigLlegadaGral
    tLlegadaGral = genera_tiempo_llegada(tLlegadaGrali, tLlegadaGralf)
    if tLlegadaGral < SigLlegadaGral:
        SigLlegadaGral = tLlegadaGral
    QGral += 1

def llegada_prioridad():
    global QPrio, SigLlegadaPrio
    tLlegadaPrio = genera_tiempo_llegada(tLlegadaPrioi, tLlegadaPriof)
    if tLlegadaPrio < SigLlegadaPrio:
        SigLlegadaPrio = tLlegadaPrio
    QPrio += 1

def llegada_servicio():
    global PS, SigLlegadaServ
    tLlegadaServ = horaActual
    if tLlegadaServ < SigLlegadaServ:
        SigLlegadaServ = tLlegadaServ
    PS = 1

def atencion_servicio():
    global QGral, QPrio, PS, SigFinServicio, SigSalidaServ, tAtencióni, tAtenciónf
    SigSalidaServ = horaActual + generar_tiempo_atencion(tAtencióni, tAtenciónf)
    if SigSalidaServ < SigFinServicio:
        SigFinServicio = SigSalidaServ
    if QPrio > 0:
        QPrio -= 1
    else:
        QGral -= 1
    if QGral == 0:
        PS = 0

def abandono_servicio():
    global QGral, QPrio, PS, SigFinServicio, SigSalidaServ, tAtencióni, tAtenciónf
    QGral -= 1
    SigSalidaServ = horaActual + generar_tiempo_atencion(tAtencióni, tAtenciónf)
    if SigSalidaServ < SigFinServicio:
        SigFinServicio = SigSalidaServ
    if QGral == 0:
        PS = 0

def abandono_cliente():
    global QGral, QPrio, PS, SigFinServicio, SigSalidaServ, tAtencióni, tAtenciónf, vAbandono
    QGral -= 1
    SigSalidaServ = horaActual + generar_tiempo_atencion(tAtencióni, tAtenciónf)
    if SigSalidaServ < SigFinServicio:
        SigFinServicio = SigSalidaServ
    if QGral == 0:
        PS = 0
    vAbandono.append(horaActual)

def zona_seguridad():
    global QGral, QPrio, PS, SigFinZona, SigSalidaServ, tAtencióni, tAtenciónf, tZS
    SigFinZona = horaActual + dt.timedelta(minutes=tZS)
    if SigFinZona < SigFinServicio:
        SigFinServicio = SigFinZona
    if QGral > 0:
        QGral -= 1
    elif QPrio > 0:
        QPrio -= 1
    if QGral == 0 and QPrio == 0:
        PS = 0

def informar():
    global QGral, QPrio, PS, T, vAbandono
    st.write("Cantidad de clientes generales en cola:", QGral)
    st.write("Cantidad de clientes con prioridad en cola:", QPrio)
    st.write("Estado del puesto de servicio:", PS)
    st.write("Tiempo transcurrido:", horaActual.time())
    st.write("Tiempo restante:", (horaFinal - horaActual).time())
    st.write("Tiempo de llegada del próximo cliente general:", SigLlegadaGral.time())
    st.write("Tiempo de llegada del próximo cliente con prioridad:", SigLlegadaPrio.time())
    st.write("Tiempo de llegada al puesto de servicio:", SigLlegadaServ.time())
    st.write("Tiempo de salida del servicio:", SigSalidaServ.time())
    st.write("Tiempo de fin del servicio:", SigFinServicio.time())
    st.write("Tiempo de fin de la zona de seguridad:", SigFinZona.time())
    st.write("Tiempos de abandono de clientes:", vAbandono[1:])
    
def simulacion():
    global QGral, QPrio, PS, T, horaActual, SigFinServicio, SigLlegadaGral, SigLlegadaPrio, SigLlegadaServ, SigSalidaServ, vAbandono
    while horaActual < horaFinal:
        if SigLlegadaGral <= SigFinServicio and SigLlegadaGral <= SigLlegadaPrio and SigLlegadaGral <= SigLlegadaServ:
            horaActual = SigLlegadaGral
            llegada_general()
        elif SigLlegadaPrio <= SigFinServicio and SigLlegadaPrio <= SigLlegadaGral and SigLlegadaPrio <= SigLlegadaServ:
            horaActual = SigLlegadaPrio
            llegada_prioridad()
        elif SigLlegadaServ <= SigFinServicio and SigLlegadaServ <= SigLlegadaGral and SigLlegadaServ <= SigLlegadaPrio:
            horaActual = SigLlegadaServ
            llegada_servicio()
        else:
            horaActual = SigFinServicio
            atencion_servicio()
        informar()
    st.write("Simulación finalizada.")

vector_inicial()
simulacion()
