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

def carga_descarga(q_R):
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
    q_R.put(x)

def sent_bytes(q_sb):
    # tomamos el primer valor
    red = psutil.net_io_counters()
    s1 = red.bytes_sent

    time.sleep(1)       # esperamos

    # tomamos el segundo valor
    red = psutil.net_io_counters()

    # calculamos diferencia
    dif_sent = diferencia_carga(red, s1)
    q_sb.put(dif_sent)

def reciving_bytes(q_rb):
    # tomamos el primer valor
    red = psutil.net_io_counters()
    r1 = red.bytes_recv

    time.sleep(1)       # esperamos

    # tomamos el segundo valor
    red = psutil.net_io_counters()

    # calculamos diferencia
    dif_recive = diferencia_descarga(red, r1)
    q_rb.put(dif_recive)