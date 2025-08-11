import tkinter as tk
import grafiqueria as grf
import matematiqueria as mat
from Juego import juego
from PIL import Image, ImageTk 
from Bando import bando
from Bot import Bot

def etiquetado(i:int, j:int, root, func):
    label = tk.Label(root, width=4, height=2, relief="solid", borderwidth=3)
    label.grid(row=i, column=j)
    label.bind("<Button-1>", func)
    return label

def obtener_Contenido(lab: tk.Label):
    return list(map (int, lab.cget("text").split()))


class vista:

    def __init__(s, jue:juego, turn=1, modo="humano"):
        s.seleccion=None  
        # Crear una instancia de la ventana
        s.ventana = tk.Toplevel()
        grf.ventor(s.ventana, "Hnefatafl")
        s.j=jue
        s.turno=turn
        s.movspos=[]
        s.modo=modo  # "humano", "bot_blancas", "bot_negras"
        
        # Inicializar bot si es necesario
        s.bot = None
        if modo != "humano":
            # Crear bot con la instancia del juego
            bot_turno = 1 if modo == "bot_blancas" else 0
            s.bot = Bot(jue, bot_turno, max_depth=3)
        
        s.llenar()
        s.Inicio()

    
    def Inicio(s, event=None):
        s.labels=grf.etiquetados(s.ventana, s.Seleccionar, s.j.dim )
        grf.graficar(s.j, s.labels)
        
        # Si es turno del bot, hacer su jugada
        if s.modo != "humano" and s.turno != (1 if s.modo == "bot_blancas" else 0):
            s.ventana.after(500, s.turno_bot)  # Delay de 500ms para que se vea el tablero
        
    def llenar(s):
        s.nuncio=tk.Label(s.ventana, width=8, height=2, borderwidth=1, relief="solid")
        re = tk.Label(s.ventana, text=" RETVRN ", borderwidth=1, relief="solid")
        re.place(x=s.j.dim*37.5, y=60)
        re.bind("<Button-1>", s.Inicio )
        s.nuncio.place(x=s.j.dim*37.5, y=6)
        
        # Mostrar modo de juego
        modo_texto = "vs Humano" if s.modo == "humano" else f"vs Bot ({'Blancas' if s.modo == 'bot_blancas' else 'Negras'})"
        s.modo_label = tk.Label(s.ventana, text=f"Modo: {modo_texto}", fg='blue', font=('Arial', 10, 'bold'))
        s.modo_label.place(x=s.j.dim*37.5, y=100)
        
        # Botón para hacer jugada del bot manualmente
        if s.modo != "humano":
            s.bot_button = tk.Label(s.ventana, text="BOT TURN", relief="solid", bg="orange")
            s.bot_button.bind("<Button-1>", s.turno_bot)
            s.bot_button.place(x=s.j.dim*37.5, y=140)
    
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
        
        # Si es turno del bot, hacer su jugada automáticamente
        #if s.modo != "humano" and s.turno != (1 if s.modo == "bot_blancas" else 0):
        #    s.ventana.after(1000, s.turno_bot)  # Delay de 1 segundo
        
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
    
    def turno_bot(s, event=None):
        """Ejecuta el turno del bot"""
        if s.bot is None:
            return
            
        try:
            # Sincronizar turno del bot con el turno actual
            s.bot.turno = s.turno
            
            # Obtener mejor jugada del bot
            mejor_movimiento = s.bot.obtener_mejor_jugada()
            
            if mejor_movimiento:
                inicio, destino = mejor_movimiento
                print(f"Bot mueve desde {inicio} hacia {destino}")
                
                # Aplicar el movimiento del bot usando el método del juego
                s.j.mover(inicio, destino)

                casSel=mat.ubicar(s.labels, inicio)
                l=obtener_Contenido(casSel)
                
                s.jugada(destino, l, inicio)
                
                print(f"Turno del bot completado. Ahora es turno de: {'Blancas' if s.turno == 1 else 'Negras'}")
            else:
                print("Bot no encontró movimientos válidos")
                
        except Exception as e:
            print(f"Error en turno del bot: {e}")
            import traceback
            traceback.print_exc()
    
        
    #ubicacion de destino, contenido de label, inicio
    def jugada(s, ub, l, t):
            s.tornar()           
            #Parte Mejorable//Vaciar lab
            s.labels[t[0]][t[1]]=etiquetado(t[0], t[1], s.ventana, s.Seleccionar)
            
            grf.asignarImagen(s.j, ub, s.labels, *l)
            s.j.mover( t, ub)
            s.Pruebas(ub)
            s.blanquear(l, ub)
    

    def Seleccionar(s, event:tk.Event):
        # No permitir selección si es turno del bot
        if s.modo != "humano" and s.turno != (1 if s.modo == "bot_blancas" else 0):
            print("Es turno del bot, espera...")
            return
            
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
                #print(s.seleccion)
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
                s.jugada(ub, l, t)
                #for i in self.j.posiciones:
                #    print(i)
                print("----------------------------------------------------------------")
            grf.restaurarMovimientos(s.labels, s.movspos)


#jue=juego(9, None)
#jue.dibujar()
#v=vista(jue)
#v.ventana.mainloop()