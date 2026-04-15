import re
import xml.etree.ElementTree as ET


class LectorHorarios:
    def extraer_horas(self, texto):
        patron_inicio = r"HorarioI:\s*(\d{2}:\d{2})"
        patron_fin = r"HorarioF:\s*(\d{2}:\d{2})"

        coincidencia_inicio = re.search(patron_inicio, texto)
        coincidencia_fin = re.search(patron_fin, texto)

        hora_inicio = coincidencia_inicio.group(1) if coincidencia_inicio else ""
        hora_fin = coincidencia_fin.group(1) if coincidencia_fin else ""

        return hora_inicio, hora_fin

    def leer_horarios(self, ruta_archivo):
        horarios = []

        arbol = ET.parse(ruta_archivo)
        raiz = arbol.getroot()

        for horario in raiz.findall("horario"):
            curso = horario.findtext("curso", default="").strip()
            tutor = horario.findtext("tutor", default="").strip()
            cadena = horario.findtext("cadena", default="").strip()

            hora_inicio, hora_fin = self.extraer_horas(cadena)

            horarios.append({
                "curso": curso,
                "tutor": tutor,
                "cadena_original": cadena,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin
            })

        return horarios