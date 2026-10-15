#!/usr/bin/env python3
"""
generate-blog-post.py — Generador de artículos para el blog de soporte IT.
Usa el agente redactor (PROMPT A de BLOG-AUTOMATION.md) vía LiteLLM.

Uso:
  python3 generate-blog-post.py --topic "tema" --keyword "keyword" --intencion "guía práctica"
  
  # Solo generar (modo borrador)
  python3 generate-blog-post.py --topic "PC lento causas" --keyword "pc lento" --intencion "guía práctica"
  
  # Generar con imagen (necesita GEMINI_API_KEY)
  python3 generate-blog-post.py --topic "..." --keyword "..." --intencion "..." --with-image

Salida:
  - Crea archivo en src/content/blog/drafts/<slug>.mdx
  - Crea imagen en public/assets/img/blog/<slug>.png (si --with-image)
  - Devuelve JSON con slug y ruta
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ── paths ─────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONTENT_DIR = PROJECT_ROOT / "src" / "content" / "blog"
DRAFTS_DIR = CONTENT_DIR / "drafts"
PUBLIC_IMG_DIR = PROJECT_ROOT / "public" / "assets" / "img" / "blog"
LLM_INVOKE = Path.home() / "scripts" / "llm-invoke.sh"
GENERATE_IMAGE = SCRIPT_DIR / "generate_blog_image.py"
TOPIC_BANK = PROJECT_ROOT / "blog-topic-bank.csv"
CONFIG_FILE = Path.home() / ".nova-config.json"

# ── sistema prompt (PROMPT A) ─────────────────────────────────────────────
BLOG_STYLE_PROMPT = """# ROL
Eres el redactor técnico del blog de Jonathan Esteban, técnico de soporte
informático en Barcelona. Escribes artículos útiles, verificados y claros para
personas y pequeños negocios que no son técnicos.

# REGLAS DE HONESTIDAD (inquebrantables)
1. Cada dato, cifra, versión de software o norma debe salir de una fuente que HAYAS
   consultado con las herramientas. Si no puedes verificarlo, no lo escribas.
2. Prohibido inventar estadísticas, precios, estudios, citas o URLs.
3. Prohibido hablar de la experiencia de Jonathan con cifras ("X años de experiencia",
   "cientos de clientes") ni atribuirle certificaciones. Nada de "garantizado al 100 %",
   "el mejor", "siempre", "nunca" sin sustento.
4. Si mencionas software o hardware, comprueba cuál es la versión vigente antes
   de afirmarlo. No des por "nuevo" lo que ya no lo es.
5. No des instrucciones que puedan dañar equipos, vulnerar cuentas ajenas o saltarse
   licencias. En seguridad, solo defensa y buenas prácticas.
6. Si el tema exige un profesional (salud, asesoría legal, reparación eléctrica), dilo.

# TONO
Español de España, tuteo, cercano y directo. Explica cualquier término técnico la primera
vez que aparece. Frases cortas. Sin relleno, sin exageraciones, sin tecnicismos
innecesarios. Menciona Barcelona solo 1 o 2 veces y solo cuando aporte (p. ej. el CTA).

# ESTRUCTURA DEL ARTÍCULO (en este orden, respeta las cabeceras ##)
1. Introducción (80–120 palabras): el problema que el lector reconoce + qué va a lograr.
2. "## Respuesta rápida" (2–3 frases): la respuesta directa, para quien solo quiere eso.
3. Desarrollo: entre 3 y 5 secciones H2 (con H3 solo si hace falta).
   - Cada H2 empieza con una frase que responde la pregunta de esa sección.
   - Procedimientos: lista numerada, un paso = una acción.
   - Enumeraciones: lista con viñetas, mínimo 3 elementos, redacción paralela.
4. Tabla APA: solo si una comparación o un dato ordenado aporta de verdad. Máximo 1.
5. "## Errores comunes" o "## Cuándo conviene llamar a un técnico" (honesto, sin presionar).
6. "## Preguntas frecuentes" con 3 preguntas en **negrita** y respuesta aparte.
7. "## Conclusión" + CTA (2–3 frases). Invita a contactar.
8. "## Referencias" — **OBLIGATORIO**. Mínimo 2 referencias en APA 7 con URL.
Extensión del cuerpo (sin incluir frontmatter): 900–1.300 palabras.

# FORMATO DEL TEXTO
- Markdown/MDX. Párrafos de 2 a 5 frases; una idea por párrafo.
- Sin negritas decorativas: negrita solo para el término clave de cada sección.
- Sin emojis, sin MAYÚSCULAS enfáticas, sin signos de exclamación.
- Los puntos de una lista terminan igual (todos con punto o ninguno).
- Números: coma decimal (3,5); separador de miles con punto desde 10.000.

# TABLAS APA 7
Usa SIEMPRE este componente, con una línea en blanco antes y después:

<TablaAPA numero="1" titulo="Comparación de [lo comparado] en [contexto]" nota="Elaboración propia a partir de Autor (año).">

| Criterio | Opción A | Opción B |
|---|---|---|
| Dato | valor | valor |

</TablaAPA>

# CITAS Y REFERENCIAS (APA 7)
- En el texto: (Autor, año) o Autor (año).
- Sección final "Referencias": una por línea, orden alfabético, con URL activa.
  Formato: Autor. (Año, día mes). *Título en cursiva*. Sitio. URL
- Mínimo 2 referencias, preferiblemente fuentes oficiales.

# FAQ FORMATO
Cada pregunta en su propio párrafo, en **negrita**; la respuesta debajo, en un párrafo independiente (nunca en la misma línea).

# SALIDA
Devuelve SOLO este JSON válido (sin texto antes ni después, sin bloques de código, sin markdown wrapper):
{
  "slug": "",
  "title": "",
  "metaDescription": "",
  "keywordPrincipal": "",
  "keywordsSecundarias": [],
  "categoria": "",
  "tiempoLectura": "",
  "resumenCorreo": "2-3 frases para el correo de aprobación",
  "markdown": "cuerpo completo (sin frontmatter y sin H1)",
  "referencias": [{"apa": "", "url": ""}],
  "imagePrompt": "escena concreta en inglés, sin texto en la imagen",
  "imageAlt": "descripción accesible 100-125 caracteres, en español",
  "autoverificacion": {
    "datosVerificados": true,
    "fuentesConsultadas": 0,
    "palabras": 0,
    "tablaIncluida": false
  }
}"""


def slugify(text: str) -> str:
    """Convierte texto a slug: minúsculas, sin tildes, guiones."""
    text = text.lower()
    text = re.sub(r'[áàäâ]', 'a', text)
    text = re.sub(r'[éèëê]', 'e', text)
    text = re.sub(r'[íìïî]', 'i', text)
    text = re.sub(r'[óòöô]', 'o', text)
    text = re.sub(r'[úùüû]', 'u', text)
    text = re.sub(r'[ñ]', 'n', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    # acortar a max 6 palabras aprox
    parts = text.split('-')
    if len(parts) > 6:
        text = '-'.join(parts[:6])
    return text


def check_dependencies() -> bool:
    """Verifica que las herramientas necesarias están disponibles."""
    if not LLM_INVOKE.is_file():
        print(f"❌ No encontrado: {LLM_INVOKE}", file=sys.stderr)
        return False
    return True


def invoke_litellm(system_prompt: str, user_prompt: str, model: str = "deepseek-v4") -> str | None:
    """Invoca LiteLLM directamente con max_tokens=4096 (sin el límite 2000 de llm-invoke)."""
    # Cargar config
    try:
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error cargando ~/.nova-config.json: {e}", file=sys.stderr)
        return None

    provider_url = cfg['litellm']['provider']
    full_model = cfg['litellm']['models'].get(model, '')
    if not full_model:
        available = ', '.join(cfg['litellm']['models'].keys())
        print(f"❌ Modelo '{model}' no encontrado. Disponibles: {available}", file=sys.stderr)
        return None

    # Obtener API key
    try:
        sys.path.insert(0, str(Path.home() / "scripts"))
        from nova_env import get_secret  # type: ignore[import-untyped]
        api_key = get_secret('LITELLM_MASTER_KEY')
    except Exception as e:
        print(f"❌ Error obteniendo API key: {e}", file=sys.stderr)
        return None

    data = {
        "model": full_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 8192,
    }

    req = urllib.request.Request(
        f"{provider_url}/chat/completions",
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        method="POST"
    )

    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                result = json.loads(resp.read())
                content = result["choices"][0]["message"]["content"]
                if content is None or content.strip() == "" or content.strip() == "None":
                    if attempt == 0:
                        print(f"[retry] modelo devolvió vacío — reintentando...", file=sys.stderr)
                        continue
                    print("❌ Modelo devolvió vacío tras reintento", file=sys.stderr)
                    return None
                return content.strip()
        except urllib.error.HTTPError as e:
            if attempt == 0 and e.code in (429, 503, 502):
                print(f"[retry] HTTP {e.code} — reintentando...", file=sys.stderr)
                continue
            print(f"ERROR HTTP {e.code}: {e.read().decode()[:500]}", file=sys.stderr)
            return None
        except (urllib.error.URLError, OSError) as e:
            print(f"❌ Error de conexión: {e}", file=sys.stderr)
            return None

    return None


def validate_article(data: dict) -> list[str]:
    """Valida el artículo según las reglas del nodo 5. Devuelve lista de errores."""
    errors = []

    # 1. Campos requeridos
    required = ["slug", "title", "metaDescription", "markdown"]
    for field in required:
        if field not in data or not data[field]:
            errors.append(f"Campo obligatorio '{field}' falta o está vacío")

    if errors:
        return errors

    # 2. title ≤ 70 caracteres (SEO: máximo recomendado)
    if len(data["title"]) > 70:
        errors.append(f"Title demasiado largo: {len(data['title'])} chars (máx 60)")

    # 3. metaDescription entre 125-180
    meta_len = len(data["metaDescription"])
    if meta_len < 125 or meta_len > 180:
        errors.append(f"metaDescription fuera de rango: {meta_len} chars (debe 125-180)")

    # 4. Markdown sin H1
    if re.search(r'(?<!#)# ', data["markdown"]):
        errors.append("El markdown contiene H1 ('# ')")

    # 5. Entre 800-2000 palabras (rango amplio para artículos completos)
    word_count = len(data["markdown"].split())
    if word_count < 800:
        errors.append(f"Demasiado corto: {word_count} palabras (mín 800)")

    # 6. Mínimo 2 H2
    h2_count = len(re.findall(r'^##\s', data["markdown"], re.MULTILINE))
    if h2_count < 2:
        errors.append(f"Muy pocos H2: {h2_count} (mín 2)")

    # 7. Secciones requeridas
    if "Preguntas frecuentes" not in data["markdown"]:
        errors.append("Falta sección 'Preguntas frecuentes'")
    if "Referencia" not in data["markdown"]:  # "Referencias" o "Referencia"
        errors.append("Falta sección 'Referencias'")

    return errors


def generate_image(slug: str, scene_prompt: str) -> bool:
    """Genera imagen para el artículo usando el generador compartido."""
    if not GENERATE_IMAGE.is_file():
        print(f"⚠️ No encontrado generador de imágenes: {GENERATE_IMAGE}", file=sys.stderr)
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(GENERATE_IMAGE), "--slug", slug, "--scene", scene_prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            print(f"✅ Imagen generada: {slug}.png", file=sys.stderr)
            return True
        else:
            print(f"❌ Fallo al generar imagen: {result.stderr[:500]}", file=sys.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("⚠️ Tiempo agotado generando imagen", file=sys.stderr)
        return False


def write_draft(data: dict) -> Path | None:
    """Escribe el archivo MDX del borrador."""
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_IMG_DIR.mkdir(parents=True, exist_ok=True)

    slug = data["slug"]
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    # Tags por categoría
    category = data.get("categoria", "general")
    tag_map = {
        "guía práctica": ["guía práctica", "mantenimiento", "PC"],
        "guía": ["guía", "PC"],
        "informativa": ["blog", "consejos"],
        "comparativa": ["comparativa", "guía práctica"],
        "lista": ["lista", "consejos"],
    }
    tags = tag_map.get(category.lower(), ["blog"])

    frontmatter = f"""---
title: "{data['title']}"
description: "{data['metaDescription']}"
pubDate: {date_str}
heroImage: "/assets/img/blog/{slug}.png"
tags: {json.dumps(tags)}
author: "Jonathan Esteban"
draft: true
---

import TablaAPA from '../../components/TablaAPA.astro';

"""
    content = frontmatter + data["markdown"]

    # Asegurar saltos de línea final
    if not content.endswith("\n"):
        content += "\n"

    out_path = DRAFTS_DIR / f"{slug}.mdx"
    out_path.write_text(content, encoding="utf-8")
    return out_path


def _repair_json(raw: str) -> str:
    """Repara JSON de LLM: newlines literales dentro de strings → \\n."""
    result = []
    in_string = False
    escaped = False
    for ch in raw:
        if escaped:
            result.append(ch)
            escaped = False
            continue
        if ch == '\\' and in_string:
            result.append(ch)
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string
            result.append(ch)
            continue
        if in_string and ch in '\n\r':
            result.append('\\n')
            continue
        result.append(ch)
    return ''.join(result)


def _extract_json_block(raw: str) -> str | None:
    """Extrae el JSON más externo entre llaves, tolerando markdown alrededor."""
    # Buscar el primer { y el último }
    start = raw.find('{')
    end = raw.rfind('}')
    if start == -1 or end == -1 or end <= start:
        return None
    return raw[start:end + 1]


def parse_json_output(raw: str) -> dict | None:
    """Parsea el JSON de la respuesta del LLM con tolerancia a errores."""
    # 1. Intentar parseo directo
    for candidate in (raw, _extract_json_block(raw)):
        if candidate is None:
            continue
        # 1a. Directo
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass
        # 1b. Reparar newlines en strings y reintentar
        try:
            return json.loads(_repair_json(candidate))
        except json.JSONDecodeError:
            pass

    # 2. Buscar JSON entre bloques de código
    for m in re.finditer(r'```(?:json)?\s*\n?(.*?)```', raw, re.DOTALL):
        block = m.group(1)
        for fn in (json.loads, lambda x: json.loads(_repair_json(x))):
            try:
                return fn(block)
            except json.JSONDecodeError:
                continue

    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera artículo para el blog")
    parser.add_argument("--topic", required=True, help="Tema del artículo")
    parser.add_argument("--keyword", default="", help="Palabra clave principal")
    parser.add_argument("--intencion", default="informativa",
                        choices=["informativa", "guía práctica", "guía", "comparativa", "lista"],
                        help="Intención del artículo")
    parser.add_argument("--model", default="deepseek-v4",
                        help="Modelo LiteLLM (deepseek-v4, groq-fast, deepseek-r1)")
    parser.add_argument("--with-image", action="store_true",
                        help="Generar imagen para el artículo")
    parser.add_argument("--publish", action="store_true",
                        help="Publicar directamente (sin pasar por drafts)")
    parser.add_argument("--force", action="store_true",
                        help="Forzar publicación aunque falle validación")

    args = parser.parse_args()

    if not check_dependencies():
        return 2

    print(f"📝 Generando artículo: {args.topic}", file=sys.stderr)
    print(f"   Modelo: {args.model} | Intención: {args.intencion}", file=sys.stderr)

    # Construir user prompt
    existing = []
    if CONTENT_DIR.exists():
        existing = [f.stem for f in CONTENT_DIR.glob("*.mdx") if f.stem != "drafts"]
    existing_str = ", ".join(existing) if existing else "ninguno aún"

    user_prompt = f"""# Tema: {args.topic}
# Palabra clave principal: {args.keyword}
# Intención de búsqueda: {args.intencion}
# Año actual: {datetime.now().year}
# Artículos ya publicados (evita repetir enfoque): {existing_str}

Genera el artículo completo siguiendo las instrucciones exactamente. Devuelve SOLO el JSON."""
    # ── Invocar LLM ───────────────────────────────────────────────────────
    raw_output = invoke_litellm(BLOG_STYLE_PROMPT, user_prompt, args.model)
    if not raw_output:
        return 1

    # ── Parsear y validar ─────────────────────────────────────────────────
    data = parse_json_output(raw_output)
    if not data:
        print("❌ No se pudo parsear el JSON de la respuesta", file=sys.stderr)
        print("--- Respuesta cruda (primeros 300 chars) ---", file=sys.stderr)
        print(raw_output[:300], file=sys.stderr)
        return 1

    if not args.force:
        errors = validate_article(data)
        if errors:
            print("❌ Validación fallida:", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
            print("\nUsa --force para publicar de todas formas.", file=sys.stderr)
            return 1
    else:
        print("⚠️  --force: saltando validación", file=sys.stderr)

    # ── Slug ──────────────────────────────────────────────────────────────
    slug = data.get("slug", "")
    if not slug or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        slug = slugify(args.topic)
        data["slug"] = slug
        print(f"   Slug generado: {slug}", file=sys.stderr)

    # ── Escribir borrador ─────────────────────────────────────────────────
    out_path = write_draft(data)
    print(f"✅ Borrador escrito: {out_path}", file=sys.stderr)

    # ── Generar imagen (opcional) ─────────────────────────────────────────
    if args.with_image:
        scene = data.get("imagePrompt", f"Blog illustration about {args.topic}")
        print(f"   Generando imagen...", file=sys.stderr)
        generate_image(slug, scene)
    
    # ── Si publish, mover a producción ────────────────────────────────────
    if args.publish:
        pub_path = CONTENT_DIR / f"{slug}.mdx"
        if out_path.exists():
            import shutil
            shutil.move(str(out_path), str(pub_path))
            print(f"✅ Publicado: {pub_path}", file=sys.stderr)
            data["published_path"] = str(pub_path)

    # ── Resultado JSON ────────────────────────────────────────────────────
    result = {
        "slug": slug,
        "title": data.get("title", ""),
        "metaDescription": data.get("metaDescription", ""),
        "keywords": [data.get("keywordPrincipal", args.keyword)],
        "wordCount": len(data.get("markdown", "").split()),
        "draftPath": str(out_path),
        "imagePrompt": data.get("imagePrompt", ""),
    }
    if args.publish:
        result["publishedPath"] = str(pub_path)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())