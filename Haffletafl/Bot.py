import matematiqueria as mat
import copy
from typing import List, Tuple, Optional
from Juego import juego

class Bot:
    def __init__(self, juego_actual: juego, turno: int, max_depth: int = 4, registro:bool=False, ruta_registro="registro_bot.txt"):
        self.juego = juego_actual
        self.dimension = juego_actual.dim
        self.turno = turno
        self.max_depth = max_depth
        self.registro = registro
        self.ruta_registro = ruta_registro
        if self.registro:
            with open(self.ruta_registro, "w", encoding="utf-8") as f:
                f.write("Registro de movimientos del bot\n")

        
        # Constantes para evaluación
        self.PESO_PEON = 10
        self.PESO_REY = 100
        self.PESO_POSICION = 5
        self.PESO_ESCAPE = 20
        
    def cuantificar(self, posiciones: List[List]) -> int:
        """Evalúa la posición actual del tablero basándose en posiciones"""
        if not posiciones:
            return 0
            
        peones_negros = 0
        peones_blancos = 0
        rey_blanco = 0
        pos_rey = None
        
        # Contar piezas y encontrar el rey
        for i in range(self.dimension):
            for j in range(self.dimension):
                if posiciones[i][j] is not None:
                    if posiciones[i][j] == (0, 0):  # Peón negro
                        peones_negros += 1
                    elif posiciones[i][j] == (1, 0):  # Peón blanco
                        peones_blancos += 1
                    elif posiciones[i][j] == (1, 1):  # Rey blanco
                        rey_blanco = 1
                        pos_rey = (i, j)
        
        # Evaluación base: peones blancos valen más (2x) y el rey vale mucho más
        evaluacion = ( peones_blancos - peones_negros) * self.PESO_PEON
        evaluacion += rey_blanco * self.PESO_REY
        
        # Evaluación de posición del rey (más cerca del centro = mejor)
        if rey_blanco and pos_rey:
            centro = self.dimension // 2
            distancia_centro = abs(pos_rey[0] - centro) + abs(pos_rey[1] - centro)
            evaluacion += (centro - distancia_centro) * self.PESO_POSICION
            
            # Bonus por estar cerca de una esquina (objetivo del rey)
            esquinas = [(0, 0), (0, self.dimension-1), (self.dimension-1, 0), (self.dimension-1, self.dimension-1)]
            for esquina in esquinas:
                dist_esquina = abs(pos_rey[0] - esquina[0]) + abs(pos_rey[1] - esquina[1])
                if dist_esquina <= 2:
                    evaluacion += (3 - dist_esquina) * self.PESO_ESCAPE
        
        return evaluacion
    
    def _registrar_movimiento(self, movimiento, valor, profundidad):
        if not self.registro:
            return
        inicio, destino = movimiento
        sangria = "\t" * (self.max_depth - profundidad)
        linea = f"{sangria}{inicio}->{destino} {valor}\n"
        with open(self.ruta_registro, "a", encoding="utf-8") as f:
            f.write(linea)

    def generar_movimientos_validos(self, posiciones: List[List], turno_actual: int) -> List[Tuple]:
        """Genera todos los movimientos válidos para el turno actual"""
        movimientos = []
        
        # Buscar todas las piezas del bando actual
        for i in range(self.dimension):
            for j in range(self.dimension):
                if posiciones[i][j] is not None:
                    # turno_actual = 0 para negras, 1 para blancas
                    if (turno_actual == 0 and posiciones[i][j][0] == 0) or \
                       (turno_actual == 1 and posiciones[i][j][0] == 1):
                        # Generar movimientos posibles para esta ficha
                        movimientos_ficha = mat.Movs.MovimientosPosibles((i, j), lambda pos: self._es_celda_ocupada(pos, posiciones))
                        
                        for destino in movimientos_ficha:
                            # Verificar que el movimiento sea válido según las reglas del Hnefatafl
                            if self._es_movimiento_valido((i, j), destino, posiciones, turno_actual):
                                movimientos.append(((i, j), destino))
        
        return movimientos
    
    def _es_celda_ocupada(self, pos: Tuple[int, int], posiciones: List[List]) -> bool:
        """Verifica si una celda está ocupada"""
        if mat.Coords.validar(pos, self.dimension):
            return posiciones[pos[0]][pos[1]] is not None
        return True
        
    
    def _es_movimiento_valido(self, inicio: Tuple[int, int], destino: Tuple[int, int], 
                             posiciones: List[List], turno_actual: int) -> bool:
        """Verifica si un movimiento es válido según las reglas del Hnefatafl"""
        # Verificar que el destino esté dentro del tablero
        if not mat.Coords.validar(destino, self.dimension):
            return False
            
        # Verificar que el destino esté vacío
        if self._es_celda_ocupada(destino, posiciones):
            return False
            
        # Verificar que el movimiento sea en línea recta (horizontal o vertical)
        if inicio[0] != destino[0] and inicio[1] != destino[1]:
            return False
            
        # Verificar que no haya piezas en el camino
        paso = mat.DupOps.getPaso(inicio, destino)
        if paso is None:
            return False
            
        pos_actual = mat.DupOps.SumaDupla(inicio, paso)
        while pos_actual != destino:
            if self._es_celda_ocupada(pos_actual, posiciones):
                return False
            pos_actual = mat.DupOps.SumaDupla(pos_actual, paso)
            
        return True
    
    def aplicar_movimiento(self, posiciones: List[List], turno_actual: int, 
                          movimiento: Tuple[Tuple[int, int], Tuple[int, int]]) -> List[List]:
        """Aplica un movimiento y retorna el nuevo estado de las posiciones"""
        inicio, destino = movimiento
        
        # Crear una copia profunda de las posiciones
        nuevas_posiciones = copy.deepcopy(posiciones)
        
        # Mover la ficha
        valor_ficha = nuevas_posiciones[inicio[0]][inicio[1]]
        nuevas_posiciones[destino[0]][destino[1]] = valor_ficha
        nuevas_posiciones[inicio[0]][inicio[1]] = None
        
        # Verificar capturas
        self._verificar_capturas(nuevas_posiciones, destino, turno_actual)
        
        return nuevas_posiciones
    
    def _verificar_capturas(self, posiciones: List[List], posicion: Tuple[int, int], turno_actual: int):
        """Verifica y aplica capturas después de un movimiento"""
        # Por ahora, una implementación básica
        mat.Caps.capturaEuro(
        posiciones,
        posicion,
        lambda p: posiciones[p[0]].__setitem__(p[1], None)
        )
    
    def minimax(self, posiciones: List[List], turno_actual: int, profundidad: int, 
                alfa: float = float('-inf'), beta: float = float('inf'), 
                es_maximizando: bool = True) -> Tuple[float, Optional[Tuple]]:
        """
        Algoritmo minimax con poda alfa-beta
        Retorna: (valor_evaluacion, mejor_movimiento)
        """
        # Condición de parada
        if profundidad == 0 or self._es_estado_final(posiciones):
            return self.cuantificar(posiciones), None
        
        movimientos = self.generar_movimientos_validos(posiciones, turno_actual)
        
        if not movimientos:
            return self.cuantificar(posiciones), None
        
        mejor_movimiento = None
        
        if es_maximizando:
            valor_max = float('-inf')
            for movimiento in movimientos:
                # Aplicar movimiento
                nuevas_posiciones = self.aplicar_movimiento(posiciones, turno_actual, movimiento)
                nuevo_turno = (turno_actual + 1) % 2
                
                # Llamada recursiva
                valor, _ = self.minimax(nuevas_posiciones, nuevo_turno, profundidad - 1, 
                                       alfa, beta, False)

                # Registrar cada movimiento y su valoración
                self._registrar_movimiento(movimiento, valor, profundidad)
                
                # Actualizar mejor valor
                if valor > valor_max:
                    valor_max = valor
                    mejor_movimiento = movimiento
                
                # Poda alfa-beta
                alfa = max(alfa, valor_max)
                if beta <= alfa:
                    break
                    
            return valor_max, mejor_movimiento
        else:
            valor_min = float('inf')
            for movimiento in movimientos:
                # Aplicar movimiento
                nuevas_posiciones = self.aplicar_movimiento(posiciones, turno_actual, movimiento)
                nuevo_turno = (turno_actual + 1) % 2
                
                # Llamada recursiva
                valor, _ = self.minimax(nuevas_posiciones, nuevo_turno, profundidad - 1, 
                                       alfa, beta, True)
                # Registrar cada movimiento y su valoración
                self._registrar_movimiento(movimiento, valor, profundidad)
                # Actualizar mejor valor
                if valor < valor_min:
                    valor_min = valor
                    mejor_movimiento = movimiento
                
                # Poda alfa-beta
                beta = min(beta, valor_min)
                if beta <= alfa:
                    break
                    
            return valor_min, mejor_movimiento
    
    def _es_estado_final(self, posiciones: List[List]) -> bool:
        """Verifica si el juego ha terminado"""
        if not posiciones:
            return True
            
        # Verificar si el rey blanco ha sido capturado
        rey_encontrado = False
        pos_rey = None
        
        for i in range(self.dimension):
            for j in range(self.dimension):
                if posiciones[i][j] == (1, 1):  # Rey blanco
                    rey_encontrado = True
                    pos_rey = (i, j)
                    break
            if rey_encontrado:
                break
        
        if not rey_encontrado:
            return True
            
        # Verificar si el rey blanco ha llegado a una esquina
        if pos_rey:
            esquinas = [(0, 0), (0, self.dimension-1), (self.dimension-1, 0), (self.dimension-1, self.dimension-1)]
            if pos_rey in esquinas:
                return True
            
        # Verificar si no hay movimientos posibles
        movimientos_blancos = self.generar_movimientos_validos(posiciones, 1)
        movimientos_negros = self.generar_movimientos_validos(posiciones, 0)
        
        return len(movimientos_blancos) == 0 and len(movimientos_negros) == 0
    
    def obtener_mejor_jugada(self) -> Optional[Tuple]:
        """Obtiene la mejor jugada usando minimax con poda alfa-beta"""
        valor, mejor_movimiento = self.minimax(
            self.juego.posiciones, 
            self.turno, 
            self.max_depth, 
            float('-inf'), 
            float('inf'), 
            True
        )
        
        return mejor_movimiento
    
    def jugar_turno(self) -> Optional[Tuple]:
        """Juega el turno del bot y retorna el movimiento realizado"""
        mejor_movimiento = self.obtener_mejor_jugada()
        
        if mejor_movimiento:
            # Aplicar el movimiento al juego
            self.juego.mover(mejor_movimiento[0], mejor_movimiento[1])
            # Cambiar turno
            self.turno = (self.turno + 1) % 2
            
        return mejor_movimiento
    
    def mostrar_tablero(self):
        """Muestra el estado actual del tablero"""
        tablero = []
        
        for i in range(self.dimension):
            fila = []
            for j in range(self.dimension):
                if self.juego.posiciones[i][j] is not None:
                    if self.juego.posiciones[i][j] == (1, 1):  # Rey blanco
                        fila.append('R ')
                    elif self.juego.posiciones[i][j] == (1, 0):  # Peón blanco
                        fila.append('B ')
                    else:  # Peón negro
                        fila.append('N ')
                else:
                    fila.append('_ ')
            tablero.append("|".join(fila))
        
        print(f"\nTablero ({self.dimension}x{self.dimension}):")
        print("=" * (self.dimension * 3 - 1))
        for fila in tablero:
            print(fila)
        print("=" * (self.dimension * 3 - 1))
        print("R: Rey blanco, B: Peón blanco, N: Peón negro, _: Vacío")
        print(f"Turno: {'Blancas' if self.turno == 1 else 'Negras'}")
        print(f"Evaluación: {self.cuantificar(self.juego.posiciones)}")
        
        # Mostrar información adicional de debug
        print(f"Fichas negras: {sum(1 for i in range(self.dimension) for j in range(self.dimension) if self.juego.posiciones[i][j] is not None and self.juego.posiciones[i][j][0] == 0)}")
        print(f"Fichas blancas: {sum(1 for i in range(self.dimension) for j in range(self.dimension) if self.juego.posiciones[i][j] is not None and self.juego.posiciones[i][j][0] == 1)}")

