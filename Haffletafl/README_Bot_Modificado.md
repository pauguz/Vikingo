# Bot Modificado para Hnefatafl

## Cambios Realizados

### 1. Modificación del Bot (`Bot.py`)

El bot ha sido modificado para trabajar directamente con la clase `juego` en lugar de manejar los bandos por separado.

#### Cambios principales:

- **Constructor modificado**: Ahora recibe una instancia de `juego` en lugar de dimension y bandos
- **Uso de `posiciones`**: El bot ahora utiliza `juego.posiciones` para entender el estado del tablero
- **Sincronización automática**: El bot se mantiene sincronizado con el estado del juego automáticamente

#### Nuevo constructor:
```python
def __init__(self, juego_actual: juego, turno: int, max_depth: int = 4):
    self.juego = juego_actual
    self.dimension = juego_actual.dim
    self.turno = turno
    self.max_depth = max_depth
```

### 2. Modificación de la Interfaz (`Interfaz.py`)

La interfaz ha sido adaptada para usar el nuevo bot:

- **Inicialización del bot**: Ahora se crea con la instancia del juego
- **Sincronización simplificada**: Ya no es necesario sincronizar manualmente los bandos
- **Uso del método `mover`**: El bot utiliza `juego.mover()` para aplicar movimientos

### 3. Funcionalidades Mantenidas

- ✅ Algoritmo minimax con poda alfa-beta
- ✅ Evaluación de posiciones
- ✅ Generación de movimientos válidos
- ✅ Verificación de estados finales
- ✅ Interfaz gráfica completa

## Cómo Usar el Bot Modificado

### 1. Crear un juego
```python
from Juego import juego
from Bot import Bot

# Crear juego
juego_actual = juego(9, None)  # Tablero 9x9
```

### 2. Crear el bot
```python
# Bot para las blancas
bot_blancas = Bot(juego_actual, turno=1, max_depth=4)

# Bot para las negras
bot_negras = Bot(juego_actual, turno=0, max_depth=4)
```

### 3. Obtener mejor jugada
```python
mejor_movimiento = bot_blancas.obtener_mejor_jugada()
if mejor_movimiento:
    inicio, destino = mejor_movimiento
    juego_actual.mover(inicio, destino)
```

### 4. Usar con la interfaz
```python
from Interfaz import vista

# Crear vista con bot
v = vista(juego_actual, turno=1, modo="bot_blancas")
v.ventana.mainloop()
```

## Ventajas de la Modificación

1. **Sincronización automática**: El bot siempre está sincronizado con el estado del juego
2. **Menos código de mantenimiento**: No es necesario sincronizar manualmente los bandos
3. **Consistencia**: El bot usa la misma representación del tablero que el resto del juego
4. **Facilidad de uso**: Más simple de integrar con el sistema existente

## Ejemplo de Uso

Ver el archivo `ejemplo_bot.py` para un ejemplo completo de cómo usar el bot modificado.

## Compatibilidad

El bot modificado es completamente compatible con:
- La clase `juego` existente
- La interfaz gráfica
- El sistema de menús
- Todas las funcionalidades del juego original

## Notas Técnicas

- El bot sigue usando el algoritmo minimax con poda alfa-beta
- La evaluación de posiciones se basa en el atributo `posiciones` del juego
- Los movimientos se aplican usando el método `mover()` del juego
- La profundidad de búsqueda se puede ajustar en el constructor 