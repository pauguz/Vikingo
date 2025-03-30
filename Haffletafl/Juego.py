from Bando import bando
import matematiqueria as mat

class juego:
    def __init__(self, dim:int, soldados:list|None ):
        if(soldados==None):
            soldados=mat.listador(dim)
        self.dim=dim
        self.bandos=[bando(i) for i in soldados]
        self.posiciones= [[None] * dim for _ in range(dim)]
        self.imgs=[] 
        self.funcs=[]
        self.fichar()
    
    def fichar(self):
        for i in self.bandos[0].miembros:
            self.posiciones[i[0]][i[1]]=(0,0)
        for i in self.bandos[1].miembros:
            self.posiciones[i[0]][i[1]]=(1,0)
        i=self.bandos[1].miembros[0]
        self.posiciones[i[0]][i[1]]=(1,1)

    def mover(self, inic, dest):
        val=mat.ubicar(self.posiciones, inic)
        self.posiciones[dest[0]][dest[1]]=val
        self.posiciones[inic[0]][inic[1]]=None

    def dibujar(self):
        self.bandos[0].setsoldado("vikingonegro.png")
        self.bandos[1].setsoldado("vikingoblanco.png")
        self.bandos[1].setRey("reg.png")

    
    def captura(self, dup:tuple):
        self.posiciones[dup[0]][dup[1]]=None


        
