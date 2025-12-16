from queue import Queue
import psutil

def obtener_procesos(q_OP):
    procs = []
    for p in psutil.process_iter():
        try:
            with p.oneshot():       # mas velocidad
                p_id = p.pid
                nombre = p.name()
                username = p.username()
                cpu_per = p.cpu_percent()
                estado = p.status()
                try:        # intenta obtener memoria
                    memoria = p.memory_full_info().uss
                    memoria, lb = transformar(memoria)
                    memoria = str(memoria) + lb
                except:
                    memoria = "NaN"     # si no se tiene acceso
        except Exception:       # por si un proceso no existe
            continue
        procs.append((p_id, nombre, username, cpu_per, estado, memoria))
    q_OP.put(procs)

def transformar(mem):
    # transformar de bytes a su correspondiente tamaño
    if mem > 1000000000:
        mem /= 1000000000
        lb = " GB"
    elif mem > 1000000:
        mem /= 1000000
        lb = " MB"
    elif mem > 1000:
        mem /= 1000
        lb = " KB"
    else:
        lb = " bytes"

    return round(mem, 2), lb

def eliminar_proceso(pid):
    p = psutil.Process(pid)
    p.kill()