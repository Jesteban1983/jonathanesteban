#!/usr/bin/env python3
"""Corrige tildes en el contenido visible de los HTML del sitio.

Usa HTMLParser y las utilidades de html_tools.py para que un error en
UN archivo NO rompa el procesamiento de los demás (try/except, atomic_write).

Solo corrige palabras que SIEMPRE llevan tilde (context-independent).
"""
import os
import re
import sys
from html.parser import HTMLParser

# Importar utilidades compartidas (desde el mismo directorio)
sys.path.insert(0, os.path.dirname(__file__))
from html_tools import (  # noqa: E402
    TEXT_ATTRS,
    BOUNDARY,
    iter_html_files,
    read_html,
    atomic_write,
    safe_process,
    summarize,
)

# ── Diccionario de correcciones (context-independent) ────────────────────
# Palabras que SIEMPRE llevan tilde
CORRECTIONS = {
    # -ción / -sión (esdrújulas)
    "automatizacion": "automatización",
    "Automatizacion": "Automatización",
    "reparacion": "reparación",
    "Reparacion": "Reparación",
    "configuracion": "configuración",
    "instalacion": "instalación",
    "Instalacion": "Instalación",
    "aplicacion": "aplicación",
    "Aplicacion": "Aplicación",
    "solucion": "solución",
    "Solucion": "Solución",
    "atencion": "atención",
    "Atencion": "Atención",
    "proteccion": "protección",
    "Proteccion": "Protección",
    "recuperacion": "recuperación",
    "integracion": "integración",
    "Integracion": "Integración",
    "publicacion": "publicación",
    "aprobacion": "aprobación",
    "comercializacion": "comercialización",
    "optimizacion": "optimización",
    "Optimizacion": "Optimización",
    "organizacion": "organización",
    "clasificacion": "clasificación",
    "migracion": "migración",
    "validacion": "validación",
    "Validacion": "Validación",
    "verificacion": "verificación",
    "notificacion": "notificación",
    "exposicion": "exposición",
    "peticion": "petición",
    "eliminacion": "eliminación",
    "Eliminacion": "Eliminación",
    "gestion": "gestión",
    "Gestion": "Gestión",
    "monitorizacion": "monitorización",
    "actualizacion": "actualización",
    "Actualizacion": "Actualización",
    "comunicacion": "comunicación",
    "Comunicacion": "Comunicación",
    "decision": "decisión",
    "certificacion": "certificación",
    "Certificacion": "Certificación",
    "formacion": "formación",
    "Formacion": "Formación",
    "operacion": "operación",
    "Operacion": "Operación",
    "condicion": "condición",
    "Condicion": "Condición",
    "obligacion": "obligación",
    "Obligacion": "Obligación",
    "suscripcion": "suscripción",
    "Suscripcion": "Suscripción",
    "transaccion": "transacción",
    "accion": "acción",
    "revision": "revisión",
    "Revision": "Revisión",
    "iteracion": "iteración",
    "implementacion": "implementación",
    "Implementacion": "Implementación",
    "documentacion": "documentación",
    "Documentacion": "Documentación",
    "demostracion": "demostración",
    "Demostracion": "Demostración",
    "simulacion": "simulación",
    "Simulacion": "Simulación",
    "generacion": "generación",
    "Generacion": "Generación",
    "valoracion": "valoración",
    "Valoracion": "Valoración",
    "informacion": "información",
    "Informacion": "Información",
    "aceptacion": "aceptación",
    "Aceptacion": "Aceptación",
    "limitacion": "limitación",
    "Limitacion": "Limitación",
    "variacion": "variación",
    "Variacion": "Variación",
    "negociacion": "negociación",
    "Negociacion": "Negociación",
    "navegacion": "navegación",
    "Navegacion": "Navegación",
    "prestacion": "prestación",
    "Prestacion": "Prestación",
    "duracion": "duración",
    "Duracion": "Duración",
    "situacion": "situación",
    "Situacion": "Situación",
    "ubicacion": "ubicación",
    "Ubicacion": "Ubicación",
    "intervencion": "intervención",
    "Intervencion": "Intervención",
    "produccion": "producción",
    "Produccion": "Producción",
    "seleccion": "selección",
    "Seleccion": "Selección",
    "prevencion": "prevención",
    "Prevencion": "Prevención",
    "ejecucion": "ejecución",
    "Ejecucion": "Ejecución",
    "definicion": "definición",
    "Definicion": "Definición",
    "descripcion": "descripción",
    "Descripcion": "Descripción",
    "introduccion": "introducción",
    "Introduccion": "Introducción",
    "proporcion": "proporción",
    "Proporcion": "Proporción",
    "precision": "precisión",
    "Precision": "Precisión",
    "expresion": "expresión",
    "Expresion": "Expresión",
    "version": "versión",
    "Version": "Versión",
    "extension": "extensión",
    "Extension": "Extensión",
    "intencion": "intención",
    "Intencion": "Intención",
    "mencion": "mención",
    "Mencion": "Mención",
    "sustitucion": "sustitución",
    "Sustitucion": "Sustitución",
    "coordinacion": "coordinación",
    "Coordinacion": "Coordinación",
    "administracion": "administración",
    "Administracion": "Administración",
    "estimacion": "estimación",
    "Estimacion": "Estimación",
    "metodologia": "metodología",
    "Metodologia": "Metodología",
    "multi-ubicacion": "multi-ubicación",
    # -ción largas
    "comercializacion": "comercialización",
    "automatizaciones": "automatizaciones",
    # Esdrújulas
    "terminos": "términos",
    "Terminos": "Términos",
    "termino": "término",
    "Termino": "Término",
    "ultima": "última",
    "Ultima": "Última",
    "ultimo": "último",
    "Ultimo": "Último",
    "publica": "pública",
    "Publica": "Pública",
    "publico": "público",
    "Publico": "Público",
    "informatico": "informático",
    "Informatico": "Informático",
    "tecnica": "técnica",
    "Tecnica": "Técnica",
    "tecnico": "técnico",
    "Tecnico": "Técnico",
    "Tecnicas": "Técnicas",
    "tecnicas": "técnicas",
    "basica": "básica",
    "basico": "básico",
    "basicas": "básicas",
    "basicos": "básicos",
    "graficos": "gráficos",
    "Graficos": "Gráficos",
    "metricas": "métricas",
    "Metricas": "Métricas",
    "practica": "práctica",
    "Practica": "Práctica",
    "Practico": "Práctico",
    "dinamico": "dinámico",
    "Dinamico": "Dinámico",
    "rapida": "rápida",
    "Rapida": "Rápida",
    "rapido": "rápido",
    "Rapido": "Rápido",
    "rapidas": "rápidas",
    "ilicitas": "ilícitas",
    "ilicito": "ilícito",
    "Ilicito": "Ilícito",
    "licito": "lícito",
    "prohibe": "prohíbe",
    "Prohibe": "Prohíbe",
    "paises": "países",
    "Paises": "Países",
    "pais": "país",
    "Pais": "País",
    "dia": "día",
    "Dia": "Día",
    "tambien": "también",
    "Tambien": "También",
    "mas": "más",
    "Mas": "Más",
    "ademas": "además",
    "Ademas": "Además",
    "despues": "después",
    "Despues": "Después",
    "traves": "través",
    "comun": "común",
    "Comun": "Común",
    "unicamente": "únicamente",
    "Unicamente": "Únicamente",
    "unica": "única",
    "Unica": "Única",
    "unico": "único",
    "Unico": "Único",
    "habiles": "hábiles",
    "Habiles": "Hábiles",
    "facil": "fácil",
    "Facil": "Fácil",
    "util": "útil",
    "Util": "Útil",
    "dificil": "difícil",
    "Dificil": "Difícil",
    "facilmente": "fácilmente",
    "automaticamente": "automáticamente",
    "Automaticamente": "Automáticamente",
    "atras": "atrás",
    "Atras": "Atrás",
    "telefono": "teléfono",
    "Telefono": "Teléfono",
    "codigo": "código",
    "Codigo": "Código",
    "Codigos": "Códigos",
    "codigos": "códigos",
    "movil": "móvil",
    "Movil": "Móvil",
    "moviles": "móviles",
    "Moviles": "Móviles",
    "electronica": "electrónica",
    "Electronica": "Electrónica",
    "tecnologia": "tecnología",
    "Tecnologia": "Tecnología",
    "tecnologias": "tecnologías",
    "Tecnologias": "Tecnologías",
    "matematicas": "matemáticas",
    "Matematicas": "Matemáticas",
    "fisica": "física",
    "Fisica": "Física",
    "quimica": "química",
    "Quimica": "Química",
    "logica": "lógica",
    "Logica": "Lógica",
    "estadistica": "estadística",
    "Estadistica": "Estadística",
    "analisis": "análisis",
    "Analisis": "Análisis",
    "sintesis": "síntesis",
    "Sintesis": "Síntesis",
    "hipotesis": "hipótesis",
    "Hipotesis": "Hipótesis",
    "critico": "crítico",
    "Critico": "Crítico",
    "critica": "crítica",
    "Critica": "Crítica",
    "teoria": "teoría",
    "Teoria": "Teoría",
    "estandar": "estándar",
    "Estandar": "Estándar",
    "portatil": "portátil",
    "Portatil": "Portátil",
    "portatiles": "portátiles",
    "Portatiles": "Portátiles",
    "sesion": "sesión",
    "Sesion": "Sesión",
    "obten": "obtén",
    "multipagina": "multipágina",
    "Multipagina": "Multipágina",
    "autonomos": "autónomos",
    "Autonomos": "Autónomos",
    "autonomo": "autónomo",
    "Autonomo": "Autónomo",
    "tipico": "típico",
    "Tipico": "Típico",
    "periodicas": "periódicas",
    "razon": "razón",
    "Razon": "Razón",
    "ocasion": "ocasión",
    "Ocasion": "Ocasión",
    "vision": "visión",
    "Vision": "Visión",
    "mision": "misión",
    "Mision": "Misión",
    "posesion": "posesión",
    "Posesion": "Posesión",
    "tension": "tensión",
    "Tension": "Tensión",
    "adhesion": "adhesión",
    "Adhesion": "Adhesión",
    "evolucion": "evolución",
    "Evolucion": "Evolución",
    "autonomia": "autonomía",
    "Autonomia": "Autonomía",
    "configuracion": "configuración",
    "Configuracion": "Configuración",
}

# Ordenado por longitud descendente para reemplazar palabras largas primero
SORTED = sorted(CORRECTIONS.items(), key=lambda x: -len(x[0]))


def fix_text(text: str) -> str:
    """Aplica correcciones de tildes al texto."""
    for wrong, correct in SORTED:
        try:
            text = re.sub(
                BOUNDARY + re.escape(wrong) + r"(?![A-Za-zÁÉÍÓÚáéíóúÑñ])",
                correct,
                text,
            )
        except re.error as exc:
            # Si una regex falla, continuamos con la siguiente
            print(f"  ⚠ [regex] patrón '{wrong}': {exc}")
    return text


class OrthoFixer(HTMLParser):
    """Parseador HTML que corrige tildes solo en texto visible y atributos seguros."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.in_script_style = False

    def handle_starttag(self, tag, attrs):
        self.out.append(self.get_starttag_text())
        if tag in ("script", "style"):
            self.in_script_style = True
        # Corregir atributos de lenguaje natural
        if attrs:
            raw = self.get_starttag_text()
            new_raw = raw
            for key, value in attrs:
                if value and key.lower() in TEXT_ATTRS and key.lower() != "name":
                    try:
                        fixed_value = fix_text(value)
                        if fixed_value != value:
                            new_raw = new_raw.replace(
                                f'{key}="{value}"', f'{key}="{fixed_value}"'
                            )
                    except Exception as exc:
                        print(f"  ⚠ [attr] {key}={value!r}: {exc}")
            if new_raw != raw:
                self.out[-1] = new_raw

    def handle_startendtag(self, tag, attrs):
        self.out.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.in_script_style = False
        self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if self.in_script_style:
            self.out.append(data)
        else:
            try:
                self.out.append(fix_text(data))
            except Exception as exc:
                print(f"  ⚠ [data] {exc}")
                self.out.append(data)

    def handle_comment(self, data):
        self.out.append(f"<!--{data}-->")

    def handle_decl(self, decl):
        self.out.append(f"<!{decl}>")

    def handle_pi(self, data):
        self.out.append(f"<?{data}>")

    def handle_entityref(self, name):
        self.out.append(f"&{name};")

    def handle_charref(self, name):
        self.out.append(f"&#{name};")

    def result(self):
        return "".join(self.out)


def process_html(content: str) -> str:
    """Procesa el contenido HTML completo."""
    parser = OrthoFixer()
    parser.feed(content)
    parser.close()
    return parser.result()


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "site")
    files = iter_html_files(root)
    print(f"Procesando {len(files)} archivos HTML...\n")

    results = {}
    for fp in files:
        rel = os.path.relpath(fp)
        status = safe_process(fp, process_html, backup=True)
        results[rel] = status
        if status == "ok":
            print(f"✓ {rel}")
        elif status == "error":
            print(f"✗ {rel} (error)")
        # "same" no se imprime para no saturar

    summarize(results)


if __name__ == "__main__":
    main()