from queue import Queue
import psutil
import time

def division_disco(q_dd):
    disk = psutil.disk_usage('/')
    libre = disk.free       # memoria disponible
    uso = disk.used     # memoria en uso
    x = [libre, uso]
    q_dd.put(x)

def lect_escrt(q_rw):
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
    q_rw.put(x)

def diferencia_lectura(disk, l1):
    l2 = disk.read_bytes
    return l2 - l1

def diferencia_escritura(disk, e1):
    e2 = disk.write_bytes
    return e2 - e1