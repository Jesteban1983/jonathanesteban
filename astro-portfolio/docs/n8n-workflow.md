# Flujo editorial — Blog Automatizado (pipeline completo)

Este documento describe el pipeline de generación de artículos del blog con
**aprobación manual vía Telegram** (botones ✅ Publicar / ❌ Cancelar).

> ⚠️ **Sustitución**: el flujo original usaba email de aprobación con botones.
> No existe infraestructura SMTP (sin SendGrid/Mailgun/Resend/n8n SMTP), por eso
> la aprobación se canaliza por **Telegram**, que ya estaba funcionando
> (bot `agente-nova.service` con botones inline).

## Arquitectura del pipeline

```
Telegram /blog  (o: bash scripts/blog-pipeline.sh run-all)
  │
  ├─ [1] RESEARCH    → research-topic.py      → DeepSeek V4 → brief JSON
  ├─ [2] REDACCION   → generate-blog-post.py  → DeepSeek V4 → draft .mdx
  ├─ [3] REFINE      → refine-image-prompt.py → Groq (qwen3.8) → prompt FLUX
  ├─ [4] IMAGEN      → generate_blog_image.py → DeepInfra (FLUX-1-dev) → .png
  │
  ├─ Estado guardado → .blog-pipeline-state.json → "aprobacion-pendiente"
  │
  └─ Telegram botones [✅ Publicar] [❌ Cancelar]
        ├─ Publicar → blog-publish.sh (build + git push + CSV → publicado)
        └─ Cancelar → borra draft/imagen + CSV → descartado (loop al siguiente)
```

## Scripts

| Fase | Script | Modelo | Salida |
|---|---|---|---|
| 1. Investigación | `scripts/research-topic.py` | DeepSeek V4 (deepseek-v4) | brief JSON estructurado (tema, datosClave, fuentes, pasos…) |
| 2. Redacción | `scripts/generate-blog-post.py` | DeepSeek V4 | draft `.mdx` en `src/content/blog/drafts/` |
| 3. Refine prompt | `scripts/refine-image-prompt.py` | Groq (groq-fast) | prompt detallado en inglés para FLUX |
| 4. Imagen | `scripts/generate_blog_image.py` | DeepInfra FLUX-1-dev | `public/assets/img/blog/<slug>.png` |
| Orquestador | `scripts/blog-pipeline.sh` | — | comandos `run-all` / `approve` / `cancel` / `state` |
| Publicación | `scripts/blog-publish.sh` | — | draft→producción + build + commit + push |

**Puntos clave de la integración:**
- El prompt de imagen se refina con Groq para que la imagen salga **bien
  especificada y estructurada** (estilo editorial, paleta #0D3C46/#F2A72A,
  sujeto en dos tercios derechos, sin texto/logos/números) → evita imágenes
  confusas como las generadas anteriormente.
- Cada fase devuelve JSON legible por máquinas (n8n/Telegram).
- Estado persistido en `.blog-pipeline-state.json` para que el bot conozca el
  slug/tema pendiente de aprobación.

## Comandos

```bash
# Pipeline completo (investiga + redacta + genera imagen)
bash scripts/blog-pipeline.sh run-all

# Publicar un draft aprobado (build + git push)
bash scripts/blog-pipeline.sh approve <slug>

# Cancelar: borra draft/imagen y marca el tema como 'descartado' (loop al siguiente)
bash scripts/blog-pipeline.sh cancel <slug>

# Estado actual del pipeline
bash scripts/blog-pipeline.sh state
```

## La aprobación (Telegram) y el loop

1. El bot atiende `/blog` → ejecuta `run-all`.
2. Cuando termina, envía un mensaje con el título, descripción, slug y los
   botones **✅ Publicar** / **❌ Cancelar**.
3. **✅ Publicar** → `approve` → `blog-publish.sh <slug>` → publica en producción
   (draft→público, tema → `publicado`), build de Astro y `git push`.
4. **❌ Cancelar** → `cancel` → borra draft e imagen, y marca el tema en
   `blog-topic-bank.csv` como `descartado`.
5. El usuario puede lanzar `/blog` de nuevo → el pipeline elige **otro tema**
   pendiente → se repite el ciclo **hasta que se apruebe uno**.

En `blog-topic-bank.csv`:
- `pendiente` → se puede generar
- `descartado` → se ignora (cancelado)
- `publicado` → ya publicado

## Variables de entorno

- Las claves de las APIs se leen de `~/IA-ENGINEERING-LAB/.env`
  (`DEEPINFRA_API_KEY`, `IMAGE_MODEL`, `IMAGE_SIZE`, `IMAGE_ASPECT_RATIO`…).
- El token de Telegram (`TELEGRAM_BOT_TOKEN` / `TELEGRAM_ADMIN_ID`) en
  `~/IA-ENGINEERING-LAB/07-agentes/.env`.
- LiteLLM gateway en `localhost:4000`; modelos en `~/litellm/config.yaml`.
- La imagen se genera con el venv `~/IA-ENGINEERING-LAB/.venv-image/bin/python`
  (tiene google-genai, Pillow, python-dotenv, requests).

## Notas n8n (opcional)

n8n puede disparar `run-all` periódicamente y dejar la aprobación el bot de
Telegram. Si se usa n8n, asegúrate de que el entorno herede `~/.nova.env`:

```bash
set -a; . /home/taisu/.nova.env; set +a; bash scripts/blog-pipeline.sh run-all
```