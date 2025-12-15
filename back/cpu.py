from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import psutil

def porcentaje_cpu():
    fig = plt.figure()      # figura principal
    ax = fig.add_subplot(111)
    x = []      # guardar la cpu
    n = psutil.cpu_count()      # numero de cpu
    ax = plt.gca()

    def update(frame, x):
        x.append(psutil.cpu_percent(interval=1, percpu=True))
        if len(x) > 60:     
            x.pop(0)        # eliminamos el primer elemento
        x = np.array(x)
        y = np.zeros(100)
        
        ax.clear()      # limpiamos la tabla
        for i in range(n):
            ax.plot(x[::-1, i], label=f"CPU {i+1}")        # ploteamos cada cpu - chat
        
        ax.set_title("Uso CPU")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("% CPU")
        
        ax.set_xlim(0, 60)      # mostrar maximo un minuto
        ax.invert_xaxis()       # invertimos
        ax.set_ylim(0, 100)     # 0% a 100%
        ax.legend()

    ani = FuncAnimation(fig=fig, func=update, frames=60, fargs=(x,))
    plt.show()

porcentaje_cpu()