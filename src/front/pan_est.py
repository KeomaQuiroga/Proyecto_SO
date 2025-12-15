from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from queue import Queue
import tkinter as tk
import threading
import time

import numpy as np
from src.back import almacenamiento, ram, cpu, net

class VentanaEstadistica(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # listas necesarios
        self.datos_cpu = []
        self.datos_ram = []
        self.datos_disco = []
        self.datos_net = []

        # colas
        self.cpu_cola = Queue()
        self.ram_cola = Queue()
        self.disk_cola = Queue()
        self.net_cola = Queue()

        # botones
        btn_cpu = tk.Button(self, text="CPU", command=self.mostrar_cpu)
        btn_cpu.grid(row=0, column=0, sticky="snew")

        btn_ram = tk.Button(self, text="RAM", command=self.mostrar_ram)
        btn_ram.grid(row=1, column=0, sticky="snew")
        
        btn_disk = tk.Button(self, text="Disco", command=self.mostrar_disco)
        btn_disk.grid(row=2, column=0, sticky="snew")

        btn_red = tk.Button(self, text="Red", command=self.mostrar_red)
        btn_red.grid(row=3, column=0, sticky="snew")

        self.mostrar_red()
        self.mostrar_ram()
        self.mostrar_disco()
        self.mostrar_cpu()

        # hilo
        self.net_th = threading.Thread(target=self.obtener_red, daemon=True)
        self.net_th.start()
        self.ram_th = threading.Thread(target=self.obtener_Ram, daemon=True)
        self.ram_th.start()
        self.disk_th = threading.Thread(target=self.obtener_disco, daemon=True)
        self.disk_th.start()
        self.cpu_th = threading.Thread(target=self.obtener_cpu, daemon=True)
        self.cpu_th.start()

        self.actualizar()       # actualizar datos

        # ajustar
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

    # actualizacion para todos
    def actualizar(self):
        self.grafico_cpu()
        self.grafico_ram()
        self.grafico_disco()
        self.grafico_red()
        self.after(1000, self.actualizar)

    # CPU-INICIO #
    def mostrar_cpu(self):
        # canvas
        self.fig_cpu = plt.figure(figsize=(4, 4))
        self.ax_cpu = self.fig_cpu.add_subplot(111)
        self.canvas_cpu = FigureCanvasTkAgg(figure=self.fig_cpu, master=self)
        self.canvas_widget_cpu = self.canvas_cpu.get_tk_widget()
        self.canvas_widget_cpu.grid(row=0, column=1, sticky="snew", padx="10", rowspan=4)

    def obtener_cpu(self):
        while True:
            cpu.cpu_porcentaje(self.cpu_cola)

    def grafico_cpu(self):
        data_cpu = self.cpu_cola.get()
        self.datos_cpu.append(data_cpu)

        if len(self.datos_cpu) > 60:
            self.datos_cpu.pop(0)
        self.datos_cpu_np = np.array(self.datos_cpu)

        self.ax_cpu.clear()
        for i in range(len(self.datos_cpu_np[0])):
            self.ax_cpu.plot(self.datos_cpu_np[::-1, i], label=f"CPU {i+1}")        # ploteamos cada cpu - chat

        self.ax_cpu.set_xlabel("Tiempo (s)")
        self.ax_cpu.set_ylabel("% CPU")

        self.ax_cpu.set_xlim(0, 60)      # mostrar maximo un minuto
        self.ax_cpu.invert_xaxis()       # invertimos
        self.ax_cpu.set_ylim(0, 100)     # 0% a 100%
        self.ax_cpu.legend()
        self.canvas_cpu.draw()
    # CPU-FIN #

    # RAM-INICIO #
    def mostrar_ram(self):
        # canvas
        self.fig_ram = plt.figure(figsize=(4, 4))
        self.ax_ram = self.fig_ram.add_subplot(111)
        self.canvas_ram = FigureCanvasTkAgg(figure=self.fig_ram, master=self)
        self.canvas_widget_ram = self.canvas_ram.get_tk_widget()
        self.canvas_widget_ram.grid(row=0, column=1, sticky="snew", padx="10", rowspan=4)

    def obtener_Ram(self):
        while True:
            ram.ram_porcentaje(self.ram_cola)
            time.sleep(1)

    def grafico_ram(self):
        data_ram = self.ram_cola.get()
        self.datos_ram.append(data_ram)

        if len(self.datos_ram) > 60:
            self.datos_ram.pop(0)
        self.datos_ram_np = np.array(self.datos_ram)

        self.ax_ram.clear()
        self.ax_ram.plot(self.datos_ram_np[::-1, 0], label="Memoria")

        self.ax_ram.set_xlabel("Tiempo (s)")
        self.ax_ram.set_ylabel("% RAM")

        self.ax_ram.set_xlim(0, 60)      # mostrar maximo un minuto
        self.ax_ram.invert_xaxis()       # invertimos
        self.ax_ram.set_ylim(0, 100)     # 0% a 100%
        self.ax_ram.legend()
        self.canvas_ram.draw()
    # RAM-FIN #

    # DISCO-INICIO #
    def mostrar_disco(self):
        # canvas
        self.fig_disco = plt.figure(figsize=(4, 4))
        self.ax_disco = self.fig_disco.add_subplot(111)
        self.canvas_disco = FigureCanvasTkAgg(figure=self.fig_disco, master=self)
        self.canvas_widget_disco = self.canvas_disco.get_tk_widget()
        self.canvas_widget_disco.grid(row=0, column=1, sticky="snew", padx="10", rowspan=4)

    def obtener_disco(self):
        while True:
            almacenamiento.lect_escrt(self.disk_cola)

    def grafico_disco(self):
        data_disk = self.disk_cola.get()
        data_disk = np.array(data_disk).flatten()       # [[]] -> []
        self.datos_disco.append(data_disk)

        if len(self.datos_disco) > 60:
            self.datos_disco.pop(0)
        self.datos_disco_np = np.array(self.datos_disco)

        self.ax_disco.clear()
        self.ax_disco.plot(self.datos_disco_np[::-1, 0], label="Leyendo")
        self.ax_disco.plot(self.datos_disco_np[::-1, 1], label="Escribiendo")

        self.ax_disco.set_xlabel("Tiempo (s)")
        self.ax_disco.set_ylabel("Velocidad (bytes/s)")

        self.ax_disco.set_xlim(0, 60)      # mostrar maximo un minuto
        self.ax_disco.invert_xaxis()       # invertimos
        self.ax_disco.legend()
        self.canvas_disco.draw()
    # DISCO-FIN #

    # RED-INICIO #
    def mostrar_red(self):
        # canvas
        self.fig_red = plt.figure(figsize=(4, 4))
        self.ax_red = self.fig_red.add_subplot(111)
        self.canvas_red = FigureCanvasTkAgg(figure=self.fig_red, master=self)
        self.canvas_widget_red = self.canvas_red.get_tk_widget()
        self.canvas_widget_red.grid(row=0, column=1, sticky="snew", padx="10", rowspan=4)

    def obtener_red(self):
        while True:
            net.carga_descarga(self.net_cola)

    def grafico_red(self):
        data_disk = self.net_cola.get()
        data_disk = np.array(data_disk).flatten()       # [[]] -> []
        self.datos_net.append(data_disk)

        if len(self.datos_net) > 60:
            self.datos_net.pop(0)
        self.datos_net_np = np.array(self.datos_net)

        self.ax_red.clear()
        self.ax_red.plot(self.datos_net_np[::-1, 0], label="Enviando")
        self.ax_red.plot(self.datos_net_np[::-1, 1], label="Recibiendo")

        self.ax_red.set_xlabel("Tiempo (s)")
        self.ax_red.set_ylabel("Velocidad (bytes/s)")

        self.ax_red.set_xlim(0, 60)      # mostrar maximo un minuto
        self.ax_red.invert_xaxis()       # invertimos
        self.ax_red.legend()
        self.canvas_red.draw()
    # RED-FIN #