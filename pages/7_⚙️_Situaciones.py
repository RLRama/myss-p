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
        QGral = 0
        PS = 0
        T = 190
        horaFinal = horaActual + dt.timedelta(minutes=T)
        tAtencióni = 10
        tAtenciónf = 10
        tLlegadaGrali = 10
        tLlegadaGralf = 20
        tDescansoi = 5
        tDescansof = 5
        tTrabajoi = 60
        tTrabajof = 60
        
#―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
        
def LlegadaCliente(case):
    a=random.randint(tAtencióni, tAtenciónf)
    global QGral, QPrio,  PS, horaActual, SigFinServicio, SigLlegadaGral, SigLlegadaPrio, caso, vAbandono, SigFinZona, ZS
    
    if caso == 1:
        #print("--------------------------------Llegada Caso 1--------------------------------")
        b=random.randint(tLlegadaGrali, tLlegadaGralf)
        if PS == 0:
            PS = 1
            SigFinServicio = horaActual + dt.timedelta(minutes=a)
        else:
            QGral = QGral + 1
        SigLlegadaGral = horaActual + dt.timedelta(minutes=b)
    elif caso == 2:
        #print("--------------------------------Llegada Caso 2--------------------------------")
        b=random.randint(tLlegadaGrali, tLlegadaGralf)
        if PS == 0 and S == 1:
            PS = 1
            SigFinServicio = horaActual + dt.timedelta(minutes=a)
        else:
            QGral = QGral + 1
        SigLlegadaGral = horaActual + dt.timedelta(minutes=b)
    elif caso == 3:
        #print("--------------------------------Llegada Caso 3--------------------------------")
        b=random.randint(tLlegadaGrali, tLlegadaGralf)
        if PS == 0:
            PS = 1
            SigFinServicio = horaActual + dt.timedelta(minutes=a)
            vAbandono[0] = horaFinal
        else:
            QGral = QGral + 1
            c = random.randint(tAbandonoi, tAbandonof)
            if vAbandono[0] == horaFinal:
                vAbandono[0] = horaActual + dt.timedelta(minutes=c)
            else:
                vAbandono.append(horaActual + dt.timedelta(minutes=c))
        SigLlegadaGral = horaActual + dt.timedelta(minutes=b)
    elif caso == 4:
        #print("--------------------------------Llegada Caso 4--------------------------------")
        if case == "Gral":
            b=random.randint(tLlegadaGrali, tLlegadaGralf)
            if PS == 0:
                PS = 1
                SigFinServicio = horaActual + dt.timedelta(minutes=a)
            else:
                QGral = QGral + 1
            SigLlegadaGral = horaActual + dt.timedelta(minutes=b)
        elif case == "Prio":
            c = random.randint(tLlegadaPrioi, tLlegadaPriof)
            if PS == 0:
                PS = 1
                SigFinServicio = horaActual + dt.timedelta(minutes=a)
            else:
                QPrio = QPrio + 1
            SigLlegadaPrio = horaActual + dt.timedelta(minutes=c)    
    elif caso == 5:
        #print("--------------------------------Llegada Caso 5--------------------------------")
        b=random.randint(tLlegadaGrali, tLlegadaGralf)
        if PS == 0 and ZS == 0:
            ZS = 1
            SigFinZona = horaActual + dt.timedelta(minutes=tZS)
        else:
            QGral = QGral + 1
        SigLlegadaGral = horaActual + dt.timedelta(minutes=b)
    elif caso == 6:
        #print("--------------------------------Llegada Caso 6--------------------------------")
        #modificamos los minutos por segundos
        b=random.randint(tLlegadaGrali, tLlegadaGralf)
        if PS == 0 and S == 1:
            PS = 1
            SigFinServicio = horaActual + dt.timedelta(seconds=a)
        else:
            QGral = QGral + 1
        SigLlegadaGral = horaActual + dt.timedelta(seconds=b)

def FinZona():
    global PS, ZS, SigFinServicio, tAtencióni, tAtenciónf, SigFinZona
    a=random.randint(tAtencióni, tAtenciónf)
    PS = 1
    ZS = 0
    SigFinServicio = horaActual + dt.timedelta(minutes=a)
    SigFinZona=horaFinal #sin esto se va al carajo

def FinServicio():
    a=random.randint(tAtencióni, tAtenciónf)
    global QGral, QPrio, PS, SigFinServicio, caso, SigFinZona, ZS, tZS, contador
    
    if caso == 1 or caso == 2:
        #print("--------------------------------Fin serv Caso 1 y 2--------------------------------")
        if QGral >= 1:
            QGral = QGral - 1
            SigFinServicio = horaActual + dt.timedelta(minutes=a)
        else:
            PS = 0
            SigFinServicio = horaFinal 
    elif caso == 3:
        #print("--------------------------------Fin serv Caso 3--------------------------------")
        if QGral >= 1:
            QGral = QGral - 1
            if len(vAbandono) == 1:
                vAbandono[0] = horaFinal
            else:
                del vAbandono[0]
            SigFinServicio = horaActual + dt.timedelta(minutes=a)
        else:
            PS = 0
            SigFinServicio = horaFinal 
            vAbandono[0] = horaFinal
    elif caso == 4:
        #print("--------------------------------Fin serv Caso 4--------------------------------")
        if QPrio >= 1:
            QPrio = QPrio - 1
            SigFinServicio = horaActual + dt.timedelta(minutes=a)
        else:
            if QGral >= 1:
                QGral = QGral - 1
                SigFinServicio = horaActual + dt.timedelta(minutes=a)
            else:
                PS = 0
                SigFinServicio = horaFinal
    elif caso == 5:
        #print("--------------------------------Fin serv Caso 5--------------------------------")
        PS = 0
        QGral = QGral - 1
        ZS = 1
        SigFinZona = horaActual +  dt.timedelta(minutes=tZS)
        SigFinServicio = horaFinal 
    elif caso == 6:
        #print("--------------------------------Fin serv Caso 6--------------------------------")
        #cambiamos los min por segundos
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
    
def AbandonoCliente():
    global QGral
    QGral = QGral-1
    if len(vAbandono) == 1:
        vAbandono[0] = horaFinal + dt.timedelta(hours=1)
    else:
        del vAbandono[0]

def Simulacion():
    global horaActual, PS, T, QGral, QPrio, SigFinServicio, SigFinZona, SigLlegadaGral, SigLlegadaPrio, SigLlegadaServ, SigSalidaServ, S, contador
    
    print("-------------- Inicio de Simulación --------------")
  
    print("--------------------------------------------------")
    LlegadaCliente("Gral")

    if caso == 1:
        print("{:<13}{:<24}{:<21}{:<6}{:<4}".format("Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "QGral", "PS"))
        while True:
            horaActual = min(SigFinServicio, SigLlegadaGral)
            if min(SigFinServicio, SigLlegadaGral) == SigFinServicio:
                FinServicio()
            elif min(SigFinServicio, SigLlegadaGral) == SigLlegadaGral:
                LlegadaCliente("Gral")
            elif SigFinServicio == SigLlegadaGral:
                print ("Error")
                break
            #"Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "QGral", "PS"
            print("{:>2}{:<1}{:<10}{:>2}{:<1}{:<21}{:>2}{:<1}{:<18}{:<6}{:<4}".format(horaActual.hour,":",horaActual.minute, SigLlegadaGral.hour,":", SigLlegadaGral.minute, SigFinServicio.hour,":", SigFinServicio.minute, QGral, PS)) 
            if horaActual >= horaFinal:
                print("-------------- Fin de la simulación -------------- ") 
                break
    elif caso == 2:
        LlegadaServidor()
        print("{:<13}{:<24}{:<21}{:<24}{:<25}{:<6}{:<3}{:<4}".format("Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "H.Prox Salida servidor", "H.Prox Llegada servidor", "QGral", "PS", "S"))
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
                print ("Error")
                break
            #"Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "H.Prox Salida servidor", "H.Prox Llegada servidor", "QGral", "PS", "S"
            print("{:>2}{:<1}{:<10}{:>2}{:<1}{:<21}{:>2}{:<1}{:<18}{:>2}{:<1}{:<21}{:>2}{:<1}{:<22}{:<6}{:<3}{:<4}".format(horaActual.hour,":", horaActual.minute, SigLlegadaGral.hour,":", SigLlegadaGral.minute, SigFinServicio.hour,":", SigFinServicio.minute, SigSalidaServ.hour,":", SigSalidaServ.minute,  SigLlegadaServ.hour,":", SigLlegadaServ.minute, QGral, PS, S)) 
            if horaActual >= horaFinal:
                print("-------------- Fin de la simulación -------------- ") 
                break
    elif caso == 3:
        print("{:<13}{:<24}{:<21}{:<18}{:<6}{:<4}".format("Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "H. Prox Abandono", "QGral", "PS"))
        while True:
            horaActual = min(SigFinServicio, SigLlegadaGral, vAbandono[0])
            if min(SigFinServicio, SigLlegadaGral, vAbandono[0]) == SigFinServicio:
                FinServicio()
            elif min(SigFinServicio, SigLlegadaGral, vAbandono[0]) == SigLlegadaGral:
                LlegadaCliente("Gral")
            elif min(SigFinServicio, SigLlegadaGral, vAbandono[0]) == vAbandono[0]:
                AbandonoCliente()
            elif SigFinServicio == SigLlegadaGral == vAbandono[0]:
                print ("Error")
                break
            #"Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "H. Prox Abandono", "QGral", "PS"
            print("{:>2}{:<1}{:<10}{:>2}{:<1}{:<21}{:>2}{:<1}{:<18}{:>2}{:<1}{:<15}{:<6}{:<4}".format(horaActual.hour,":", horaActual.minute, SigLlegadaGral.hour,":", SigLlegadaGral.minute, SigFinServicio.hour,":", SigFinServicio.minute, vAbandono[0].hour,":", vAbandono[0].minute, QGral, PS)) 
            if horaActual >= horaFinal:
                print("-------------- Fin de la simulación -------------- ") 
                break
    elif caso == 4:
        LlegadaCliente("Prio")
        print("{:<13}{:<24}{:<21}{:<34}{:<6}{:<6}{:<4}".format("Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "H.Prox llegada cliente prioridad", "QGral", "QPrio", "PS"))
        while True:
            horaActual = min(SigFinServicio, SigLlegadaGral, SigLlegadaPrio)
            if min(SigFinServicio, SigLlegadaGral, SigLlegadaPrio) == SigFinServicio:
                FinServicio()
            elif min(SigFinServicio, SigLlegadaGral, SigLlegadaPrio) == SigLlegadaGral:
                LlegadaCliente("Gral")
            elif min(SigFinServicio, SigLlegadaGral, SigLlegadaPrio) == SigLlegadaPrio:
                LlegadaCliente("Prio")
            elif SigFinServicio == SigLlegadaGral == SigLlegadaPrio:
                print ("Error")
                break
            #"Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "QGral", "PS"
            print("{:>2}{:<1}{:<10}{:>2}{:<1}{:<21}{:>2}{:<1}{:<18}{:>2}{:<1}{:<31}{:<6}{:<6}{:<4}".format(horaActual.hour,":",horaActual.minute, SigLlegadaGral.hour,":", SigLlegadaGral.minute, SigFinServicio.hour,":", SigFinServicio.minute, SigLlegadaPrio.hour,":", SigLlegadaPrio.minute , QGral, QPrio, PS)) 
            if horaActual >= horaFinal:
                print("-------------- Fin de la simulación -------------- ") 
                break
    elif caso == 5:
        print("{:<13}{:<24}{:<21}{:<23}{:<6}{:<3}{:<4}".format("Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "H.Prox fin zona segura" ,"QGral", "ZS", "PS"))
        while True:
            horaActual = min(SigFinServicio, SigLlegadaGral, SigFinZona)
            if min(SigFinServicio, SigLlegadaGral, SigFinZona) == SigFinServicio:
                FinServicio()
            elif min(SigFinServicio, SigLlegadaGral, SigFinZona) == SigLlegadaGral:
                LlegadaCliente("Gral")
            elif min(SigFinServicio, SigLlegadaGral, SigFinZona) == SigFinZona:
                FinZona()
            elif SigFinServicio == SigLlegadaGral:
                print ("Error")
                break
            #"Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "QGral", "PS"
            print("{:>2}{:<1}{:<10}{:>2}{:<1}{:<21}{:>2}{:<1}{:<18}{:>2}{:<1}{:<20}{:<6}{:<3}{:<4}".format(horaActual.hour,":",horaActual.minute, SigLlegadaGral.hour,":", SigLlegadaGral.minute, SigFinServicio.hour,":", SigFinServicio.minute, SigFinZona.hour, ":", SigFinZona.minute, QGral, ZS, PS)) 
            if horaActual >= horaFinal:
                print("-------------- Fin de la simulación -------------- ") 
                break
    elif caso == 6:
        LlegadaServidor()
        print("{:<13}{:<24}{:<21}{:<24}{:<25}{:<6}{:<3}{:<4}".format("Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "H.Prox Salida servidor", "H.Prox Llegada servidor", "QGral", "PS", "S"))
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
                print ("Error")
                break
            #"Hora actual", "H.Prox llegada cliente", "H.Prox fin servicio", "H.Prox Salida servidor", "H.Prox Llegada servidor", "QGral", "PS", "S"
            print("{:>2}{:<1}{:<10}{:>2}{:<1}{:<21}{:>2}{:<1}{:<18}{:>2}{:<1}{:<21}{:>2}{:<1}{:<22}{:<6}{:<3}{:<4}".format(horaActual.hour,":", horaActual.minute, SigLlegadaGral.hour,":", SigLlegadaGral.minute, SigFinServicio.hour,":", SigFinServicio.minute, SigSalidaServ.hour,":", SigSalidaServ.minute,  SigLlegadaServ.hour,":", SigLlegadaServ.minute, QGral, PS, S)) 
            if horaActual >= horaFinal:
                print("-------------- Fin de la simulación -------------- ") 
                print("Cantidad de piezas producidas: ", contador)
                break
    return

# Llamadas a las funciones
VectorInicial()
Simulacion()