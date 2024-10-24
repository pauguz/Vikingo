from Bando import bando
import matematiqueria as mat
import tkinter as tk

def listador(dim:int):
    lisB=[]
    lisN=[]
    media=dim//2
    medium=(dim**2)//2
    #Llenar con Fichas negras
    for i in range(media-2, media+3):
        k=i*dim
        lisN.extend(mat.coordenarEnlistado(dim, i, medium*2-i, k, medium*2-k))
    lisN.extend(mat.coordenarEnlistado(dim, dim+media, 2*medium-media*3-1, (media)*dim+1, (media+1)*dim-2) )
    #Llenar con Fichas blancas  
    for i in range(-2,3):
        j=2-abs(i)
        for k in range (medium+i*dim-j,medium+i*dim+j+1):
            lisB.append(mat.coordenar(k, dim))
    lisB[0], lisB[6]=lisB[6],lisB[0]
    return [lisN, lisB]

class juego:
    def __init__(self, dim:int, soldados:list|None ):
        if(soldados==None):
            soldados=listador(dim)
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


        
