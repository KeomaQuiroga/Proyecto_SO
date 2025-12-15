import psutil

def obtener_procesos():
    procs = {}
    for p in psutil.process_iter():
        with p.oneshot():       # mas velocidad
            p_id = p.pid
            nombre = p.name()
            username = p.username()
            cpu_per = p.cpu_percent()
            estado = p.status()
            try:        # intenta obtener memoria
                memoria = p.memory_full_info().uss
            except:
                memoria = "NaN"     # si no puede
        procs[p_id] = nombre, username, cpu_per, estado, memoria        
        
    return procs

def obtener_memoria_procesos():
    proc_mem = []
    for p in psutil.process_iter():
        with p.oneshot():       # mas velocidad
            try:        # intenta obtener memoria
                memoria = p.memory_full_info().uss
            except:
                memoria = 1     # si no puede
        proc_mem.append(memoria)
        
    return proc_mem

def obtener_nombre_procesos():
    proc_name = []
    for p in psutil.process_iter():
        with p.oneshot():       # mas velocidad
            nombre = p.name()
        proc_name.append(nombre)
        
    return proc_name