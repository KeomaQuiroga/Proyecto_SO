import tkinter as tk
import front.estadistica as estadistica
import front.memoria as memoria
import front.procesos as procesos

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # caracteristicas
        self.title("Proyecto SO")
        self.geometry("800x600")
        self.resizable(False, False)
        fuente = ("Arial", 20)

        # pantallas principales
        self.pantalla_estadistica = estadistica.VentanaEstadistica(self)
        self.pantalla_procesos = procesos.VentanaProcesos(self)
        self.pantalla_memoria = memoria.VentanaMemoria(self)

        self.pantalla_estadistica.grid(row=1, column=0, sticky="snew")      # mostramos primera pantalla

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

        # ajustar botones
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def cambiar_pantalla(self, frame):
        self.pantalla_estadistica.grid_remove()
        self.pantalla_procesos.grid_remove()
        self.pantalla_memoria.grid_remove()

        frame.grid(row=1, column=0, sticky="snew")

if __name__ == "__main__":
    root = App()
    root.mainloop()