import tkinter as tk
from matematiqueria import Coords
from Juego import juego
from Interfaz import vista

class menu:
    v=tk.Tk()
    v.title("Menu")
    v.geometry("400x400")

    
    def __init__(s):
        #Input Espacio
        txt=tk.Label(s.v, text='Ingrese la dimension del Tablero (Numero impar mayor que 9)')
        txt.place(x=60, y=40)

        s.dim=tk.Entry(s.v)
        s.dim.place(x=150, y=60)

        #Input Tiempo
        txt=tk.Label(s.v, text='Ingrese el tiempo')
        txt.place(x=60, y=80)

        s.tem=tk.Entry(s.v)
        s.tem.place(x=150, y=100)
        
        # Botón para jugar contra otro humano
        s.bot_humano=tk.Label(s.v, text='Jugar vs Humano', relief='solid', bg='lightblue')
        s.bot_humano.bind("<Button-1>", lambda e: s.dimendir(e, modo="humano"))
        s.bot_humano.place(x=155, y=120)
        
        # Botón para jugar como blancas contra bot
        s.bot_blancas=tk.Label(s.v, text='Jugar Blancas vs Bot', relief='solid', bg='white')
        s.bot_blancas.bind("<Button-1>", lambda e: s.dimendir(e, modo="bot_blancas"))
        s.bot_blancas.place(x=155, y=160)
        
        # Botón para jugar como negras contra bot
        s.bot_negras=tk.Label(s.v, text='Jugar Negras vs Bot', relief='solid', bg='gray')
        s.bot_negras.bind("<Button-1>", lambda e: s.dimendir(e, modo="bot_negras"))
        s.bot_negras.place(x=155, y=200)
        
        # Información sobre el bot
        info_bot = tk.Label(s.v, text='Bot con IA Minimax + Poda Alfa-Beta', fg='blue')
        info_bot.place(x=60, y=240)
        
        info_dificultad = tk.Label(s.v, text='Dificultad: Media (Profundidad 4)', fg='green')
        info_dificultad.place(x=60, y=260)

    
    def dimendir(s, event=None, modo="humano"):
        d=s.dim.get()
        t=s.tem.get()
        print(Coords.Dimendor(d))
        if (Coords.Dimendor(d)):
            s.dim.delete(0, tk.END)  
            j=juego(int(d), None)
            j.dibujar()
            
            # Determinar el turno inicial según el modo
            turno_inicial = 1  # Por defecto blancas empiezan
            if modo == "bot_blancas":
                turno_inicial = 1  # Jugador como blancas
            elif modo == "bot_negras":
                turno_inicial = 0  # Jugador como negras
            
            vent=vista(j, turno_inicial, modo, seg=int(t))
            vent.llenar()
            #vent.Inicio()
            vent.ventana.mainloop()

m=menu()
m.v.mainloop()