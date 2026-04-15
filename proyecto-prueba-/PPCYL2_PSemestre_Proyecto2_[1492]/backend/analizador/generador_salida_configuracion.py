import os
import xml.etree.ElementTree as ET


class GeneradorSalidaConfiguracion:
    def validar_y_generar_salida(self, datos, ruta_salida):
        # =========================
        # CONTAR TUTORES Y ESTUDIANTES CARGADOS
        # =========================
        total_tutores_cargados = len(datos["tutores"])
        total_estudiantes_cargados = len(datos["estudiantes"])

        # =========================
        # PREPARAR CONJUNTOS PARA VALIDAR
        # =========================
        codigos_cursos = set()
        registros_tutores = set()
        carnets_estudiantes = set()

        for curso in datos["cursos"]:
            codigos_cursos.add(curso["codigo"])

        for tutor in datos["tutores"]:
            registros_tutores.add(tutor["registro"])

        for estudiante in datos["estudiantes"]:
            carnets_estudiantes.add(estudiante["carnet"])

        # =========================
        # VALIDAR ASIGNACIONES DE TUTORES
        # =========================
        total_asig_tutores = len(datos["asignaciones_tutor"])
        correctas_tutores = 0
        incorrectas_tutores = 0

        for asignacion in datos["asignaciones_tutor"]:
            registro_tutor = asignacion["registro_tutor"]
            codigo_curso = asignacion["codigo_curso"]

            if registro_tutor in registros_tutores and codigo_curso in codigos_cursos:
                correctas_tutores += 1
            else:
                incorrectas_tutores += 1

        # =========================
        # VALIDAR ASIGNACIONES DE ESTUDIANTES
        # =========================
        total_asig_estudiantes = len(datos["asignaciones_estudiante"])
        correctas_estudiantes = 0
        incorrectas_estudiantes = 0

        for asignacion in datos["asignaciones_estudiante"]:
            carnet = asignacion["carnet"]
            codigo_curso = asignacion["codigo_curso"]

            if carnet in carnets_estudiantes and codigo_curso in codigos_cursos:
                correctas_estudiantes += 1
            else:
                incorrectas_estudiantes += 1

        # =========================
        # CREAR XML DE SALIDA
        # =========================
        raiz = ET.Element("configuraciones_aplicadas")

        tutores_cargados = ET.SubElement(raiz, "tutores_cargados")
        tutores_cargados.text = str(total_tutores_cargados)

        # Mantengo el nombre exactamente como lo pusiste en la tarea
        estudiantes_cargados = ET.SubElement(raiz, "estdudiantes_cargados")
        estudiantes_cargados.text = str(total_estudiantes_cargados)

        asignaciones = ET.SubElement(raiz, "asignaciones")

        bloque_tutores = ET.SubElement(asignaciones, "tutores")
        total_tutores = ET.SubElement(bloque_tutores, "total")
        total_tutores.text = str(total_asig_tutores)

        correcto_tutores = ET.SubElement(bloque_tutores, "correcto")
        correcto_tutores.text = str(correctas_tutores)

        incorrecto_tutores = ET.SubElement(bloque_tutores, "incorrecto")
        incorrecto_tutores.text = str(incorrectas_tutores)

        bloque_estudiantes = ET.SubElement(asignaciones, "estudiantes")
        total_estudiantes = ET.SubElement(bloque_estudiantes, "total")
        total_estudiantes.text = str(total_asig_estudiantes)

        correcto_estudiantes = ET.SubElement(bloque_estudiantes, "correcto")
        correcto_estudiantes.text = str(correctas_estudiantes)

        incorrecto_estudiantes = ET.SubElement(bloque_estudiantes, "incorrecto")
        incorrecto_estudiantes.text = str(incorrectas_estudiantes)

        # =========================
        # GUARDAR XML
        # =========================
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

        arbol = ET.ElementTree(raiz)
        arbol.write(ruta_salida, encoding="utf-8", xml_declaration=True)

        # También devolver resumen en diccionario
        return {
            "tutores_cargados": total_tutores_cargados,
            "estudiantes_cargados": total_estudiantes_cargados,
            "asignaciones_tutor": {
                "total": total_asig_tutores,
                "correcto": correctas_tutores,
                "incorrecto": incorrectas_tutores
            },
            "asignaciones_estudiante": {
                "total": total_asig_estudiantes,
                "correcto": correctas_estudiantes,
                "incorrecto": incorrectas_estudiantes
            },
            "ruta_salida": ruta_salida
        }