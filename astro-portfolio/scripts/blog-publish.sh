#!/bin/bash
# blog-publish.sh — Publica un artículo del blog: de drafts/ a producción,
# actualiza topic bank, construye el proyecto y hace commit.
#
# Uso:
#   ./scripts/blog-publish.sh <slug>              # Publica un draft específico
#   ./scripts/blog-publish.sh                      # Publica TODOS los drafts
#   ./scripts/blog-publish.sh --list               # Lista drafts disponibles
#   ./scripts/blog-publish.sh --undo <slug>        # Revierte (mueve a drafts otra vez)
#   ./scripts/blog-publish.sh --topic "..." <slug> # Especifica el tema para marcar CSV

set -euo pipefail

# ── paths ─────────────────────────────────────────────────────────────────
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONTENT_DIR="$PROJECT_DIR/src/content/blog"
DRAFTS_DIR="$CONTENT_DIR/drafts"
TOPIC_BANK="$PROJECT_DIR/blog-topic-bank.csv"
LOG_DIR="$HOME/.nova-logs"
mkdir -p "$LOG_DIR"
PUB_LOG="$LOG_DIR/blog-publish-$(date '+%Y%m%d_%H%M%S').log"

# ── colores (si hay terminal) ─────────────────────────────────────────────
if [ -t 1 ]; then
    GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
else
    GREEN=''; YELLOW=''; RED=''; NC=''
fi

ok()  { echo -e " ${GREEN}✓${NC} $1"; }
warn(){ echo -e " ${YELLOW}⚠${NC} $1"; }
fail(){ echo -e " ${RED}✖${NC} $1"; }

# ── funciones ─────────────────────────────────────────────────────────────

list_drafts() {
    echo "📄 Drafts disponibles:"
    for f in "$DRAFTS_DIR"/*.mdx; do
        [ -f "$f" ] || continue
        slug=$(basename "$f" .mdx)
        title=$(grep -m1 '^title:' "$f" | sed "s/^title: *['\"]//; s/['\"],*$//" 2>/dev/null || echo "—")
        echo "  • $slug  —  $title"
    done
}

publish_draft() {
    local slug="$1"
    local draft_file="$DRAFTS_DIR/$slug.mdx"
    local pub_file="$CONTENT_DIR/$slug.mdx"

    if [ ! -f "$draft_file" ]; then
        fail "Draft no encontrado: $draft_file"
        return 1
    fi

    if [ -f "$pub_file" ]; then
        warn "Ya existe $pub_file — se hará backup en $pub_file.bak"
        cp "$pub_file" "$pub_file.bak"
    fi

    # Cambiar draft: true → draft: false y actualizar pubDate si no tiene
    sed -i \
        -e 's/^draft: true/draft: false/' \
        -e '/^pubDate:/{s/.*/pubDate: '"$(date '+%Y-%m-%d')"'/;}' \
        "$draft_file"

    # Si no tiene línea pubDate, añadirla tras description
    if ! grep -q '^pubDate:' "$draft_file"; then
        sed -i '/^description:/a\pubDate: '"$(date '+%Y-%m-%d')" "$draft_file"
    fi

    mv "$draft_file" "$pub_file"
    ok "Publicado: $pub_file"

    # Marcar en topic bank
    if python3 "$PROJECT_DIR/scripts/update-topic-bank.py" "$pub_file" "$TOPIC_BANK"; then
        ok "Topic bank actualizado"
    else
        warn "No se pudo actualizar topic bank"
    fi

    return 0
}

undo_publish() {
    local slug="$1"
    local pub_file="$CONTENT_DIR/$slug.mdx"
    local draft_file="$DRAFTS_DIR/$slug.mdx"

    if [ ! -f "$pub_file" ]; then
        fail "No existe: $pub_file"
        return 1
    fi

    # Revertir a draft
    sed -i 's/^draft: false/draft: true/' "$pub_file"
    mv "$pub_file" "$draft_file"
    ok "Revertido a draft: $draft_file"

    # Desmarcar en topic bank
    if python3 "$PROJECT_DIR/scripts/update-topic-bank.py" --undo "$draft_file" "$TOPIC_BANK"; then
        ok "Topic bank revertido"
    fi

    return 0
}

build_and_commit() {
    echo ""
    echo "🏗️  Construyendo el proyecto..."
    cd "$PROJECT_DIR"
    if npm run build 2>&1 | tail -5; then
        ok "Build completado"
    else
        fail "Build falló — revisa errores"
        return 1
    fi

    # Git add y commit
    if git rev-parse --git-dir > /dev/null 2>&1; then
        git add -A
        if git diff --cached --quiet; then
            warn "No hay cambios nuevos para commit"
        else
            git commit -m "blog: publicar artículo(s) $(date '+%Y-%m-%d')"
            ok "Commit realizado"
            # Push si hay upstream
            if git rev-parse --abbrev-ref @{upstream} > /dev/null 2>&1; then
                git push
                ok "Push a remoto"
            else
                warn "No hay upstream configurado — saltando push"
            fi
        fi
    else
        warn "No es un repo git — saltando commit"
    fi
}

# ── main ──────────────────────────────────────────────────────────────────
echo "═══════════════════════════════════════════════"
echo "  📰 Blog Publisher — $(date '+%Y-%m-%d %H:%M')"
echo "═══════════════════════════════════════════════"
echo ""

action="${1:-all}"
case "$action" in
    --list|-l)
        list_drafts
        exit 0
        ;;
    --undo|-u)
        if [ -z "${2:-}" ]; then
            fail "Uso: $0 --undo <slug>"
            exit 1
        fi
        undo_publish "$2"
        ;;
    --help|-h)
        echo "Uso: $0 [slug|--list|--undo <slug>]"
        echo ""
        echo "  slug          Publica un draft específico"
        echo "  (sin args)    Publica TODOS los drafts"
        echo "  --list        Lista drafts disponibles"
        echo "  --undo <slug> Revierte una publicación"
        echo "  --help        Esta ayuda"
        exit 0
        ;;
    *)
        if [ "$action" = "all" ]; then
            # Publicar todos
            count=0
            for f in "$DRAFTS_DIR"/*.mdx; do
                [ -f "$f" ] || continue
                slug=$(basename "$f" .mdx)
                publish_draft "$slug" && ((count++))
            done
            if [ "$count" -eq 0 ]; then
                warn "No hay drafts para publicar"
                exit 0
            fi
            ok "Publicados $count artículo(s)"
        else
            # Publicar específico
            publish_draft "$action" || exit 1
        fi
        ;;
esac

build_and_commit
echo ""
ok "Proceso completado — log: $PUB_LOG"