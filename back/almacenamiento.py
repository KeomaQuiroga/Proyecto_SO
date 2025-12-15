from matplotlib.animation import FuncAnimation
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

def fracc_disco_basico():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    def update(frame):
        disk = psutil.disk_usage('/')
        libre = disk.free       # memoria disponible
        uso = disk.used     # memoria en uso

        x = [libre, uso]
        lb = ["Libre", "En uso"]

        ax.clear()      # se limpia
        ax.title("Fraccionamiento basico almacenamiento")
        ax.pie(x, labels=lb, autopct="%0.1f%%")

    ani = FuncAnimation(fig=fig, func=update, frames=60)
    plt.show()

def lectura_escritura_disco():
    fig = plt.figure()      # figura principal
    ax = fig.add_subplot(111)
    x = []      # guardar la cpu

    def update(frame, x):
        # primer tiempo de recibida
        disk = psutil.disk_io_counters()      # tomamos datos
        l1 = disk.read_bytes
        e1 = disk.write_bytes
        time.sleep(1)       # esperamos 1 segundo
        disk = psutil.disk_io_counters()      # volvemos a tomar datos

        df_lectura = diferencia_lectura(disk, l1)
        df_escritura = diferencia_escritura(disk, e1)
        lb1 = "Escribiendo bytes/s"
        lb2 = "Leyendo bytes/s"

        x.append([df_escritura, df_lectura])       # diferencia entre final e inicial
        if len(x) > 60:     
            x.pop(0)        # eliminamos el primer elemento
        x = np.array(x)

        ax.clear()      # limpiamos la tabla
        ax.plot(x[::-1, 0], label=lb1, color="orange")      # ploteamos escritura
        ax.plot(x[::-1, 1], label=lb2, color="blue")      # ploteamos lectura
        
        ax.set_title("Lectura-Escritura")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Velocidad")
        ax.legend()
        ax.set_xlim(0, 60)      # mostrar maximo un minuto
        ax.invert_xaxis()

    ani = FuncAnimation(fig=fig, func=update, frames=60, fargs=(x,))
    plt.show()

def diferencia_lectura(disk, l1):
    l2 = disk.read_bytes
    return l2 - l1

def diferencia_escritura(disk, e1):
    e2 = disk.write_bytes
    return e2 - e1

lectura_escritura_disco()