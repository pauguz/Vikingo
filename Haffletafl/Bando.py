import tkinter as tk
from PIL import Image, ImageTk

class bando:
    def __init__(self, booleano: bool, imagen, lis:list):
        self.polo=booleano
        self.miembros=lis
        self.logo=Image.open(imagen)

    def setRey(self, imagen):
        self.imagen_real=Image.open(imagen)

    def capturar(self, n:int):
        self.miembros.pop(n)
    



    