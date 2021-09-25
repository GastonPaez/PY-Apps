from tkinter import *
from vista import VistaApp


class AgendaApp:
    def __init__(self, window):
        # Ventana Principal
        self.ventana = window
        VistaApp(self.ventana)


if __name__ == "__main__":
    root = Tk()
    AgendaApp(root)
    root.mainloop()
