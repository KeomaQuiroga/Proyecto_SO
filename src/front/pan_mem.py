import tkinter as tk
import threading

class VentanaMemoria(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.fraccionamiento_memoria()

        lb = tk.Label(self, text="Almacenamiento")
        lb.grid(row=0, column=1, sticky="snew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def fraccionamiento_memoria(self):
        lb = tk.Label(self, text="Memoria", font=("Arial", 15))
        lb.grid(row=0, column=0, sticky="snew")