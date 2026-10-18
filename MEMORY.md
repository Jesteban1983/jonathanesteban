# MEMORY.md — Memoria del proyecto

> Registro persistente para cualquier agente. **Léelo antes de empezar** y **añade una entrada al terminar** (fecha, qué, por qué). Lo más reciente arriba.

---

## Contexto fijo

- **Sitio:** https://jonathanesteban.dev — soporte informático (particulares, pymes, autónomos).
- **Base:** L'Hospitalet de Llobregat (Barcelona). Servicio a domicilio y en remoto. **No hay local físico y no se dice así.**
- **Stack:** Astro 7 (static) + Tailwind 4 vía Vite + MDX + Netlify (hosting y Functions) + n8n (recepcionista IA) + Leaflet.
- **Raíz del código:** `astro-portfolio/`. El README antiguo hablaba de `site/` y `functions/`: **ya no existen**.
- **Dev:** `0.0.0.0:4321`; el usuario accede por Tailscale `http://100.107.45.16:4321/`.

## Decisiones vigentes

| Tema | Decisión |
|---|---|
| Privacidad | Nunca dirección de casa ni pin en el mapa. Mostrar zona (círculos ~12,5 y ~15,5 km). |
| Copy | "Servicio a domicilio y en remoto". Prohibido "sin local físico". |
| Mapa | Leaflet + Esri World Street Map (sin key). Dark mode con filtro CSS en `.leaflet-tile-pane`. |
| Formulario | `/contacto/` → Netlify Function `contact-recepcionista` → n8n; fallback Formspree; éxito → `/gracias/?name=&email=`. |
| Garantía | 15 días desde la entrega. |
| Indexación | `gracias`, `auth/*`, `certificaciones` en `noindex` y fuera del sitemap. |
| Sitemap | `@astrojs/sitemap` → `/sitemap-index.xml`. `trailingSlash: 'always'`. |
| Canonical | Siempre absoluto (lo resuelve `Layout.astro`). |

## Gotchas (errores ya cometidos)

1. **Node del sistema es v18**; Astro exige ≥ 22.12. Usar `export PATH=/home/taisu/.nvm/versions/node/v24.20.0/bin:$PATH`.
2. **CARTO** exige API key (marca de agua "API KEY REQUIRED"). Esri World Street Map no.
3. **Esri Dark Canvas** sale gris y sin etiquetas legibles → no usar.
4. **404 al enviar el formulario:** `public/assets/js/form.js` tenía un listener a `/api/contact-submit` (no existe). Se eliminó; el `<script>` inline de `contacto/index.astro` es el único manejador.
5. **Formspree `movzjdbz` devolvía 404:** Se sustituyó por fallback nativo a Netlify Forms y `contact-recepcionista` ahora es resiliente (guarda en Netlify Blobs, envía email por Resend si hay key, reenvía a n8n si hay webhook, y responde 200 para redirigir a `/gracias/` sin fallar).
6. **`astro dev` no ejecuta Netlify Functions.** En local el envío se simula (hostname `localhost`, `100.x` o puerto 4321). Para probar de verdad: `netlify dev`.
7. **Webhook n8n de pruebas** (`/webhook/recepcionista-leads-test`) responde 404 si el workflow no está activo.
8. **CRLF** en varios `.astro`: `sed -i '...$'` falla en silencio. Usar Python o las herramientas de edición.
9. **`curl /sitemap.xml` en el dev server puede colgarse**; validar con `astro build --outDir /tmp/…`.
10. **CSP** (`netlify.toml`): ya incluye `server.arcgisonline.com` en `img-src` y `font-src 'self'`. Si se añade otro recurso externo (CDN, analítica), hay que permitirlo ahí o se bloqueará en producción.
11. Google Fonts estaba bloqueado por la CSP en producción (sin `font-src`); resuelto autoalojando Inter.

## Pendiente de Jonathan

- Código `google-site-verification` truncado en `Layout.astro`.
- Google Business Profile (área de servicio).
- Imagen OG de marca 1200×630.

---

## Bitácora

### 2026-10-18 (corrección de error al enviar formulario de contacto)
- `contact-recepcionista.js`: ya no devuelve 503 si `N8N_WEBHOOK_LEADS_URL` no está definida en Netlify. Ahora valida, registra el lead en consola de Netlify, guarda en Netlify Blobs si está disponible, envía email vía Resend (si `RESEND_API_KEY` existe), reenvía a n8n (si `N8N_WEBHOOK_LEADS_URL` existe) y responde 200 `{ ok: true }`.
- `contacto/index.astro`: añadido `name="contact" data-netlify="true" data-netlify-honeypot="_gotcha"` y campo oculto `form-name="contact"`. En el cliente, si el endpoint serverless fallase, se realiza fallback a Netlify Forms nativo. Tras el envío correcto, siempre redirige limpiamente a `/gracias/?name=...&email=...`.

### 2026-10-18 (ejecución del plan SEO/GEO)
- `Layout.astro`: prop `jsonld`; `BreadcrumbList` automático; `Service` automático en `/servicios/<slug>/`; Inter autoalojada (`@fontsource-variable/inter`), sin Google Fonts; OG por defecto `assets/img/og/og-default.jpg`.
- Metadatos (title ≤ 60, description ≈ 140–165) reescritos en home, servicios, sobre-mí, contacto, faq, blog y 6 servicios.
- Cada servicio: bloque «En resumen» (citable, con precios reales de la propia web) + «Te puede interesar». Cada post: servicios relacionados + `Article` JSON-LD.
- `public/llms.txt`, `docs/seo-keywords.md` (mapa keyword→URL + clústeres).
- `netlify.toml`: CSP con `img-src` Esri y `font-src 'self'`, `base-uri`, `form-action`; cabeceras de caché.
- Accesibilidad: `aria-expanded` en FAQ, `role=alert/status` en el formulario, `aria-invalid`, label en buscador FAQ, región del mapa; contraste `--color-text-faint` corregido (4,55:1 dark / 5,49:1 light).
- Sin Chrome en el servidor: Lighthouse no ejecutado.
- `content.config.ts` incluye `drafts/` en la colección; los borradores deben llevar `draft: true`.
- Mapa de `/servicios/`: eliminada dirección personal; Esri keyless; dark mode legible; copy "domicilio y en remoto".
- Rollback completo de una auditoría de agencia pegada por error (páginas `proyectos/`, `desarrollo-web/`, etc. eliminadas).
- Verificada `/gracias/`; el formulario ahora redirige a ella; página rediseñada (3 pasos + WhatsApp urgencias).
- Corregido 404 del formulario (listener duplicado en `form.js`) y añadido modo simulado en dev.
- Auditoría SEO/GEO/accesibilidad: sitemap creado, robots.txt corregido, canonicals/OG absolutos, noindex, JSON-LD de zona, skip-link. Ver `PLAN-SEO-GEO-v1.md`.
- Eliminación de destellos / FOUC al cargar página: script inline de tema movido al `<head>` antes del primer paint; retirada la transición CSS automática de 300ms en el `body` durante la carga (ahora solo se activa al hacer clic en el botón); renderizado previo de iconos SVG del tema en HTML/CSS; y activación inmediata de elementos `.fade-in` ya en viewport.
