#!/usr/bin/env python3
"""Buscar palabras que aún les falten tildes en los archivos HTML."""
import re
import os

WORDS = [
    'evolucion', 'autonomia', 'autonoma', 'medica', 'practico', 'practica',
    'fisica', 'limites', 'tipico', 'dinamico', 'sintesis', 'analisis',
    'util', 'facil', 'camara', 'logica', 'estadistica', 'matematicas',
    'teoria', 'codigo', 'telefono', 'movil', 'portatil', 'sesion',
    'razon', 'ocasion', 'vision', 'mision', 'exito', 'pagina', 'segun',
    'dia', 'tambien', 'mas', 'ademas', 'despues', 'traves', 'comun',
    'unicamente', 'unica', 'unico', 'habiles', 'dificil', 'facilmente',
    'automaticamente', 'atras', 'ultima', 'ultimo', 'publica', 'publico',
    'terminos', 'termino', 'estandar', 'obten', 'multipagina', 'autonomos',
    'autonomo', 'periodo', 'periodicas', 'graficos', 'metricas', 'rapida',
    'rapido', 'rapidas', 'ilicitas', 'ilicito', 'licito', 'prohibe',
    'paises', 'pais', 'especifico', 'especificos', 'especifica',
    'electronica', 'tecnologia', 'tecnologias', 'critico', 'critica',
    'portatiles', 'informatico', 'tecnico', 'tecnica', 'legitima',
    'basica', 'diagnostico', 'envios', 'informacion', 'aceptacion',
    'posible', 'funcion', 'funciones', 'accion', 'acciones', 'opcion',
    'gestion', 'solucion', 'pregunta', 'respuesta', 'seccion', 'direccion',
    'atencion', 'proteccion', 'conexion', 'instalacion', 'configuracion',
    'obligacion', 'decision', 'intencion', 'prevencion', 'adaptacion',
    'comunicacion', 'verificacion', 'aplicacion', 'validacion',
    'metodo', 'metodos', 'numero', 'exito', 'insercion',
]

def main():
    root = 'site'
    found_any = False
    for dirpath, _dirs, files in os.walk(root):
        for f in sorted(files):
            if not f.endswith('.html'):
                continue
            fp = os.path.join(dirpath, f)
            with open(fp, 'r', encoding='utf-8') as fh:
                content = fh.read()
            # Procesar solo bloques de texto entre tags
            for m in re.finditer(r'>([^<]+)<', content):
                text = m.group(1)
                if not text.strip():
                    continue
                for word in WORDS:
                    pattern = r'(?<![A-Za-zÁÉÍÓÚáéíóúÑñ])' + word + r'(?![A-Za-zÁÉÍÓÚáéíóúÑñ])'
                    for mm in re.finditer(pattern, text, re.IGNORECASE):
                        found_any = True
                        print(f'{os.path.relpath(fp)}: word="{mm.group()}" in text="{text[:90]}"')
    if not found_any:
        print("No se encontraron palabras faltantes de tildes.")

if __name__ == '__main__':
    main()