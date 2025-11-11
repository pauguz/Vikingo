direccionales = [[(1,0), (-1,0)], [(0,1), (0,-1)]]

def mcd(a, b):
    while b != 0:
        remainder = a % b
        a = b
        b = remainder
    return a


class DupOps:
    @staticmethod
    def SumaDupla(dup1:tuple, dup2:tuple):
        return tuple(a + b for a, b in zip(dup1, dup2))

    @staticmethod
    def MultDupla(dup:tuple, f:float):
        return tuple(int(x*f) for x in dup)

    @staticmethod
    def RestDupla(dup1: tuple, dup2:tuple):
        return DupOps.SumaDupla(dup1, DupOps.MultDupla(dup2, -1))
    
    @staticmethod
    def SimDupla(dup):
        a, b = dup
        m=mcd(a,b)
        return tuple(a/m, b/m)


    @staticmethod
    def MultDuplaT(dup:tuple, t):
        pass

    @staticmethod
    def getPaso(dup1:tuple, dup2:tuple):
        paso = DupOps.RestDupla(dup2, dup1)
        a = (paso[0]==0) or (paso[1]==0)
        b = (paso[0]!=paso[1])
        if (a and b):
            while(abs(paso[0]+paso[1])!=1):
                paso = DupOps.MultDupla(paso, 0.5)
            return paso


class Coords:
    @staticmethod
    def coordenar(numero:int, unidad:int):
        return (numero//unidad, numero%unidad)

    @staticmethod
    def coordenarEnlistado(unidad:int, *args):
        lis=[]
        for i in args:
            lis.append(Coords.coordenar(i, unidad))
        return lis

    @staticmethod
    def listador(dim:int):
        lisB=[]
        lisN=[]
        media=dim//2
        medium=(dim**2)//2
        #Llenar con Fichas negras
        for i in range(media-2, media+3):
            k=i*dim
            lisN.extend(Coords.coordenarEnlistado(dim, i, medium*2-i, k, medium*2-k))
        lisN.extend(Coords.coordenarEnlistado(dim, dim+media, 2*medium-media*3-1, (media)*dim+1, (media+1)*dim-2) )
        #Llenar con Fichas blancas  
        for i in range(-2,3):
            j=2-abs(i)
            for k in range (medium+i*dim-j,medium+i*dim+j+1):
                lisB.append(Coords.coordenar(k, dim))
        lisB[0], lisB[6] = lisB[6], lisB[0]
        return [lisN, lisB]

    @staticmethod
    def ubicar(labels, dup:tuple):
        return labels[dup[0]][dup[1]]

    @staticmethod
    def validar(dup, n):
        return dup[0]<n and dup[0]>=0 and dup[1]<n and dup[1]>=0

    @staticmethod
    def Dimendor(d):
        if d.isdigit():
            d=int(d)
            return d>=9 and d%2==1
        return False

    @staticmethod
    def MenorHuida(dup, dim):
        a=min(dup[0], dim-dup[0])
        b=min(dup[1], dim-dup[1])
        return a+b


class Movs:
    @staticmethod
    def Comprobar(pos:tuple, eje:int, func, p:bool=False,n:bool=False):
        vec=[DupOps.SumaDupla(pos, i) for i in direccionales[eje]]
        if not p:
            p=func(pos, vec[0])
        if not n:
            n=func(pos, vec[1])
        return p and n 

    @staticmethod
    def Mover(inicio, destino, func):
        paso=DupOps.getPaso(inicio, destino)
        if(paso!=None):
            while(inicio != destino):
                inicio=DupOps.SumaDupla(inicio, paso)
                if (func(inicio) ):
                    return False
            print("Destino: ")
            print(inicio)
            return True

    @staticmethod
    def MovimientosPosibles(inicio, func):
        movimientosPosibles = []
        d=direccionales[0] + direccionales[1]
        for direccion in d:
            puedoAgregar = True
            i = 1  # Para ir avanzando en la dirección
            while puedoAgregar:
                # Calcular el nuevo fin sumando la dirección multiplicada por la iteración
                fin = DupOps.SumaDupla(inicio, DupOps.MultDupla(direccion, i))
                # Verificar si se puede mover al nuevo fin
                puedoAgregar = not func(fin)
                if puedoAgregar:
                    movimientosPosibles.append(fin)  # Agregar el movimiento posible
                i += 1  # Aumentar la distancia en esa dirección
        return movimientosPosibles


class Tablero:
    @staticmethod
    def Generar(dispin, d):
        r=[[None for _ in range(d)] for _ in range(d)]
        k=dispin[1].pop(0)
        print(k)
        r[k[0]][k[1]]=[1,0]
        for i in range(2):
            for j in dispin[i]:
                r[j[0]][j[1]]=i
        return r


class Caps:
    @staticmethod
    def Discriminante(matriz:list, dup1, dup2, l):
        a=Coords.ubicar(matriz, dup1) 
        b=0
        if(not Coords.validar(dup2,l)):
            return False # si esto es true se acorrala contra el borde
        l-=1
        if(dup2[0]%l + dup2[1]%l == 0):
            b=[1]
        else: 
            b=Coords.ubicar(matriz, dup2)
        if b and a:
            print("contacto")
            return a[0]!=b[0]
        return False

    @staticmethod
    def DiscDirecta(matriz, dup, drec, l):
        return Caps.Discriminante(matriz, dup, DupOps.SumaDupla(dup, drec), l)

    @staticmethod
    def DiscDoble(matriz, dup, drec, l):
        if(Caps.DiscDirecta(matriz, dup, drec, l)):
            print("enemigo")
            return Caps.DiscDirecta(matriz, DupOps.SumaDupla(dup, drec), drec, l)
        return False

    @staticmethod
    def capturaEuro(matriz:list, dup,capt): #usa esto en combinacion con las funciones para quitar la ficha capturada
        dir=direccionales[0]+direccionales[1]
        l=matriz.__len__()
        for i in dir:
            if(Caps.DiscDoble(matriz, dup, i, l) ):
                print("capturado")
                capt(DupOps.SumaDupla(dup, i))
        # mejorable, hace 4 iteraciones cuando podrian ser 3
