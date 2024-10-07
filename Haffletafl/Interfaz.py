import tkinter as tk
from Juego import juego
from PIL import Image, ImageTk 
from Bando import bando
from matematiqueria import SumaDupla, MultDupla, Comprobar, direccionales

#array letras
letras=list(['a','b','c','d','e','f','g','h','i','j','k'])
def etiquetado(i:int, j:int, root, func):
    label = tk.Label(root, width=4, height=2, relief="solid", borderwidth=3)
    label.grid(row=i, column=j)
    label.bind("<Button-1>", func)
    return label

def obtener_Contenido(lab: tk.Label):
    return list(map (int, lab.cget("text").split()))

class vista:
    seleccion=None  
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
        
    def llenar(self):
        dim=self.j.dim
        self.labels=[[etiquetado(i,j,self.ventana, self.Seleccionar) for j in range(dim)] for i in range(dim)]
        self.nuncio=tk.Label()
    
    def validar(self, dup):
        d=self.j.dim
        return not (dup[0]<0 or dup[0]>=d or dup[1]<0 or dup[1]>=d)
    
    def ubicar(self, dup:tuple):
        return self.labels[dup[0]][dup[1]]
    def obtenerContNum(self, dup:tuple):
        if(not self.validar(dup)):
            return [None]
        casSel=self.ubicar(dup)
        return obtener_Contenido(casSel)
    
    #Devuelve verdadero si y solo si las dos duplas son coordenadas de casillas con fichas de distinto color o si hay una ficha y una direccion invalida
    def Discriminante(self, dup1, dup2):
        a=self.obtenerContNum(dup1)
        b=self.obtenerContNum(dup2)
        if(not self.validar(dup2)):
            if b and a:
                if a[0] == None and b[0] == None:
                    return False
            return True
        if b:
            if a:
                if a[0] == None and b[0] == None:
                    return False
                else: 
                    return not a[0]==b[0]
        else: return False
    
    def Prueba(self,pos, eje, p=False, n=False):
        if Comprobar(pos, eje, self.Discriminante, p, n):
            l=self.obtenerContNum(pos)
            if l==[1, 0]:
                self.j.Terminar(self.labels, 'NEGRAS')
            self.j.captura(l)
            self.labels[pos[0]][pos[1]]=etiquetado(pos[0], pos[1], self.ventana, self.Seleccionar)
            return True
            
    def Pruebas(self, pos):
        if self.Prueba(pos, 0) or self.Prueba(pos, 1):
            return
        l=direccionales
        for i in l: 
            for j in i:
                c=SumaDupla(j, pos)
                if(self.validar(j)):
                    #print(j)
                    self.Prueba(c, abs(j[1]))

        

#Las siguientes 3 funciones llenan las casillas con los iconos de la ficha, a nivel individual, de bando y de tablero respectivamente
    def asignarImagen(self, dup, num1:int, num2:int):
        imago=None
        if(num1==0):
            imago=self.j.bandos[0].logo
        elif(num2==0):
            imago=self.j.bandos[1].imagen_real
        else:
            imago=self.j.bandos[1].logo
    #Tomar el valor de la casilla
        casilla=self.ubicar(dup)
    #Ajustar tamaño de la imagen y su formato
        #imago=imago.resize((casilla.winfo_width(),casilla.winfo_height()), Image.LANCZOS )
        imago=imago.resize((30,30), Image.LANCZOS )
        tkimago=ImageTk.PhotoImage(image=imago)
    #Crear Texto identificador
        t=str(num1)+" "+str(num2)
    #Asignar Imagen y Texto
        casilla.config(image=tkimago, text=t, width=30, height=32)
        casilla.image=tkimago 
        #casilla.grid(row=dup[0],column=dup[1])
    #Reemplazar vieja casilla por la nueva
        self.labels[dup[0]][dup[1]]=casilla
        
    def graficarBando(self, b:bando, num1:int):
        l=b.miembros
        for i in range(len(l)):
            self.asignarImagen(l[i],num1, i)
    
    def graficar(self):
        band=self.j.bandos
        for i in range(len(band)):
            self.graficarBando(band[i], i)

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

        if(not boola and boolb):
        #inicio y destino guardados en variables
            t=self.seleccion
            self.seleccion=None
            l=self.obtenerContNum(t)
            destino=event.widget
            ub=self.ObtenerUbicación(destino)
            print("Ubicacion: ", end=" ")
            print(ub)
        #comprobar si el movimiento es posible
            if(self.j.mover(l, self.ObtenerUbicación(destino), self.labels)):                 
            #Parte Mejorable//Vaciar lab
                self.turno+=1
                self.turno%=2
                self.labels[t[0]][t[1]]=etiquetado(t[0], t[1], self.ventana, self.Seleccionar)
                self.asignarImagen(ub, l[0], l[1] )
                self.Pruebas(ub)
                print("----------------------------------------------------------------")
                

# Ejecutar el bucle principal de la aplicación
jue=juego(15, None)
v=vista(jue)
v.llenar()
v.graficar()
v.ventana.mainloop()