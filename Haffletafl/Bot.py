

class bot:
    def __init__(self, dimension, bandos, turno):
        self.dimension = dimension
        self.bandos = bandos
        self.turno = turno

    def buscarDupla(self, duplas, dupla):
        for dup in duplas:
            if dupla == dup:
                return True
        
        return False
    
    def mejoresMovimientos(self, ficha, bandos, turno, movimientosPosibles):
        # Lógica para buscar los mejores 4 movimientos
        
        pass

    def jugarBot(self, bandos, turno, profundidad=1):
        # Busar la siguiente mejor jugada y retornarla. Pendiente
        ficha = bandos[turno].miembros.pop[0]
        movimientosPosibles = [] #calcular para una ficha
        mejorJuego = movimientosPosibles[0]
        if profundidad == 0:
            return 0
        else:
            for fichaMiembro in bandos[turno].miembros:
                movimientosPosibles = []
                bandosLista = self.mejoresMovimientos(fichaMiembro, bandos, turno, movimientosPosibles)
                for bandosMovimiento in bandosLista:
                    self.jugarBot(bandosMovimiento, (turno + 1)%2, profundidad - 1)

    def obtenerMiBando(self, bandos):
        tablero = []

        for i in range(self.dimension):
            fila = []
            for j in range(self.dimension):
                if self.buscarDupla(bandos[self.turno].miembros, (i, j)):
                    fila.append(str((i, j)))
                    continue
                fila.append('(_)')
            tablero.append(" | ".join(fila))

        for fila in tablero:
            print(fila)
            print('-' * len(fila))

