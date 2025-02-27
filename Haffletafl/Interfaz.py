import tkinter as tk
from Juego import juego
import grafiqueria as grf
import matematiqueria as mat
from agent import Agent
from piece import Piece
#array letras
letras=list(['a','b','c','d','e','f','g','h','i','j','k'])

def obtener_Contenido(lab: tk.Label):
    return list(map (int, lab.cget("text").split()))

def ventor(v):
 # Configurar el título de la ventana
    v.title("Mi Ventana")
# Configurar las dimensiones de la ventana
    v.geometry("800x600")
# Configurar el tamaño mínimo y máximo de la ventana para evitar deformación
    v.minsize(800, 600)
    v.maxsize(1200, 900) 
    v.resizable(True, True)
    v.config(bg="beige")

class vista:
    seleccion=None  
    movimientos_graficados = []    
    #pantalla=tk.Frame()

    def __init__(self, jue:juego):
        self.ventana = tk.Toplevel()
        ventor(self.ventana)
        self.j=jue
        self.agent = Agent()
        newBoard, whites, blacks = self.builBoardMatrix()
        self.agent.setBoard(newBoard, whites, blacks)
        self.Inicio()
        self.llenar()

    def builBoardMatrix(self):
        matrix = []
        for i in range(11):
            matrix.append([0 for j in range(11)])
        for black in self.j.bandos[0].miembros:
            matrix[black[0]][black[1]] =(Piece(black[0], black[1], 'black'))

        for white in self.j.bandos[1].miembros:
            matrix[white[0]][white[1]] =(Piece(white[0], white[1], 'white'))
        
        return matrix, len(self.j.bandos[0].miembros), len(self.j.bandos[1].miembros)


    def Inicio(self, event=None, t=1):
        self.turno=t
        self.labels=grf.etiquetados(self.ventana, self.Seleccionar, self.j.dim)
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
    
    def obtenerContNum(self, dup:tuple):
        if(self.validar(dup)):
            return obtener_Contenido(mat.ubicar(self.labels, dup))
        return [None]
        
    #Devuelve verdadero si y solo si las dos duplas son coordenadas de casillas con fichas de distinto color o si hay una ficha y una direccion invalida
    def Discriminante(self, dup1, dup2):
        a=self.obtenerContNum(dup1)
        if(not self.validar(dup2)):
            return True
        b=obtener_Contenido(mat.ubicar(self.labels, dup2))
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
    
    def Terminar(self, st):
        for i in self.labels:
            for j in i:
                j.unbind("<Button-1>")
        grf.fin(st)

    def blanquear(self, lis, destino):
        #Codigo por si gana el blanco
        comp=[self.j.dim-1, 0]
        if(lis==[1, 0] and destino[0] in comp and destino[1] in comp):
            self.Terminar('BLANCAS')

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
                dicresult = self.agent.select(self.seleccion[0], self.seleccion[1])
                print(f"{dicresult}")

        if(not boola and boolb):
        #inicio y destino guardados en variables
            self.seleccion=None
            l=self.obtenerContNum(sel)
            destino=event.widget
            ub=self.ObtenerUbicación(destino)
            self.agent.select(ub[0], ub[1])
            print("Destino: ", end=" ")
            print(ub)
            grf.restaurarMovimientos(self.labels, self.movimientos_graficados)
        #comprobar si el movimiento es posible
            if(ub in self.movimientos_graficados):                 
            #Parte Mejorable//Vaciar label
                iaOn = True
                if iaOn: 
                    # Turn White
                    self.labels[sel[0]][sel[1]]=grf.etiquetado(sel[0], sel[1], self.ventana, self.Seleccionar)
                    grf.asignarImagen(self.j, ub, self.labels, *l )
                    self.Pruebas(ub)
                    self.blanquear(l, ub)
                    print("----------------------------------------------------------------")
                    # White movimiento exitoso.

                    move, piece, final_position = self.agent.algo(self.agent.board) 
                    print(f"Black IA Move DeepCopy: {(move, (piece.row, piece.col), final_position)}")

                    # Turn Black. IA moves
                    best_piece_move = self.agent.ia_move('black') #(('black', (1, 5)), ((1, 9), 2))
                    print(f"Black IA Move: {best_piece_move}")
                    sel = best_piece_move[0][1] # inicio
                    ub  = best_piece_move[1][0] # fin
                    l   = [0]                   # team
                    self.agent.select(sel[0], sel[1])
                    self.agent.select(ub[0], ub[1])

                    self.labels[sel[0]][sel[1]]=grf.etiquetado(sel[0], sel[1], self.ventana, self.Seleccionar)
                    grf.asignarImagen(self.j, ub, self.labels, *l )
                    self.Pruebas(ub)
                    self.blanquear(l, ub)
                    print("----------------------------------------------------------------")
                    # Turn White. Choose Piece
                
                else:
                    self.turno+=1
                    self.turno%=2
                    self.labels[sel[0]][sel[1]]=grf.etiquetado(sel[0], sel[1], self.ventana, self.Seleccionar)
                    grf.asignarImagen(self.j, ub, self.labels, *l )
                    self.Pruebas(ub)
                    self.blanquear(l, ub)
                    print("----------------------------------------------------------------")

# Ejecutar el bucle principal de la aplicación
jue=juego(11, None)
jue.dibujar()
v=vista(jue)
v.ventana.mainloop()