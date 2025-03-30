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

    def __init__(self, jue:juego, turn=1):
        self.seleccion=None  
        # Crear una instancia de la ventana
        self.ventana = tk.Toplevel()
        grf.ventor(self.ventana, "Hnefatafl")
        self.j=jue
        self.turno=turn
        self.movspos=[]
        self.llenar()
        self.Inicio()
    
    def Inicio(self, event=None):
        self.labels=grf.etiquetados(self.ventana, self.Seleccionar, self.j.dim )
        grf.graficar(self.j, self.labels)
        
    def llenar(self):
        self.nuncio=tk.Label(self.ventana, width=8, height=2, borderwidth=1, relief="solid")
        re = tk.Label(self.ventana, text=" RETVRN ", borderwidth=1, relief="solid")
        re.place(x=self.j.dim*37.5, y=60)
        re.bind("<Button-1>", self.Inicio )
        self.nuncio.place(x=self.j.dim*37.5, y=6)
    
    def validar(self, dup):
        d=self.j.dim
        return dup[0]>=0 and dup[0]<d and dup[1]>=0 and dup[1]<d    
    
    def obtenerContNum(self, d:tuple):
        if(self.validar(d)):
            return obtener_Contenido(mat.ubicar(self.labels, d))
        return [None]
    
    #Funciones para el movimiento -------------------------------------------------------------------------------------------
    
    def captura(self, p):
        self.j.captura(p)
        self.labels[p[0]][p[1]]=grf.etiquetado(p[0], p[1], self.ventana, self.Seleccionar)
        l=self.obtenerContNum(p)
        if l==[1, 0]:
            grf.fin('NEGRAS')
            self.liberar(self.labels)

    def Pruebas(self, p):
        mat.capturaEuro(self.j.posiciones, p, self.captura)
    #-------------------------------------------------------------------------
    
    def liberar(labels):
        for i in labels:
            for j in i:
                j.unbind("<Button-1>") 

#Esta funcion devuelve la tupla con las 2 coordenadas de la casilla seleccionada
    def ObtenerUbicación(self, label:tk.Label):
        # Get the grid info of the widget
        grid_info = label.grid_info()
        row = grid_info.get('row', None)  # Default to None if not found
        column = grid_info.get('column', None)  # Default to None if not found
        # Return the position as a tuple
        return (row, column)

    def blanquear(self, lis, destino):
        comp=[self.j.dim-1, 0]
        if(lis==[1, 0] and destino[0] in comp and destino[1] in comp):
            grf.fin('BLANCAS')
            self.liberar(self.labels)
    

    def Seleccionar(self, event:tk.Event):
        #sel es None cuando se hace el primer clic y es una tupla cuando se hace el segundo
        sel=self.seleccion
        l=obtener_Contenido(event.widget)
        boola=(sel==None)
        boolb=(l==[])
        if (boola and not boolb):
            if (self.turno==l[0]):
                self.seleccion=self.ObtenerUbicación(event.widget) 
                print("Contenido:", end=" ")
                print(l)
                print("Inicio: ", end=" ")
                print(self.seleccion)
                self.movspos=mat.MovimientosPosibles(self.seleccion, self.obtenerContNum)
                grf.graficarMovimientosPosibles(self.labels, self.movspos)

        if(not boola and boolb):
            t=self.seleccion
            casSel=mat.ubicar(self.labels, t)
            self.seleccion=None
            l=obtener_Contenido(casSel)
            destino=event.widget
            ub=self.ObtenerUbicación(destino)
            print("Destino: ", end=" ")
            print(ub)
        #comprobar si el movimiento es posible
            if( ub in self.movspos ): 
                self.turno+=1
                self.turno=(self.turno)%2                
                #Parte Mejorable//Vaciar lab
                self.labels[t[0]][t[1]]=etiquetado(t[0], t[1], self.ventana, self.Seleccionar)
                grf.asignarImagen(self.j, ub, self.labels, *l)
                self.j.mover( t, ub)
                self.Pruebas(ub)
                self.blanquear(l, ub)
                for i in self.j.posiciones:
                    print(i)
                print("----------------------------------------------------------------")
            grf.restaurarMovimientos(self.labels, self.movspos)

# Ejecutar el bucle principal de la aplicación
jue=juego(9, None)
jue.dibujar()
v=vista(jue)
v.ventana.mainloop()