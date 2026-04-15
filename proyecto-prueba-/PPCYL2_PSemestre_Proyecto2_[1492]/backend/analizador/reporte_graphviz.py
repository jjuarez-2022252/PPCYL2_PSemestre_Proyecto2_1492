from graphviz import Digraph


class ReporteGraphviz:
    def generar_reporte_matriz(self, matriz, nombre_salida="matriz_dispersa"):
        dot = Digraph(comment="Reporte de Matriz Dispersa")
        dot.attr(rankdir="LR")
        dot.attr("node", shape="box")

        # Nodo principal
        dot.node("MATRIZ", "Matriz Dispersa")

        # Recorrer la matriz por filas
        datos = matriz.recorrer_filas()

        if not datos:
            dot.node("VACIA", "Matriz vacía")
            dot.edge("MATRIZ", "VACIA")
        else:
            anterior_id = None

            for i, dato in enumerate(datos):
                nodo_id = f"N{i}"
                etiqueta = (
                    f"Actividad: {dato['fila']}\n"
                    f"Carnet: {dato['columna']}\n"
                    f"Nota: {dato['valor']}"
                )

                dot.node(nodo_id, etiqueta)

                if i == 0:
                    dot.edge("MATRIZ", nodo_id)
                else:
                    dot.edge(anterior_id, nodo_id)

                anterior_id = nodo_id

        # Guardar el archivo PNG
        ruta_generada = dot.render(
            filename=nombre_salida,
            directory="archivos_datos/salida",
            format="png",
            cleanup=True
        )

        return ruta_generada