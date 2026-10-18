# 🌐 jonathanesteban.dev — Soporte informático (Astro + Netlify)

> **Sitio:** [https://jonathanesteban.dev](https://jonathanesteban.dev)
> **Autor:** Jonathan Esteban Barona — técnico de soporte informático
> **Zona:** L'Hospitalet de Llobregat y área metropolitana de Barcelona · servicio a domicilio y en remoto
> **Hosting:** Netlify (deploy automático desde `main`)

---

## 🏗️ Arquitectura

Sitio estático con **Astro 7**, **Tailwind 4** (Vite), **MDX** y funciones serverless de Netlify.

```
.
├── astro-portfolio/                  # Código fuente (base de Netlify)
│   ├── src/
│   │   ├── layouts/Layout.astro      # <head> SEO: canonical absoluto, OG, JSON-LD, noindex, skip-link
│   │   ├── components/               # Header, Footer
│   │   ├── pages/                    # Rutas (index, servicios/*, sobre-mi, blog, faq, contacto, gracias, legal…)
│   │   ├── content/blog/             # Artículos MDX (+ drafts/)
│   │   └── styles/global.css         # Tokens de diseño y utilidades
│   ├── public/                       # robots.txt, assets, brand, leaflet, favicon
│   ├── netlify/functions/            # contact-recepcionista.js (proxy → n8n)
│   ├── scripts/                      # Pipeline del blog (Python/Bash)
│   ├── docs/                         # Workflow n8n
│   └── astro.config.mjs              # site, trailingSlash, mdx, sitemap
├── netlify.toml                      # Build, cabeceras de seguridad/CSP, redirecciones
├── PLAN-SEO-GEO-v1.md                # ▶ Plan vigente de SEO / GEO / accesibilidad / CRO
├── PLAN-AGENTE-v2.md                 # Plan de reestructuración original
├── MEMORY.md                         # Decisiones y gotchas (leer antes de trabajar)
├── TOOLS.md                          # Comandos y herramientas
├── BRAND.md · CV-DATA.md · MARKET-ANALYSIS.md · STACK.md · AUDIT.md
└── WORKFLOW-RECEPCIONISTA.md · BLOG-AUTOMATION.md · FISCALIZACION.md
```

---

## 🚀 Comandos

Requiere **Node ≥ 22.12** (`export PATH=/home/taisu/.nvm/versions/node/v24.20.0/bin:$PATH`).

```bash
cd astro-portfolio
npm install
npx astro dev --host 0.0.0.0 --port 4321   # desarrollo (accesible por Tailscale)
npm run build                              # producción → dist/
npm run preview
npx netlify dev                            # prueba las Netlify Functions en local
```

Más en [`TOOLS.md`](TOOLS.md).

---

## 🔎 SEO y GEO — estado

| Elemento | Estado |
|---|---|
| `robots.txt` | ✅ Permite buscadores y bots de IA (GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot, Google-Extended…); bloquea `/gracias/`, `/auth/`, `/certificaciones/` |
| Sitemap | ✅ `@astrojs/sitemap` → `/sitemap-index.xml` |
| Canonical / OG | ✅ URLs absolutas desde `Layout.astro`; imagen OG de marca 1200×630 |
| Rendimiento | ✅ Inter autoalojada, caché inmutable, CSP ajustada |
| `noindex` | ✅ gracias, auth, certificaciones |
| JSON-LD | ✅ `Person`, `ProfessionalService`, `BreadcrumbList`, `Service` (por servicio), `Article` (blog), `FAQPage` (/faq/) |
| Accesibilidad | ✅ skip-link, foco visible, ARIA en FAQ/formulario/mapa, contraste AA en tokens · ⏳ Lighthouse |
| `llms.txt` | ✅ `public/llms.txt` |
| Google Business Profile | ⏳ Acción de Jonathan |

Hoja de ruta completa: [`PLAN-SEO-GEO-v1.md`](PLAN-SEO-GEO-v1.md).

---

## ✉️ Flujo del formulario de contacto

```
/contacto/ ──► /.netlify/functions/contact-recepcionista ──► webhook n8n (recepcionista IA)
     │                  (honeypot + rate-limit)                        │
     │                                                                 └─► borrador → aprobación por Telegram
     ├─ fallback: Formspree
     └─ éxito ──► /gracias/?name=…&email=…   (noindex)
```

| Variable | Descripción |
|---|---|
| `N8N_WEBHOOK_LEADS_URL` | Webhook n8n del recepcionista |
| `N8N_WEBHOOK_SECRET` | Secreto compartido (header, nunca en el body) |

Se configuran en Netlify (*Site settings → Environment variables*) y en `astro-portfolio/.env` para local. `astro dev` **no** ejecuta Functions: en local el envío se simula.

---

## 🔒 Seguridad y privacidad

- Ningún secreto en el frontend; el proxy serverless guarda las claves.
- Cabeceras HSTS, CSP, `X-Frame-Options`, `Permissions-Policy` en `netlify.toml`.
- **No se publica dirección personal ni ubicación exacta**; el mapa muestra zona de cobertura.
- Cookies: banner de consentimiento; políticas en `/legal/cookies/` y `/privacy-policy/`.

---

## 🤖 Trabajo con agentes

1. Leer [`MEMORY.md`](MEMORY.md) y las reglas de `astro-portfolio/AGENTS.md`.
2. Seguir la fase vigente de [`PLAN-SEO-GEO-v1.md`](PLAN-SEO-GEO-v1.md); no avanzar sin validación de Jonathan.
3. Al terminar: `npm run build`, actualizar `MEMORY.md`, `TOOLS.md` y este README si cambia algo.

---

*Desarrollado para jonathanesteban.dev. El README anterior (arquitectura `site/` + `functions/`) está en el historial de git.*