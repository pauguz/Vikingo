import tkinter as tk
from matematiqueria import Dimendor
from Juego import juego
#from Interfaz import vista

class menu:
    v=tk.Tk()
    v.title("Menu de Parametros")
    v.geometry("400x300")
    txt=tk.Label(v, text='Ingrese la dimension del Tablero')
    txt.place(x=150, y=40)
    dim=tk.Entry(v)
    dim.place(x=150, y=60)
    
    
    def cosas(self):
        self.bot=tk.Button(self.v, text='Iniciar', command=self.dimendir())
        #self.bot.bind("<Button-1>", self.dimendir)
        self.bot.place(x=155, y=70)
    
    def dimendir(self):
        d= self.dim.get()
        print(Dimendor(d))
        if (Dimendor(d)):
            self.dim.delete(0, tk.END)  # Vacía el input
            j=juego(d)
            #vent=vista(j)
            #vent.ventana.mainloop()
    


m=menu()
m.cosas()
m.v.mainloop()
