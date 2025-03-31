import tkinter as tk
import grafiqueria as grf
import matematiqueria as mat
from Juego import juego
from PIL import Image, ImageTk 
from Bando import bando

def etiquetado(i:int, j:int, root, func):
    label = tk.Label(root, width=4, height=2, relief="solid", borderwidth=3)
    label.grid(row=i, column=j)
    label.bind("<Button-1>", func)
    return label

def obtener_Contenido(lab: tk.Label):
    return list(map (int, lab.cget("text").split()))


class vista:

    def __init__(s, jue:juego, turn=1):
        s.seleccion=None  
        # Crear una instancia de la ventana
        s.ventana = tk.Toplevel()
        grf.ventor(s.ventana, "Hnefatafl")
        s.j=jue
        s.turno=turn
        s.movspos=[]
        s.llenar()
        s.Inicio()

    
    def Inicio(s, event=None):
        s.labels=grf.etiquetados(s.ventana, s.Seleccionar, s.j.dim )
        grf.graficar(s.j, s.labels)
        
    def llenar(s):
        s.nuncio=tk.Label(s.ventana, width=8, height=2, borderwidth=1, relief="solid")
        re = tk.Label(s.ventana, text=" RETVRN ", borderwidth=1, relief="solid")
        re.place(x=s.j.dim*37.5, y=60)
        re.bind("<Button-1>", s.Inicio )
        s.nuncio.place(x=s.j.dim*37.5, y=6)
    
    def validar(s, dup):
        d=s.j.dim
        return dup[0]>=0 and dup[0]<d and dup[1]>=0 and dup[1]<d    
    
    def obtenerContNum(s, d:tuple):
        if(s.validar(d)):
            return obtener_Contenido(mat.ubicar(s.labels, d))
        return [None]
    
    def tornar(s):
        s.turno+=1
        s.turno%=2
        
    def captura(s, p):
        s.j.captura(p)
        s.labels[p[0]][p[1]]=grf.etiquetado(p[0], p[1], s.ventana, s.Seleccionar)
        l=s.obtenerContNum(p)
        if l==[1, 0]:
            grf.fin('NEGRAS')
            grf.liberar(s.labels)

    def Pruebas(s, p):
        mat.capturaEuro(s.j.posiciones, p, s.captura)
    
    def blanquear(s, lis, destino):
        comp=[s.j.dim-1, 0]
        if(lis==[1, 0] and destino[0] in comp and destino[1] in comp):
            grf.fin('BLANCAS')
            grf.liberar(s.labels)
    

    def Seleccionar(s, event:tk.Event):
        #sel es None cuando se hace el primer clic y es una tupla cuando se hace el segundo
        sel=s.seleccion
        l=obtener_Contenido(event.widget)
        boola=(sel==None)
        boolb=(l==[])
        if (boola and not boolb):
            if (s.turno==l[0]):
                s.seleccion=grf.ObtenerUbicación(event.widget) 
                print("Contenido:", end=" ")
                print(l)
                print("Inicio: ", end=" ")
                print(s.seleccion)
                s.movspos=mat.MovimientosPosibles(s.seleccion, s.obtenerContNum)
                grf.graficarMovimientosPosibles(s.labels, s.movspos)

        if(not boola and boolb):
            t=s.seleccion
            casSel=mat.ubicar(s.labels, t)
            s.seleccion=None
            l=obtener_Contenido(casSel)
            destino=event.widget
            ub=grf.ObtenerUbicación(destino)
            print("Destino: ", end=" ")
            print(ub)
        #comprobar si el movimiento es posible
            if( ub in s.movspos ): 
                s.tornar()           
                #Parte Mejorable//Vaciar lab
                s.labels[t[0]][t[1]]=etiquetado(t[0], t[1], s.ventana, s.Seleccionar)
                grf.asignarImagen(s.j, ub, s.labels, *l)
                s.j.mover( t, ub)
                s.Pruebas(ub)
                s.blanquear(l, ub)
                #for i in self.j.posiciones:
                #    print(i)
                print("----------------------------------------------------------------")
            grf.restaurarMovimientos(s.labels, s.movspos)


#jue=juego(9, None)
#jue.dibujar()
#v=vista(jue)
#v.ventana.mainloop()