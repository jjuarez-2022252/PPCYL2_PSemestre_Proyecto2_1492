# PPCYL2-AcadNet

Proyecto universitario desarrollado con **Frontend en Django** y **Backend/API en Flask**, orientado a la gestión académica de usuarios, cursos, horarios, notas y reportes, utilizando **POO**, **XML**, **expresiones regulares**, **matriz dispersa**, **Graphviz**, **Plotly** y **PDF**.

---

## Descripción general

PPCYL2-AcadNet es una plataforma académica que permite administrar información de cursos, tutores, estudiantes, horarios y notas mediante archivos XML.

El sistema está dividido en dos partes principales:

- **Frontend en Django**: interfaz de usuario, login por roles, dashboards y visualización.
- **Backend en Flask**: procesamiento de XML, lógica de negocio, generación de reportes, matriz dispersa y comunicación HTTP.

---

## Tecnologías utilizadas

### Backend
- Python
- Flask
- Flask-Cors
- XML (`xml.etree.ElementTree`)
- Expresiones regulares (`re`)
- Graphviz

### Frontend
- Django
- Requests
- Plotly
- ReportLab

### Otras herramientas
- Git
- GitHub

---

## Arquitectura del proyecto

El proyecto está organizado en dos módulos principales:

- **backend/** → API Flask
- **frontend/** → Aplicación web Django

La comunicación entre ambos se realiza por medio de **HTTP**, consumiendo endpoints Flask desde Django.

---

## Estructura del proyecto

```text
PPCYL2_PSemestre_Proyecto2_[1492]/
│
├── readme.md
├── .gitignore
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── rutas/
│   │   └── __init__.py
│   ├── estructuras/
│   │   ├── __init__.py
│   │   ├── nodo.py
│   │   └── matriz_dispersa.py
│   ├── analizador/
│   │   ├── __init__.py
│   │   ├── lector_xml.py
│   │   ├── lector_configuracion.py
│   │   ├── lector_horarios.py
│   │   ├── reporte_graphviz.py
│   │   └── generador_salida_configuracion.py
│   └── archivos_datos/
│       ├── entrada/
│       │   ├── configuracion.xml
│       │   ├── horarios.xml
│       │   └── notas.xml
│       └── salida/
│           ├── configuraciones_aplicadas.xml
│           └── matriz_dispersa.png
│
└── frontend/
    ├── manage.py
    ├── requirements.txt
    ├── db.sqlite3
    ├── acadnet_project/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    └── app_cliente/
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── decorators.py
        ├── forms.py
        ├── models.py
        ├── signals.py
        ├── urls.py
        ├── views.py
        ├── migrations/
        ├── templates/
        │   ├── login.html
        │   ├── admin_dashboard.html
        │   ├── tutor_dashboard.html
        │   └── estudiante_dashboard.html
        └── static/
            └── css/