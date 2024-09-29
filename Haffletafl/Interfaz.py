import tkinter as tk
from Juego import juego
from PIL import Image, ImageTk 
from Bando import bando
from matematiqueria import SumaDupla
from itertools import chain

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
        #version en varias lineas luego de declarar labels como lista de None's:
        # for i in range(dim):
        #    for j in range(dim):
            # Crear y colocar la etiqueta en la ventana
        #        label = tk.Label(self.ventana, width=4, height=2, relief="solid", borderwidth=1)
        #        label.grid(row=i, column=j)
        #        self.labels[i][j]=label
        self.nuncio=tk.Label()
    
    def ubicar(self, dup:tuple):
        return self.labels[dup[0]][dup[1]]
    
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
        logos=b.logo

        for i in range(len(l)):
            self.asignarImagen(l[i],num1, i)
    
    def graficar(self):
        band=self.j.bandos
        for i in range(len(band)):
            self.graficarBando(band[i], i)

#Esta funcion devuelve la tupla con las 2 coordenadas de la casilla seleccionada
    def ObtenerUbicación(self, label):
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
                self.turno+=1
                self.turno=(self.turno)%2
        if(not boola and boolb):
            t=self.seleccion
            casSel=self.ubicar(t)
            self.seleccion=None
            l=obtener_Contenido(casSel)
            destino=event.widget
            ub=self.ObtenerUbicación(destino)
            print("Ubicacion: ", end=" ")
            print(ub)
        #comprobar si el movimiento es posible
            #print(self.j.mover(l, self.ObtenerUbicación(destino)))
            if(self.j.mover(l, self.ObtenerUbicación(destino))):                 
                #Parte Mejorable//Vaciar lab
                self.labels[t[0]][t[1]]=etiquetado(t[0], t[1], self.ventana, self.Seleccionar)
                self.asignarImagen(ub, l[0], l[1] )
                print("----------------------------------------------------------------")
                print(self.Verificar(ub, l[0]))
    
    def Verificar(self, ub,turno):
        dim=self.j.dim
        enemigos = []
        desplazar = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if abs(i) != abs(j)]
        for d in desplazar:
            enemigo = SumaDupla(ub, d)
            if (enemigo[0] < dim  and enemigo[1] < dim):
                cas=self.ubicar(enemigo) #label
                content = list(map (int, cas.cget("text").split()))
                if content != []:
                    if (content[0] != turno):
                        enemigos.append(enemigo)
                        
                        compañero = SumaDupla(enemigo, d)
                        if (compañero[0] < dim  and compañero[1] < dim):
                            cas=self.ubicar(compañero) #label
                            content = list(map (int, cas.cget("text").split()))
                            if content != []:
                                if (content[0] != turno):
                                    print("Kill,", enemigo)

        return enemigos


# Ejecutar el bucle principal de la aplicación
jue=juego(9, None)
v=vista(jue)
v.llenar()
v.graficar()
#v.labels[7][7].config(image=ImageTk.PhotoImage(image=Image.open("reg.png")) )
v.ventana.mainloop()

