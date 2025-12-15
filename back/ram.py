from matplotlib.animation import FuncAnimation
from pypalettes import load_cmap
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import psutil
import squarify
import procesos

def porcentaje_memoria():
    fig = plt.figure()      # figura principal
    ax = fig.add_subplot(111)
    x = []      # guardar la cpu
    n = psutil.cpu_count()      # numero de cpu

    def update(frame, x):
        mem = psutil.virtual_memory()
        mem = mem.percent

        swap = psutil.swap_memory()
        swap = swap.percent

        x.append([mem, swap])
        if len(x) > 60:     # tras 60 segundos
            x.pop(0)        # eliminamos el primer elemento
        x = np.array(x)

        ax.clear()      # limpiamos la tabla
        ax.plot(x[::-1,0], label="Memoria")
        ax.plot(x[::-1,1], label="Memoria Swap")
        
        ax.set_title("Uso Memoria")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("% Uso")
        ax.legend()
        ax.set_xlim(0, 60)      # mostrar maximo un minuto
        ax.invert_xaxis()       # invertimos
        ax.set_ylim(0, 100)     # 0% a 100%

    ani = FuncAnimation(fig=fig, func=update, frames=60, fargs=(x,))
    plt.show()

def fracc_memoria_basico():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    def update(frame):
        mem = psutil.virtual_memory()
        libre = mem.available       # memoria disponible
        uso = mem.total - libre     # memoria en uso

        x = [libre, uso]
        lb = ["Libre", "En uso"]

        ax.clear()      # se limpia
        ax.pie(x, labels=lb, autopct="%0.1f%%")

    ani = FuncAnimation(fig=fig, func=update, frames=60)
    plt.show()

def fracc_memoria_avanzado():
    x = procesos.obtener_memoria_procesos()
    lb = procesos.obtener_nombre_procesos()
    df = pd.DataFrame({"Memoria" : x, "Nombres" : lb})

    fig = px.treemap(data_frame=df, path=["Nombres"], values="Memoria")
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig.show()