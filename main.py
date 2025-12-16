import tkinter as tk
from src.front import pan_est, pan_mem, pan_pro

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # caracteristicas
        self.title("Proyecto SO")
        self.geometry("800x600")
        self.resizable(False, False)
        fuente = ("Arial", 20)

        # pantallas principales
        self.pantalla_estadistica = pan_est.VentanaEstadistica(self)
        self.pantalla_procesos = pan_pro.VentanaProcesos(self)
        self.pantalla_memoria = pan_mem.VentanaMemoria(self)

        self.pantalla_estadistica.grid(row=1, column=0, columnspan=3, sticky="snew")      # mostramos primera pantalla

        # botones para cambiar
        btn_estadistica = tk.Button(self, text="Estadistica", command=lambda: self.cambiar_pantalla(self.pantalla_estadistica))
        btn_estadistica.config(font=fuente)
        btn_estadistica.grid(row=0, column=0, sticky="we")

        btn_procesos = tk.Button(self, text="Procesos", command=lambda: self.cambiar_pantalla(self.pantalla_procesos))
        btn_procesos.config(font=fuente)
        btn_procesos.grid(row=0, column=1, sticky="we")

        btn_memoria = tk.Button(self, text="Memoria", command=lambda: self.cambiar_pantalla(self.pantalla_memoria))
        btn_memoria.config(font=fuente)
        btn_memoria.grid(row=0, column=2, sticky="we")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ajustar botones
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def cambiar_pantalla(self, frame):
        self.pantalla_estadistica.grid_remove()
        self.pantalla_procesos.grid_remove()
        self.pantalla_memoria.grid_remove()

        frame.grid(row=1, column=0, columnspan=3, sticky="snew")
    
    def on_closing(self):
        # parar hilos de cada proceso
        self.pantalla_estadistica.detener_hilos()
        self.pantalla_memoria.detener_hilos()
        self.pantalla_procesos.detener_hilos()

        self.destroy()

if __name__ == "__main__":
    root = App()
    root.mainloop()