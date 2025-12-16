from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from queue import Queue
import tkinter as tk
import threading
import time

import numpy as np
import squarify
from src.back import almacenamiento, ram

class VentanaMemoria(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parada= threading.Event()

        # colas
        self.cola_ram = Queue()        # cola para memoria
        self.cola_disco = Queue()        # cola para disco
        self.etiquetas = ["Libre", "Uso"]

        # ajuste basico
        lb = tk.Label(self, text="Memoria", font=("Arial", 15))
        lb.grid(row=0, column=0, sticky="snew")
        lb = tk.Label(self, text="Almacenamiento", font=("Arial", 15))
        lb.grid(row=0, column=1, sticky="snew")

        # hilos
        self.thread_ram = threading.Thread(target=self.obtener_memoria, daemon=True)
        self.thread_ram.start()
        self.thread_disk = threading.Thread(target=self.obtener_disco, daemon=True)
        self.thread_disk.start()

        # canvas
        self.fig_ram = plt.figure(figsize=(4, 4))
        self.ax_ram = self.fig_ram.add_subplot(111)
        self.canvas_ram = FigureCanvasTkAgg(figure=self.fig_ram, master=self)
        self.canvas_widget_ram = self.canvas_ram.get_tk_widget()
        self.canvas_widget_ram.grid(row=1, column=0, sticky="snew", padx="10")

        self.fig_disk = plt.figure(figsize=(4, 4))
        self.ax_disk = self.fig_disk.add_subplot(111)
        self.canvas_disk = FigureCanvasTkAgg(figure=self.fig_disk, master=self)
        self.canvas_widget_disk = self.canvas_disk.get_tk_widget()
        self.canvas_widget_disk.grid(row=1, column=1, sticky="snew", padx="10")

        # boton para cambiar
        btn = tk.Button(self, text="Memoria en procesos", font=("Arial", 15), command=self.tree_map)
        btn.grid(row=2, column=0, sticky="snew")

        # ajuste
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # repeticiones
        self.actualizar()

    def obtener_memoria(self):
        while not self.parada.is_set():
            ram.division_memoria(self.cola_ram)
            time.sleep(1)
    
    def obtener_disco(self):
        while not self.parada.is_set():
            almacenamiento.division_disco(self.cola_disco)
            time.sleep(1)
    
    def grafico_ram(self):
        data_ram = self.cola_ram.get()
        self.ax_ram.clear()
        self.ax_ram.pie(data_ram, labels=self.etiquetas, autopct="%0.1f%%")
        self.canvas_ram.draw()

    def grafico_disco(self):
        data_disk = self.cola_disco.get()
        self.ax_disk.clear()
        self.ax_disk.pie(data_disk, labels=self.etiquetas, autopct="%0.1f%%")
        self.canvas_disk.draw()

    def actualizar(self):
        self.grafico_ram()
        self.grafico_disco()
        self.after(1000, self.actualizar)
    
    def tree_map(self):
        # caracteristicas
        self.q_mem = Queue()
        nueva = tk.Toplevel(self)
        nueva.title("Treemap")
        nueva.geometry("640x480")
        nueva.resizable(False, False)

        # hilo
        nueva.t_bas = threading.Thread(target=self.obtener, daemon=True)
        nueva.t_bas.start()

        # canvas
        self.fig_tree = plt.figure()
        self.ax_tree = self.fig_tree.add_subplot()
        self.canvas_tree = FigureCanvasTkAgg(figure=self.fig_tree, master=nueva)
        self.canvas_widget_tree = self.canvas_tree.get_tk_widget()
        self.canvas_widget_tree.grid(row=0, column=0, sticky="snew", padx="10")

        self.act(nueva)

        # ajuste
        nueva.grid_columnconfigure(0, weight=1)
        nueva.grid_rowconfigure(0, weight=1)

    def act(self,nueva):
        self.grafico()
        nueva.after(1000, self.act)

    def obtener(self):
        ram.fracc_memoria_avanzado()
        while True:
            ram.treemap(self.q_mem)
            time.sleep(1)

    def grafico(self):
        mem = self.q_mem.get()
        mem = np.array(mem)
        
        self.ax_tree.clear()
        squarify.plot(sizes=mem, ax=self.ax_tree)
        self.ax_tree.axis("off")
        self.canvas_tree.draw()

    def detener_hilos(self):
        self.parada.set()       # señal
        self.thread_ram.join()
        self.thread_disk.join()