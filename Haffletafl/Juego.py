from Bando import bando
import matematiqueria as mat
import tkinter as tk



class juego:
    def __init__(self, dim:int, soldados:list|None ):
        if(soldados==None):
            soldados=mat.listador(dim)
        self.dim=dim
        self.bandos=[bando(i) for i in soldados]

    def dibujar(self):
        self.bandos[0].setsoldado("vikingonegro.png")
        self.bandos[1].setsoldado("vikingoblanco.png")
        self.bandos[1].setRey("reg.png")


    def ubicar(self, lis:list):
        return self.bandos[lis[0]].miembros[lis[1]]
    
    def captura(self, lis:list):
        self.bandos[lis[0]].capturar(lis[1])


        
