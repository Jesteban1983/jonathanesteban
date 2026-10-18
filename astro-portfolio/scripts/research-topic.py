#!/usr/bin/env python3
"""
research-topic.py — Fase de investigación previa a la redacción del blog.

Usa DeepSeek V4 (vía LiteLLM) para investigar un tema antes de redactar el
artículo: recopila datos verificables, versiones vigentes de software/hardware,
fuentes potenciales y errores comunes. El resultado alimenta el prompt del
generador de artículos (generate-blog-post.py), evitando que el redactor
invente datos.

Uso:
  python3 research-topic.py --topic "PC lento causas" --keyword "pc lento" \
      --intencion "guía práctica" [--output research.json]

Salida:
  - Por defecto imprime el research brief como JSON (raw) por stdout.
  - Con --output <file> escribe el JSON además de imprimirlo.
  - Con --pretty imprime una versión legible del brief a stderr.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Reutilizar la invocación LiteLLM de generate-blog-post (patrón probado).
# El nombre de archivo lleva guiones, así que se carga vía importlib.
import importlib.util  # noqa: E402

_GENERATOR = Path(__file__).resolve().parent / "generate-blog-post.py"


def _load_invoke_litellm():
    spec = importlib.util.spec_from_file_location("generate_blog_post", _GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.invoke_litellm


invoke_litellm = _load_invoke_litellm()

RESEARCH_SYSTEM_PROMPT = """# ROL
Eres un investigador técnico riguroso para el blog de soporte informático de
Jonathan Esteban (Barcelona). Antes de que un redactor escriba un artículo, tú
investigas el tema y devuelves un brief con los datos verificables.

# REGLAS DE INVESTIGACIÓN (inquebrantables)
1. Solo incluye datos que puedas afirmar con razonable seguridad a partir de tu
conocimiento. Si no estás seguro de una cifra o versión, márcala con "(verificar)".
2. NO inventes estadísticas, estudios, citas ni URLs falsas. Si citas una fuente,
usa sitios oficiales conocidos (Microsoft, Apple, Google, fabricantes, prensa
técnica reconocida) y descríbela por nombre, sin fabricar URLs exactas salvo las
bien conocidas.
3. Indica la versión vigente conocida de cualquier software/OS/hardware mencionado.
4. Separa claramente: hechos consolidados vs. suposiciones a verificar.
5. Prioriza información práctica y actual que un técnico de soporte pueda usar.

# ESTRUCTURA DEL BRIEF (devuelve SOLO JSON válido, sin markdown wrapper)
{
  "tema": "",
  "resumen": "2-3 frases con la idea central y el enfoque recomendado",
  "datosClave": ["dato 1", "dato 2", "..."],
  "versionesVigentes": "cualquier versión actual relevante de software/hardware, o '' si no aplica",
  "especificacionesRelevantes": ["especificación o requisito relevante", "..."],
  "fuentesPotenciales": [{"sitio": "nombre del sitio", "tipo": "documentación oficial / prensa / foro"}],
  "erroresComunes": ["error o mito frecuente que el artículo debe aclarar", "..."],
  "pasosPracticos": ["paso concreto", "..."],
  "riesgoTecnico": "advertencia de seguridad/daño si aplica, o ''",
  "enfoqueRecomendado": "ángulo editorial sugerido en 2-3 frases"
}

# EXTENSIÓN
Brief conciso y útil: 350-600 palabras en total. En español de España."""


def build_user_prompt(topic: str, keyword: str, intencion: str) -> str:
    return f"""# Tema a investigar: {topic}
# Palabra clave principal: {keyword}
# Intención de búsqueda: {intencion}
# Año actual: {datetime.now().year}

Investiga este tema como haría un técnico de soporte informático de Barcelona
antes de escribir una guía para clientes no técnicos. Devuelve SOLO el JSON del
brief, sin texto adicional."""


def main() -> int:
    parser = argparse.ArgumentParser(description="Investiga un tema con DeepSeek V4 antes de redactar")
    parser.add_argument("--topic", required=True, help="Tema a investigar")
    parser.add_argument("--keyword", default="", help="Palabra clave principal")
    parser.add_argument("--intencion", default="informativa", help="Intención de búsqueda")
    parser.add_argument("--model", default="deepseek-v4", help="Modelo LiteLLM (deepseek-v4)")
    parser.add_argument("--output", type=Path, help="Archivo donde escribir el brief JSON")
    parser.add_argument("--pretty", action="store_true", help="Muestra el brief legible a stderr")
    args = parser.parse_args()

    raw = invoke_litellm(RESEARCH_SYSTEM_PROMPT,
                         build_user_prompt(args.topic, args.keyword, args.intencion),
                         args.model)
    if not raw:
        print(json.dumps({"error": "La investigación no devolvió respuesta"}, ensure_ascii=False))
        return 1

    # Intentar extraer JSON (puede venir envuelto o con texto)
    data = None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        start, end = raw.find("{"), raw.rfind("}")
        if start != -1 and end > start:
            try:
                data = json.loads(raw[start:end + 1])
            except json.JSONDecodeError:
                data = None

    if not isinstance(data, dict):
        # Fallback: guardar raw como texto y avisar
        data = {"error": "No se pudo parsear el brief como JSON", "raw": raw[:2000]}

    if args.pretty:
        print("── Research Brief ─────────────────────────", file=sys.stderr)
        for key, value in data.items():
            print(f"\n▶ {key}:", file=sys.stderr)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        print(f"  - {json.dumps(item, ensure_ascii=False)}", file=sys.stderr)
                    else:
                        print(f"  - {item}", file=sys.stderr)
            else:
                print(f"  {value}", file=sys.stderr)

    if args.output:
        args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"ok": True, "briefPath": str(args.output)}, ensure_ascii=False))
    else:
        print(json.dumps(data, ensure_ascii=False))

    # Log de errores para diagnóstico
    if data.get("error"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())