import tkinter as tk
from Juego import juego
import grafiqueria as grf
import matematiqueria as mat

#array letras
letras=list(['a','b','c','d','e','f','g','h','i','j','k'])

def obtener_Contenido(lab: tk.Label):
    return list(map (int, lab.cget("text").split()))

class vista:
    seleccion=None  
    movimientos_graficados = []
# Crear una instancia de la ventana
    ventana = tk.Tk()
# Configurar el título de la ventana
    ventana.title("Mi Ventana")
# Configurar las dimensiones de la ventana
    ventana.geometry("800x600")
# Configurar el tamaño mínimo y máximo de la ventana para evitar deformación
    ventana.minsize(800, 600)
    ventana.maxsize(1200, 900) 
    ventana.resizable(True, True)
    ventana.config(bg="beige")
    pantalla=tk.Frame()

    def __init__(self, jue:juego, turn=1):
        self.j=jue
        self.turno=turn
        self.Inicio()
        self.llenar()
        
    def Inicio(self, event=None):
        self.labels=grf.etiquetados(self.ventana, self.Seleccionar, self.j.dim)
        grf.graficar(self.j, self.labels)
        
    def llenar(self):
        self.nuncio=tk.Label(self.ventana, width=8, height=2, borderwidth=1, relief="solid")
        re = tk.Label(self.ventana, text=" RETVRN ", borderwidth=1, relief="solid")
        re.place(x=432, y=150)
        re.bind("<Button-1>", self.Inicio )
        self.nuncio.place(x=self.j.dim*37.5, y=6)
    
    def validar(self, dup):
        d=self.j.dim
        return dup[0]>=0 and dup[0]<d and dup[1]>=0 and dup[1]<d    
    
    def obtenerContNum(self, dup:tuple):
        if(self.validar(dup)):
            return obtener_Contenido(mat.ubicar(self.labels, dup))
        return [None]
        
    #Devuelve verdadero si y solo si las dos duplas son coordenadas de casillas con fichas de distinto color o si hay una ficha y una direccion invalida
    def Discriminante(self, dup1, dup2):
        a=self.obtenerContNum(dup1)
        b=self.obtenerContNum(dup2)
        if(not self.validar(dup2)):
            return True
        if b and a:
                return not a[0]==b[0]
        else: return False
    
    def Prueba(self,pos, eje, p=False, n=False):
        if mat.Comprobar(pos, eje, self.Discriminante, p, n):
            l=self.obtenerContNum(pos)
            if l==[1, 0]:
                self.j.Terminar(self.labels, 'NEGRAS')
            self.labels[pos[0]][pos[1]]=grf.etiquetado(pos[0], pos[1], self.ventana, self.Seleccionar)
            return True
            
    def Pruebas(self, pos):
        if self.Prueba(pos, 0) or self.Prueba(pos, 1):
            return
        l=mat.direccionales
        for i in l: 
            for j in i:
                c=mat.SumaDupla(j, pos)
                if(self.validar(c)):
                    self.Prueba(c, abs(j[1]))

#Esta funcion devuelve la tupla con las 2 coordenadas de la casilla seleccionada
    def ObtenerUbicación(self, label:tk.Label):
    # Get the grid info of the widget
        grid_info = label.grid_info()
    # Extract the row and column from the grid info
        row = grid_info.get('row', None)  # Default to None if not found
        column = grid_info.get('column', None)  # Default to None if not found
    # Return the position as a tuple
        return (row, column)

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
                self.movimientos_graficados = mat.MovimientosPosibles(self.seleccion, self.obtenerContNum)
                movimientos = self.movimientos_graficados
                grf.graficarMovimientosPosibles(self.labels, movimientos)

        if(not boola and boolb):
        #inicio y destino guardados en variables
            self.seleccion=None
            l=self.obtenerContNum(sel)
            destino=event.widget
            ub=self.ObtenerUbicación(destino)
            print("Ubicacion: ", end=" ")
            print(ub)
            grf.restaurarMovimientos(self.labels, self.movimientos_graficados)
        #comprobar si el movimiento es posible
            if(ub in self.movimientos_graficados):                 
            #Parte Mejorable//Vaciar label
                self.turno+=1
                self.turno%=2
                self.labels[sel[0]][sel[1]]=grf.etiquetado(sel[0], sel[1], self.ventana, self.Seleccionar)
                grf.asignarImagen(self.j, ub, self.labels, *l )
                self.Pruebas(ub)
                self.j.blanquear(l, ub, self.labels)
                print("----------------------------------------------------------------")

# Ejecutar el bucle principal de la aplicación
jue=juego(11, None)
v=vista(jue)
v.ventana.mainloop()
