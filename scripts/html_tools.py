#!/usr/bin/env python3
"""Utilidades compartidas para procesar archivos HTML de forma segura.

Objetivo: que un error en UN archivo no rompa el procesamiento de los demás.

Proporciona:
  - iter_html_files(root): recorre los .html del sitio de forma ordenada.
  - read_html(filepath):   lectura segura (devuelve None si falla, sin lanzar).
  - atomic_write(...):     escritura atómica (temp + rename) con backup opcional.
  - safe_process(...):     ejecuta un procesador por archivo capturando errores.

Un error (permisos, encoding, HTML malformado, regex, etc.) se reporta y se
continúa con el siguiente archivo: la estructura del sitio nunca se rompe.
"""
import os
import re
import shutil
import tempfile


def iter_html_files(root: str):
    """Devuelve lista ordenada de rutas .html bajo `root`."""
    html_files = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(".html"):
                html_files.append(os.path.join(dirpath, f))
    return sorted(html_files)


def read_html(filepath: str):
    """Lee un archivo HTML. Devuelve el contenido (str) o None si falla."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeError) as exc:
        print(f"  ⚠ [lectura] {os.path.relpath(filepath)}: {exc}")
        return None


def atomic_write(filepath: str, content: str, backup: bool = True) -> bool:
    """Escribe contenido de forma atómica: temp file + os.replace().

    - backup=True  → copia .bak del original antes de sobrescribir.
    - Si algo falla a mitad de escritura, el archivo original queda intacto.
    Devuelve True si se escribió correctamente.
    """
    try:
        if backup and os.path.exists(filepath):
            shutil.copy2(filepath, filepath + ".bak")

        dirpath = os.path.dirname(filepath) or "."
        fd, tmp_path = tempfile.mkstemp(dir=dirpath, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(content)
            # Reemplazo atómico: nunca deja el archivo a medias
            os.replace(tmp_path, filepath)
        except Exception:
            # Limpiar el temporal si algo falló
            try:
                os.remove(tmp_path)
            except OSError:
                pass
            raise
        return True
    except (OSError, UnicodeError) as exc:
        print(f"  ⚠ [escritura] {os.path.relpath(filepath)}: {exc}")
        return False


def safe_process(filepath: str, processor, backup: bool = True) -> str:
    """Procesa un archivo HTML capturando cualquier error.

    `processor(content) -> nuevo_contenido`
    Devuelve:
      - "ok"    → se procesó y cambió.
      - "same"  → se procesó y no cambió.
      - "error" → falló (se reporta y se continúa).
    """
    content = read_html(filepath)
    if content is None:
        return "error"

    try:
        new_content = processor(content)
    except Exception as exc:  # noqa: BLE001 - queremos continuar con el resto
        print(f"  ⚠ [procesado] {os.path.relpath(filepath)}: {exc}")
        return "error"

    if new_content == content:
        return "same"

    if atomic_write(filepath, new_content, backup=backup):
        return "ok"
    return "error"


def summarize(results: dict) -> None:
    """Imprime un resumen legible de los resultados de safe_process."""
    ok = sum(1 for v in results.values() if v == "ok")
    same = sum(1 for v in results.values() if v == "same")
    errors = sum(1 for v in results.values() if v == "error")
    total = len(results)
    print("\n" + "=" * 60)
    print(f"RESUMEN: {total} archivos | {ok} modificados | {same} sin cambios | {errors} errores")
    if errors:
        print("Hubo errores; revisa los mensajes '⚠' de arriba.")
    else:
        print("Sin errores.")
    print("=" * 60)


# Atributos cuyo valor es lenguaje natural (seguro corregir tildes)
TEXT_ATTRS = {"content", "placeholder", "alt", "title"}

# Patrón de frontera de palabra (para no tocar subcadenas dentro de palabras)
BOUNDARY = r"(?<![A-Za-zÁÉÍÓÚáéíóúÑñ])"
