from matplotlib.animation import FuncAnimation
from queue import Queue
import matplotlib.pyplot as plt
import numpy as np
import psutil
import time

def porcentaje_almacenamiento():
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
        ax.plot(x[::-1])
        
        ax.set_title("Uso Almacenamiento")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("% Uso")
        ax.set_xlim(0, 60)      # mostrar maximo un minuto
        ax.invert_xaxis()
        ax.set_ylim(0, 100)     # 0% a 100%

    ani = FuncAnimation(fig=fig, func=update, frames=60, fargs=(x,))
    plt.show()

def diferencia_lectura(disk, l1):
    l2 = disk.read_bytes
    return l2 - l1

def diferencia_escritura(disk, e1):
    e2 = disk.write_bytes
    return e2 - e1

def division_disco(q):
    disk = psutil.disk_usage('/')
    libre = disk.free       # memoria disponible
    uso = disk.used     # memoria en uso
    x = [libre, uso]
    q.put(x)

def lect_escrt(q):
    """
    Devuelve la velocidad de escritura y lectura en bytes
    
    :param q: QUeue para compartir datos
    """
    x = []

    # tomamos el primer valor
    disk = psutil.disk_io_counters()
    l1 = disk.read_bytes
    e1 = disk.write_bytes

    time.sleep(1)       # esperamos

    # tomamos el segundo valor
    disk = psutil.disk_io_counters()

    # calculamos diferencia
    dif_lectura = diferencia_lectura(disk, l1)
    dif_escritura = diferencia_escritura(disk, e1)

    x.append([dif_lectura, dif_escritura])
    q.put(x)