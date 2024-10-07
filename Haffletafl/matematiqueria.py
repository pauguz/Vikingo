direccionales=[[(1,0), (-1,0)], [(0,1), (0,-1)]]

@staticmethod
def coordenar(numero:int, unidad:int):
    return (numero//unidad, numero%unidad)

@staticmethod
def coordenarEnlistado(unidad:int, *args ):
    lis=[]
    for i in args:
        lis.append(coordenar(i, unidad))
    return lis

@staticmethod
def SumaDupla(dup1:tuple, dup2:tuple):
    return tuple(a + b for a, b in zip(dup1, dup2))

@staticmethod
def MultDupla(dup:tuple, f:float):
    return tuple( int(x*f) for x in dup)

@staticmethod
def getPaso(dup1:tuple, dup2:tuple):
    paso= SumaDupla( MultDupla(dup1, -1), dup2 )
    a=(paso[0]==0) or (paso[1]==0)
    b=(paso[0]!=paso[1])
    if (a and b):
        while(abs(paso[0]+paso[1])!=1):
            paso=MultDupla(paso, 0.5)
        return paso
    
@staticmethod
def Comprobar(pos:tuple, eje:int, func, p:bool=False,n:bool=False):
    vec=[SumaDupla(pos, i) for i in direccionales[eje]]
    if not p:
        p=func(pos, vec[0])
    if not n:
        n=func(pos, vec[1])
    return p and n 
    
