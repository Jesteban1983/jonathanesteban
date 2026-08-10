#!/usr/bin/env python3
"""Corrige ortografía (tildes) en el contenido visible de los HTML del sitio.

Usa HTMLParser para tocar SOLO nodos de texto (no script/style/atributos con código).
Solo corrige palabras que SIEMPRE llevan tilde (no dependientes de contexto).
"""
import os
import re
from html.parser import HTMLParser


# Corrections that are ALWAYS correct (context-independent):
# "Xcion" (esdrújula de nombre) siempre lleva tilde.
CORRECTIONS = {
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
    "legitima": "legítima",
    "basica": "básica",
    "diagnostico": "diagnóstico",
    "Diagnostico": "Diagnóstico",
    "limites": "límites",
    "envios": "envíos",
    "segun": "según",
    "Segun": "Según",
    "pagina": "página",
    "Pagina": "Página",
    "exito": "éxito",
    "Exito": "Éxito",
    "periodo": "período",
    "automaticas": "automáticas",
    "automatica": "automática",
    "Automatica": "Automática",
    "automatico": "automático",
    "Automatico": "Automático",
    "automaticos": "automáticos",
    "especifico": "específico",
    "Especifico": "Específico",
    "especificos": "específicos",
    "Especificos": "Específicos",
    "especifica": "específica",
    "Especifica": "Específica",
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
    "multi-ubicacion": "multi-ubicación",
}

# Order by length descending so longer words are replaced first
SORTED = sorted(CORRECTIONS.items(), key=lambda x: -len(x[0]))
_BOUNDARY = r"(?<![A-Za-zÁÉÍÓÚáéíóúÑñ])"


def fix_text(text: str) -> str:
    for wrong, correct in SORTED:
        text = re.sub(
            _BOUNDARY + re.escape(wrong) + r"(?![A-Za-zÁÉÍÓÚáéíóúÑñ])",
            correct,
            text,
        )
    return text


# Attributes whose value is natural language (safe to fix)
TEXT_ATTRS = {"content", "placeholder", "alt", "title", "name"}


class Fixer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.in_script_style = False

    def handle_starttag(self, tag, attrs):
        self.out.append(self.get_starttag_text())
        if tag in ("script", "style"):
            self.in_script_style = True
        # Fix natural-language attribute values
        if attrs:
            raw = self.get_starttag_text()
            new_raw = raw
            for key, value in attrs:
                if value and key.lower() in TEXT_ATTRS and key.lower() != "name":
                    fixed_value = fix_text(value)
                    if fixed_value != value:
                        # Replace within the raw tag: key="value"
                        new_raw = new_raw.replace(f'{key}="{value}"', f'{key}="{fixed_value}"')
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
            self.out.append(fix_text(data))

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


def process_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    parser = Fixer()
    parser.feed(content)
    parser.close()
    new_content = parser.result()
    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


def main():
    root = "site"
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(".html"):
                html_files.append(os.path.join(dirpath, f))
    html_files.sort()

    fixed = []
    for fp in html_files:
        if process_html(fp):
            fixed.append(fp)
            print(f"FIXED: {fp}")
        else:
            print(f"(no changes): {fp}")
    print(f"\nTotal files modified: {len(fixed)}")


if __name__ == "__main__":
    main()
