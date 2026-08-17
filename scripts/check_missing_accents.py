#!/usr/bin/env python3
"""Busca palabras que aún les falten tildes en los archivos HTML.

Usa html_tools.py para que un error en UN archivo no rompa el análisis.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from html_tools import BOUNDARY, iter_html_files, read_html  # noqa: E402

# Palabras que deberían tener tilde (esdrújulas, agudas acabadas en n/s/vocal, etc.)
# Incluye SOLO palabras que NO cambian de significado con tilde.
WORDS = [
    'evolucion',
    'autonomia',
    'autonoma', 'autonomo', 'autonomos',
    'medica', 'medico', 'medicos',
    'practico', 'practica', 'practicos',
    'fisica', 'fisico',
    'tipico', 'tipica',
    'dinamico', 'dinamica',
    'sintesis',
    'analisis',
    'util', 'utilmente',
    'facil', 'facilmente',
    'dificil',
    'camara', 'camaras',
    'logica', 'logico',
    'estadistica', 'estadistico',
    'matematicas', 'matematico',
    'teoria', 'teorica',
    'codigo', 'codigos',
    'telefono', 'telefonos',
    'movil', 'moviles',
    'portatil', 'portatiles',
    'sesion',
    'razon',
    'ocasion',
    'vision',
    'mision',
    'exito',
    'pagina', 'paginas',
    'segun',
    'dia',
    'tambien',
    'mas',
    'ademas',
    'despues',
    'traves',
    'comun',
    'unicamente',
    'unica', 'unico', 'unicos', 'unicas',
    'habiles',
    'automaticamente',
    'atras',
    'ultima', 'ultimo', 'ultimas', 'ultimos',
    'publica', 'publico', 'publicos', 'publicas',
    'terminos', 'termino',
    'estandar',
    'obten',
    'multipagina',
    'periodo', 'periodicas', 'periodico', 'periodica',
    'graficos', 'grafico', 'grafica',
    'metricas', 'metrica',
    'rapida', 'rapido', 'rapidas', 'rapidos',
    'ilicitas', 'ilicito', 'ilicita',
    'licito', 'licita',
    'prohibe',
    'paises', 'pais',
    'especifico', 'especificos', 'especifica', 'especificas',
    'electronica', 'electronico',
    'tecnologia', 'tecnologias', 'tecnologico',
    'critico', 'critica', 'criticos', 'criticas',
    'portatiles',
    'informatico', 'informatica',
    'tecnico', 'tecnica', 'tecnicos', 'tecnicas',
    'legitima', 'legitimo',
    'basica', 'basico', 'basicas',
    'diagnostico',
    'envios',
    'informacion',
    'aceptacion',
    'posible', 'posibles',
    'funcion',
    'opcion',
    'gestion',
    'solucion',
    'pregunta',
    'seccion', 'secciones',
    'direccion',
    'atencion',
    'proteccion',
    'conexion',
    'instalacion',
    'configuracion',
    'obligacion',
    'decision',
    'intencion',
    'prevencion',
    'adaptacion',
    'comunicacion',
    'verificacion',
    'aplicacion',
    'validacion',
    'metodo', 'metodos',
    'numero', 'numeros',
    'insercion',
    'constitucion',
    'distribucion',
    'evaluacion',
    'explotacion',
    'facturacion',
    'federacion',
    'fundacion',
    'iluminacion',
    'implantacion',
    'indemnizacion',
    'inspeccion',
    'liquidacion',
    'negociacion',
    'notificacion',
    'observacion',
    'participacion',
    'poblacion',
    'reclamacion',
    'recomendacion',
    'reputacion',
    'senalizacion',
    'tributacion',
    'utilizacion',
    'variacion',
    'suscripcion',
    'transaccion',
    'accion',
    'revision',
    'iteracion',
    'implementacion',
    'documentacion',
    'demostracion',
    'simulacion',
    'generacion',
    'valoracion',
    'limitacion',
    'prestacion',
    'duracion',
    'situacion',
    'ubicacion',
    'intervencion',
    'produccion',
    'seleccion',
    'ejecucion',
    'definicion',
    'descripcion',
    'introduccion',
    'proporcion',
    'precision',
    'expresion',
    'version',
    'extension',
    'mencion',
    'sustitucion',
    'coordinacion',
    'administracion',
    'estimacion',
    'metodologia',
    'formacion',
    'operacion',
    'condicion',
    'certificacion',
    'monitorizacion',
    'actualizacion',
    'recuperacion',
    'integracion',
    'publicacion',
    'aprobacion',
    'comercializacion',
    'optimizacion',
    'organizacion',
    'clasificacion',
    'migracion',
    'eliminacion',
    'exposicion',
    'peticion',
    'navegacion',
    'reparacion',
    'instalacion',
    'configuracion',
    'automatizacion',
    'multi-ubicacion',
    'posesion',
    'tension',
    'adhesion',
]


def check_file(filepath: str):
    """Busca palabras sin tilde en un archivo HTML. Devuelve lista de (palabra, contexto)."""
    content = read_html(filepath)
    if content is None:
        return []

    found = []
    try:
        # Extraer bloques de texto entre tags
        for m in re.finditer(r'>([^<]+)<', content):
            text = m.group(1)
            if not text.strip():
                continue
            for word in WORDS:
                try:
                    pattern = BOUNDARY + re.escape(word) + r"(?![A-Za-zÁÉÍÓÚáéíóúÑñ])"
                    for mm in re.finditer(pattern, text, re.IGNORECASE):
                        found.append((mm.group(), text.strip()[:90]))
                except re.error:
                    continue
    except re.error as exc:
        print(f"  ⚠ [regex] {os.path.relpath(filepath)}: {exc}")

    return found


def main():
    root = os.path.join(os.path.dirname(__file__), "..", "site")
    files = iter_html_files(root)
    total_found = 0

    for fp in files:
        rel = os.path.relpath(fp)
        try:
            results = check_file(fp)
        except Exception as exc:
            print(f"✗ {rel}: error inesperado: {exc}")
            continue

        if results:
            print(f"\n{rel}:")
            for word, context in results:
                print(f'  word="{word}" in "{context}"')
                total_found += 1

    if total_found == 0:
        print("\nNo se encontraron palabras faltantes de tildes. ✓")
    else:
        print(f"\n--- Total: {total_found} palabra(s) sin tilde ---")


if __name__ == '__main__':
    main()