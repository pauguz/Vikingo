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



    