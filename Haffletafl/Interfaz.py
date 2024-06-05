import tkinter as tk
import Tablero
from PIL import Image, ImageTk 

#array letras
letras=list(['a','b','c','d','e','f','g','h','i','j','k'])


class vista:
      
# Crear una instancia de la ventana
    ventana = tk.Tk()

# Configurar el título de la ventana
    ventana.title("Mi Ventana")

# Configurar las dimensiones de la ventana
    ventana.geometry("600x400")

    ventana.config(bg="beige")

    pantalla=tk.Frame()
    def __init__(self, dimension):
        self.tafl=Tablero.tablero(dim=dimension)
        self.dimension=dimension
        
    def llenar(self):
        dim=self.dimension
        self.labels=[None]*(dim*dim)
        for i in range(dim):
            for j in range(dim):
            # Crear y colocar la etiqueta en la ventana
                label=tk.Label()
                label = tk.Label(self.ventana, width=4, height=2, relief="solid", borderwidth=1)
                label.grid(row=i, column=j)
                self.labels[i*dim+j]=label
    def graficar(self):
        dim=self.dimension
        etiquetas=self.labels
        tab=self.tafl
        for i in range(dim**2):
            if(tab.fichas[i] is not None):
                etiquetas[i].config(image=tab.fichas[i].imagen)





# Ejecutar el bucle principal de la aplicación

v=vista(11)
v.llenar()
v.graficar()
v.ventana.mainloop()

