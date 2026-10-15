#!/bin/bash
# blog-workflow.sh — Script llamado por n8n (Execute Command) para generar
# un artículo del blog de principio a fin.
#
# Modos:
#   ./scripts/blog-workflow.sh generate          # Siguiente tema pendiente → draft
#   ./scripts/blog-workflow.sh generate --image   # Lo mismo + generar imagen
#   ./scripts/blog-workflow.sh publish <slug>    # Publicar un draft específico
#   ./scripts/blog-workflow.sh publish-all       # Publicar todos los drafts
#   ./scripts/blog-workflow.sh next-topic        # Mostrar el siguiente tema pendiente (JSON)
#   ./scripts/blog-workflow.sh list-drafts       # Lista drafts como JSON
#
# Para llamada desde n8n, se recomienda:
#   ./scripts/blog-workflow.sh next-topic        # → JSON con tema
#   ./scripts/blog-workflow.sh generate           # → JSON con resultado
#   ./scripts/blog-workflow.sh publish-all        # → JSON con resultado

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SCRIPTS_DIR="$PROJECT_DIR/scripts"
TOPIC_BANK="$PROJECT_DIR/blog-topic-bank.csv"
LOG_DIR="$HOME/.nova-logs"
mkdir -p "$LOG_DIR"

GENERATE_SCRIPT="$SCRIPTS_DIR/generate-blog-post.py"
PUBLISH_SCRIPT="$SCRIPTS_DIR/blog-publish.sh"

# ── Colores ──
if [ -t 1 ]; then GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
else GREEN=''; YELLOW=''; RED=''; NC=''
fi

ok()  { echo -e " ${GREEN}✓${NC} $1"; }
warn(){ echo -e " ${YELLOW}⚠${NC} $1"; }
fail(){ echo -e " ${RED}✖${NC} $1"; }

# ── Obtener siguiente tema pendiente ──
next_topic() {
    if [ ! -f "$TOPIC_BANK" ]; then
        echo '{"error":"No existe topic bank","file":"'"$TOPIC_BANK"'"}'
        return 1
    fi

    # Usar Python para parsear CSV correctamente (con campos entrecomillados)
    python3 -c "
import csv, json, sys

with open('$TOPIC_BANK') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, start=2):
        if row['estado'].strip().lower() == 'pendiente':
            out = {
                'tema': row['tema'],
                'keyword': row['keyword'],
                'keywordIntencion': row.get('keyword_intencion', ''),
                'intencion': row['intencion'],
                'estado': row['estado'],
                'linea': i
            }
            print(json.dumps(out, ensure_ascii=False))
            sys.exit(0)
    print(json.dumps({'error': 'No hay temas pendientes'}))
    sys.exit(1)
" 2>/dev/null
}

# ── Generar artículo desde el siguiente tema ──
generate() {
    local with_image="${1:-}"

    local topic_json
    topic_json=$(next_topic)
    local exit_code=$?
    echo "$topic_json" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(1) if d.get('error') else None" 2>/dev/null || {
        echo "$topic_json"
        return 1
    }

    local tema keyword intencion
    tema=$(echo "$topic_json" | python3 -c "import sys,json; print(json.load(sys.stdin)['tema'])")
    keyword=$(echo "$topic_json" | python3 -c "import sys,json; print(json.load(sys.stdin)['keyword'])")
    intencion=$(echo "$topic_json" | python3 -c "import sys,json; print(json.load(sys.stdin)['intencion'])")

    echo "📝 Generando: $tema (keyword: $keyword, intención: $intencion)" >&2

    local cmd=("python3" "$GENERATE_SCRIPT" "--topic" "$tema" "--keyword" "$keyword" "--intencion" "$intencion")
    if [ "$with_image" = "--image" ]; then
        cmd+=("--with-image")
    fi

    local result
    result=$("${cmd[@]}" 2>/dev/null)
    local exit_code=$?

    if [ $exit_code -ne 0 ]; then
        echo "{\"error\":\"Fallo al generar\",\"exitCode\":$exit_code,\"tema\":\"$tema\"}"
        return 1
    fi

    # Devolver el JSON del generador
    echo "$result"
}

# ── Listar drafts como JSON ──
list_drafts_json() {
    local drafts_dir="$PROJECT_DIR/src/content/blog/drafts"
    if [ ! -d "$drafts_dir" ]; then
        echo '{"drafts":[]}'
        return 0
    fi

    python3 "$SCRIPT_DIR/list-drafts.py" "$drafts_dir"
}

# ── main ──
action="${1:-help}"
case "$action" in
    next-topic|next)
        next_topic
        ;;
    generate|gen)
        generate "${2:-}"
        ;;
    publish)
        if [ -z "${2:-}" ]; then
            echo '{"error":"Uso: blog-workflow.sh publish <slug>"}'
            exit 1
        fi
        bash "$PUBLISH_SCRIPT" "$2" 2>&1 | tail -1
        ;;
    publish-all|publish_all)
        bash "$PUBLISH_SCRIPT" 2>&1 | tail -1
        ;;
    list-drafts|drafts)
        list_drafts_json
        ;;
    help|--help|-h)
        echo "Uso: blog-workflow.sh <comando> [opciones]"
        echo ""
        echo "  next-topic      Mostrar el siguiente tema pendiente (JSON)"
        echo "  generate        Generar draft desde el siguiente tema"
        echo "  generate --image  Generar draft + imagen"
        echo "  publish <slug>  Publicar un draft"
        echo "  publish-all     Publicar todos los drafts"
        echo "  list-drafts     Listar drafts (JSON)"
        echo ""
        echo "Usar en n8n con nodo 'Execute Command' para integrar el flujo."
        ;;
    *)
        echo '{"error":"Comando desconocido","accion":"'"$action"'"}'
        exit 1
        ;;
esac