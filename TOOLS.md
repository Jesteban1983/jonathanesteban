# TOOLS.md — Herramientas y comandos del proyecto

Todos los comandos se ejecutan desde `astro-portfolio/` salvo que se indique.

## Entorno

```bash
export PATH=/home/taisu/.nvm/versions/node/v24.20.0/bin:$PATH   # Node >= 22.12 obligatorio
```

## Astro

| Acción | Comando |
|---|---|
| Servidor dev (red/Tailscale) | `npx astro dev --host 0.0.0.0 --port 4321` |
| Build de producción | `npm run build` |
| Build de validación sin tocar `dist/` | `npx astro build --outDir /tmp/aud-dist` |
| Previsualizar build | `npm run preview` |
| Comprobación de tipos | `npx astro check` |

## SEO / GEO — verificación

```bash
# Sitemap generado (tras un build)
cat /tmp/aud-dist/sitemap-index.xml
grep -o '<loc>[^<]*</loc>' /tmp/aud-dist/sitemap-0.xml

# Canonical y robots de una página
grep -o '<link rel="canonical"[^>]*>' /tmp/aud-dist/index.html
grep -o '<meta name="robots"[^>]*>' /tmp/aud-dist/gracias/index.html

# H1 por página (debe ser 1)
grep -rc '<h1' src/pages --include=*.astro

# Imágenes sin alt
grep -rn '<img' src | grep -v 'alt='
```

Herramientas externas: Google Search Console, Bing Webmaster Tools, Lighthouse (Chrome DevTools o `npx lighthouse <url> --view`), Rich Results Test, validator.schema.org, PageSpeed Insights, axe DevTools (accesibilidad).

## Verificaciones añadidas (plan SEO/GEO)

```bash
# JSON-LD por página (tipos presentes)
grep -o '<script type="application/ld+json">[^<]*' /tmp/aud-dist/servicios/redes/index.html | grep -o '"@type":"[A-Za-z]*"' | sort -u

# Contraste WCAG: ver script en MEMORY (tokens --color-text-* en global.css); objetivo >= 4.5:1
# Google Fonts no debe aparecer
grep -c fonts.googleapis /tmp/aud-dist/index.html   # 0
```

| Recurso | Ubicación |
|---|---|
| Resumen para IAs | `public/llms.txt` |
| Mapa keyword → URL | `docs/seo-keywords.md` |
| Imagen OG por defecto | `public/assets/img/og/og-default.jpg` (1200×630) |
| Redimensionar imágenes (sin PIL) | `node -e "require('sharp')(in).resize(1200,630,{fit:'cover'}).jpeg({quality:85}).toFile(out)"` |
| Lighthouse | No hay Chrome en el servidor: usar PageSpeed Insights o tu equipo local |

## Formulario de contacto

| Pieza | Ubicación |
|---|---|
| UI + manejador | `src/pages/contacto/index.astro` |
| Prefill por URL | `public/assets/js/form.js` |
| Proxy → n8n | `netlify/functions/contact-recepcionista.js` |
| Variables | `.env` → `N8N_WEBHOOK_LEADS_URL`, `N8N_WEBHOOK_SECRET` |
| Éxito | `src/pages/gracias/index.astro` |

```bash
npx netlify dev        # ejecuta Functions en local (astro dev no lo hace)
curl -s -X POST http://localhost:5678/webhook/recepcionista-leads-test \
  -H 'Content-Type: application/json' -d '{"test":true}'   # n8n debe estar activo
```

## Mapa (Leaflet)

- Archivo: `src/pages/servicios/index.astro`.
- Teselas: `https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}`.
- Dark mode: `filter` CSS sobre `.leaflet-tile-pane`.
- Assets locales de Leaflet: `public/leaflet/`.

## Blog automatizado

| Script | Función |
|---|---|
| `scripts/blog-pipeline.sh` | Orquesta investigación → borrador → imagen |
| `scripts/research-topic.py` | Investiga el tema |
| `scripts/generate-blog-post.py` | Genera el borrador en `src/content/blog/drafts/` |
| `scripts/refine-image-prompt.py`, `generate_blog_image.py`, `generate-missing-blog-image.sh` | Imágenes |
| `scripts/list-drafts.py`, `blog-publish.sh`, `update-topic-bank.py` | Revisión y publicación (**aprobación humana**) |
| `blog-topic-bank.csv` | Banco de temas |

## Despliegue

- Netlify construye con `netlify.toml` (`base = astro-portfolio`, `publish = dist`, Node 22).
- Deploy automático al hacer push a `main`.

## Git

```bash
git status --short
git diff -- src/pages/contacto/index.astro
```

## Herramientas del agente (Antigravity)

- Edición: `replace_file_content`, `multi_replace_file_content`, `write_to_file`.
- Búsqueda: `grep_search`, `list_dir`.
- Terminal: `run_command` (los procesos largos pasan a segundo plano; consultar con `manage_task`).
- Navegador: `browser_subagent` **no funciona** en este entorno (Playwright no puede descargarse). Verificar con `curl` o build.
