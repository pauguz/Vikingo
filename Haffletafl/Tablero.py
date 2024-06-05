import Soldado
class tablero:
    def __init__(self, dim=7):
        self.media=dim//2
        self.medium=dim*dim//2
        self.dimension=dim
        self.fichas=[None]*dim*dim
        self.llenarfichas()

    def llenarfichas(self):
        for i in range(self.media-2,self.media+3):
            self.fichas[i]=Soldado.soldado(False)
            self.fichas[-i-1]=Soldado.soldado(False)
            self.fichas[i*self.dimension]=Soldado.soldado(False)
            self.fichas[(i+1)*self.dimension-1]=Soldado.soldado(False)
        
        for i in range(-2,3):
            j=2-abs(i)
            for k in range (self.medium+i*self.dimension-j,self.medium+i*self.dimension+j+1):
                self.fichas[k]=Soldado.soldado(True)

    def moverfichas(self, inicio, destino):
        if(self.fichas[destino]==None and destino in self.fichas[inicio].mover[inicio]):
            self.fichas[destino]==self.fichas[inicio]
            self.fichas[inicio]==None
            


        




