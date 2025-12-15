import tkinter as tk

class VentanaProcesos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        lb = tk.Label(self, text="Procesos")
        lb.pack()