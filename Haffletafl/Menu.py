import tkinter as tk
from matematiqueria import Dimendor
from Juego import juego
from Interfaz import vista

class menu:
    v=tk.Tk()
    v.title("Menu")
    v.geometry("400x300")
    dim=tk.Entry(v)
    dim.place(x=150, y=60)
    
    def __init__(self):
        txt=tk.Label(self.v, text='Ingrese la dimension del Tablero (Numero impar mayor que 9)')
        txt.place(x=150, y=40)
        #self.bot=tk.Button(self.v, text='Iniciar', command=self.dimendir())
        self.bot=tk.Label(self.v, text='Inicio', relief='solid' )
        self.bot.bind("<Button-1>", self.dimendir)
        self.bot.place(x=155, y=80)
    
    def dimendir(self, label):
        d=self.dim.get()
        print(Dimendor(d))
        if (Dimendor(d)):
            self.dim.delete(0, tk.END)  # Vacía el input
            j=juego(int(d), None)
            j.dibujar()
            vent=vista(j)
            vent.ventana.mainloop()
    
m=menu()
m.v.mainloop()
