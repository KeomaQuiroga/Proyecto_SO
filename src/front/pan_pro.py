from tkinter import ttk
from queue import Queue
import tkinter as tk
import threading
import time
from src.back import procesos

class VentanaProcesos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.q_procesos = Queue()

        self.mostrar_procesos()

        # hilo principal
        self.procesos_th = threading.Thread(target=self.get_procesos, daemon=True)
        self.procesos_th.start()

        self.actualizar()       # actualizacion

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
    
    def actualizar(self):
        self.llenar()
        self.after(1000, self.actualizar)

    def get_procesos(self):
        while True:
            procesos.obtener_procesos(self.q_procesos)
            time.sleep(1)

    def mostrar_procesos(self):
        heads = ("PID", "Nombre", "Username", "%CPU", "Estado", "Memoria")
        self.tv = ttk.Treeview(self)
        self.scroll = tk.Scrollbar(self, orient="vertical", command=self.tv.yview)
        self.scroll.grid(row=0, column=1)

        self.tv["columns"] = heads
        self.tv["show"] = "headings"
        for n in range(6):
            self.tv.column(heads[n], width=100, anchor="center")
            self.tv.heading(heads[n], text=heads[n])

        self.tv.grid(row=0, column=0, sticky="snew")

    def llenar(self):
        procs = self.q_procesos.get()       # obtener procesos

        # eliminamos
        for i in self.tv.get_children():
            self.tv.delete(i)

        # agregar
        for p in procs:
            self.tv.insert("", "end", values=(p[0], p[1], p[2], p[3], p[4], p[5]))