# AUDIT — jonathanesteban.dev
**Fecha:** 2026-10-11
**Auditor:** Nova Sistema Multiagente
**Repo:** `~/IA-ENGINEERING-LAB/08-proyectos/it-support-portfolio`

---

## 1. Stack real detectado

| Componente | Detectado | Evidencia |
|------------|-----------|-----------|
| **Framework** | HTML estático MPA (HTML + CSS + JS puro) | Sin `package.json`, sin `next.config.*`, sin `tsconfig.json` |
| **CSS** | Tailwind vía CDN (`cdn.tailwindcss.com`) + CSS modular (`tokens.css`, `base.css`, `layout.css`, etc.) | `site/index.html:54` — `<script src="https://cdn.tailwindcss.com">` |
| **Hosting** | ✅ Netlify | `netlify.toml` — publish = "site", functions = "functions" |
| **Dominio** | Namecheap → Netlify DNS | `netlify.toml` redirect: `jonathanesteban.netlify.app/*` → `jonathanesteban.dev` |
| **Backend** | Netlify Functions (7 funciones serverless en `functions/`) | `functions/` directorio con 7 archivos `.js` |
| **SEO** | JSON-LD schemas, sitemap.xml, robots.txt | Presentes en `site/` |
| **Analytics/Tracking** | Script de tracking propio | `site/assets/js/tracking.js` |

**Conclusión:** Sitio estático MPA de 29 páginas HTML. Sin framework JS. Tailwind vía CDN (no compilado). Sin TypeScript.

---

## 2. Estructura de rutas (29 páginas HTML)

```
/
├── index.html                              # Home (414 líneas)
├── sobre-mi/index.html                     # Sobre mí (458 líneas)
├── contacto/index.html                     # Contacto (195 líneas)
├── faq/index.html                          # FAQ (218 líneas)
├── gracias/index.html                      # Página post-formulario
├── privacy-policy/index.html               # Política de privacidad
├── terms-of-service/index.html             # Términos del servicio
├── data-deletion/index.html                # Eliminación de datos
│
├── servicios/
│   ├── index.html                          # Servicios general (669 líneas)
│   ├── desarrollo-web/index.html           # Desarrollo Web
│   ├── automatizacion/index.html           # Automatización IA
│   ├── soporte-it/index.html               # Soporte IT
│   ├── reparacion-ordenadores-portatiles/index.html
│   ├── formateo-limpieza-optimizacion/index.html
│   └── mantenimiento-preventivo-pc/index.html
│
├── proyectos/
│   ├── index.html                          # Portfolio
│   ├── trackflow/index.html
│   ├── clawmate/index.html
│   ├── demo-app/index.html
│   ├── talk-to-the-machine/index.html
│   └── casos/
│       ├── automatizacion-leads/index.html
│       ├── landing-negocio/index.html
│       └── portfolio-redesign/index.html
│
├── certificaciones/index.html
├── legal/
│   ├── aviso-legal/index.html
│   ├── cookies/index.html
│   └── privacidad/index.html
│
├── auth/
│   ├── facebook/callback/index.html
│   └── tiktok/callback/index.html
│
├── robots.txt
├── sitemap.xml
└── favicon.ico
```

**Tamaño total:** 2.5 MB (`site/`), imágenes: 1.8 MB

---

## 3. Contenido a corregir / reposicionar

| # | Hallazgo | Archivo(s) | Acción |
|---|----------|-----------|--------|
| 1 | **"Desarrollador Web & AI Engineer"** como título principal | `index.html:3`, `sobre-mi/index.html:211` | ✅ Cambiar a "Técnico Soporte IT" |
| 2 | **Servicios de "Desarrollo Web" y "Automatización"** como oferta principal | `index.html`, `servicios/index.html`, `servicios/desarrollo-web/index.html`, `servicios/automatizacion/index.html` | ✅ Retirar, dejar solo Soporte IT |
| 3 | **Referencias a 4Geeks Academy** como foco principal | `sobre-mi/index.html:211,264,306,331` | ✅ Mencionar como formación pasada, no identidad actual |
| 4 | **Nav menciona "Automatización"** en todas las páginas | `contacto/index.html:41,65`, +14 archivos más | ✅ Retirar del nav principal |
| 5 | **knowsAbout incluye tecnologías dev/IA** en JSON-LD | `index.html:67`, `sobre-mi/index.html:130` | ✅ Reemplazar con tecnologías IT/Soporte |
| 6 | **TrackFlow, Talk to the Machine** en proyectos activos | `site/proyectos/trackflow/`, `site/proyectos/talk-to-the-machine/` | ✅ Marcar como deprecated (mantener como histórico) |
| 7 | **Redirecciones a servicios antiguos** | `netlify.toml` (redirects a /soporte-it/#reparacion, etc.) | ✅ Revisar si aplican al nuevo contenido |
| 8 | **sitemap.xml** incluye URLs de servicios dev/automatización | `site/sitemap.xml` | ✅ Actualizar al nuevo contenido |

**NO se encontraron:** "15+ años", "16+ años", "EISIC" en el HTML actual (el typo solo está en PLAN-AGENTE-v2.md como referencia).

---

## 4. APIs y servicios externos

| Endpoint API | Archivo |
|-------------|---------|
| `/api/contact-submit` → Netlify Function | `netlify.toml` (redirect 200) |
| `/api/tiktok-oauth-callback` | `site/auth/tiktok/callback/index.html:74` |
| `/api/facebook-oauth-callback` | `site/auth/facebook/callback/index.html:74` |
| `/api/data-deletion-request` | `netlify.toml` (redirect 200) |
| Netlify Identity API | `connect-src 'self' https://api.netlify.com` |

**Funciones serverless (7):**
- `autoresponse.js`
- `contact-submit.js`
- `data-deletion-request.js`
- `facebook-oauth-callback.js`
- `notify-owner.js`
- `tiktok-oauth-callback.js`
- `webhook-n8n.js`

---

## 5. Deuda técnica

| Problema | Severidad | Propuesta |
|----------|-----------|-----------|
| **Tailwind vía CDN** (no compilado) | Media | Migrar a Tailwind compilado con PostCSS o framework |
| **Sin framework JS** (29 HTMLs, 11 JS) | Media | Valorar Astro como SSG ligero (mínimo JS, SEO nativo) |
| **Sin TypeScript** | Baja | No crítico para MPA estático |
| **Sin tests automatizados** | Baja | Añadir checks de ortografía/links existentes |
| **Imágenes sin optimizar** (1.8 MB) | Media | Comprimir WebP + lazy loading |
| **CSS duplicado** en cada página | Media | Beneficio de migrar a framework con imports compartidos |
| **Sin lazy loading** en imágenes | Baja | Añadir `loading="lazy"` |

---

## 6. Riesgos de seguridad

| Riesgo | Archivo | Estado |
|--------|---------|--------|
| **CSP actual permite `unsafe-inline`** | `netlify.toml` | ⚠️ Necesario por Tailwind CDN. Se resolverá al migrar a framework |
| **Tailwind CDN externo** (dependencia de 3ro) | Múltiples HTMLs | ⚠️ Se resuelve con Tailwind compilado |
| **OAuth callbacks** (TikTok/Facebook) | `auth/` | 🔒 Ya están server-side |
| **Formularios:** honeypot + rate limiting | `functions/contact-submit.js` | ✅ Ya implementado |

---

## 7. Recomendación preliminar

### No migrar a Next.js ni Astro todavía
El sitio es **HTML estático MPA** funcional con 29 páginas. Migrar ahora a Astro añadiría complejidad sin beneficio inmediato para el objetivo (reposicionar a Soporte IT).

### ✅ Plan recomendado (manteniendo HTML estático):

| Fase | Acción |
|------|--------|
| **Fase 1** | Limpiar contenido: retirar servicios dev/automatización del nav, reposicionar "Sobre Mí", actualizar JSON-LD |
| **Fase 2** | Crear marca personal (logo, paleta, tono de voz) |
| **Fase 3** | Reestructurar home y servicios → 100% Soporte IT con 4 servicios |
| **Fase 4** | Añadir blog como HTML estático + n8n backend |
| **Fase 5** | Seguridad webhooks n8n + checklist fiscalización |
| **Fase 6** | SEO, QA, deploy |

### Deuda técnica para después de la migración:
- Evaluar Astro como SSG cuando el sitio se estabilice
- Tailwind compilado (no CDN)
- Imágenes en WebP + lazy loading
- Tests de regresión visual

---

**Auditoría generada por:** Nova Sistema Multiagente
**ESPERANDO APROBACIÓN FASE 0**