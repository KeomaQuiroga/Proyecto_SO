from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import queue as Queue
import psutil

def cpu_porcentaje(q):
    """
    Porcentaje de cpu
    
    :param q: Queue para compartir datos
    """
    cpu = []
    cpu.append(psutil.cpu_percent(interval=1, percpu=True))     # tomamos cpu
    cpu = np.array(cpu)
    q.put(psutil.cpu_percent(interval=1, percpu=True))