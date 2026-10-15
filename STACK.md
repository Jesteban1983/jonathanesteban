# STACK.md — Decisión Tecnológica Definitiva
**Fecha:** 2026-10-11
**Basado en:** AUDIT.md (FASE 0 completada)
**Hosting confirmado:** Netlify + Namecheap (no se discute)

---

## Resumen de la decisión

| Aspecto | Elegido | Alternativa descartada |
|---------|---------|----------------------|
| **Framework** | ✅ **Astro 5** (Static Site Generator) | HTML estático MPA, Next.js |
| **CSS** | ✅ Tailwind CSS compilado (vía Astro) | Tailwind CDN |
| **Blog** | ✅ Content Collections MDX (Astro nativo) | next-mdx-remote, HTML manual |
| **Backend/Automatización** | ✅ Netlify Functions + n8n oculto | — |
| **Hosting** | ✅ Netlify (confirmado) | Vercel (descartado) |
| **Dominio** | ✅ Namecheap (Netlify DNS) | — |

---

## 🧭 Análisis de opciones

### Opción A: Mantener HTML estático MPA 🟡

| Ventajas | Desventajas |
|----------|-------------|
| ❌ Migración cero — editar HTMLs existentes | ❌ Blog requiere crear HTML manual cada vez (incompatible con automatización n8n) |
| ❌ Sin dependencias, sin build | ❌ CSS duplicado en 29 páginas |
| ❌ Se despliega directo en Netlify | ❌ Sin componentes reutilizables (cambiar header = editar 29 archivos) |
| | ❌ Sin MDX, sin content collections |
| | ❌ Sin RSS/sitemap automáticos |
| | ❌ Tailwind sigue siendo CDN (dependencia externa, `unsafe-inline` en CSP) |

**Veredicto:** Descartada. El blog automatizado (FASE 4) es incompatible con HTML estático puro.

### Opción B: Next.js 🟠

| Ventajas | Desventajas |
|----------|-------------|
| ✅ Netlify lo soporta nativamente (Next.js Runtime) | ❌ Mucho más pesado de lo que necesitas |
| ✅ Server Actions para formularios | ❌ JS bundle innecesario para un sitio de soporte IT |
| ✅ MDX vía `next-mdx-remote` | ❌ Mayor curva de aprendizaje |
| | ❌ Builds lentos para 10-15 páginas |
| | ❌ Overkill total para tu proyecto |

**Veredicto:** Descartada. Next.js está pensado para apps con mucho estado, no para un sitio informativo de soporte IT.

### Opción C: Astro ✅ (ELEGIDA)

| Ventajas | Desventajas |
|----------|-------------|
| ✅ **Output 100% HTML estático** — cero JS por defecto | ❌ Migración única de los HTMLs actuales a .astro |
| ✅ **Componentes reutilizables** (Header, Footer, ServiceCard, AboutMe) — cambias uno, se actualiza todo | ❌ Aprender sintaxis .astro (mínimo, es casi HTML) |
| ✅ **Content Collections para blog** — n8n genera .mdx, Astro lo convierte a HTML automáticamente | |
| ✅ **MDX nativo** — blog en Markdown con componentes incrustables | |
| ✅ **Tailwind CSS compilado** — sin CDN, sin `unsafe-inline`, CSP limpio | |
| ✅ **RSS y sitemap automáticos** | |
| ✅ **SEO nativo** — OpenGraph, JSON-LD por página, `canonical` automático | |
| ✅ **Netlify adapter** — deploy directo, funciones serverless coexisten | |
| ✅ **Build ultrarrápido** — < 1 segundo para tu número de páginas | |
| ✅ **Cero JS en cliente** — tu web de soporte IT carga instantáneo | |

**Veredicto: ✅ Elegida.** Astro es el framework ideal para un sitio de contenido/servicios como el tuyo.

---

## 📋 Stack detallado

### Frontend

| Capa | Tecnología | Justificación |
|------|-----------|---------------|
| **Framework** | Astro 5 | SSG → HTML estático. Componentes reutilizables. Build ultrarrápido |
| **Lenguaje** | TypeScript (opcional en .astro) | Tipado en data/services, no obligatorio en componentes simples |
| **CSS** | Tailwind CSS 4 (compilado vía `@astrojs/tailwind`) | Sin CDN, sin `unsafe-inline`. Clases utilitarias rápidas |
| **Blog** | Content Collections (`src/content/blog/*.mdx`) | n8n genera .mdx, Astro build lo convierte a HTML |
| **Iconos** | Lucide (SVG, sin JS) | Librería de iconos ligera, compatible con Astro |
| **Fuentes** | Google Fonts (vía CSS `@import` o descarga local) | Según se decida en BRAND.md (FASE 2) |

### Backend / Automatización

| Capa | Tecnología | Justificación |
|------|-----------|---------------|
| **Formularios** | Netlify Functions (proxy → n8n) | Ya existen, se reutilizan. El navegador nunca ve n8n |
| **Orquestador** | n8n (oculto, nunca expuesto) | Automatización de blog, respuestas, notificaciones por correo |
| **Blog automation** | n8n → GitHub API (commit .mdx) → Netlify deploy | Flujo aprobado: borrador → correo → click → publicado |
| **Mailing** | n8n email (SMTP) | Sin dependencia de SendGrid/Mailgun — n8n puede enviar directo |

### Hosting (Confirmado — no se re-evalúa)

| Capa | Proveedor | Detalle |
|------|-----------|---------|
| **Dominio** | Namecheap (Netlify DNS) | `jonathanesteban.dev` — sin cambios |
| **Hosting** | Netlify | Build: `astro build`, publish: `dist/`. Plan gratuito |
| **Functions** | Netlify Functions | Las 7 existentes se mantienen, se añaden las nuevas |
| **CI/CD** | Netlify (GitHub integration) | Auto-deploy al hacer push a `main` |

---

## 📐 Plan de migración HTML → Astro

| Paso | Archivos actuales | Destino en Astro | Esfuerzo | Riesgo |
|------|------------------|------------------|----------|--------|
| 1. Scaffold Astro | — | `astro init` (src/, public/, astro.config.mjs) | ✅ Bajo | Ninguno |
| 2. Layout base | `site/*.html` (header/footer comunes) | `src/layouts/BaseLayout.astro` | ⏳ Medio | Bajo — extraer el layout común de los HTMLs actuales |
| 3. Componentes | HTML suelto | `src/components/Nav.astro`, `Footer.astro`, `Hero.astro`, `ServiceCard.astro`, `AboutMe.astro`, `CTA.astro` | ⏳ Medio | Bajo — componentes pequeños y reutilizables |
| 4. Páginas principales | `site/index.html`, `site/sobre-mi/`, `site/contacto/`, `site/faq/` | `src/pages/index.astro`, `about.astro`, `contact.astro`, `faq.astro` | ✅ Bajo | Bajo — pasar contenido a .astro |
| 5. Páginas de servicios | `site/servicios/*.html` (6 existentes → 6 nuevas) | `src/pages/services/` | ⏳ Medio | Bajo — mismo contenido, distinto formato |
| 6. Proyectos históricos | `site/proyectos/` (TrackFlow, ClawMate, etc.) | `src/pages/legacy/` (o sección "Anteriores proyectos") | ✅ Bajo | Bajo — contenido que se reduce a una sección |
| 7. Páginas legales | `site/legal/*.html`, `site/privacy-policy/`, `site/terms-of-service/` | `src/pages/legal/` | ✅ Bajo | Ninguno |
| 8. Blog | No existe | `src/content/blog/` + `src/pages/blog/` + `src/pages/blog/[slug].astro` | ⏳ Medio | **Nuevo** — crear desde cero |
| 9. JSON-LD dinámico | Hardcodeado en HTML | `src/components/Seo.astro` (por página) | ✅ Bajo | Bajo — mejora respecto a hardcode |
| 10. sitemap.xml + RSS | `site/sitemap.xml` manual | Automático con `@astrojs/sitemap` | ✅ Bajo | Ninguno — Astro lo genera solo |
| 11. Tailwind compilado | CDN | `@astrojs/tailwind` | ✅ Bajo | Ninguno |
| 12. Netlify Functions | `functions/*.js` | Se mantienen igual (no se tocan) | ✅ Ninguno | Ninguno |
| 13. netlify.toml | Actualizar publish dir | `publish = "dist"` | ✅ Bajo | **Importante** — un solo cambio en config |
| 14. Assets estáticos | `site/assets/` (JS, CSS, images) | `public/assets/` | ✅ Bajo | Bajo — copiar y referenciar rutas nuevas |

**Esfuerzo total estimado:** 2-3 días de trabajo real.
**Estrategia:** Rama `refactor/v2` → migración progresiva → PR → revisión → merge a `main`.

---

## 📂 Estructura de carpetas propuesta (en Astro)

```
it-support-portfolio/
├── src/
│   ├── layouts/
│   │   └── BaseLayout.astro         # Header + Footer + SEO base
│   ├── components/
│   │   ├── Nav.astro                # Navegación principal
│   │   ├── Footer.astro             # Footer con datos contacto
│   │   ├── Hero.astro               # Sección hero home
│   │   ├── ServiceCard.astro        # Card de servicio (reutilizable)
│   │   ├── AboutMe.astro            # Componente "Sobre Mí"
│   │   ├── CTA.astro                # Call to action reutilizable
│   │   └── Seo.astro                # JSON-LD + OpenGraph
│   ├── pages/
│   │   ├── index.astro              # Home
│   │   ├── about.astro              # Sobre mí
│   │   ├── contact.astro            # Contacto + formulario
│   │   ├── faq.astro                # FAQ
│   │   ├── services/
│   │   │   ├── index.astro          # Todos los servicios
│   │   │   ├── helpdesk.astro       # Servicio 1
│   │   │   ├── reparacion.astro     # Servicio 2
│   │   │   ├── instalacion.astro    # Servicio 3
│   │   │   ├── redes.astro          # Servicio 4
│   │   │   ├── ofimatica.astro      # Servicio 5
│   │   │   └── licencias.astro      # Servicio 6 (NUEVO)
│   │   ├── blog/
│   │   │   ├── index.astro          # Listado de posts
│   │   │   └── [slug].astro         # Post individual
│   │   └── legal/
│   │       ├── aviso-legal.astro
│   │       ├── cookies.astro
│   │       └── privacidad.astro
│   ├── content/
│   │   ├── blog/                    # Posts en .mdx (n8n los genera aquí)
│   │   └── config.ts                # Content Collections config
│   └── data/
│       ├── cv.ts                    # Datos del CV (tipados)
│       └── services.ts             # 6 servicios (tipados, con precios)
├── public/
│   ├── assets/
│   │   ├── images/                  # Imágenes optimizadas
│   │   └── js/
│   │       └── tracking.js          # Script de tracking (existente)
│   ├── favicon.ico
│   └── robots.txt
├── functions/                       # Netlify Functions (sin cambios)
│   ├── contact-submit.js
│   ├── webhook-n8n.js
│   └── ... (resto igual)
├── astro.config.mjs                 # Config con adaptador Netlify
├── tailwind.config.mjs
├── tsconfig.json
├── netlify.toml
└── package.json
```

---

## ⚠️ Lo que NO cambia

| Aspecto | Se queda igual |
|---------|---------------|
| **Dominio** | `jonathanesteban.dev` en Namecheap |
| **Hosting** | Netlify |
| **Netlify Functions** | `functions/*.js` — se mantienen tal cual |
| **netlify.toml** | Solo cambia `publish` de `"site"` a `"dist"` y `functions` de `"functions"` |
| **Assets estáticos** | Imágenes, JS tracking, favicon |
| **SEO base** | JSON-LD, OpenGraph (mejorado, no reemplazado) |
| **Contenido textual** | Se traslada, no se reescribe (salvo reposicionamiento de marca) |

---

## 🚫 Lo que se elimina definitivamente

| Archivo/Ruta | Motivo |
|-------------|--------|
| `site/auth/facebook/callback/` | OAuth para dev/IA — no aplica a Soporte IT |
| `site/auth/tiktok/callback/` | OAuth para dev/IA — no aplica |
| `site/proyectos/` (páginas completas) | Se reducen a mención histórica en "Sobre Mí" |
| `site/servicios/desarrollo-web/` | No se ofrece |
| `site/servicios/automatizacion/` | No se ofrece |
| `site/assets/css/*.css` | Reemplazado por Tailwind compilado |
| Referencias CDN Tailwind | Reemplazado por compilación local |

---

## 📝 Notas técnicas importantes

### Tailwind compilado vs CDN
- **Antes:** `<script src="https://cdn.tailwindcss.com">` → CSP requiere `unsafe-inline`
- **Después:** `@astrojs/tailwind` → genera CSS estático → CSP limpio, sin dependencia externa

### Blog con Content Collections
- Los posts son archivos `.mdx` en `src/content/blog/`
- n8n genera el archivo + lo commitea a GitHub → Netlify detecta el push → build automático
- Cada post tiene: título, fecha, slug, meta description, tags, cuerpo en MDX
- Astro genera automáticamente: lista de posts, página individual, RSS, sitemap

### Formularios
- El formulario de contacto sigue yendo a Netlify Function (`contact-submit.js`)
- La función hace proxy al webhook oculto de n8n (el navegador nunca ve la URL de n8n)
- Rate limiting + honeypot ya implementados (se mantienen)

### Proyectos históricos
- TrackFlow, ClawMate, Talk to the Machine **no se borran** del repo
- En la web aparecen como una sección menor "Proyectos anteriores" en "Sobre Mí" o una página `/legacy`
- Los proyectos son reales y forman parte de tu trayectoria — no se ocultan, se ponen en contexto

---

## ✅ Decisión cerrada

```
FRAMEWORK:   Astro 5 (Static Site Generator)
CSS:         Tailwind CSS 4 compilado
BLOG:        Content Collections MDX
HOSTING:     Netlify (sin cambios)
FUNCTIONS:   Netlify Functions (sin cambios)
BACKEND:     n8n oculto (proxy vía Functions)
DOMINIO:     Namecheap → Netlify DNS
```

**Razón principal:** Astro combina lo mejor del HTML estático actual (cero JS, carga instantánea, SEO) con componentes reutilizables y un blog automatizado en MDX — todo sin el overhead de Next.js. El sitio de soporte IT debe cargar al instante, y con Astro eso es nativo.

---

## Referencias

- **AUDIT.md** — Auditoría técnica FASE 0
- **MARKET-ANALYSIS.md** — Investigación de mercado (6 servicios)
- **PLAN-AGENTE-v2.md** — Plan maestro del proyecto
- **CV-DATA.md** — Datos literales extraídos del CV

---

**Documento generado por:** Nova Sistema Multiagente
**Autorrevisión:** ✅ Stack evaluado contra AUDIT.md, 3 opciones analizadas con ventajas/desventajas, plan de migración detallado paso a paso, estructura de carpetas completa, riesgos identificados.

**ESPERANDO APROBACIÓN FASE 1 — ¿Confirmas Astro como framework?**