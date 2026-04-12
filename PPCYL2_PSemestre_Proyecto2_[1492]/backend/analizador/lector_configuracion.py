import xml.etree.ElementTree as ET


class LectorConfiguracion:
    def leer_configuracion(self, ruta_archivo):
        # Diccionario donde guardaremos toda la información extraída
        datos = {
            "cursos": [],
            "tutores": [],
            "estudiantes": [],
            "asignaciones_tutor": [],
            "asignaciones_estudiante": []
        }

        # Cargar el XML
        arbol = ET.parse(ruta_archivo)
        raiz = arbol.getroot()

        # =========================
        # LEER CURSOS
        # =========================
        bloque_cursos = raiz.find("cursos")
        if bloque_cursos is not None:
            for curso in bloque_cursos.findall("curso"):
                codigo = curso.findtext("codigo", default="").strip()
                nombre = curso.findtext("nombre", default="").strip()

                datos["cursos"].append({
                    "codigo": codigo,
                    "nombre": nombre
                })

        # =========================
        # LEER TUTORES
        # =========================
        bloque_tutores = raiz.find("tutores")
        if bloque_tutores is not None:
            for tutor in bloque_tutores.findall("tutor"):
                registro = tutor.findtext("registro", default="").strip()
                nombre = tutor.findtext("nombre", default="").strip()
                usuario = tutor.findtext("usuario", default="").strip()

                datos["tutores"].append({
                    "registro": registro,
                    "nombre": nombre,
                    "usuario": usuario
                })

        # =========================
        # LEER ESTUDIANTES
        # =========================
        bloque_estudiantes = raiz.find("estudiantes")
        if bloque_estudiantes is not None:
            for estudiante in bloque_estudiantes.findall("estudiante"):
                carnet = estudiante.findtext("carnet", default="").strip()
                nombre = estudiante.findtext("nombre", default="").strip()
                usuario = estudiante.findtext("usuario", default="").strip()

                datos["estudiantes"].append({
                    "carnet": carnet,
                    "nombre": nombre,
                    "usuario": usuario
                })

        # =========================
        # LEER ASIGNACIONES DE TUTOR
        # =========================
        bloque_asignaciones_tutor = raiz.find("asignaciones_tutor")
        if bloque_asignaciones_tutor is not None:
            for asignacion in bloque_asignaciones_tutor.findall("asignacion"):
                registro_tutor = asignacion.findtext("registro_tutor", default="").strip()
                codigo_curso = asignacion.findtext("codigo_curso", default="").strip()

                datos["asignaciones_tutor"].append({
                    "registro_tutor": registro_tutor,
                    "codigo_curso": codigo_curso
                })

        # =========================
        # LEER ASIGNACIONES DE ESTUDIANTE
        # =========================
        bloque_asignaciones_estudiante = raiz.find("asignaciones_estudiante")
        if bloque_asignaciones_estudiante is not None:
            for asignacion in bloque_asignaciones_estudiante.findall("asignacion"):
                carnet = asignacion.findtext("carnet", default="").strip()
                codigo_curso = asignacion.findtext("codigo_curso", default="").strip()

                datos["asignaciones_estudiante"].append({
                    "carnet": carnet,
                    "codigo_curso": codigo_curso
                })

        return datos