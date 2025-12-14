from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import psutil

def mostrar_almacenamiento():
    fig = plt.figure()      # figura principal
    ax = fig.add_subplot(111)
    x = []      # guardar la cpu
    n = psutil.cpu_count()      # numero de cpu

    def update(frame, x):
        disk = psutil.disk_usage('/')
        disk = disk.percent

        x.append(disk)

        if len(x) > 60:     # tras 60 segundos
            x.pop(0)        # eliminamos el primer elemento
        x = np.array(x)

        ax.clear()      # limpiamos la tabla
        ax.plot(x)
        
        ax.set_title("Uso Almacenamiento")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("% Uso")
        ax.set_xlim(0, 60)      # mostrar maximo un minuto
        ax.set_ylim(0, 100)     # 0% a 100%

    ani = FuncAnimation(fig=fig, func=update, frames=60, fargs=(x,))
    plt.show()

mostrar_almacenamiento()