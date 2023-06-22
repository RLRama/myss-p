import random
import datetime as dt

QGral= QPrio= ZS= PS= T= caso= S= 0
tLlegadaGrali= tLlegadaGralf= tLlegadaPrioi= tLlegadaPriof= tAtencióni= tAtenciónf= tDescansoi= tDescansof= tTrabajoi= tTrabajof= tAbandonoi= tAbandonof= tZS= contador= 0
horaActual= horaFinal= SigFinServicio= SigFinZona= SigLlegadaGral= SigLlegadaPrio= SigLlegadaServ= SigSalidaServ= dt.datetime(2000,1,1,0,0,0)

vAbandono = [horaFinal]

def VectorInicial():
    global QGral, QPrio, PS, T, contador, tLlegadaGrali, tLlegadaGralf, tLlegadaPrioi, tLlegadaPriof, tAtencióni, tAtenciónf, caso, S, tDescansoi, tDescansof, tTrabajoi, tTrabajof, SigFinServicio, SigLlegadaGral, SigLlegadaPrio, SigLlegadaServ, SigFinZona, SigSalidaServ, horaFinal, horaActual, tAbandonoi, tAbandonof, tZS
    #―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
    print("Indique el tipo de simulación que quiere hacer:")
    print("1 - Caso Base, sin abandono de servidor, sin abandono de clientes")
    print("2 - Caso con abandono de servidor")
    print("3 - Caso con abandono de clientes")
    print("4 - Caso con clientes con prioridad")
    print("5 - Caso con zona de seguridad")
    print("6 - Caso parcial")
    caso = int(input("caso: "))
    #―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
    aux = dt.timedelta(hours=int(input("Ingrese hora de inicio de la simulación: ")))
    horaActual = horaActual + aux
    QGral = int(input("Ingrese la cantidad inicial de clientes en cola: "))
    PS = int(input("Ingrese el estado inicial del puesto de trabajo (ocupado = 1; libre = 0): "))
    T = int(input("Ingrese la duración de la simulación (en minutos): "))
    horaFinal = horaActual + dt.timedelta(minutes=T)
    SigFinServicio= SigFinZona= SigLlegadaGral= SigLlegadaPrio= SigLlegadaServ= SigSalidaServ= vAbandono[0]= horaFinal
    
    print("Ingrese el intervalo que tarda el puesto de servicio en atender los clientes: ")
    tAtencióni = int(input("Mínimo: "))
    tAtenciónf = int(input("Máximo: "))
    
    if caso == 1:
        #print("--------------------------------Caso 1--------------------------------")
        print("Ingrese el intervalo en el que llegan los clientes: ") 
        tLlegadaGrali = int(input("Mínimo: "))
        tLlegadaGralf = int(input("Máximo: "))
        S = 1
    elif caso == 2:
        #print("--------------------------------Caso 2--------------------------------")
        print("Ingrese el intervalo en el que llegan los clientes: ") 
        tLlegadaGrali = int(input("Mínimo: "))
        tLlegadaGralf = int(input("Máximo: "))
        S = int(input("Ingrese el valor inicial del servidor del puesto de trabajo (presente = 1; ausente = 0): "))
        print("Ingrese el intervalo de duración de los descansos: ")
        tDescansoi = int(input("Mínimo: "))
        tDescansof = int(input("Máximo: "))
        print("Ingrese el intervalo de tiempo en el que trabaja el servidor: ")
        tTrabajoi = int(input("Mínimo: "))
        tTrabajof = int(input("Máximo: "))
    elif caso == 3:
        #print("--------------------------------Caso 3--------------------------------")
        print("Ingrese el intervalo en el que llegan los clientes: ") 
        tLlegadaGrali = int(input("Mínimo: "))
        tLlegadaGralf = int(input("Máximo: "))
        print("Ingrese el intervalo de los abandonos: ")
        tAbandonoi = int(input("Mínimo: "))
        tAbandonof = int(input("Máximo: "))
        S = 1
    elif caso == 4:
        #print("--------------------------------Caso 4--------------------------------")
        print("Ingrese el intervalo en el que llegan los clientes SIN prioridad: ") 
        tLlegadaGrali = int(input("Mínimo: "))
        tLlegadaGralf = int(input("Máximo: "))
        QPrio = int(input("Ingrese la cantidad inicial de clientes en cola CON prioridad: "))
        print("Ingrese el intervalo en el que llegan los clientes CON prioridad: ") 
        tLlegadaPrioi = int(input("Mínimo: "))
        tLlegadaPriof = int(input("Máximo: "))
        S = 1
    elif caso == 5:
        #print("--------------------------------Caso 5--------------------------------")
        print("Ingrese el intervalo en el que llegan los clientes: ") 
        tLlegadaGrali = int(input("Mínimo: "))
        tLlegadaGralf = int(input("Máximo: "))
        S = 1
        tZS= int(input("Ingrese el tiempo que demora el cliente en pasar por la zona de seguridad: "))
    elif caso ==6:
        #-----------Ajuste de vatriables-----------
        tAtencióni = 10
        tAtenciónf = 10
        tLlegadaGrali = 10
        tLlegadaGralf = 20
        tDescansoi = 5
        tDescansof = 5
        tTrabajoi = 60
        tTrabajof = 60