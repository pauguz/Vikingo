import tkinter as tk
from PIL import Image, ImageTk

class bando:
    def __init__(s, lis:list):
        s.miembros=lis
        s.logo=None
        
    def setsoldado(s, imagen):
        s.logo=Image.open(imagen)

    def setRey(s, imagen):
        s.imagen_real=Image.open(imagen)

    def capturar(s, n:int):
        s.miembros.pop(n)

    
 

