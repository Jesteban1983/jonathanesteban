#!/usr/bin/env bash
# Genera la imagen de portada para un blog EXISTENTE que quedó sin imagen.
# Uso: generate-missing-blog-image.sh "<slug>" "<tema>" "<descripción de escena en español>"
set -uo pipefail

SLUG="$1"
TOPIC="$2"
SCENE="$3"

cd /home/taisu/IA-ENGINEERING-LAB/08-proyectos/it-support-portfolio/astro-portfolio

echo "=== Generando imagen para: $SLUG ==="
echo "Tema: $TOPIC"

# Paso 1: Refinar el prompt con Groq
echo "── Paso 1/2: Refinando prompt con Groq…"
PROMPT_FILE=".blog-pipeline-tmp/prompt_${SLUG}.txt"
mkdir -p .blog-pipeline-tmp
python3 scripts/refine-image-prompt.py --topic "$TOPIC" --scene "$SCENE" --output "$PROMPT_FILE"
if [ ! -s "$PROMPT_FILE" ]; then
  echo "ERROR: no se obtuvo prompt refinado" >&2
  exit 1
fi
echo "Prompt refinado OK (primeros 120 chars):"
head -c 120 "$PROMPT_FILE"
echo ""
echo ""

# Paso 2: Generar imagen con DeepInfra FLUX
echo "── Paso 2/2: Generando imagen con DeepInfra FLUX…"
python3 scripts/generate_blog_image.py --slug "$SLUG" --scene "$(cat "$PROMPT_FILE")" --provider deepinfra
RC=$?
if [ $RC -ne 0 ] || [ ! -f "public/assets/img/blog/${SLUG}.png" ]; then
  echo "ERROR: la generación falló (rc=$RC)" >&2
  exit 1
fi

ls -la "public/assets/img/blog/${SLUG}.png"
echo "✅ Imagen creada para $SLUG"