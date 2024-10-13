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
        lisN.extend(mat.coordenarEnlistado(dim, i, medium*2-i, i*dim,(i+1)*dim-1 ))
    #Llenar con Fichas blancas  
    for i in range(-2,3):
        j=2-abs(i)
        for k in range (medium+i*dim-j,medium+i*dim+j+1):
            lisB.append(mat.coordenar(k, dim))
    lisN.extend(mat.coordenarEnlistado(dim, dim+media, 2*medium-media*3-1, (media)*dim+1, (media+1)*dim-2) )
    lisB[0], lisB[6]=lisB[6],lisB[0]
    return [lisN, lisB]

class juego:
    def __init__(self, dim:int, soldados:list|None ):
        if(soldados==None):
            soldados=listador(dim)
        Negro=bando(False, "vikingonegro.png",soldados[0])
        Blanco=bando(True, "vikingoblanco.png",soldados[1])
        Blanco.setRey("reg.png")
        self.bandos=[Negro, Blanco]
        self.dim=dim

    def ubicar(self, lis:list):
        return self.bandos[lis[0]].miembros[lis[1]]
    
    def captura(self, lis:list):
        self.bandos[lis[0]].capturar(lis[1])

    def mover(self, lis, destino, labels):
        #Codigo por si gana el blanco
        comp=[self.dim-1, 0]
        if(lis==[1, 0] and destino[0] in comp and destino[1] in comp):
            self.Terminar(labels, 'BLANCAS')

        
        


    def Terminar(self, labels, st):
        for i in labels:
            for j in i:
                j.unbind("<Button-1>")
        fin=tk.Tk()
        fin.title("Fin del Juego")
        fin.geometry("600x450")
        st=st+' GANAN'
        label = tk.Label(fin, text=st, bg="lightgreen", font=("Helvetica", 16))
        label.pack(fill=tk.BOTH, expand=True)
        fin.mainloop()
        
