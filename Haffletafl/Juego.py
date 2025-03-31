from Bando import bando
import matematiqueria as mat

class juego:
    def __init__(s, dim:int, soldados:list|None ):
        if(soldados==None):
            soldados=mat.listador(dim)
        s.dim=dim
        s.bandos=[bando(i) for i in soldados]
        s.posiciones= [[None] * dim for _ in range(dim)]
        s.imgs=[] 
        s.funcs=[]
        s.fichar()
    
    def fichar(s):
        for i in s.bandos[0].miembros:
            s.posiciones[i[0]][i[1]]=(0,0)
        for i in s.bandos[1].miembros:
            s.posiciones[i[0]][i[1]]=(1,0)
        i=s.bandos[1].miembros[0]
        s.posiciones[i[0]][i[1]]=(1,1)

    def mover(s, inic, dest):
        val=mat.ubicar(s.posiciones, inic)
        s.posiciones[dest[0]][dest[1]]=val
        s.posiciones[inic[0]][inic[1]]=None

    def dibujar(s):
        s.bandos[0].setsoldado("vikingonegro.png")
        s.bandos[1].setsoldado("vikingoblanco.png")
        s.bandos[1].setRey("reg.png")

    
    def captura(s, dup:tuple):
        s.posiciones[dup[0]][dup[1]]=None


        
