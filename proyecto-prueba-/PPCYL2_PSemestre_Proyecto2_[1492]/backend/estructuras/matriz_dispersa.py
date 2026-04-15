from estructuras.nodo import Nodo


class NodoEncabezado:
    def __init__(self, id_encabezado):
        # Nombre o identificador del encabezado
        self.id = id_encabezado

        # Apunta al siguiente encabezado de la lista
        self.siguiente = None

        # Apunta al primer nodo de esa fila o columna
        self.acceso = None


class ListaEncabezados:
    def __init__(self):
        self.primero = None

    def obtener_encabezado(self, id_encabezado):
        actual = self.primero

        while actual is not None:
            if actual.id == id_encabezado:
                return actual
            actual = actual.siguiente

        return None

    def insertar_encabezado(self, nuevo):
        # Si la lista está vacía
        if self.primero is None:
            self.primero = nuevo
            return

        # Si el nuevo encabezado va al inicio
        if nuevo.id < self.primero.id:
            nuevo.siguiente = self.primero
            self.primero = nuevo
            return

        # Insertar ordenadamente
        actual = self.primero
        while actual.siguiente is not None:
            if nuevo.id < actual.siguiente.id:
                break
            actual = actual.siguiente

        nuevo.siguiente = actual.siguiente
        actual.siguiente = nuevo

    def mostrar_encabezados(self):
        resultado = []
        actual = self.primero

        while actual is not None:
            resultado.append(actual.id)
            actual = actual.siguiente

        return resultado


class MatrizDispersa:
    def __init__(self):
        # Lista de encabezados de filas
        self.filas = ListaEncabezados()

        # Lista de encabezados de columnas
        self.columnas = ListaEncabezados()

    def existe_nodo(self, fila, columna):
        encabezado_fila = self.filas.obtener_encabezado(fila)

        if encabezado_fila is None:
            return None

        actual = encabezado_fila.acceso
        while actual is not None:
            if actual.columna == columna:
                return actual
            actual = actual.derecha

        return None

    def insertar(self, fila, columna, valor):
        # Verificar si ya existe un nodo en esa posición
        existente = self.existe_nodo(fila, columna)
        if existente is not None:
            existente.valor = valor
            return

        nuevo = Nodo(fila, columna, valor)

        # ===== ENCABEZADO DE FILA =====
        encabezado_fila = self.filas.obtener_encabezado(fila)
        if encabezado_fila is None:
            encabezado_fila = NodoEncabezado(fila)
            self.filas.insertar_encabezado(encabezado_fila)

        # ===== ENCABEZADO DE COLUMNA =====
        encabezado_columna = self.columnas.obtener_encabezado(columna)
        if encabezado_columna is None:
            encabezado_columna = NodoEncabezado(columna)
            self.columnas.insertar_encabezado(encabezado_columna)

        # ===== INSERTAR EN LA FILA =====
        if encabezado_fila.acceso is None:
            encabezado_fila.acceso = nuevo
        else:
            if nuevo.columna < encabezado_fila.acceso.columna:
                nuevo.derecha = encabezado_fila.acceso
                encabezado_fila.acceso.izquierda = nuevo
                encabezado_fila.acceso = nuevo
            else:
                actual = encabezado_fila.acceso

                while actual.derecha is not None and actual.derecha.columna < nuevo.columna:
                    actual = actual.derecha

                nuevo.derecha = actual.derecha
                if actual.derecha is not None:
                    actual.derecha.izquierda = nuevo

                nuevo.izquierda = actual
                actual.derecha = nuevo

        # ===== INSERTAR EN LA COLUMNA =====
        if encabezado_columna.acceso is None:
            encabezado_columna.acceso = nuevo
        else:
            if nuevo.fila < encabezado_columna.acceso.fila:
                nuevo.abajo = encabezado_columna.acceso
                encabezado_columna.acceso.arriba = nuevo
                encabezado_columna.acceso = nuevo
            else:
                actual = encabezado_columna.acceso

                while actual.abajo is not None and actual.abajo.fila < nuevo.fila:
                    actual = actual.abajo

                nuevo.abajo = actual.abajo
                if actual.abajo is not None:
                    actual.abajo.arriba = nuevo

                nuevo.arriba = actual
                actual.abajo = nuevo

    def buscar(self, fila, columna):
        return self.existe_nodo(fila, columna)

    def recorrer_filas(self):
        resultado = []
        encabezado_fila = self.filas.primero

        while encabezado_fila is not None:
            actual = encabezado_fila.acceso
            while actual is not None:
                resultado.append(
                    {
                        "fila": actual.fila,
                        "columna": actual.columna,
                        "valor": actual.valor
                    }
                )
                actual = actual.derecha
            encabezado_fila = encabezado_fila.siguiente

        return resultado

    def recorrer_columnas(self):
        resultado = []
        encabezado_columna = self.columnas.primero

        while encabezado_columna is not None:
            actual = encabezado_columna.acceso
            while actual is not None:
                resultado.append(
                    {
                        "fila": actual.fila,
                        "columna": actual.columna,
                        "valor": actual.valor
                    }
                )
                actual = actual.abajo
            encabezado_columna = encabezado_columna.siguiente

        return resultado

    def mostrar_matriz(self):
        datos = self.recorrer_filas()

        if not datos:
            return ["La matriz está vacía"]

        salida = []
        for dato in datos:
            salida.append(
                f"Fila={dato['fila']} | Columna={dato['columna']} | Valor={dato['valor']}"
            )

        return salida