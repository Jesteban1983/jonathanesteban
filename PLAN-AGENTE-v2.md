# PLAN-AGENTE-v2.md
## Reestructuración de jonathanesteban.dev — Soporte IT

> **Versión:** 2.0 — incorpora las 5 decisiones cerradas tras la auditoría (`auditoria-plan-soporte-it.md`)
> **Ejecutor principal:** DeepSeek V4 Flash (orquestador, plan de pago vía 4Geeks Academy) — delega tareas de contenido a Qwen3.5 local / DeepSeek R1 local / Groq, **nunca** la Fase 5
> **Product Owner:** Jonathan Esteban
> **Objetivo:** Un sitio de soporte IT honesto (grounded en el CV real), con marca propia, blog semi-automatizado con aprobación humana, y una capa de seguridad que Jonathan pueda verificar él mismo sin ser experto en código.

### Qué cambió respecto a v1.0

| # | Decisión | v1.0 | v2.0 |
|---|---|---|---|
| 1 | Alcance | Mezclaba soporte IT con desarrollo/IA | 100% soporte IT; desarrollo queda, como mucho, en una frase |
| 2 | Hosting | Asumía migración a Vercel | Se queda en Netlify + Namecheap, sin migración |
| 3 | Ejecutor Fase 5 | Agente local Qwen 2.5 Coder | DeepSeek V4 Flash (orquestador) — regla explícita de no delegar esta fase |
| 4 | Instituciones | "EISIC" (typo) | ESIC Business & Marketing School |
| 5 | Garantía | No definida | 15 días desde la entrega del servicio |
| — | Nuevo | — | Fase de identidad de marca (logo propio, reutilizable en futuros proyectos) |
| — | Nuevo | — | Blog con automatización editorial + aprobación por correo + subida manual fácil |
| — | Nuevo | — | Checklist de fiscalización para que Jonathan verifique la Fase 5 sin leer código |
| — | Servicios | 5 servicios → 6 servicios (se añade "Licencias Originales Low-Cost" tras análisis de mercado) |
| — | Nuevo | — | Documento `MARKET-ANALYSIS.md` con investigación de mercado España/Europa/LATAM |

---

## 📌 ROL DEL AGENTE

Eres un **Senior Full-Stack Architect + Auditor Técnico + Diseñador de Marca**.
Ejecutas en fases. Cada fase termina con un artefacto `.md` (o archivos de diseño) que el Product Owner (Jonathan) valida antes de que pases a la siguiente.

**NUNCA avanzas sin validación explícita del humano.**

---

## 🚫 REGLAS INQUEBRANTABLES

1. **No modificas código en Fase 0 ni Fase 1.** Solo auditas y propones.
2. Cada hallazgo debe **citar `archivo:línea`** donde lo encontraste.
3. Si no tienes certeza de algo, escribe **"NO VERIFICADO"** y explica por qué.
4. **Nunca borras archivos.** Los marcas como `deprecated/` y esperas confirmación.
5. Toda propuesta tecnológica incluye: **ventaja, desventaja, coste de migración**.
6. Cada fase termina con el grito de guerra: **"ESPERANDO APROBACIÓN FASE X"**.
7. Si detectas un riesgo de seguridad crítico, **detente y avisa inmediatamente**.
8. **La Fase 5 (seguridad/n8n) la ejecutas tú directamente, orquestador principal. Nunca la delegas** a Qwen3.5 local, DeepSeek R1 local, ni a ningún sub-agente, aunque tu sistema lo haga por defecto en otras fases.
9. **Ningún contenido de blog se publica sin pasar por uno de dos caminos:** (a) borrador generado por ti → aprobación de Jonathan por correo, o (b) tema enviado directamente por Jonathan. Nunca publicas automáticamente sin ninguno de los dos.
10. **Cero cifras de experiencia infladas.** Ningún copy dice "X años de experiencia" salvo que esté literalmente sustentado por una fecha del CV. Ante la duda, se describe el hecho concreto, no un número redondo.
11. No migras de proveedor de hosting, dominio o DNS sin que Jonathan lo pida explícitamente.

---

## 🧭 METODOLOGÍA SENIOR (aplica a todas las fases de código)

- Commits atómicos, Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`).
- Nombres descriptivos, sin abreviar; cero código comentado "por si acaso".
- Comentarios solo donde la lógica no se explica sola.
- TypeScript sin `any` salvo que lo justifiques por escrito.
- Accesibilidad básica: `alt` en imágenes, labels en formularios, contraste suficiente, navegación por teclado.
- Un `README.md` que se actualiza al final de cada fase con: qué se hizo, qué decisiones se tomaron, cómo levantar el proyecto en local.
- Antes de pedir aprobación de cualquier fase, te autorrevisas con esta misma lista y lo dices explícitamente: *"Autorrevisión: [qué comprobaste]"*.

---

## 🗺️ ARQUITECTURA DEL PLAN

```
[FASE 0] AUDITORÍA TÉCNICA            → AUDIT.md
        ↓ (aprobación humana)
[FASE 1] DECISIÓN TECNOLÓGICA         → STACK.md
        ↓ (aprobación humana)
[FASE 2] IDENTIDAD DE MARCA           → BRAND.md + logo-v1/v2/v3.svg
        ↓ (aprobación humana)
[FASE 3] REESTRUCTURA DE CONTENIDO    → 100% Soporte IT (data + UI)
        ↓ (aprobación humana)
[FASE 4] BLOG + AUTOMATIZACIÓN        → /blog + flujo de aprobación por correo
        ↓ (aprobación humana)
[FASE 5] SEGURIDAD n8n + FISCALIZACIÓN→ Server Actions + webhooks + FISCALIZACION.md
        ↓ (aprobación humana, checklist 100%)
[FASE 6] QA + SEO + DEPLOY            → Producción en Netlify + Google Business Profile
```

---

## 🔍 FASE 0 — AUDITORÍA TÉCNICA

### Objetivo
Entender qué hay realmente en el repositorio antes de tocar nada — incluyendo el hosting real (Netlify), no el que asumía la v1.0.

### Comandos (en orden, documentando cada salida)

```bash
# 1. Estructura completa
find . -type f -not -path "*/node_modules/*" -not -path "*/.git/*" | head -100

# 2. Stack declarado
cat package.json 2>/dev/null
cat next.config.* 2>/dev/null
cat tsconfig.json 2>/dev/null
cat tailwind.config.* 2>/dev/null

# 3. Hosting real (Netlify, confirmado — no asumir Vercel)
cat netlify.toml 2>/dev/null
ls netlify/functions 2>/dev/null
cat _redirects 2>/dev/null

# 4. Contenido HTML/JSX real
find . -maxdepth 2 -name "*.html"
grep -rln "15+ años\|16+ años\|EISIC" --include="*.html" --include="*.md" --include="*.tsx" .

# 5. APIs y endpoints
grep -rn "fetch(" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" .
grep -rn "webhook\|n8n\|GROQ_API_KEY\|NEXT_PUBLIC_" . 2>/dev/null

# 6. Deuda técnica
grep -rn "TODO\|FIXME\|HACK" --include="*.js" --include="*.ts" .
```

Nota sobre el paso 4: busca explícitamente las cadenas que sabemos que hay que corregir (cifras de años infladas, el typo "EISIC") para que el `AUDIT.md` las cite con `archivo:línea` exacto, en vez de que alguien tenga que volver a buscarlas a mano en la Fase 3.

### Artefacto de salida: `AUDIT.md`

```markdown
# AUDIT — jonathanesteban.dev
Fecha: [auto]

## 1. Stack real detectado
- Framework / Hosting real: [HTML estático / Next.js / Netlify Functions]
- Evidencia: [archivo:línea]

## 2. Estructura de rutas
[Árbol de páginas y componentes]

## 3. Referencias a corregir ya detectadas
| Cadena | Archivo:línea | Acción |
|---|---|---|
| "15+ años" / "16+ años" | | Reescribir sin cifra (Fase 3) |
| "EISIC" | | Cambiar a "ESIC" (Fase 3) |
| Enlaces a TrackFlow / Talk to the Machine | | Retirar de nav/páginas principales (Fase 3) |

## 4. APIs y servicios externos
[fetch/webhooks detectados]

## 5. Deuda técnica
| Problema | Archivo | Severidad | Propuesta |

## 6. Riesgos de seguridad
[XSS, CSRF, exposición de .env, etc.]

## 7. Recomendación preliminar
[Qué se queda, qué se refactoriza, qué se migra]
```

### Criterio de aceptación
Jonathan lee `AUDIT.md` y responde **"FASE 0 OK"**.

---

## 🧭 FASE 1 — DECISIÓN TECNOLÓGICA

### Objetivo
Definir el stack definitivo. **Hosting ya decidido: Netlify, dominio en Namecheap — no se discute en esta fase.**

### Artefacto de salida: `STACK.md`

```markdown
# STACK DECISION

## Frontend
- Framework elegido: [justifica con base en AUDIT.md — si el sitio actual es HTML estático simple,
  evalúa también Astro como alternativa más ligera que Next.js antes de decidir; de cualquier modo
  debe correr sobre el runtime de Next.js de Netlify o ser un sitio estático servido por Netlify]
- Estilos: Tailwind CSS (compilado, nunca vía CDN)
- Blog: MDX con `next-mdx-remote` o `contentlayer` (o colección de contenido de Astro si se elige Astro)

## Backend / Automatización
- Server Actions / Netlify Functions para formularios
- n8n como orquestador de automatizaciones (nunca expuesto al cliente — ver Fase 5)

## Hosting (confirmado, no se re-evalúa)
- Netlify (sitio actual), dominio en Namecheap
- Sin migración a Vercel salvo que Jonathan lo pida explícitamente por escrito

## Migración
| Archivo actual | Destino | Esfuerzo | Riesgo |
|----------------|---------|----------|--------|
```

### Criterio de aceptación
Jonathan aprueba `STACK.md` — **solo entonces** se escribe código.

---

## 🎨 FASE 2 — IDENTIDAD DE MARCA

### Objetivo
Crear una marca personal — no un nombre de "servicio" — que acompañe a Jonathan en este y en futuros proyectos, más allá del soporte IT.

### Entrada
`STACK.md` aprobado.

### Tareas

1. Propón **3 conceptos de logo** en SVG, en un único archivo editable cada uno (variables CSS para color, fácil de recolorear):
   - Monograma con las iniciales ("JE").
   - Wordmark (el nombre completo, tipografía como protagonista).
   - Ícono abstracto simple + nombre al lado.
   - Ninguno debe llevar la palabra "soporte", "IT" ni similar en el propio logo — el logo es de **Jonathan**, no del servicio actual. El servicio puede tener un subtítulo/tagline aparte ("Soporte Informático") que sí cambie si el negocio cambia.
2. Propón una paleta de 2-3 colores + 1 tipografía de titulares + 1 de cuerpo, ambas de Google Fonts (licencia libre, cargables sin CDN de terceros problemático).
3. Documenta todo en `BRAND.md`: uso mínimo del logo, espacio de seguridad, versión en un solo color (para fondos oscuros/claros), paleta en hex con su uso previsto, tipografías, y 3-4 líneas sobre el tono de voz (cercano, directo, sin jerga técnica innecesaria — coherente con cómo ya hablas en el sitio).

### Artefacto de salida
`BRAND.md` + `brand/logo-v1.svg`, `brand/logo-v2.svg`, `brand/logo-v3.svg`

### Criterio de aceptación
Jonathan responde **"FASE 2 OK: uso el logo [1/2/3]"** (o pide ajustes puntuales antes de decidir).

---

## 🏗️ FASE 3 — REESTRUCTURA DE CONTENIDO (100% Soporte IT)

### Objetivo
Reposicionar la marca como técnico de soporte IT, aplicando la identidad de marca de la Fase 2, sin absolutamente nada que no esté sustentado por el CV real.

### Entrada
`BRAND.md` aprobado + repo limpio (rama `refactor/v2`).

### Tareas atómicas

| # | Tarea | Tipo | Detalle |
|---|-------|------|------|
| 3.1 | `data/cv.ts` con tipos TypeScript | Data | Datos extraídos literalmente del CV, sin inventar nada |
| 3.2 | `data/services.ts` con los 6 servicios | Data | Con palabras clave locales (Barcelona + L'Hospitalet + área metropolitana sur) |
| 3.3 | `<AboutMe />` con el copy reposicionado (ver abajo) | UI | Aplica tipografía/colores de `BRAND.md` |
| 3.4 | Retirar del nav y de las páginas principales: TrackFlow, Talk to the Machine, contenido de la era 4Geeks | UI | Si quieres, una sola frase breve queda en "Sobre mí" — nunca una página ni un ítem de menú |
| 3.5 | `<ServiceCard />` con CTA a `/contacto?servicio=X` | UI | |
| 3.6 | Sección/FAQ de garantía: 15 días desde la entrega del servicio | Data + UI | Debe quedar igual de redactada en FAQ, en condiciones del servicio y en cualquier presupuesto generado |
| 3.7 | Corregir "ESIC" (antes "EISIC") en todo el sitio, en el CV fuente y en PLAN-AGENTE | Contenido | ⚠️ El typo "EISIC" está en ambos PDFs de CV — corregir también ahí si se regeneran |
| 3.8 | Refactor de la home | Integración | |

### Copy actualizado para "Sobre Mí" (basado en el CV real)

> Soy **Jonathan Esteban**, técnico de soporte informático afincado en **Barcelona (L'Hospitalet de Llobregat)**.
>
> Mi primer contacto con la informática fue en **2006**, en unas prácticas de laboratorio de cómputo. Desde entonces trabajé como **Administrador Técnico en Locutorios de Internet** (2007-2012), donde hacía mantenimiento de equipos, instalación y configuración de sistemas operativos, resolución de incidencias de cableado y conectividad, y gestión básica de un servidor local.
>
> Tras unos años dedicado a otras actividades —administración de un negocio familiar y gestión operativa—, retomé el camino técnico con un **voluntariado en soporte operativo y gestión digital** (2024-2026), y actualmente curso **Sistemas Microinformáticos (FPLlefia)** para formalizar mi vuelta al sector.
>
> Mi enfoque es **resolutivo y cercano**: no solo resuelvo la incidencia, explico qué pasó y cómo evitarlo. Trabajo con entornos **Windows y Linux**, diagnostico redes TCP/IP, y ofrezco soporte **Helpdesk Nivel 1** con atención remota o presencial en el área metropolitana de Barcelona. Todo servicio incluye **15 días de garantía** desde la entrega.

**Datos de contacto verificados del CV:**
- Móvil: (34) 614 739 345
- Email: joonathanesteban@gmail.com
- Zona: Barcelona CP 08906 (L'Hospitalet) — cobertura presencial Barcelona + área metropolitana sur, remoto nacional

### Los 6 servicios principales para la web (basados en el CV real + análisis de mercado)

| # | Servicio | Sustento del CV / Mercado |
|---|----------|--------------------------|
| 1 | **Soporte Helpdesk Nivel 1** — Atención a usuarios, gestión de incidencias, asistencia remota/presencial | ✅ Competencia "Soporte y Helpdesk" + experiencia Locutorios (2007-2012) + Voluntariado Iglesia (2024-2026) |
| 2 | **Mantenimiento y Reparación de Ordenadores** — Montaje, mantenimiento preventivo/correctivo, diagnóstico hardware y software | ✅ Competencia "Sistemas y Hardware" + prácticas Laboratorio Cómputo (2006) + Locutorios |
| 3 | **Instalación y Configuración de Sistemas** — Windows, Linux, periféricos, software y licencias | ✅ Competencia directa del CV + exp. Locutorios 5.5 años instalando/configurando SO |
| 4 | **Diagnóstico y Configuración de Redes** — Routers, switches, cableado, protocolos TCP/IP | ✅ Competencia "Redes y Conectividad" + exp. Locutorios: "resolución de incidencias de cableado y conectividad" |
| 5 | **Soporte Ofimático y Migración a la Nube** — Microsoft 365, Google Workspace, bases de datos | ✅ Competencia "Productividad Ofimática" del CV |
| 6 | **Licencias Originales Low-Cost** — Asesoría, búsqueda de ofertas, instalación y configuración de licencias Microsoft 365, Office, Windows, antivirus. Sin vender claves — cobras por el servicio de consultoría + instalación | ✅ Mercado detectado: alta demanda en pymes que necesitan licencias baratas pero legales. Sustento CV: instalación/configuración de SO y periféricos + experiencia ESIC en ciberseguridad. Ver `MARKET-ANALYSIS.md` |

> **Servicios que NO se ofrecen** (no sustentados por el CV): Desarrollo web, Automatización con IA, Agentes MCP. La mención "ampliando conocimientos" en el CV no constituye un servicio.

### Servicios adicionales bajo demanda (no en web — se ofrecen en consulta/cotización)

Ver `MARKET-ANALYSIS.md` para detalle completo. Breve resumen:

| # | Servicio | Modalidad | Precio Base |
|---|----------|-----------|-------------|
| 7 | **Ciberseguridad Básica Pymes** — Antivirus, firewall, backups | Remoto+Presencial | 50€ setup |
| 8 | **Soporte para Teletrabajadores** — Configuración PC + VPN + M365 | Remoto | 60-80€ setup |
| 9 | **Digitalización de Comercios Locales** — PC + impresora + router + correo | Presencial (Barcelona) | 120€ pack |
| 10 | **Recuperación de Datos y Migración** — Discos dañados, PC→PC | Presencial+Remoto | 40-70€ |

### Copy actualizado para "Sobre Mí" (basado en CV)

> Soy **Jonathan Esteban**, técnico de soporte informático afincado en **Barcelona (L'Hospitalet de Llobregat)**.
> 
> Mi primer contacto con la informática fue en **2006**, en unas prácticas de laboratorio de cómputo. Desde entonces trabajé como **Administrador Técnico en Locutorios de Internet** (2007-2012), donde hacía mantenimiento de equipos, instalación y configuración de sistemas operativos, resolución de incidencias de cableado y conectividad, y gestión básica de un servidor local.
> 
> Tras unos años dedicado a otras actividades —administración de un negocio familiar y gestión operativa—, retomé el camino técnico con un **voluntariado en soporte operativo y gestión digital** (2024-2026), y actualmente curso **Sistemas Microinformáticos (FPLlefia)** para formalizar mi vuelta al sector.
> 
> Mi enfoque es **resolutivo y cercano**: no solo resuelvo la incidencia, explico qué pasó y cómo evitarlo. Trabajo con entornos **Windows y Linux**, diagnostico redes TCP/IP, y ofrezco soporte **Helpdesk Nivel 1** con atención remota o presencial en el área metropolitana de Barcelona. Todo servicio incluye **15 días de garantía** desde la entrega.

**Datos de contacto verificados del CV:**
- Móvil: (34) 614 739 345
- Email: joonathanesteban@gmail.com
- Zona: Barcelona CP 08906 (L'Hospitalet) — cobertura presencial Barcelona + área metropolitana sur, remoto nacional

### Objetivo
Publicar contenido con regularidad sin que Jonathan tenga que escribir código cada vez, pero **sin que nada se publique sin su aprobación o su propia mano**.

### Cadencia recomendada
**2 veces al mes (días 1 y 15)** como ritmo base — es más sostenible que 3 veces/mes para alguien que estudia y trabaja a la vez, y la constancia pesa más en SEO que el volumen puro. Déjalo configurable para subir a 3/mes en meses con más margen.

### Camino A — Borrador automático con aprobación por correo

1. **Disparador:** cron en n8n, días 1 y 15 de cada mes.
2. **Generación:** n8n llama al orquestador (DeepSeek V4 Flash) con un banco de temas + palabras clave locales (Barcelona) y genera: título, cuerpo en MDX, meta description.
3. **Aprobación:** n8n envía un correo a Jonathan con el borrador completo y dos enlaces de un solo uso, con token aleatorio y caducidad corta (24-48h): **"Aprobar y publicar"** / **"Rechazar"**.
4. **Publicación:** el enlace de aprobación llama a una función serverless que valida el token (un solo uso, no adivinable), hace commit del archivo `.mdx` vía la API de GitHub, y dispara el deploy de Netlify.
5. Si se rechaza, el borrador queda archivado en `/content/blog/drafts/` para revisión manual — nunca se borra automáticamente.

### Camino B — Jonathan sube un tema él mismo

1. Reutiliza tu cuenta ya existente de **Cognito Forms** (`jonathanesteban2`): un formulario simple — Título, Contenido, imagen opcional.
2. n8n recibe el envío vía webhook, lo convierte a `.mdx`, hace commit y dispara el deploy — **sin paso de aprobación por correo**, porque lo estás enviando tú mismo.
3. Por seguridad ante envíos accidentales: el correo de confirmación llega igual, con un botón de **"Cancelar publicación"** válido durante 10 minutos antes de que el deploy se dispare de verdad.

### Seguridad de los enlaces de aprobación/cancelación
- Token aleatorio (no un ID secuencial ni el título del post), de un solo uso, con caducidad.
- Validación siempre en el servidor, nunca solo en el frontend.
- Mismo patrón de "nunca expuesto al cliente" que el resto de webhooks de n8n (ver Fase 5).

### Artefacto de salida
- `/content/blog/*.mdx`, `app/blog/page.tsx`, `app/blog/[slug]/page.tsx`
- Workflow de n8n documentado en `BLOG-AUTOMATION.md` (diagrama simple: disparador → generación → aprobación → publicación)
- Formulario de Cognito Forms para subida manual

### Criterio de aceptación
- Un borrador automático completa el ciclo completo (correo → aprobación → publicado) de verdad, una vez, antes de dar la fase por buena.
- Un envío manual vía Cognito Forms completa su ciclo también.
- Slugs limpios, SEO dinámico por artículo, CTA a `/contacto` al final de cada uno.

---

## 🤖 FASE 5 — SEGURIDAD n8n (OCULTA) + FISCALIZACIÓN

> **Regla de esta fase, sin excepción: la ejecutas tú, el orquestador (DeepSeek V4 Flash). Nunca la delegas** a Qwen3.5 local, DeepSeek R1 local, ni a Groq, aunque tu sistema multiagente lo haga por defecto en otras fases. Dilo explícitamente al terminar: *"Fase 5 ejecutada directamente por el orquestador, sin delegación."*

### Objetivo
Automatizar formularios y flujos sin exponer n8n al cliente — y dejarle a Jonathan una forma de comprobarlo él mismo sin tener que leer código.

### Configuración (`.env.local`, nunca commiteado)

```env
N8N_WEBHOOK_CONTACT=https://tu-n8n/webhook/contacto
N8N_WEBHOOK_NEWSLETTER=https://tu-n8n/webhook/newsletter
N8N_WEBHOOK_BUDGET=https://tu-n8n/webhook/presupuesto
N8N_WEBHOOK_BLOG=https://tu-n8n/webhook/blog
```

### Requisitos técnicos (todos obligatorios)

1. **Server Action / Netlify Function como proxy.** El navegador nunca ve la URL de n8n.
2. **Ninguna variable con prefijo `NEXT_PUBLIC_`** si contiene un webhook, token o clave — ese prefijo las empaqueta en el bundle del cliente.
3. **Rate limiting con almacén persistente** (Upstash Redis, Netlify Blobs, o equivalente) — un contador en memoria no sirve en funciones serverless, porque cada invocación puede arrancar sin estado compartido.
4. **Honeypot** en el formulario de contacto (campo oculto que solo rellenan los bots).
5. **Validación server-side con Zod**, nunca confiar solo en la validación del navegador.
6. **Cabeceras de seguridad explícitas:** `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`.
7. **Si se registran visitas/IPs**, deben truncarse o hashearse, o declararse explícitamente en la Política de Privacidad con su base legal.

### Artefacto: `FISCALIZACION.md` — checklist para que Jonathan lo verifique él mismo

```markdown
# FISCALIZACION.md — Verificación de la Fase 5

Marca cada punto ✅/❌ con fecha. Ninguno requiere leer código.

- [ ] 1. Abre DevTools → pestaña Network. Envía el formulario de contacto.
      Confirma que NO aparece ninguna petición a una URL de n8n — solo a tu propio dominio.
- [ ] 2. Clic derecho → "Ver código fuente de la página". Busca (Ctrl+F) "n8n" o "webhook".
      No debe aparecer en ningún sitio.
- [ ] 3. Pídele al agente la lista de variables de entorno usadas. Confirma que ninguna
      que contenga un webhook, token o clave empieza por `NEXT_PUBLIC_`.
- [ ] 4. Envía el formulario de contacto 15-20 veces seguidas y rápido. Confirma que,
      pasado cierto número, se bloquea o aparece un mensaje de "demasiados intentos".
- [ ] 5. En DevTools → Network, clica la petición del documento principal (la primera
      de la lista) → pestaña "Headers" → "Response Headers". Confirma que aparecen
      Content-Security-Policy, Strict-Transport-Security y X-Frame-Options.
- [ ] 6. Pídele al agente un resumen de qué archivos tocó en esta fase. Abre 2-3 al azar:
      no hace falta entender cada línea, solo confirmar que no hay ninguna clave o URL
      de webhook escrita directamente en el código (debe venir siempre de una variable
      de entorno).
- [ ] 7. Revisa la Política de Privacidad: si hay registro de visitas, confirma que está
      descrito ahí.

**Solo cuando los 7 estén en ✅, responde "FASE 5 OK".**
```

### Criterio de aceptación
Los 7 puntos del checklist en ✅, firmados con fecha por Jonathan.

---

## ✅ FASE 6 — QA, SEO Y DEPLOY

### Checklist final

- [ ] Lighthouse ≥ 90 en Performance, SEO, Accessibility
- [ ] `sitemap.xml` sin URLs redirigidas (corrige el P0 ya detectado en la auditoría anterior)
- [ ] `robots.txt` correcto
- [ ] JSON-LD: `LocalBusiness` (home/servicios), `Service` (uno por cada uno de los 4), `FAQPage` (FAQ) — sin `Review`/`AggregateRating` hasta tener reseñas reales
- [ ] OpenGraph en cada página
- [ ] Google Business Profile: creado desde cero como **negocio de área de servicio**, categoría específica ("Servicio de reparación de ordenadores" o la más precisa disponible), NAP idéntico al del sitio
- [ ] Responsive verificado: 375px, 768px, 1440px
- [ ] `.env.local` fuera de git (`git check-ignore .env.local`)
- [ ] `FISCALIZACION.md` con los 7 puntos en ✅
- [ ] Deploy en **Netlify** (confirmado), dominio en Namecheap sin cambios

### Criterio de aceptación
Jonathan revisa el preview y aprueba el merge a `main`.

---

## 🚀 PROMPT INICIAL PARA EL AGENTE

```text
Eres un Senior Full-Stack Architect + Diseñador de Marca ejecutando un plan por fases.
Lee PLAN-AGENTE-v2.md completo antes de actuar.

TÚ ERES EL ORQUESTADOR PRINCIPAL (DeepSeek V4 Flash). Puedes delegar tareas de
contenido a tus sub-agentes (Qwen3.5 local, DeepSeek R1 local, Groq), EXCEPTO
la Fase 5 completa, que ejecutas tú directamente sin delegar — dilo explícitamente
al terminar esa fase.

REGLAS:
- Ejecutas UNA fase a la vez. Al terminar, entregas el artefacto y ESPERAS mi aprobación.
- No modificas código hasta que yo diga "FASE 1 OK".
- Cada hallazgo cita archivo:línea. Si no estás seguro, escribe "NO VERIFICADO".
- Ningún contenido de blog se publica sin aprobación por correo o envío directo mío.
- Cero cifras de experiencia que no estén literalmente en el CV.
- Hosting: Netlify + Namecheap. No propongas ni ejecutes una migración a otro proveedor.

Empieza ejecutando la FASE 0 (AUDITORÍA TÉCNICA). Devuélveme AUDIT.md.
```

---

## 🧠 DESAFÍOS TÉCNICOS (para el Product Owner)

1. ¿Por qué la Fase 5 nunca se delega a un sub-agente local, aunque el resto del plan sí pueda hacerlo?
2. En el flujo de aprobación del blog por correo, ¿qué pasaría si el enlace de aprobación fuera simplemente `?publicar=true` en vez de un token aleatorio de un solo uso? ¿Qué tipo de ataque habilita eso?
3. Si mañana cambias de "soporte IT" a otra cosa, ¿qué parte de la marca (Fase 2) seguiría sirviendo tal cual, y qué parte habría que rehacer?
4. En la Fase 4, el camino B (subida manual) se salta el correo de aprobación porque lo envías tú — pero sí mantiene una ventana de cancelación de 10 minutos. ¿Por qué tiene sentido ese matiz en vez de quitar toda fricción, o en vez de exigir el mismo proceso de aprobación que el camino A?

---

## 📋 HISTORIAL DE VERSIONES

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | — | Versión inicial del plan |
| 2.0 | 10 oct 2026 | Alcance 100% soporte IT; hosting confirmado en Netlify (sin Vercel); ejecutor DeepSeek V4 Flash con regla de no-delegación en Fase 5; ESIC corregido; garantía de 15 días; nueva Fase 2 de identidad de marca; Fase 4 con automatización editorial + aprobación por correo + subida manual vía Cognito Forms; Fase 5 con checklist de fiscalización no técnica |

---

**FIN DEL PLAN**
