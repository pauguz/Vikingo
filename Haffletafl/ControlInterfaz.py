import Interfaz
import Tablero
import tkinter as tk
import Soldado
from PIL import Image, ImageTk 


@staticmethod
def getImagen(t,numero):
    cas=t.fichas[numero]
    return cas.imagen

@staticmethod
def graficarTablero(v,t): 
    for i in range(len(v.labels)):
        v.labels[i].configure(getImagen(t,i))


    
    



