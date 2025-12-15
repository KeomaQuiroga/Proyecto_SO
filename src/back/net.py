from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import psutil
import time

def diferencia_descarga(red, r1):
    r2 = red.bytes_recv
    return r2 - r1

def diferencia_carga(red, s1):
    s2 = red.bytes_sent
    return s2 - s1

def carga_descarga(q):
    """
    Devuelve la velocidad de escritura y lectura en bytes
    
    :param q: QUeue para compartir datos
    """
    x = []

    # tomamos el primer valor
    red = psutil.net_io_counters()
    r1 = red.bytes_recv
    s1 = red.bytes_sent

    time.sleep(1)       # esperamos

    # tomamos el segundo valor
    red = psutil.net_io_counters()

    # calculamos diferencia
    dif_recive = diferencia_descarga(red, r1)
    dif_sent = diferencia_carga(red, s1)

    x.append([dif_sent, dif_recive])
    q.put(x)