from tkinter import ttk
from queue import Queue
import tkinter as tk
from src.back import procesos
import threading

class VentanaProcesos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.q = Queue()

        self.mostrar_procesos()

    def mostrar_procesos(self):
        self.q = Queue()
        a = threading.Thread(target=procesos.obtener_procesos, args=(self.q,), daemon=True)
        a.start()
        a.join()

        procs = self.q.get()
        num_procs = len(procs)
        headings = ["PID", "Nombre", "Username", "% CPU", "Estado", "Memoria"]

        # plantilla de tabla
        self.tv = ttk.Treeview(self, selectmode="browse")
        self.tv.grid(row=0, column=0, sticky="nsew")

        # barra scroll
        scroll_bar = ttk.Scrollbar(self, orient="vertical", command=self.tv.yview)
        scroll_bar.grid(row=0, column=1)
        self.tv.configure(yscrollcommand=scroll_bar.set)

        self.tv["columns"] = ("1","2", "3", "4", "5", "6")
        self.tv["show"] = "headings"

        for i in range(len(headings)):
            self.tv.column(f"{i+1}", width=130, anchor="center")
            self.tv.heading(f"{i+1}", text=headings[i])

        for p in range(num_procs):
            self.tv.insert("", "end", values=procs[p])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.after(5000, self.mostrar_procesos)