from Bando import bando
import matematiqueria
import tkinter as tk

def listador(dim:int):
    lisB=[]
    lisN=[]
    media=dim//2
    medium=(dim**2)//2
    #Llenar con Fichas negras
    for i in range(media-2, media+3):
        lisN.extend(matematiqueria.coordenarEnlistado(dim, i, medium*2-i, i*dim,(i+1)*dim-1 ))
    #Llenar con Fichas blancas  
    for i in range(-2,3):
        j=2-abs(i)
        for k in range (medium+i*dim-j,medium+i*dim+j+1):
            lisB.append(matematiqueria.coordenar(k, dim))
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

        #Movimiento como tal
        inicio=self.ubicar(lis)
        paso=matematiqueria.getPaso(inicio, destino)
        print("Inicio en Paso: ", end=" ")
        print(inicio)
        print("Paso: ", end=" ")
        print(paso)
        if(paso!=None):
            l=self.bandos[0].miembros +self.bandos[1].miembros
            while(inicio != destino):
                inicio=matematiqueria.SumaDupla(inicio, paso)
                if (inicio in l):
                    return False
            self.bandos[lis[0]].miembros[lis[1]]=inicio
            print("Destino: ")
            print(inicio)
            return True
        


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
        
