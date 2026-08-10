#!/usr/bin/env python3
"""Corrige mayúsculas después de punto y dos puntos en textos HTML.

Usa HTMLParser para tocar SOLO nodos de texto (no script/style).
Ignora emails, URLs, dominios, n8n, abreviaturas y código preformateado.
NO aplica regla de "primer carácter" para evitar dañar etiquetas inline.
"""
import os
import re
from html.parser import HTMLParser


def looks_like_email(text: str) -> bool:
    return bool(re.match(r'^[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}$', text.strip()))


def looks_like_url(text: str) -> bool:
    return bool(re.match(r'^https?://', text.strip()))


def looks_like_domain(text: str) -> bool:
    return bool(re.match(r'^[\w-]+\.[a-zA-Z]{2,}(/[\w/#.-]*)?$', text.strip()))


def has_abbreviation_before(text: str, pos: int) -> bool:
    """Check if the word ending at `pos` is an abbreviation like EE.UU. or exp."""
    before = text[:pos].rstrip()
    # Get the last "word" considering dots as part of the word
    # Find the last alphanumeric-or-dot sequence
    m = re.search(r'([A-Za-zÁÉÍÓÚáéíóúñÑ.]+)$', before)
    if not m:
        return False
    word = m.group(1).rstrip('.')
    if not word:
        return False
    # Case: all-uppercase short word (EE, UU, USA, etc.)
    if len(word) <= 5 and word.isupper():
        return True
    # Common abbreviations (lowercase or mixed)
    common = {'exp', 'tel', 'etc', 'ej', 'pág', 'dr', 'dra', 'sr', 'sra',
              'ud', 'vd', 'núm', 'vol', 'av', 'prof', 'ilmo', 'ilma',
              'n', 's', 'p', 'cap', 'tomo', 'ed'}
    if word.lower() in common:
        return True
    return False


def fix_capitalization(text: str) -> str:
    """Apply capitalization rules to visible text."""
    stripped = text.strip()
    # Skip emails, URLs, domains, brand names
    if (looks_like_email(stripped) or looks_like_url(stripped)
            or looks_like_domain(stripped) or stripped == 'n8n'):
        return text

    result = text

    # 1. Capitalize after period + space (skip abbreviations)
    def cap_after_period(m):
        if has_abbreviation_before(result, m.start()):
            return m.group(0)  # Don't change
        return m.group(0)[:-1] + m.group(1).upper()

    result = re.sub(
        r'(?<=[.!?])\s+([a-záéíóúñ])',
        cap_after_period,
        result,
    )

    # 2. Capitalize after colon + space
    result = re.sub(
        r'(?<=:)\s+([a-záéíóúñ])',
        lambda m: m.group(0)[:-1] + m.group(1).upper(),
        result,
    )

    # NOTE: No "first character" rule — HTMLParser splits text at inline tags,
    # so "impulsan" inside <em>impulsan</em> would be wrongly capitalized.

    return result


class CapFixer(HTMLParser):
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
            self.out.append(fix_capitalization(data))

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


def main():
    root = "site"
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(".html"):
                html_files.append(os.path.join(dirpath, f))
    html_files.sort()

    # Show dry-run
    print("=" * 70)
    print("DRY RUN - Cambios propuestos")
    print("=" * 70)
    total_changes = 0
    for fp in html_files:
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
        parser = CapFixer()
        parser.feed(content)
        parser.close()
        new_content = parser.result()
        if new_content != content:
            rel = os.path.relpath(fp)
            # Show only changed lines
            old_lines = content.split('\n')
            new_lines = new_content.split('\n')
            for i, (ol, nl) in enumerate(zip(old_lines, new_lines)):
                if ol != nl:
                    print(f"\n{rel}:L{i+1}")
                    print(f"  - {ol.strip()}")
                    print(f"  + {nl.strip()}")
                    total_changes += 1

    print(f"\n--- Total cambios: {total_changes} ---")

    if total_changes == 0:
        print("No hay cambios que aplicar.")
        return

    print("\n" + "=" * 70)
    confirm = input("¿Aplicar cambios? (s/N): ").strip().lower()
    if confirm != 's':
        print("Cancelado por el usuario.")
        return

    # Apply
    print("\n" + "=" * 70)
    print("APLICANDO CAMBIOS")
    print("=" * 70)
    fixed = []
    for fp in html_files:
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
        parser = CapFixer()
        parser.feed(content)
        parser.close()
        new_content = parser.result()
        if new_content != content:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_content)
            fixed.append(fp)
            print(f"✓ {os.path.relpath(fp)}")
    print(f"\nTotal archivos modificados: {len(fixed)}")


if __name__ == "__main__":
    main()