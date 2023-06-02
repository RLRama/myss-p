import streamlit as st
import random
import simpy
import numpy as np
import pandas as pd

# Configurar página
st.set_page_config(
    page_title="Simulación de colas",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "MySS - 2023 - UNLaR"
    }
)

with st.sidebar:
    st.header("⌨️")
    st.subheader("Configurar parámetros")
    INTERVAL_CUSTOMERS = st.number_input(
        "Tiempo promedio entre llegadas de clientes `(min)`",
        min_value=1.00
    )
    t_serv = st.number_input(
        "Tiempo promedio de servicio `(min)`",
        min_value=1.00
    )
    NEW_CUSTOMERS = st.number_input(
        "Clientes generados",
        min_value=1
    )
    t = st.number_input(
        "Duración de la simulación `(min)`",
        min_value=1.00
    )
    RANDOM_SEED = st.number_input(
        "Semilla para generar números aleatorios",
        value=9999, min_value=1
    )

MIN_PATIENCE = 9999999999
MAX_PATIENCE = 9999999999

st.markdown(
    """
    # Situación I
    ## Descripción
    - Obedece al problema n° 1
    - Clientes que llegan individualmente en intervalos aleatorios
    - Cola FIFO (los clientes son atendidos en el orden que llegan)
    - Tiempos de prestación de servicios aleatorios
    - El servidor no abandona el puesto de servicio

    ## Uso
    - Configure parámetros usando la **👈 barra lateral** para dar valores
    - Presione el botón **'Simular'** para mostrar la tabla de simulación generada
    """
)

## Model components ------------------------           

class Source(Process):
    """ Source generates customers randomly """

    def generate(self,number,meanTBA):         
        for i in range(number):
            c = Customer(name = "Customer%02d"%(i,),sim=self.sim)
            self.sim.activate(c,c.visit(b=self.sim.k))              
            t = expovariate(1.0/meanTBA)               
            yield hold,self,t

class Customer(Process):
    """ Customer arrives, is served and leaves """
        
    def visit(self,b):                                
        arrive = self.sim.now()
        st.text("%8.4f %s: Here I am     "%(self.sim.now(),self.name))
        yield request,self,b                          
        wait = self.sim.now()-arrive
        st.text("%8.4f %s: Waited %6.3f"%(self.sim.now(),self.name,wait))
        tib = expovariate(1.0/t_serv)            
        yield hold,self,tib                          
        yield release,self,b                         
        st.text("%8.4f %s: Finished      "%(self.sim.now(),self.name))
        
## Model -----------------------------------

class BankModel(Simulation):
    def run(self,aseed):
        self.initialize()
        seed(aseed)        
        self.k = Resource(name="Counter",unitName="Clerk",sim=self)       
        s = Source('Source',sim=self)
        self.activate(s,s.generate(number=NEW_CUSTOMERS,meanTBA=INTERVAL_CUSTOMERS),at=0.0)           
        self.simulate(until=t)

## Experiment data -------------------------         

## Experiment ------------------------------

if st.button('Simular'):
    BankModel().run(aseed=RANDOM_SEED)
else:
    st.text('')