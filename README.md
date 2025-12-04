# 📂 KIT MULTIFUNCIONAL DE AUTOMATIZACIÓN DE ARCHIVOS

Este proyecto consiste en el desarrollo de un Kit Multifuncional de Automatización de Archivos, implementado exclusivamente desde la **línea de comandos (CLI)** en Python.

El sistema simula un entorno real de trabajo al permitir al usuario organizar, analizar, auditar y generar reportes sobre una carpeta del sistema.

---

## ✨ Características Principales

El sistema está construido mediante programación estructurada y modular[cite: 12, 18, 64], ofreciendo las siguientes funcionalidades agrupadas:

**Gestor de Organización (`organizer.py`)**: Clasificación de archivos por extensión, tamaño y fecha de modificación. Incluye renombrado por expresiones regulares y un modo simulación.
**Analizador de Contenido (`analyzer.py`)**: Búsqueda y extracción de información relevante (correos, fechas) de archivos de texto utilizando expresiones regulares. Implementa la lectura eficiente mediante **Generadores**.
**Auditor de Cambios (`auditor.py`)**: Detección de archivos nuevos, modificados o eliminados mediante *snapshots*. Mantiene un registro histórico de actividades (`audit.log`) y usa **Decoradores** en funciones críticas.
**Generador de Reportes (`reports.py`)**: Creación de reportes automáticos en formatos `.txt` y `.csv` con estadísticas de las operaciones realizadas.

---

## 🛠️ Requisitos e Instalación

### Requisitos Técnicos

* Python 3.x
* Git (para la clonación)
* Se recomienda el uso de **Entornos Virtuales** para gestionar dependencias.



## 🚀 Uso del Sistema

El programa se ejecuta llamando al archivo principal (`main.py`) desde la terminal:
python main.py