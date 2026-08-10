#!/usr/bin/env python3
"""Busca abreviaturas seguidas de minúscula en el texto HTML.

Útil para verificar que el script de mayúsculas no dañará abreviaturas.
Usa html_tools.py para manejo de errores.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from html_tools import iter_html_files, read_html  # noqa: E402


def check_file(filepath: str):
    """Busca patrones 'abrev. minúscula' en un archivo. Devuelve lista de resultados."""
    content = read_html(filepath)
    if content is None:
        return []

    results = []
    try:
        # Remover script/style (no tocar su contenido)
        cleaned = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        cleaned = re.sub(r'<style[^>]*>.*?</style>', '', cleaned, flags=re.DOTALL)
    except re.error as exc:
        print(f"  ⚠ [regex] {os.path.relpath(filepath)}: {exc}")
        return results

    try:
        for m in re.finditer(r'>([^<]+)<', cleaned):
            text = m.group(1)
            if not text.strip():
                continue
            for mm in re.finditer(r'[A-Za-z]{1,4}\. [a-z]', text):
                results.append((mm.group(), text.strip()[:80]))
    except re.error as exc:
        print(f"  ⚠ [regex] {os.path.relpath(filepath)}: {exc}")

    return results


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
            for abbrev, context in results:
                print(f'  "{abbrev}" in "{context}"')
                total_found += 1

    if total_found == 0:
        print("\nNo se encontraron abreviaturas. ✓")
    else:
        print(f"\n--- Total: {total_found} abreviatura(s) encontrada(s) ---")


if __name__ == '__main__':
    main()