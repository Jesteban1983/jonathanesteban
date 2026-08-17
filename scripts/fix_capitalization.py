#!/usr/bin/env python3
"""Corrige mayúsculas después de punto y dos puntos en textos HTML.

Usa HTMLParser + html_tools.py para que un error en UN archivo no
rompa el procesamiento de los demás (try/except, atomic_write, backup).

Ignora emails, URLs, dominios, n8n, abreviaturas y código preformateado.
NO aplica regla de "primer carácter" para evitar dañar etiquetas inline.
"""
import os
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(__file__))
from html_tools import (  # noqa: E402
    iter_html_files,
    safe_process,
    summarize,
)


# ── Funciones auxiliares ──────────────────────────────────────────────────


def looks_like_email(text: str) -> bool:
    try:
        return bool(re.match(r'^[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}$', text.strip()))
    except re.error:
        return False


def looks_like_url(text: str) -> bool:
    try:
        return bool(re.match(r'^https?://', text.strip()))
    except re.error:
        return False


def looks_like_domain(text: str) -> bool:
    try:
        return bool(re.match(r'^[\w-]+\.[a-zA-Z]{2,}(/[\w/#.-]*)?$', text.strip()))
    except re.error:
        return False


def has_abbreviation_before(text: str, pos: int) -> bool:
    """Check if the word ending at `pos` is an abbreviation like EE.UU. or exp."""
    try:
        before = text[:pos].rstrip()
        m = re.search(r'([A-Za-zÁÉÍÓÚáéíóúñÑ.]+)$', before)
        if not m:
            return False
        word = m.group(1).rstrip('.')
        if not word:
            return False
        # All-uppercase short word (EE, UU, USA, etc.)
        if len(word) <= 5 and word.isupper():
            return True
        # Common abbreviations (lowercase or mixed)
        common = {'exp', 'tel', 'etc', 'ej', 'pág', 'dr', 'dra', 'sr', 'sra',
                  'ud', 'vd', 'núm', 'vol', 'av', 'prof', 'ilmo', 'ilma',
                  'n', 's', 'p', 'cap', 'tomo', 'ed'}
        if word.lower() in common:
            return True
        return False
    except Exception:
        # Si algo falla al analizar, asumimos que NO es abreviatura
        return False


def _is_skippable(text: str) -> bool:
    """Devuelve True si el texto no debe ser modificado."""
    stripped = text.strip()
    return (
        looks_like_email(stripped)
        or looks_like_url(stripped)
        or looks_like_domain(stripped)
        or stripped == 'n8n'
    )


def fix_capitalization(text: str) -> str:
    """Apply capitalization rules to visible text."""
    try:
        if _is_skippable(text):
            return text
    except Exception:
        return text  # Si algo falla, devolvemos el texto original

    result = text

    # 1. Capitalize after period + space (skip abbreviations)
    try:
        def cap_after_period(m):
            try:
                if has_abbreviation_before(result, m.start()):
                    return m.group(0)
            except Exception:
                pass
            return m.group(0)[:-1] + m.group(1).upper()

        result = re.sub(
            r'(?<=[.!?])\s+([a-záéíóúñ])',
            cap_after_period,
            result,
        )
    except re.error as exc:
        print(f"  ⚠ [regex periodo] {exc}")

    # 2. Capitalize after colon + space
    try:
        result = re.sub(
            r'(?<=:)\s+([a-záéíóúñ])',
            lambda m: m.group(0)[:-1] + m.group(1).upper(),
            result,
        )
    except re.error as exc:
        print(f"  ⚠ [regex colon] {exc}")

    return result


class CapFixer(HTMLParser):
    """Parseador HTML que corrige mayúsculas solo en texto visible."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.in_script_style = False
        self.in_code = False

    def handle_starttag(self, tag, attrs):
        self.out.append(self.get_starttag_text())
        if tag in ("script", "style"):
            self.in_script_style = True
        if tag in ("pre", "code"):
            self.in_code = True

    def handle_startendtag(self, tag, attrs):
        self.out.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.in_script_style = False
        if tag in ("pre", "code"):
            self.in_code = False
        self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if self.in_script_style or self.in_code:
            self.out.append(data)
        else:
            try:
                self.out.append(fix_capitalization(data))
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
    parser = CapFixer()
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

    summarize(results)


if __name__ == "__main__":
    main()