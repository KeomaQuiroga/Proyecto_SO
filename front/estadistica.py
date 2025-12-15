import tkinter as tk

class VentanaEstadistica(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        lb = tk.Label(self, text="Estadistica")
        lb.pack()