import tkinter as tk
from PIL import Image, ImageTk

class bando:
    def __init__(self, lis:list):
        self.miembros=lis
        
    def setsoldado(self, imagen):
        self.logo=Image.open(imagen)

    def setRey(self, imagen):
        self.imagen_real=Image.open(imagen)

    def capturar(self, n:int):
        self.miembros[n]=None

    
 

