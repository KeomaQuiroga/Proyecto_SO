from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import psutil

def mostrar_memoria():
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
        ax.plot(x[:,0], label="Memoria")
        ax.plot(x[:,1], label="Memoria Swap")
        
        ax.set_title("Uso Memoria")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("% Uso")
        ax.legend()
        ax.set_xlim(0, 60)      # mostrar maximo un minuto
        ax.set_ylim(0, 100)     # 0% a 100%

    ani = FuncAnimation(fig=fig, func=update, frames=60, fargs=(x,))
    plt.show()

mostrar_memoria()