#!/usr/bin/env python3
"""update-topic-bank.py — Marca/desmarca un tema en blog-topic-bank.csv
basándose en el título del artículo.

Uso:
  python3 update-topic-bank.py <mdx_file> <topic_bank_csv>     # marcar como publicado
  python3 update-topic-bank.py --undo <mdx_file> <topic_bank_csv>  # revertir a pendiente
"""

import csv
import re
import sys
from typing import Optional


def get_title_from_mdx(mdx_path: str) -> Optional[str]:
    """Extrae el campo 'title:' del frontmatter de un archivo .mdx"""
    with open(mdx_path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r'^title:\s*["\']?(.+?)["\']?\s*$', line)
            if m:
                title = m.group(1).strip().rstrip(",").strip("\"'")
                return title
    return None


def update_estado(csv_path: str, title: str, new_estado: str) -> bool:
    """Busca 'tema' en CSV (coincidencia parcial: el tema CSV debe estar
    contenido en el título del MDX) y cambia su estado."""
    rows: list[dict] = []
    fieldnames: list[str] = []
    found = False

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            tema = (row.get("tema", "") or "").strip("\"' ")
            estado = (row.get("estado", "") or "").strip("\"' ")
            # Coincidencia parcial: si el tema CSV está contenido en el título del MDX
            if tema and tema in title and estado != new_estado:
                row["estado"] = new_estado
                found = True
            rows.append(row)

    if not found:
        return False

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return True


def main():
    args = sys.argv[1:]

    undo = False
    if args and args[0] == "--undo":
        undo = True
        args = args[1:]

    if len(args) < 2:
        print("Uso: update-topic-bank.py [--undo] <mdx_file> <topic_bank_csv>",
              file=sys.stderr)
        sys.exit(1)

    mdx_path, csv_path = args[0], args[1]

    title = get_title_from_mdx(mdx_path)
    if not title:
        print("ERROR: No se pudo extraer título del MDX", file=sys.stderr)
        sys.exit(2)

    new_estado = "pendiente" if undo else "publicado"
    if update_estado(csv_path, title, new_estado):
        accion = "revertido a pendiente" if undo else "marcado como publicado"
        print(f"✓ Topic bank: «{title}» → {accion}")
        sys.exit(0)
    else:
        print(f"⚠ No se encontró «{title}» en topic bank, o ya estaba en estado '{new_estado}'",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()