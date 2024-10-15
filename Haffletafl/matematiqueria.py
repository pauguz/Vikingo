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
def ubicar(labels, dup:tuple):
    return labels[dup[0]][dup[1]]

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
    
@staticmethod
def Mover(inicio, destino, func):
    #Movimiento como tal
    paso=getPaso(inicio, destino)
    print("Inicio en Paso: ", end=" ")
    print(inicio)
    print("Paso: ", end=" ")
    print(paso)
    if(paso!=None):
        while(inicio != destino):
            inicio=SumaDupla(inicio, paso)
            
            if (func(inicio) ):
                
                return False
        print("Destino: ")
        print(inicio)
        return True

@staticmethod
def MovimientosPosibles(inicio, func):
    direccionales = [(1, 0), (-1, 0), (0, 1), (0, -1)]  
    movimientosPosibles = []
    
    for direccion in direccionales:
        puedoAgregar = True
        iteracion = 1  # Para ir aumentando la distancia de la torre en la dirección
        while puedoAgregar:
            # Calcular el nuevo fin sumando la dirección multiplicada por la iteración
            fin = SumaDupla(inicio, MultDupla(direccion, iteracion))
            
            # Verificar si se puede mover al nuevo fin
            puedoAgregar = Mover(inicio, fin, func)
            if puedoAgregar:
                movimientosPosibles.append(fin)  # Agregar el movimiento posible
            iteracion += 1  # Aumentar la distancia en esa dirección
    
    return movimientosPosibles

@staticmethod
def Dimendor(d):
    if d.isdigit():
        d=int(d)
        return d>=9 and d%2==1
    return False