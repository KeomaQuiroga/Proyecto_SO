from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import psutil
import time

def mostrar_red(tipo):
    fig = plt.figure()      # figura principal
    ax = fig.add_subplot(111)
    x = []      # guardar la cpu

    def update(frame, x):
        # primer tiempo de recibida
        red = psutil.net_io_counters()      # tomamos tiempo
        s1 = red.bytes_sent
        r1 = red.bytes_recv
        time.sleep(1)       # esperamos 1 segundo
        red = psutil.net_io_counters()      # volvemos a tomar tiempo

        if tipo == 0:
            lb = "Recibiendo bytes/s"
            dif = diferencia_descarga(red, r1)
        elif tipo == 1:
            lb = "Enviando bytes/s"
            dif = diferencia_carga(red, s1)

        x.append(dif)       # diferencia entre final e inicial
        if len(x) > 60:     
            x.pop(0)        # eliminamos el primer elemento
        x = np.array(x)

        ax.clear()      # limpiamos la tabla
        ax.plot(x[::-1], label=lb)
        
        ax.set_title("Uso Red")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Velocidad")
        ax.legend()
        ax.set_xlim(0, 60)      # mostrar maximo un minuto
        ax.invert_xaxis()

    ani = FuncAnimation(fig=fig, func=update, frames=60, fargs=(x,))
    plt.show()

def diferencia_descarga(red, r1):
    r2 = red.bytes_recv
    return r2 - r1

def diferencia_carga(red, s1):
    s2 = red.bytes_sent
    return s2 - s1