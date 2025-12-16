import queue as Queue
import psutil

def cpu_porcentaje(q_C):
    q_C.put(psutil.cpu_percent(interval=1, percpu=True))