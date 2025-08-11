#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo de uso del Bot modificado para trabajar con la clase juego
"""

from Juego import juego
from Bot import Bot
import matematiqueria as mat

def main():
    print("=== Ejemplo de uso del Bot con clase juego ===\n")
    
    # Crear un juego de 9x9
    dimension = 9
    juego_actual = juego(dimension, None)
    
    print(f"Juego creado con dimensión {dimension}x{dimension}")
    print("Posiciones iniciales:")
    for i in range(dimension):
        for j in range(dimension):
            if juego_actual.posiciones[i][j] is not None:
                pieza = juego_actual.posiciones[i][j]
                if pieza == (1, 1):
                    print(f"  Rey blanco en ({i}, {j})")
                elif pieza == (1, 0):
                    print(f"  Peón blanco en ({i}, {j})")
                else:
                    print(f"  Peón negro en ({i}, {j})")
    
    # Crear bot para las blancas
    bot_blancas = Bot(juego_actual, turno=1, max_depth=3)
    
    print(f"\nBot creado para las blancas con profundidad {bot_blancas.max_depth}")
    
    # Mostrar evaluación inicial
    evaluacion_inicial = bot_blancas.cuantificar(juego_actual.posiciones)
    print(f"Evaluación inicial: {evaluacion_inicial}")
    
    # Mostrar tablero inicial
    print("\nTablero inicial:")
    bot_blancas.mostrar_tablero()
    
    # Obtener mejor jugada para las blancas
    print("\nCalculando mejor jugada para las blancas...")
    mejor_movimiento = bot_blancas.obtener_mejor_jugada()
    
    if mejor_movimiento:
        inicio, destino = mejor_movimiento
        print(f"Mejor movimiento: desde {inicio} hacia {destino}")
        
        # Aplicar el movimiento
        print("\nAplicando movimiento...")
        juego_actual.mover(inicio, destino)
        
        # Mostrar tablero después del movimiento
        print("\nTablero después del movimiento:")
        bot_blancas.mostrar_tablero()
        
        # Mostrar evaluación después del movimiento
        evaluacion_final = bot_blancas.cuantificar(juego_actual.posiciones)
        print(f"Evaluación después del movimiento: {evaluacion_final}")
        
    else:
        print("No se encontraron movimientos válidos")
    
    print("\n=== Fin del ejemplo ===")

if __name__ == "__main__":
    main()
