import xml.etree.ElementTree as ET


class LectorXML:
    def leer_notas(self, ruta_archivo):
        notas = []

        # Cargar y parsear el XML
        arbol = ET.parse(ruta_archivo)
        raiz = arbol.getroot()

        # Recorrer cada etiqueta <nota>
        for nota in raiz.findall("nota"):
            actividad = nota.find("actividad").text
            carnet = nota.find("carnet").text
            valor = float(nota.find("valor").text)

            notas.append({
                "actividad": actividad,
                "carnet": carnet,
                "valor": valor
            })

        return notas