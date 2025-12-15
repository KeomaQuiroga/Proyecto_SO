from matplotlib.animation import FuncAnimation
from queue import Queue
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import pandas as pd
import psutil

def division_memoria(q):
    """
    Devuelve la memoria disponible y la memoria libre (RAM ambas)
    
    :param q: Queue para compartir entre procesos
    """
    mem = psutil.virtual_memory()
    libre = mem.available
    uso = mem.total - libre
    x = [libre, uso]
    q.put(x)

def fracc_memoria_avanzado():
    x = obtener_memoria_procesos()
    lb = obtener_nombre_procesos()
    df = pd.DataFrame({"Memoria" : x, "Nombres" : lb})

    fig = px.treemap(data_frame=df, path=["Nombres"], values="Memoria")
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig.show()

def obtener_memoria_procesos():
    proc_mem = []
    for p in psutil.process_iter():
        with p.oneshot():       # mas velocidad
            try:        # intenta obtener memoria
                memoria = p.memory_full_info().uss
            except:
                memoria = 1     # si no puede
        proc_mem.append(memoria)
        
    return proc_mem

def obtener_nombre_procesos():
    proc_name = []
    for p in psutil.process_iter():
        with p.oneshot():       # mas velocidad
            nombre = p.name()
        proc_name.append(nombre)
        
    return proc_name

def ram_porcentaje(q):
    """
    Devuelve el procentaje de RAM que se usas
    
    :param q: Queue para compartir datos
    """
    x = []
    mem = psutil.virtual_memory().percent       # ram
    swap = psutil.swap_memory().percent     # swap
    x.append([mem, swap])
    x = np.array(x)
    q.put(x)