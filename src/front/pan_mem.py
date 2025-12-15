from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from queue import Queue
import tkinter as tk
import threading
import time
from src.back import almacenamiento, ram

class VentanaMemoria(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

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

        # ajuste
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # repeticiones
        self.actualizar()

    def obtener_memoria(self):
        while True:
            ram.division_memoria(self.cola_ram)
            time.sleep(1)
    
    def obtener_disco(self):
        while True:
            almacenamiento.division_disco(self.cola_disco)
            time.sleep(1)
    
    def grafico_ram(self):
        data_ram = self.cola_ram.get()
        if data_ram:
            self.ax_ram.clear()
            self.ax_ram.pie(data_ram, labels=self.etiquetas, autopct="%0.1f%%")
            self.canvas_ram.draw()

    def grafico_disco(self):
        data_disk = self.cola_disco.get()
        if data_disk:
            self.ax_disk.clear()
            self.ax_disk.pie(data_disk, labels=self.etiquetas, autopct="%0.1f%%")
            self.canvas_disk.draw()

    def actualizar(self):
        self.grafico_ram()
        self.grafico_disco()
        self.after(1000, self.actualizar)