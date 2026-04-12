class Nodo:
    def __init__(self, fila, columna, valor):
        # Identificadores de posición
        self.fila = fila
        self.columna = columna

        # Dato guardado en la matriz
        self.valor = valor

        # Enlaces horizontales y verticales
        self.arriba = None
        self.abajo = None
        self.izquierda = None
        self.derecha = None

    def mostrar_dato(self):
        return f"Nodo(fila={self.fila}, columna={self.columna}, valor={self.valor})"