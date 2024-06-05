import tkinter as tk
from PIL import Image, ImageTk

class soldado:

    def __init__(self, bool):   
        self.bando=bool
        self.listaMov=list([])
        if (self.bando):
            self.imagen=ImageTk.PhotoImage(file="vikingoblanco.png") 
        else:
            self.imagen=ImageTk.PhotoImage(file="vikingonegro.png") 


    def mover(self, n):
        m=n%11
        for i in range (m+1, m, (i+1)%11):
            self.listaMov.append(11*(n//11)+i)
        m=n//11
        for i in range (m+1, m, (i+1)%11):
            self.listaMov.append(n%11+i*11)
    

class rey(soldado):
    def __init__(self):
        soldado.__init__(True)
        self.imagen=ImageTk.PhotoImage(file="reg.png") 


    