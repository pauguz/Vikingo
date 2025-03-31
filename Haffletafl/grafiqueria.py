import tkinter as tk
from Bando import bando
from PIL import Image, ImageTk 
from matematiqueria import ubicar


def etiquetado(i:int, j:int, root, func):
    label = tk.Label(root, width=4, height=2, relief="solid", borderwidth=3)
    label.grid(row=i, column=j)
    label.bind("<Button-1>", func)
    return label
def etiquetados(v, func, d):
    return [[etiquetado(i,j, v, func) for j in range(d)] for i in range(d)]

def ventor(v, tit):
    # Configurar el título de la ventana
    v.title(tit)
    # Configurar las dimensiones de la ventana
    v.geometry("800x600")
    # Configurar el tamaño mínimo y máximo de la ventana para evitar deformación
    v.minsize(800, 600)
    v.maxsize(1200, 900) 
    v.resizable(True, True)
    v.config(bg="beige")

#Las siguientes 3 funciones llenan las casillas con los iconos de la ficha, a nivel individual, de bando y de tablero respectivamente
def asignarImagen(j, dup, labels, num1:int, num2:int=1):
    imago=None
    #Crear Texto identificador
    t=str(num1)
    if(num1==0):
        imago=j.bandos[0].logo
    elif(num2==0):
        imago=j.bandos[1].imagen_real
        t=t+" "+str(num2)
    else:
        imago=j.bandos[1].logo
    #Tomar el valor de la casilla
    casilla=ubicar(labels, dup)
    #Ajustar tamaño de la imagen y su formato
    #imago=imago.resize((casilla.winfo_width(),casilla.winfo_height()), Image.LANCZOS )
    imago=imago.resize((30,30), Image.LANCZOS )
    tkimago=ImageTk.PhotoImage(image=imago)
    
    #Asignar Imagen y Texto
    casilla.config(image=tkimago, text=t, width=30, height=32)
    casilla.image=tkimago 
    #casilla.grid(row=dup[0],column=dup[1])

        
def graficarBando(labels, b:bando, num1:int, j):
    l=b.miembros
    for i in range(len(l)):
        asignarImagen(j, l[i],labels, num1, i)
    
def graficar(j, labels):
    band=j.bandos
    for i in range(len(band)):
        graficarBando(labels, band[i], i, j)

def graficarMovimientosPosibles(labels, movimientos):
    for mov in movimientos:
        fila, columna = mov
        casilla = labels[fila][columna]
        casilla.config(bg='turquoise')

def restaurarMovimientos(labels, movs):
    for mov in movs: #restaurar el estado original de las casillas con posibles movimientos
        fila, columna = mov
        casilla = labels[fila][columna]
        casilla.config(bg="SystemButtonFace")

#Esta funcion devuelve la tupla con las 2 coordenadas de la casilla seleccionada
def ObtenerUbicación(label:tk.Label):
    # Get the grid info of the widget
    grid_info = label.grid_info()
    row = grid_info.get('row', None)  # Default to None if not found
    column = grid_info.get('column', None)  # Default to None if not found
    return (row, column)


def fin():
        fin=tk.Toplevel()
        fin.title("Fin del Juego")
        fin.geometry("600x450")
        st+=' GANAN'
        label = tk.Label(fin, text=st, bg="lightgreen", font=("Helvetica", 16))
        label.pack(fill=tk.BOTH, expand=True)
        fin.mainloop()

def liberar(labels):
    for i in labels:
        for j in i:
            j.unbind("<Button-1>") 