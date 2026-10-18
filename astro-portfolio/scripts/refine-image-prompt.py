#!/usr/bin/env python3
"""
refine-image-prompt.py — Refina y estructura el prompt de imagen con Groq.

Paso 1 del pipeline de imagen: toma un prompt de escena inicial (el que genera
el redactor con DeepSeek) y lo transforma en un prompt altamente detallado,
estructurado y optimizado para el modelo FLUX de DeepInfra. El objetivo es que
la imagen no se confunda: se especifica composición, estilo, iluminación,
paleta, ambiente, restricciones y ausencia de texto.

Uso:
  python3 refine-image-prompt.py --topic "PC lento causas" --scene "un técnico ..." \
      [--output prompt.txt] [--pretty]

  # Si solo se pasa --topic, usa un prompt de escena por defecto
  python3 refine-image-prompt.py --topic "disco duro fallando"

Salida:
  - Por defecto imprime el prompt refinado por stdout (una línea, bien estructurado).
  - Con --output <file> lo escribe a un archivo además de imprimirlo.
  - Con --pretty imprime el razonamiento de refinamiento a stderr.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import importlib.util

_GENERATOR = Path(__file__).resolve().parent / "generate-blog-post.py"


def _load_invoke_litellm():
    spec = importlib.util.spec_from_file_location("generate_blog_post", _GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.invoke_litellm


invoke_litellm = _load_invoke_litellm()

REFINE_SYSTEM_PROMPT = """# ROL
Eres un director de arte experto en prompts para modelos de imagen FLUX
(black-forest-labs). Tu trabajo: transformar una descripción de escena corta en
un prompt EN INGLÉS, extremadamente detallado y estructurado, que genere una
imagen editorial de blog de soporte informático.

# REGLAS
1. Responde SOLO con el prompt refinado en inglés, sin texto adicional.
2. El prompt debe ser específico y no dejar ambigüedad a la IA (evita que la
imagen "se confunda"): composición, sujeto, vestimenta, entorno, iluminación,
ángulo, lente, paleta de color, estilo fotográfico.
3. PROHIBIDO texto en la imagen: sin letras, palabras, números, logos, marcas,
watermarks. Está explícitamente prohibido.
4. El estilo del blog es: fotografía editorial premium para blog de soporte
técnico, hardware contemporáneo 2026, espacio de trabajo mediterráneo tranquilo,
luz natural suave por la mañana, fotografía de 35mm a full-frame, sujeto nítido,
profundidad de campo sutil. Sujeto principal en los dos tercios derechos.
Espacio negativo limpio y más oscuro a la izquierda para superposición de título.
Sombra azul petróleo profundo (#0D3C46) y un acento pequeño ámbar (#F2A72A).
Realista, elegante, sin desorden.
5. Evita: estilo cartoon, iconografía hacker, hardware obsoleto, glow excesivo,
sobreexposición, objetos deformados, clichés de stock, caras reconocibles de
famosos, cualquier texto.
6. El prompt debe indicar claramente "NO TEXT, NO LETTERS, NO LOGOS,
NO WATERMARKS".
7. Máximo 180 palabras. Idioma: inglés.

# FORMATO
Devuelve el prompt como texto plano en una sola línea (puede tener comas y ;
internos). Sin comillas envolventes, sin JSON, sin markdown."""


def build_user_prompt(topic: str, scene: str) -> str:
    return f"""# Tema del artículo: {topic}
# Descripción de escena inicial (puede estar en español o inglés):
{scene}

Refina esta descripción en un prompt FLUX detallado en inglés siguiendo todas las
reglas. Devuelve SOLO el prompt refinado."""


def _default_scene(topic: str) -> str:
    return (
        "A technician working on a modern computer in a clean Mediterranean "
        f"home office. Topic: {topic}. Warm, calm atmosphere."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Refina un prompt de imagen con Groq para FLUX")
    parser.add_argument("--topic", required=True, help="Tema del artículo")
    parser.add_argument("--scene", default="", help="Descripción de escena inicial")
    parser.add_argument("--output", type=Path, help="Archivo donde escribir el prompt")
    parser.add_argument("--pretty", action="store_true", help="Muestra información a stderr")
    args = parser.parse_args()

    scene = args.scene.strip() or _default_scene(args.topic)

    raw = invoke_litellm(REFINE_SYSTEM_PROMPT,
                         build_user_prompt(args.topic, scene),
                         "groq-fast")
    if not raw:
        print("ERROR: Groq no devolvió prompt refinado", file=sys.stderr)
        return 1

    prompt = raw.strip().strip('"').strip()
    # Limpiar wrappers de markdown si vinieran
    prompt = re.sub(r"^```(?:text|plain)?\s*", "", prompt)
    prompt = re.sub(r"\s*```$", "", prompt)
    # Normalizar saltos de línea a espacio
    prompt = re.sub(r"\s+", " ", prompt).strip()

    if args.pretty:
        print(f"── Prompt refinado (Groq → FLUX) ────────", file=sys.stderr)
        print(json.dumps({"topic": args.topic, "scene": scene, "prompt": prompt[:300]},
                         ensure_ascii=False, indent=2), file=sys.stderr)

    if args.output:
        args.output.write_text(prompt + "\n", encoding="utf-8")

    print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())