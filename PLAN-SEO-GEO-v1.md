# PLAN-SEO-GEO-v1.md
## Posicionamiento, GEO, accesibilidad y conversión — jonathanesteban.dev

> **Versión:** 1.0 · **Fecha:** 2026-10-18
> **Ejecutor:** agente de código (Antigravity / Claude / DeepSeek según tarea)
> **Product Owner:** Jonathan Esteban (valida cada fase)
> **Base:** auditoría SEO/GEO/UX del 2026-10-18 (ver §1) y `PLAN-AGENTE-v2.md`


## 📌 Estado de ejecución (2026-10-18)

| Fase | Estado | Nota |
|---|---|---|
| 1 Verificación en producción | ⏳ **Bloqueada** | Requiere deploy y acciones de Jonathan (Search Console, código de verificación, prueba del formulario real) |
| 2 SEO on-page | ✅ Código hecho | Metadatos reescritos, breadcrumbs, resumen citable, enlazado interno, OG por defecto |
| 3 SEO local y GEO | 🟡 Parcial | `llms.txt`, `Service`/`Article`/`Breadcrumb` JSON-LD hechos. **Pendiente:** Google Business Profile, reseñas, páginas por municipio (no creadas a propósito) |
| 4 Rendimiento y accesibilidad | 🟡 Parcial | Fuentes autoalojadas, CSP, caché, ARIA, contraste corregido. **Pendiente:** Lighthouse (no hay Chrome en el servidor; ejecutarlo en tu equipo/PageSpeed) |
| 5 Conversión | ⏳ **Pendiente decisión** | Requiere elegir analítica (Plausible/GA4) y testimonios reales autorizados |
| 6 Contenido | 🟡 Parcial | Clústeres y calendario en `docs/seo-keywords.md`; `Article` JSON-LD hecho. Los artículos nuevos pasan por el pipeline con aprobación humana |

---

## 0. Reglas del agente (inquebrantables)

1. **Nunca avanzar de fase sin validación explícita de Jonathan.**
2. **Privacidad:** no publicar dirección de casa ni coordenadas exactas. Base = *L'Hospitalet de Llobregat* + radio de desplazamiento.
3. **Marketing:** nunca escribir "sin local físico". Usar "servicio a domicilio y en remoto".
4. **Honestidad (E-E-A-T):** nada inventado — cifras, reseñas, clientes ni certificaciones. Fuente de verdad: `CV-DATA.md`. Si falta un dato, escribir `NO VERIFICADO`.
5. **No borrar archivos:** moverlos a `deprecated/` y pedir confirmación.
6. **Node:** usar Node ≥ 22.12 (`~/.nvm/versions/node/v24.20.0/bin`). El `/usr/bin/node` (v18) no sirve.
7. **Mapa:** Leaflet + teselas Esri World Street Map (sin API key). Nunca CARTO sin key ni Esri Dark Canvas. Modo oscuro = filtro CSS sobre `.leaflet-tile-pane`.
8. Cada tarea termina con: `npm run build` sin errores + entrada en `MEMORY.md`.
9. Los ficheros `.astro` pueden tener finales de línea CRLF: no usar `sed` con `$`; editar con herramientas de edición o Python normalizando `\r\n`.

---

## 1. Estado de partida (auditoría 2026-10-18)

### Ya corregido ✅
| Área | Cambio |
|---|---|
| Sitemap | `@astrojs/sitemap` instalado → `sitemap-index.xml` + `sitemap-0.xml` (excluye `/gracias/`, `/auth/`, `/certificaciones/`) |
| robots.txt | `Disallow` de rutas sin valor, `OAI-SearchBot` añadido, `Sitemap:` apunta a `sitemap-index.xml` |
| Canonicals | Absolutos vía `Layout.astro` (`abs()`); home y blog con canonical; bug `post.slug` → `post.id` |
| Open Graph | `og:image` absoluta |
| Indexación | Prop `noindex` en `Layout`; aplicada a gracias, auth y certificaciones |
| JSON-LD | `areaServed` = L'Hospitalet / Barcelona / Baix Llobregat; `priceRange`, `image`, `inLanguage` |
| Accesibilidad | Skip-link, `:focus-visible`, `prefers-reduced-motion`, `id="main-content"` en gracias y blog |
| Formulario | Redirección a `/gracias/?name=&email=`; modo simulado en dev local; eliminado listener duplicado a `/api/contact-submit` (daba 404) |
| Servicios | Dirección personal retirada del mapa; zona de cobertura + copy de marketing |

### Pendiente ⏳
Ver fases 1–6.

---

## 2. Fases

### FASE 1 — Verificación de base (bloqueante)
**Objetivo:** confirmar que lo ya hecho funciona en producción.

- [ ] Subir los cambios a `main` y esperar el deploy de Netlify.
- [ ] Comprobar `https://jonathanesteban.dev/sitemap-index.xml` y `/robots.txt` (HTTP 200, URLs absolutas con barra final).
- [ ] Enviar el sitemap en **Google Search Console** y **Bing Webmaster Tools**.
- [ ] **Jonathan:** corregir `google-site-verification` en `Layout.astro` (el valor actual `m7HiJ34wfzUNV` parece truncado). Copiarlo de Search Console.
- [ ] Inspeccionar con "Inspección de URL" la home, `/servicios/` y `/contacto/`.
- [ ] Probar el formulario en producción (función Netlify → n8n → Telegram) y confirmar redirección a `/gracias/`.

**Criterio de salida:** Search Console acepta el sitemap sin errores; `/gracias/` no aparece indexada.

### FASE 2 — SEO on-page
**Objetivo:** que cada URL tenga intención de búsqueda clara y metadatos únicos.

- [x] Tabla `keyword → URL` en `docs/seo-keywords.md` (una keyword principal por URL, sin canibalizar).
  - Ejemplos: `técnico informático a domicilio L'Hospitalet`, `reparación de ordenadores Barcelona`, `formatear PC a domicilio`, `configurar red wifi Barcelona`.
- [x] Revisar `<title>` (≤ 60 car.) y `description` (140–160 car.) de **todas** las páginas; cada una incluye keyword + ciudad + CTA.
- [x] Un único `<h1>` por página; jerarquía h2/h3 coherente. (`certificaciones` es redirección: se deja `noindex`.)
- [x] Enlazado interno: cada servicio enlaza a 2 artículos del blog y viceversa; breadcrumbs visibles.
- [x] Añadir `BreadcrumbList` JSON-LD (Layout, calculado desde `Astro.url`).
- [x] Imagen OG propia de 1200×630 por sección (home, servicios, blog) → `public/assets/img/og/`.
- [x] Imágenes: `width`/`height` explícitos, `loading="lazy"` salvo LCP, formato WebP/AVIF.

### FASE 3 — SEO local y GEO (motores generativos)
**Objetivo:** aparecer en Google Maps/local y ser citado por ChatGPT, Perplexity, Gemini y Claude.

- [ ] **Google Business Profile** como *negocio de área de servicio* (sin mostrar dirección): categoría "Servicio de reparación de ordenadores", zona L'Hospitalet + municipios del radio. *Acción de Jonathan.*
- [x] Crear `public/llms.txt` (resumen de servicios, zona, precios orientativos, contacto, enlaces a páginas clave) y `public/llms-full.txt` opcional.
- [x] `FAQPage` JSON-LD en `/faq/` y en cada página de servicio (preguntas reales: precio, tiempo, garantía 15 días, desplazamiento).
- [x] `Service` JSON-LD por página de servicio (`provider`, `areaServed`, `offers` con rango de precio real de `MARKET-ANALYSIS.md`).
- [x] Respuestas "citables": primer párrafo de cada servicio responde en 40–60 palabras a "qué es / cuánto cuesta / cuánto tarda".
- [ ] Páginas por zona (`/servicios/tecnico-informatico-hospitalet/`, `/…-cornella/`, `/…-esplugues/`…) solo si hay contenido útil y diferenciado (evitar *doorway pages*).
- [ ] NAP coherente (nombre, teléfono, email) en web, GBP, LinkedIn y directorios.
- [ ] Pedir reseñas reales tras cada servicio (enlace corto a GBP en el correo de cierre).

### FASE 4 — Rendimiento y accesibilidad (WCAG 2.2 AA)
**Objetivo:** Lighthouse ≥ 95 en Performance, Accesibilidad, SEO y Buenas prácticas.

- [ ] Ejecutar Lighthouse (móvil) sobre home, servicios, contacto, blog, post; guardar informes en `docs/lighthouse/`.
- [x] Fuentes: autoalojar Inter (`font-display: swap`, subset latin) y quitar `fonts.googleapis.com` (mejora LCP y RGPD).
- [x] Revisar contraste de color en modo claro y oscuro (≥ 4.5:1 texto, ≥ 3:1 UI).
- [x] Todos los controles con nombre accesible; hamburguesa con `aria-expanded` sincronizado; menú desplegable operable con teclado.
- [ ] Formulario: `aria-live="polite"` en errores, `aria-invalid`, `autocomplete` correcto, mensajes asociados con `aria-describedby`.
- [x] Mapa Leaflet: alternativa textual de la zona de cobertura (lista de municipios) para lectores de pantalla.
- [x] Cabeceras de caché en `netlify.toml` para `/assets/*` y `/_astro/*` (`immutable`, 1 año).
- [x] Revisar CSP en `netlify.toml`: añadir los orígenes de las teselas (`server.arcgisonline.com`) a `img-src`, y de Leaflet si se carga de CDN. **Si no, el mapa fallará en producción.**

### FASE 5 — Conversión (CRO) y confianza
**Objetivo:** convertir visitas en consultas.

- [ ] CTA principal consistente: "Pide presupuesto sin compromiso" + WhatsApp visible en móvil.
- [ ] Bloque de confianza: garantía 15 días, precios claros, respuesta < 24 h, atención a domicilio y en remoto.
- [ ] Página `/gracias/`: añadir evento de conversión (Plausible/GA4 con consentimiento) y siguiente paso claro.
- [ ] Copy de `/servicios/` revisado por intención de compra; evitar jerga.
- [ ] Prueba social **real**: solo testimonios autorizados por escrito. Si no hay, no incluir sección.
- [ ] Medición: analítica respetuosa con RGPD (Plausible o GA4 con Consent Mode v2) + banner de cookies ya existente.

### FASE 6 — Contenido y blog
**Objetivo:** autoridad temática (topical authority) en soporte IT local.

- [x] Calendario de 12 artículos en `blog-topic-bank.csv`, agrupados en clústeres: *PC lento*, *Wi-Fi/redes*, *seguridad/copias*, *Windows/Microsoft 365*.
- [ ] Cada artículo: autor visible, fecha de actualización, `Article` JSON-LD, FAQ, enlaces a servicio relacionado, imagen original.
- [x] Pipeline existente (`scripts/blog-pipeline.sh`) sigue con **aprobación humana** antes de publicar.
- [ ] Actualizar artículos antiguos cada 6 meses (`updatedDate`).

---

## 3. Mantenimiento de documentación (parte del trabajo del agente)

Al terminar **cada fase**, el agente debe actualizar:

| Archivo | Qué actualizar |
|---|---|
| `README.md` | Arquitectura, comandos y estado SEO |
| `astro-portfolio/AGENTS.md` y `CLAUDE.md` | Reglas del proyecto (mantenerlos idénticos) |
| `MEMORY.md` | Decisiones, hallazgos y "gotchas" nuevos (con fecha) |
| `TOOLS.md` | Herramientas/comandos nuevos o cambiados |
| `PLAN-SEO-GEO-v1.md` | Marcar casillas `[x]` y anotar fecha |

---

## 4. Definición de "hecho" por fase

1. `npm run build` termina sin errores ni *warnings* nuevos.
2. `dist/sitemap-0.xml` contiene solo URLs indexables con dominio absoluto.
3. Ninguna página indexable sin `<title>`, `description`, `canonical` ni `<h1>` único.
4. Documentación (§3) actualizada.
5. **Jonathan valida** y da paso a la siguiente fase.

---

## 5. Tareas que solo puede hacer Jonathan

- Corregir el código de verificación de Search Console.
- Crear y verificar Google Business Profile.
- Autorizar testimonios reales y pedir reseñas.
- Aprobar precios publicados y la lista de municipios del radio.
- Aprobar el borrador del blog antes de publicar.
