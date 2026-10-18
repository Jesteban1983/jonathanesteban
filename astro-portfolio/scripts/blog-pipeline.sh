#!/bin/bash
# blog-pipeline.sh — Orquestador del pipeline completo de publicación del blog.
#
# Pipeline:
#   1. INVESTIGACIÓN  → DeepSeek V4 investiga el tema (research-topic.py)
#   2. REDACCIÓN      → DeepSeek V4 redacta usando el brief (generate-blog-post.py)
#   3. REFINE PROMPT  → Groq refina el prompt de imagen (refine-image-prompt.py)
#   4. IMAGEN         → DeepInfra/FLUX genera la imagen (generate_blog_image.py)
#   5. APROBACIÓN     → Estado guardado en JSON; Telegram ofrece botones Publicar/Cancelar
#   6. LOOP           → Si Cancelar, genera el siguiente tema y reenvía; Publicar publica
#
# Uso (una fase a la vez para permitir aprobación manual entre medias):
#   ./scripts/blog-pipeline.sh research            # Siguiente tema → research brief JSON
#   ./scripts/blog-pipeline.sh generate            # research brief → draft + imagen
#   ./scripts/blog-pipeline.sh approve <slug>      # Publicar un draft aprobado
#   ./scripts/blog-pipeline.sh run-all             # research + generate de un solo golpe
#   ./scripts/blog-pipeline.sh cancel <slug>       # Descarta draft y marca tema como "descartado"
#   ./scripts/blog-pipeline.sh state               # Muestra el estado del pipeline
#
# Para uso con n8n/Telegram, cada comando devuelve JSON en stdout.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SCRIPTS_DIR="$PROJECT_DIR/scripts"
TOPIC_BANK="$PROJECT_DIR/blog-topic-bank.csv"
STATE_FILE="$PROJECT_DIR/.blog-pipeline-state.json"
WORK_DRAFT_DIR="$PROJECT_DIR/.blog-pipeline-tmp"
LOG_DIR="$HOME/.nova-logs"
mkdir -p "$LOG_DIR" "$WORK_DRAFT_DIR"

RESEARCH_SCRIPT="$SCRIPTS_DIR/research-topic.py"
GENERATE_SCRIPT="$SCRIPTS_DIR/generate-blog-post.py"
REFINE_SCRIPT="$SCRIPTS_DIR/refine-image-prompt.py"
IMAGE_SCRIPT="$SCRIPTS_DIR/generate_blog_image.py"
PUBLISH_SCRIPT="$SCRIPTS_DIR/blog-publish.sh"

# ── Colores ──
if [ -t 1 ]; then GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
else GREEN=''; YELLOW=''; RED=''; NC=''
fi
ok()  { echo -e " ${GREEN}✓${NC} $1"; }
warn(){ echo -e " ${YELLOW}⚠${NC} $1"; }
fail(){ echo -e " ${RED}✖${NC} $1"; }

# ── Siguiente tema pendiente (reutiliza blog-workflow.sh) ──
next_topic() {
    python3 -c "
import csv, json, sys

with open('$TOPIC_BANK') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, start=2):
        if row['estado'].strip().lower() == 'pendiente':
            out = {
                'tema': row['tema'], 'keyword': row['keyword'],
                'keywordIntencion': row.get('keyword_intencion', ''),
                'intencion': row['intencion'], 'estado': row['estado'], 'linea': i
            }
            print(json.dumps(out, ensure_ascii=False))
            sys.exit(0)
    print(json.dumps({'error': 'No hay temas pendientes'}))
    sys.exit(1)
" 2>/dev/null
}

# ── Guardar/leer estado del pipeline ──
get_state() {
    if [ -f "$STATE_FILE" ]; then cat "$STATE_FILE"; else echo '{}'; fi
}
set_state() {
    # set_state '<json>'
    printf '%s' "$1" > "$STATE_FILE"
}

# ── Extraer dato del estado ──
state_get() {
    local key="$1"
    get_state | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('$key',''))"
}

# ── Fase 1+2+3+4: research + generate + imagen, todo de un golpe ──
run_all() {
    local topic_json
    topic_json=$(next_topic)
    local exit_code=$?
    echo "$topic_json" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(1) if d.get('error') else None" 2>/dev/null || {
        echo "$topic_json"; return 1
    }

    local tema keyword intencion
    tema=$(echo "$topic_json" | python3 -c "import sys,json; print(json.load(sys.stdin)['tema'])")
    keyword=$(echo "$topic_json" | python3 -c "import sys,json; print(json.load(sys.stdin)['keyword'])")
    intencion=$(echo "$topic_json" | python3 -c "import sys,json; print(json.load(sys.stdin)['intencion'])")

    echo "🚀 Fase 1/4 — Investigando tema: $tema" >&2
    local brief_file="$WORK_DRAFT_DIR/brief_$(date +%s).json"
    local brief_rc
    "$RESEARCH_SCRIPT" --topic "$tema" --keyword "$keyword" --intencion "$intencion" \
        --output "$brief_file" >/dev/null 2>"$LOG_DIR/research.err"
    brief_rc=$?

    if [ $brief_rc -ne 0 ] || [ ! -s "$brief_file" ]; then
        echo "{\"error\":\"Fallo la investigación\",\"exitCode\":$brief_rc,\"tema\":\"$tema\"}"
        return 1
    fi
    ok "Research completado → $brief_file"

    echo "🚀 Fase 2/4 — Redactando artículo..." >&2
    local draft_result gen_rc gen_err
    gen_err="$LOG_DIR/generate.err"
    draft_result=$("$GENERATE_SCRIPT" \
        --topic "$tema" --keyword "$keyword" --intencion "$intencion" \
        --research "$brief_file" --with-image 2>"$gen_err") || true
    gen_rc=$?

    if [ $gen_rc -ne 0 ]; then
        echo "{\"error\":\"Fallo al generar el artículo\",\"exitCode\":$gen_rc,\"tema\":\"$tema\"}" >&2
        echo "── stderr (últimas 15 líneas) ──" >&2
        tail -15 "$gen_err" >&2 || true
        return 1
    fi
    if ! echo "$draft_result" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
        echo "{\"error\":\"Salida de generación no es JSON válido\",\"tema\":\"$tema\"}" >&2
        echo "── salida cruda ──" >&2
        echo "$draft_result" >&2
        tail -15 "$gen_err" >&2 || true
        return 1
    fi

    # Guardar estado para que el bot Telegram pueda mostrarlo y aprobar
    local slug title
    slug=$(echo "$draft_result" | python3 -c "import sys,json; print(json.load(sys.stdin).get('slug',''))")
    title=$(echo "$draft_result" | python3 -c "import sys,json; print(json.load(sys.stdin).get('title',''))")
    set_state "{\"slug\":\"$slug\",\"title\":\"$title\",\"tema\":\"$tema\",\"briefFile\":\"$brief_file\",\"estado\":\"aprobacion-pendiente\",\"updated\":\"$(date -Iseconds)\"}"

    ok "Draft + imagen listos → $slug"
    echo "$draft_result"
    return 0
}

# ── Publicar un draft aprobado ──
approve() {
    local slug="${1:-}"
    if [ -z "$slug" ]; then
        slug=$(state_get slug)
    fi
    if [ -z "$slug" ]; then
        echo '{"error":"No hay slug para publicar"}'
        return 1
    fi
    echo "🚀 Publicando: $slug" >&2
    local out rc
    out=$(bash "$PUBLISH_SCRIPT" "$slug" 2>&1 | tail -6)
    rc=$?
    # Nuevo estado tras el intento
    local new_estado="publicacion-fallida"
    if [ $rc -eq 0 ]; then new_estado="publicado"; fi
    set_state "$(get_state | python3 -c "
import sys,json
d=json.load(sys.stdin)
d['estado']='$new_estado'
d['updated']='$(date -Iseconds)'
print(json.dumps(d, ensure_ascii=False))")"
    if [ $rc -eq 0 ]; then
        ok "Publicado correctamente: $slug"
    else
        fail "Error al publicar: $slug"
    fi
    # JSON robusto: escapar el detalle con python
    local detalle
    detalle=$(printf '%s' "$out" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
    local estado_out="fallo"
    if [ $rc -eq 0 ]; then estado_out="publicado"; fi
    echo "{\"slug\":\"$slug\",\"estado\":\"$estado_out\",\"detalle\":$detalle}"
    return $rc
}

# ── Cancelar un draft: marca tema como descartado y deja el siguiente ──
cancel() {
    local slug="${1:-}"
    slug=$( [ -n "$slug" ] && echo "$slug" || state_get slug )
    if [ -z "$slug" ]; then
        echo '{"error":"No hay slug para cancelar"}'
        return 1
    fi
    local draft_dir="$PROJECT_DIR/src/content/blog/drafts"
    if [ -f "$draft_dir/$slug.mdx" ]; then
        rm -f "$draft_dir/$slug.mdx"
        ok "Borrador eliminado: $slug"
    fi
    local img="$PROJECT_DIR/public/assets/img/blog/$slug.png"
    if [ -f "$img" ]; then
        rm -f "$img"
        ok "Imagen eliminada: $slug"
    fi

    # Marcar tema en el CSV como 'descartado' para que el próximo run-all
    # elija OTRO tema (requisito del loop "hasta que apruebes")
    local tema_estado
    tema_estado=$(state_get tema)
    if echo "$tema_estado" | grep -q "No hay tema\|^$"; then
        warn "No hay tema registrado en estado para marcar en CSV"
    else
        if python3 -c "
import csv, sys
csv_path = '$TOPIC_BANK'
tema = '''$tema_estado'''
rows = []
fieldnames = []
found = False
with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames or []
    for row in reader:
        row_tema = (row.get('tema', '') or '').strip('\"\' ')
        if row_tema and row_tema == tema and row.get('estado','').strip().lower() == 'pendiente':
            row['estado'] = 'descartado'
            found = True
        rows.append(row)
if found:
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
" 2>/dev/null; then
            ok "Tema marcado como descartado en topic bank: $tema_estado"
        else
            warn "No se pudo marcar tema en CSV (¿ya estaba modificado?)"
        fi
    fi

    # Actualizar estado
    set_state "$(get_state | python3 -c "
import sys,json
d=json.load(sys.stdin)
d['estado']='cancelado'
d['canceladoSlug']=d.get('slug','')
d['slug']=''
d['updated']='$(date -Iseconds)'
print(json.dumps(d, ensure_ascii=False))")"
    echo "{\"slug\":\"$slug\",\"estado\":\"cancelado\"}"
    return 0
}

# ── Estado del pipeline ──
state() {
    get_state
}

# ── main ──
action="${1:-help}"
case "$action" in
    research)
        run_all
        ;;
    generate)
        echo '{"error":"Uso directo: use run-all para research+generate integrados"}'
        return 1
        ;;
    run-all|run_all|run)
        run_all
        ;;
    approve|publicar)
        approve "${2:-}"
        ;;
    cancel|cancelar)
        cancel "${2:-}"
        ;;
    state)
        state
        ;;
    help|--help|-h)
        echo "Uso: blog-pipeline.sh <comando> [opciones]"
        echo ""
        echo "  run-all             research + redactar + imagen (todo el pipeline)"
        echo "  approve [slug]      publicar un draft aprobado"
        echo "  cancel [slug]       descartar draft, marcar tema como cancelado"
        echo "  state               mostrar estado del pipeline (JSON)"
        ;;
    *)
        echo '{"error":"Comando desconocido","accion":"'"$action"'"}'
        exit 1
        ;;
esac