import tkinter as tk
from Bando import bando
from PIL import Image, ImageTk 
from matematiqueria import ubicar


def etiquetado(i:int, j:int, root, func):
    label = tk.Label(root, width=4, height=2, relief="solid", borderwidth=3)
    label.grid(row=i, column=j)
    label.bind("<Button-1>", func)
    return label

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
    #Reemplazar vieja casilla por la nueva
    labels[dup[0]][dup[1]]=casilla
        
def graficarBando(labels, b:bando, num1:int, j):
    l=b.miembros
    for i in range(len(l)):
        asignarImagen(j, l[i],labels, num1, i)
    
def graficar(j, labels):
    band=j.bandos
    for i in range(len(band)):
        graficarBando(labels, band[i], i, j)
