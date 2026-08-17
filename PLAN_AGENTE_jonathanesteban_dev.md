# 🔧 PLAN COMPLETO DE REDISEÑO — jonathanesteban.dev
**Documento para agente IA — Ejecución fase por fase**
**Sitio actual:** https://jonathanesteban.dev  
**Stack:** HTML · CSS · JavaScript · Serverless Functions  
**Objetivo:** Corregir incongruencias, mejorar UX/UI, añadir submenús, desplegar demos en Vercel

---

> ⚠️ **AVISO PARA EL AGENTE:** Lee este documento completo antes de ejecutar cualquier cambio. Cada fase depende de la anterior. Haz un commit de git entre fases. No inventas contenido — usas solo el texto indicado o el que ya existe en el sitio.

---

## 📋 RESUMEN DE PROBLEMAS DETECTADOS

| # | Problema | Ubicación | Gravedad |
|---|----------|-----------|----------|
| 1 | "16+ años de experiencia" es FALSO | Home, Servicios, Sobre Mí, meta-tags | 🔴 Crítico |
| 2 | Navbar duplicado en el HTML (aparece dos veces) | Todas las páginas | 🔴 Crítico |
| 3 | Navbar no alineado al contenido, márgenes inconsistentes | Todas las páginas | 🟠 Alto |
| 4 | Servicios mezcla desarrollo web y soporte IT sin separación | /servicios/ | 🟠 Alto |
| 5 | No existe submenú de "Automatización con n8n + Composio" | /servicios/ | 🟠 Alto |
| 6 | Certificaciones es página separada, debe estar en Sobre Mí | /certificaciones/ | 🟡 Medio |
| 7 | Homepage repite la sección Proyectos y el falso "16 años" | / | 🟠 Alto |
| 8 | Proyectos sin demos en vivo (solo GitHub) | /proyectos/ | 🟡 Medio |
| 9 | Meta-descripción menciona "16+ años" — daña credibilidad | SEO head tags | 🟠 Alto |
| 10 | Stats "10+ Proyectos" y "100% Clientes satisfechos" — exagerado sin clientes reales | /servicios/ | 🟡 Medio |
| 11 | Sección "Formación & respaldo" en /servicios/ repite "16+ años Linux" | /servicios/ | 🟠 Alto |
| 12 | Página /certificaciones/ aparece en navbar principal como ítem separado | Nav | 🟡 Medio |

---

## 🏗️ ARQUITECTURA FINAL (estado deseado)

```
jonathanesteban.dev/
├── /                          → Home (hero + featured projects + CTA)
├── /servicios/                → Página principal de servicios (con submenús)
│   ├── /servicios/desarrollo-web/     → (ya existe)
│   ├── /servicios/automatizacion/     → (ya existe, ampliar)
│   └── /servicios/soporte-it/         → (ya existe)
├── /proyectos/                → Portfolio con demos en vivo
│   ├── /proyectos/trackflow/
│   ├── /proyectos/clawmate/
│   ├── /proyectos/talk-to-the-machine/
│   └── /proyectos/demo-app/   → Cinema Seat Manager
├── /sobre-mi/                 → Sobre Mí + Certificaciones integradas
├── /faq/
└── /contacto/
```

**NAVBAR FINAL (una sola línea):**
```
[Logo]  Servicios ▾   Proyectos   Sobre Mí   FAQ   Contacto   [Solicitar Presupuesto →]
```
> `Servicios` tiene un mega-dropdown con 3 categorías

---

## ━━━━━━━━━━━━━━━━━━━━━━━━
## FASE 1 — CORRECCIÓN DE CONTENIDO FALSO
## ━━━━━━━━━━━━━━━━━━━━━━━━

**Objetivo:** Eliminar toda referencia a "16+ años de experiencia" y reemplazarla por texto honesto y convincente.

### 1.1 — Archivo: `index.html` (Homepage)

**BUSCAR y REEMPLAZAR (todas las ocurrencias):**

```
ANTES:
  16+
  Años exp. operativa

DESPUÉS:
  5+
  Años en Soporte IT
```

```
ANTES (stat badge):
  16+

DESPUÉS: (eliminar este stat completamente o cambiarlo a:)
  2026
  Bootcamp 4Geeks
```

**En el hero/subtítulo, si dice:**
```
ANTES:
  "16+ años de experiencia operativa"
  
DESPUÉS:
  "Bootcamp AI Engineering · 4Geeks Academy Madrid"
```

---

### 1.2 — Archivo: `servicios/index.html`

**BUSCAR:**
```html
<strong>16+</strong> Años de experiencia operativa
```
**REEMPLAZAR:**
```html
<strong>5+</strong> Años en Soporte IT
```

**BUSCAR:**
```html
<strong>100%</strong> Clientes satisfechos
```
**REEMPLAZAR:**
```html
<strong>100%</strong> Compromiso con la calidad
```

**En la sección "Formación & respaldo", BUSCAR:**
```
🐧 Linux & VPS · 16+ años de experiencia
```
**REEMPLAZAR:**
```
🐧 Linux & VPS · Experiencia práctica avanzada
```

---

### 1.3 — Archivo: `sobre-mi/index.html`

**BUSCAR en el hero stats:**
```
16+
Años Experiencia Operativa
```
**REEMPLAZAR:**
```
5+
Años Soporte IT
```

**En la meta-description del `<head>`:**
```
ANTES:
  "Trayectoria profesional de 16+ años..."
DESPUÉS:
  "Desarrollador web en formación con experiencia en soporte IT. Bootcamp AI Engineering en 4Geeks Academy Madrid."
```

---

### 1.4 — Archivo `sobre-mi/index.html` — Sección Experiencia Laboral

La línea `2026 — Presente · Full-Stack Developer & AI Engineer` es ambigua porque suena como trabajo remunerado. Cambiar a:

```
ANTES:
  Full-Stack Developer & AI Engineer
  4Geeks Academy · Madrid

DESPUÉS:
  AI Engineering Bootcamp (en curso)
  4Geeks Academy · Madrid · 2025 – Presente
  Formación práctica: Python, FastAPI, React, Next.js, OpenClaw, n8n
```

---

### 1.5 — Todos los archivos `<head>` — Meta tags globales

En **cada página**, revisar `<meta name="description">` y `<title>` para eliminar "16+" y mensajes engañosos.

**Plantilla corregida para homepage:**
```html
<meta name="description" content="Jonathan Esteban — Desarrollador web en formación y técnico IT. Bootcamp AI Engineering en 4Geeks Madrid. Automatización con n8n y Composio. Proyectos reales con demos en vivo.">
<title>Jonathan Esteban | Desarrollador Web & Soporte IT · Madrid</title>
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━
## FASE 2 — NAVBAR: ELIMINAR DUPLICADO Y ALINEAR
## ━━━━━━━━━━━━━━━━━━━━━━━━

**Objetivo:** Un solo navbar limpio, alineado al contenido, con dropdown en Servicios.

### 2.1 — Diagnóstico del duplicado

En cada página existe este patrón (HAY DOS NAVBARS):
```html
<!-- NAV 1 (desktop) -->
<nav>
  <a href="/servicios/">Servicios</a>
  ...
</nav>

<!-- NAV 2 (mobile o alternativo) -->
<nav>
  <a href="/servicios/">Servicios & Presupuesto</a>
  ...
</nav>
```

**ACCIÓN:** Eliminar completamente el segundo bloque `<nav>` de todas las páginas. Conservar solo el primero y convertirlo en el único navbar responsivo.

---

### 2.2 — Estructura HTML del nuevo navbar (copiar exactamente)

```html
<header class="site-header">
  <nav class="navbar" role="navigation" aria-label="Navegación principal">
    <div class="navbar__inner">
      
      <!-- LOGO -->
      <a href="/" class="navbar__logo" aria-label="Jonathan Esteban - Inicio">
        Jonathan <span>Esteban</span>
      </a>

      <!-- LINKS DESKTOP -->
      <ul class="navbar__links" id="navbar-menu">
        
        <!-- SERVICIOS con mega-dropdown -->
        <li class="navbar__item navbar__item--dropdown">
          <button class="navbar__link navbar__dropdown-toggle" 
                  aria-expanded="false" 
                  aria-haspopup="true">
            Servicios <span class="navbar__arrow">▾</span>
          </button>
          <div class="navbar__dropdown" role="menu">
            <div class="navbar__dropdown-col">
              <span class="navbar__dropdown-label">💻 Desarrollo Web</span>
              <a href="/servicios/desarrollo-web/" role="menuitem">Sitios Web & Landing Pages</a>
              <a href="/servicios/desarrollo-web/#apis" role="menuitem">APIs REST & Backend</a>
            </div>
            <div class="navbar__dropdown-col">
              <span class="navbar__dropdown-label">⚙️ Automatización</span>
              <a href="/servicios/automatizacion/" role="menuitem">Agentes IA (OpenClaw)</a>
              <a href="/servicios/automatizacion/#n8n" role="menuitem">Flujos n8n</a>
              <a href="/servicios/automatizacion/#composio" role="menuitem">Composio & MCP</a>
            </div>
            <div class="navbar__dropdown-col">
              <span class="navbar__dropdown-label">🔧 Soporte IT</span>
              <a href="/servicios/soporte-it/" role="menuitem">Reparación de Ordenadores</a>
              <a href="/servicios/soporte-it/#mantenimiento" role="menuitem">Mantenimiento Preventivo</a>
              <a href="/servicios/soporte-it/#remoto" role="menuitem">Soporte Remoto & VPS</a>
            </div>
          </div>
        </li>

        <li class="navbar__item">
          <a href="/proyectos/" class="navbar__link">Proyectos</a>
        </li>
        <li class="navbar__item">
          <a href="/sobre-mi/" class="navbar__link">Sobre Mí</a>
        </li>
        <li class="navbar__item">
          <a href="/faq/" class="navbar__link">FAQ</a>
        </li>
        <li class="navbar__item">
          <a href="/contacto/" class="navbar__link">Contacto</a>
        </li>
      </ul>

      <!-- CTA BUTTON -->
      <a href="/contacto/" class="navbar__cta">Solicitar Presupuesto →</a>

      <!-- HAMBURGER (mobile) -->
      <button class="navbar__hamburger" 
              aria-label="Abrir menú" 
              aria-controls="navbar-menu"
              aria-expanded="false">
        <span></span><span></span><span></span>
      </button>

    </div>
  </nav>
</header>
```

---

### 2.3 — CSS del navbar (añadir/reemplazar en el CSS principal)

```css
/* ═══════════════════════════════════
   NAVBAR — Una sola línea, alineada
   ═══════════════════════════════════ */

:root {
  --nav-height: 64px;
  --content-max: 1200px;
  --nav-bg: #0f0f0f;        /* Fondo oscuro (ajusta a tu paleta) */
  --nav-border: #1e1e1e;
  --nav-text: #e2e8f0;
  --nav-text-hover: #ffffff;
  --nav-accent: #6366f1;    /* Color acento (tu color principal) */
  --nav-dropdown-bg: #161616;
  --nav-pad-x: 24px;        /* Padding horizontal igual al contenido */
}

/* Sticky header */
.site-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: var(--nav-bg);
  border-bottom: 1px solid var(--nav-border);
  box-shadow: 0 1px 12px rgba(0,0,0,0.4);
}

/* Navbar wrapper */
.navbar {
  width: 100%;
}

/* Alinear al mismo ancho que el contenido de la página */
.navbar__inner {
  max-width: var(--content-max);
  margin: 0 auto;
  padding: 0 var(--nav-pad-x);
  height: var(--nav-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

/* Logo */
.navbar__logo {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--nav-text);
  text-decoration: none;
  white-space: nowrap;
  flex-shrink: 0;
}
.navbar__logo span {
  color: var(--nav-accent);
}

/* Links desktop */
.navbar__links {
  display: flex;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 4px;
  flex: 1;
  justify-content: center;
}

.navbar__link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 8px 14px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--nav-text);
  text-decoration: none;
  border-radius: 6px;
  border: none;
  background: none;
  cursor: pointer;
  transition: color 0.2s, background 0.2s;
  white-space: nowrap;
}
.navbar__link:hover,
.navbar__link:focus-visible {
  color: var(--nav-text-hover);
  background: rgba(255,255,255,0.06);
}

/* Arrow icon */
.navbar__arrow {
  font-size: 0.65rem;
  transition: transform 0.2s;
}
.navbar__item--dropdown.is-open .navbar__arrow {
  transform: rotate(180deg);
}

/* CTA Button */
.navbar__cta {
  display: inline-flex;
  align-items: center;
  padding: 9px 18px;
  background: var(--nav-accent);
  color: #fff;
  font-size: 0.85rem;
  font-weight: 600;
  border-radius: 8px;
  text-decoration: none;
  white-space: nowrap;
  flex-shrink: 0;
  transition: opacity 0.2s, transform 0.15s;
}
.navbar__cta:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

/* ─── MEGA DROPDOWN ─── */
.navbar__item--dropdown {
  position: relative;
}

.navbar__dropdown {
  position: absolute;
  top: calc(100% + 12px);
  left: 50%;
  transform: translateX(-50%);
  min-width: 600px;
  background: var(--nav-dropdown-bg);
  border: 1px solid var(--nav-border);
  border-radius: 12px;
  padding: 24px;
  display: none;             /* JS toggles to flex */
  gap: 8px;
  box-shadow: 0 16px 40px rgba(0,0,0,0.5);
  z-index: 999;
}
.navbar__item--dropdown.is-open .navbar__dropdown {
  display: flex;
}

.navbar__dropdown-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.navbar__dropdown-label {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--nav-accent);
  padding: 0 12px 8px;
  border-bottom: 1px solid var(--nav-border);
  margin-bottom: 4px;
}

.navbar__dropdown a {
  padding: 8px 12px;
  font-size: 0.85rem;
  color: #94a3b8;
  text-decoration: none;
  border-radius: 6px;
  transition: color 0.2s, background 0.2s;
}
.navbar__dropdown a:hover {
  color: #fff;
  background: rgba(255,255,255,0.05);
}

/* ─── HAMBURGER (mobile) ─── */
.navbar__hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 36px;
  height: 36px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
}
.navbar__hamburger span {
  display: block;
  height: 2px;
  background: var(--nav-text);
  border-radius: 2px;
  transition: transform 0.25s, opacity 0.25s;
}

/* ─── RESPONSIVE ─── */
@media (max-width: 900px) {
  .navbar__links,
  .navbar__cta {
    display: none;
  }
  .navbar__hamburger {
    display: flex;
  }

  /* Mobile menu open */
  .navbar__links.is-open {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    position: fixed;
    top: var(--nav-height);
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--nav-bg);
    padding: 24px;
    gap: 8px;
    overflow-y: auto;
    z-index: 998;
  }
  .navbar__links.is-open .navbar__cta {
    display: inline-flex;
    margin-top: 16px;
    width: 100%;
    justify-content: center;
  }
  .navbar__dropdown {
    position: static;
    transform: none;
    min-width: 100%;
    box-shadow: none;
    border: none;
    padding: 8px 0 8px 16px;
    flex-direction: column;
  }
}

/* Asegurar que el contenido de página también tenga el mismo max-width */
.container,
.page-content,
main > section,
.hero__inner,
.section__inner {
  max-width: var(--content-max);
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--nav-pad-x);
  padding-right: var(--nav-pad-x);
}
```

---

### 2.4 — JavaScript del navbar (reemplazar el JS existente del nav)

```javascript
/* navbar.js — Dropdown accesible + hamburger */
(function () {
  const header = document.querySelector('.site-header');
  const hamburger = document.querySelector('.navbar__hamburger');
  const menu = document.getElementById('navbar-menu');
  const dropdownToggle = document.querySelector('.navbar__dropdown-toggle');
  const dropdownParent = document.querySelector('.navbar__item--dropdown');

  // ─── Hamburger ───
  hamburger?.addEventListener('click', () => {
    const isOpen = menu.classList.toggle('is-open');
    hamburger.setAttribute('aria-expanded', isOpen);
  });

  // ─── Dropdown Servicios (desktop) ───
  dropdownToggle?.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = dropdownParent.classList.toggle('is-open');
    dropdownToggle.setAttribute('aria-expanded', isOpen);
  });

  // Cerrar dropdown al hacer click fuera
  document.addEventListener('click', () => {
    dropdownParent?.classList.remove('is-open');
    dropdownToggle?.setAttribute('aria-expanded', 'false');
  });

  // Cerrar con Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      dropdownParent?.classList.remove('is-open');
      menu?.classList.remove('is-open');
    }
  });
})();
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━
## FASE 3 — REESTRUCTURAR PÁGINA /servicios/
## ━━━━━━━━━━━━━━━━━━━━━━━━

**Objetivo:** Separar visualmente los 3 bloques de servicios en secciones claramente diferenciadas con anclas. Añadir el nuevo servicio de Automatización.

### 3.1 — Nueva estructura de `/servicios/index.html`

Reemplazar la sección principal "Qué ofrezco" por esta estructura de 3 bloques:

```html
<main id="main-content">

  <!-- HERO DE SERVICIOS -->
  <section class="services-hero">
    <div class="section__inner">
      <span class="eyebrow">Qué ofrezco</span>
      <h1>Servicios digitales para <em>hacer crecer tu negocio</em></h1>
      <p>Elige la categoría que necesitas — o combínalas en la calculadora.</p>
      <!-- Tabs navegación interna -->
      <nav class="services-tabs" aria-label="Categorías de servicios">
        <a href="#desarrollo" class="services-tab services-tab--active">💻 Desarrollo Web</a>
        <a href="#automatizacion" class="services-tab">⚙️ Automatización IA</a>
        <a href="#soporte" class="services-tab">🔧 Soporte IT</a>
      </nav>
    </div>
  </section>

  <!-- ══════════════════════════════ -->
  <!-- BLOQUE 1: DESARROLLO WEB      -->
  <!-- ══════════════════════════════ -->
  <section id="desarrollo" class="services-block">
    <div class="section__inner">
      <div class="services-block__header">
        <span class="services-block__badge services-block__badge--dev">💻 Desarrollo Web</span>
        <h2>Presencia digital <em>profesional</em></h2>
        <p>Sitios web, aplicaciones y APIs construidos con tecnología moderna y orientados a resultados.</p>
      </div>

      <div class="services-grid">
        
        <!-- Servicio 1.1 -->
        <article class="service-card">
          <div class="service-card__icon">🌐</div>
          <h3>Sitios Web & Landing Pages</h3>
          <p>Web corporativa o landing page optimizada para SEO y velocidad. Responsive, accesible y lista para convertir visitantes.</p>
          <ul class="service-card__features">
            <li>Single & Multi-page apps</li>
            <li>SEO técnico optimizado</li>
            <li>Diseño responsive mobile-first</li>
            <li>Integración con formularios y CMS</li>
          </ul>
          <div class="service-card__footer">
            <span class="service-card__price">Desde 450 €</span>
            <a href="/servicios/desarrollo-web/" class="service-card__cta">Ver detalles →</a>
          </div>
        </article>

        <!-- Servicio 1.2 -->
        <article class="service-card">
          <div class="service-card__icon">⚡</div>
          <h3>APIs REST & Backend</h3>
          <p>Servicios backend robustos con FastAPI y Python. APIs documentadas, autenticadas y listas para escalar con tu negocio.</p>
          <ul class="service-card__features">
            <li>Endpoints RESTful documentados (Swagger)</li>
            <li>Autenticación JWT & OAuth2</li>
            <li>Base de datos PostgreSQL / Supabase</li>
            <li>Testing con Pytest</li>
          </ul>
          <div class="service-card__footer">
            <span class="service-card__price">Desde 750 €</span>
            <a href="/contacto/?subject=APIs+REST" class="service-card__cta">Consultar →</a>
          </div>
        </article>

        <!-- Servicio 1.3 -->
        <article class="service-card">
          <div class="service-card__icon">🎨</div>
          <h3>Aplicaciones Web Full-Stack</h3>
          <p>Aplicaciones completas con panel de administración, autenticación de usuarios y base de datos. Stack: Next.js + FastAPI.</p>
          <ul class="service-card__features">
            <li>Frontend con React / Next.js</li>
            <li>Panel de gestión / backoffice</li>
            <li>Autenticación y roles de usuario</li>
            <li>Despliegue en Vercel / Railway</li>
          </ul>
          <div class="service-card__footer">
            <span class="service-card__price">Desde 950 €</span>
            <a href="/servicios/desarrollo-web/" class="service-card__cta">Ver detalles →</a>
          </div>
        </article>

      </div>
    </div>
  </section>

  <!-- ══════════════════════════════ -->
  <!-- BLOQUE 2: AUTOMATIZACIÓN IA   -->
  <!-- ══════════════════════════════ -->
  <section id="automatizacion" class="services-block services-block--alt">
    <div class="section__inner">
      <div class="services-block__header">
        <span class="services-block__badge services-block__badge--ai">⚙️ Automatización con IA</span>
        <h2>Que las máquinas <em>trabajen por ti</em></h2>
        <p>Flujos inteligentes con n8n, agentes autónomos con OpenClaw y conexiones entre herramientas con Composio. Sin código repetitivo, sin intervención manual.</p>
      </div>

      <div class="services-grid">

        <!-- Servicio 2.1 -->
        <article class="service-card service-card--highlight">
          <div class="service-card__badge-new">NUEVO</div>
          <div class="service-card__icon">🔄</div>
          <h3>Automatización con n8n</h3>
          <p>Construyo flujos de trabajo automatizados visualmente con n8n. Conecta tus aplicaciones, elimina tareas manuales y trabaja más rápido.</p>
          <ul class="service-card__features">
            <li>Flujos de trabajo entre apps (CRM, email, Notion, Sheets)</li>
            <li>Automatización de captación de leads</li>
            <li>Notificaciones y alertas automáticas</li>
            <li>Integración con APIs externas</li>
          </ul>
          <div class="service-card__footer">
            <span class="service-card__price">Desde 300 €</span>
            <a href="/servicios/automatizacion/#n8n" class="service-card__cta">Ver ejemplos →</a>
          </div>
        </article>

        <!-- Servicio 2.2 -->
        <article class="service-card service-card--highlight">
          <div class="service-card__badge-new">NUEVO</div>
          <div class="service-card__icon">🔗</div>
          <h3>Integraciones con Composio</h3>
          <p>Conecta tu agente IA o tu aplicación con más de 150 herramientas: Gmail, Calendar, Drive, Notion, Slack, Telegram y mucho más.</p>
          <ul class="service-card__features">
            <li>Composio MCP para agentes autónomos</li>
            <li>Conexión con Google Workspace</li>
            <li>Automatización de comunicaciones</li>
            <li>Sincronización de datos entre plataformas</li>
          </ul>
          <div class="service-card__footer">
            <span class="service-card__price">Desde 400 €</span>
            <a href="/servicios/automatizacion/#composio" class="service-card__cta">Ver detalles →</a>
          </div>
        </article>

        <!-- Servicio 2.3 -->
        <article class="service-card service-card--highlight">
          <div class="service-card__icon">🤖</div>
          <h3>Agentes de IA con OpenClaw</h3>
          <p>Asistentes autónomos que gestionan tareas complejas: clasifican correos, responden clientes, actualizan bases de datos y coordinan flujos sin intervención humana.</p>
          <ul class="service-card__features">
            <li>Agentes OpenClaw personalizados</li>
            <li>Integración con tus herramientas actuales</li>
            <li>Pipelines Python + n8n</li>
            <li>Clasificación automática de incidencias</li>
          </ul>
          <div class="service-card__footer">
            <span class="service-card__price">Desde 850 €</span>
            <a href="/servicios/automatizacion/" class="service-card__cta">Ver servicio →</a>
          </div>
        </article>

      </div>
    </div>
  </section>

  <!-- ══════════════════════════════ -->
  <!-- BLOQUE 3: SOPORTE IT          -->
  <!-- ══════════════════════════════ -->
  <section id="soporte" class="services-block">
    <div class="section__inner">
      <div class="services-block__header">
        <span class="services-block__badge services-block__badge--it">🔧 Soporte IT Presencial</span>
        <h2>Tu equipo a punto, <em>sin complicaciones</em></h2>
        <p>Diagnóstico, reparación y mantenimiento de ordenadores en Madrid y Barcelona. Recogida y entrega a domicilio.</p>
      </div>

      <div class="services-grid services-grid--4">

        <!-- Servicio 3.1 -->
        <article class="service-card service-card--sm">
          <span class="service-card__mode">Presencial</span>
          <div class="service-card__icon">🧹</div>
          <h3>Formateo & Virus</h3>
          <p>Instalación limpia, eliminación de malware y configuración profesional. Copia de seguridad incluida.</p>
          <a href="/servicios/soporte-it/" class="service-card__cta">Ver más →</a>
        </article>

        <article class="service-card service-card--sm">
          <span class="service-card__mode">Presencial</span>
          <div class="service-card__icon">🔧</div>
          <h3>Mantenimiento Preventivo</h3>
          <p>Limpieza interna, revisión de componentes y optimización de rendimiento. Incluye informe técnico.</p>
          <a href="/servicios/soporte-it/" class="service-card__cta">Ver más →</a>
        </article>

        <article class="service-card service-card--sm">
          <span class="service-card__mode">Presencial</span>
          <div class="service-card__icon">🖥️</div>
          <h3>Reparación de Ordenadores</h3>
          <p>Hardware y software. Pantallas, componentes, diagnóstico gratuito. Portátiles y sobremesa.</p>
          <a href="/servicios/soporte-it/" class="service-card__cta">Ver más →</a>
        </article>

        <article class="service-card service-card--sm">
          <span class="service-card__mode">Remoto</span>
          <div class="service-card__icon">☁️</div>
          <h3>Soporte Remoto & VPS</h3>
          <p>Administración Linux, gestión de incidencias, migración de datos y soporte técnico continuo.</p>
          <a href="/servicios/soporte-it/#remoto" class="service-card__cta">Ver más →</a>
        </article>

      </div>
    </div>
  </section>

  <!-- [Mantener la sección de metodología "Cómo trabajo" y la calculadora como estaban] -->

</main>
```

### 3.2 — CSS adicional para los bloques de servicios

```css
/* ─── Tabs de categorías ─── */
.services-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 32px;
}
.services-tab {
  padding: 10px 20px;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  color: #94a3b8;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  transition: all 0.2s;
}
.services-tab:hover,
.services-tab--active {
  color: #fff;
  background: var(--nav-accent);
  border-color: transparent;
}

/* ─── Bloques alternos ─── */
.services-block { padding: 80px 0; }
.services-block--alt { background: rgba(255,255,255,0.02); }

.services-block__header {
  text-align: center;
  max-width: 680px;
  margin: 0 auto 56px;
}

.services-block__badge {
  display: inline-block;
  padding: 6px 16px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 16px;
}
.services-block__badge--dev  { background: #1e3a5f; color: #60a5fa; }
.services-block__badge--ai   { background: #2d1f5e; color: #a78bfa; }
.services-block__badge--it   { background: #1a3a2a; color: #4ade80; }

/* ─── Grid de servicios ─── */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}
.services-grid--4 {
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

/* ─── Tarjeta de servicio ─── */
.service-card {
  position: relative;
  background: #111;
  border: 1px solid #1e1e1e;
  border-radius: 16px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: border-color 0.2s, transform 0.2s;
}
.service-card:hover {
  border-color: var(--nav-accent);
  transform: translateY(-4px);
}
.service-card--highlight {
  border-color: rgba(99,102,241,0.3);
}
.service-card--sm {
  padding: 20px;
}

.service-card__badge-new {
  position: absolute;
  top: 16px;
  right: 16px;
  background: var(--nav-accent);
  color: #fff;
  font-size: 0.65rem;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 9999px;
  letter-spacing: 0.1em;
}

.service-card__icon {
  font-size: 2rem;
  line-height: 1;
}
.service-card h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
}
.service-card p {
  font-size: 0.875rem;
  color: #94a3b8;
  line-height: 1.6;
}
.service-card__features {
  list-style: none;
  padding: 0;
  margin: 8px 0 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.service-card__features li::before {
  content: "✓ ";
  color: var(--nav-accent);
  font-weight: 700;
}
.service-card__features li {
  font-size: 0.8rem;
  color: #cbd5e1;
}
.service-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid #1e1e1e;
}
.service-card__price {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--nav-accent);
}
.service-card__cta {
  font-size: 0.8rem;
  color: #94a3b8;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}
.service-card__cta:hover { color: #fff; }

.service-card__mode {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #4ade80;
  background: rgba(74,222,128,0.1);
  padding: 2px 10px;
  border-radius: 9999px;
  display: inline-block;
  margin-bottom: 4px;
}
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━
## FASE 4 — INTEGRAR CERTIFICACIONES EN /sobre-mi/
## ━━━━━━━━━━━━━━━━━━━━━━━━

**Objetivo:** Mover el contenido de `/certificaciones/` a una sección dentro de `/sobre-mi/`. Mantener la URL `/certificaciones/` solo como redirección o eliminarla del navbar.

### 4.1 — En `/sobre-mi/index.html`

Añadir esta sección DESPUÉS de la sección de Habilidades Técnicas:

```html
<!-- SECCIÓN CERTIFICACIONES dentro de Sobre Mí -->
<section id="certificaciones" class="about-section">
  <div class="section__inner">
    
    <div class="section-header">
      <span class="eyebrow">Formación Continua</span>
      <h2>🏅 Certificaciones & Formación</h2>
      <p>Aprendizaje constante y acreditaciones que respaldan mi trabajo.</p>
    </div>

    <!-- Bootcamp destacado -->
    <div class="cert-featured">
      <div class="cert-featured__icon">🎓</div>
      <div class="cert-featured__info">
        <h3>AI Engineering — Full Stack + IA</h3>
        <span class="cert-featured__school">4Geeks Academy · Madrid, España · 2025 – Presente</span>
        <div class="cert-progress">
          <div class="cert-progress__bar">
            <div class="cert-progress__fill" style="width: 71%"></div>
          </div>
          <span>71% completado · 194 / 273 tareas · 4/6 hitos</span>
        </div>
        <p>Python, FastAPI, React, Next.js, PostgreSQL, OpenClaw, Composio MCP, n8n</p>
      </div>
    </div>

    <!-- Grid de certificaciones -->
    <div class="certs-grid">

      <div class="cert-card">
        <div class="cert-card__icon">🎨</div>
        <div class="cert-card__info">
          <h4>Frontend HTML5 / CSS3 / JS</h4>
          <span>Fundación Adecco · Nov 2025 · 30h</span>
        </div>
      </div>

      <div class="cert-card">
        <div class="cert-card__icon">🗄️</div>
        <div class="cert-card__info">
          <h4>Bases de Datos (SQL)</h4>
          <span>Fundación Adecco · Nov 2025 · 30h</span>
        </div>
      </div>

      <div class="cert-card">
        <div class="cert-card__icon">☕</div>
        <div class="cert-card__info">
          <h4>Java SE Básico</h4>
          <span>Fundación Adecco · Ago 2025 · 30h</span>
        </div>
      </div>

      <div class="cert-card">
        <div class="cert-card__icon">🔧</div>
        <div class="cert-card__info">
          <h4>Desarrollo Back-End Básico</h4>
          <span>Min. Trabajo Perú · May 2025 · Nota: 17/20</span>
        </div>
      </div>

      <div class="cert-card">
        <div class="cert-card__icon">🌐</div>
        <div class="cert-card__info">
          <h4>Diseño Web HTML5 + CSS</h4>
          <span>Fundación Telefónica · Dic 2024 · 30h</span>
        </div>
      </div>

      <div class="cert-card">
        <div class="cert-card__icon">🛡️</div>
        <div class="cert-card__info">
          <h4>Ciberseguridad Básica</h4>
          <span>ESIC Business & Marketing · Nov 2024</span>
        </div>
      </div>

      <div class="cert-card">
        <div class="cert-card__icon">🖥️</div>
        <div class="cert-card__info">
          <h4>Reparación de Computadoras</h4>
          <span>Instituto SISE · 2007</span>
        </div>
      </div>

    </div>
  </div>
</section>
```

### 4.2 — CSS para certificaciones

```css
/* Certificaciones dentro de Sobre Mí */
.cert-featured {
  display: flex;
  gap: 24px;
  background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.05));
  border: 1px solid rgba(99,102,241,0.25);
  border-radius: 16px;
  padding: 28px;
  margin-bottom: 32px;
}
.cert-featured__icon { font-size: 3rem; }
.cert-featured h3 { font-size: 1.2rem; font-weight: 700; color: #fff; margin-bottom: 4px; }
.cert-featured__school { font-size: 0.85rem; color: #94a3b8; }

.cert-progress {
  margin: 12px 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.cert-progress__bar {
  height: 6px;
  background: rgba(255,255,255,0.1);
  border-radius: 9999px;
  overflow: hidden;
}
.cert-progress__fill {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  border-radius: 9999px;
}
.cert-progress span { font-size: 0.75rem; color: #64748b; }

.certs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}
.cert-card {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  background: #111;
  border: 1px solid #1e1e1e;
  border-radius: 12px;
  padding: 16px;
  transition: border-color 0.2s;
}
.cert-card:hover { border-color: rgba(99,102,241,0.4); }
.cert-card__icon { font-size: 1.5rem; flex-shrink: 0; }
.cert-card h4 { font-size: 0.9rem; font-weight: 600; color: #e2e8f0; margin-bottom: 4px; }
.cert-card span { font-size: 0.75rem; color: #64748b; }
```

### 4.3 — Actualizar el navbar

En la lista `<ul class="navbar__links">`, ELIMINAR el item de Certificaciones:
```html
<!-- ELIMINAR ESTA LÍNEA del navbar: -->
<li class="navbar__item"><a href="/certificaciones/" class="navbar__link">Certificaciones</a></li>
```

En la página `/sobre-mi/`, actualizar el link de "Certificaciones" en el mega-menú del dropdown de servicios si aparece, y añadir un anchor link dentro de Sobre Mí:
```
Sobre Mí → /sobre-mi/
  └── #certificaciones → Certificaciones & Formación
```

### 4.4 — Redirección de /certificaciones/

Si el servidor lo permite, añadir una redirección 301:
```
/certificaciones/ → /sobre-mi/#certificaciones
```
Si es un generador estático, en `/certificaciones/index.html` añadir en el `<head>`:
```html
<meta http-equiv="refresh" content="0; url=/sobre-mi/#certificaciones">
<link rel="canonical" href="https://jonathanesteban.dev/sobre-mi/#certificaciones">
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━
## FASE 5 — HOMEPAGE: ELIMINAR REDUNDANCIA
## ━━━━━━━━━━━━━━━━━━━━━━━━

### 5.1 — Eliminar stat "16 años" del hero

En `index.html`, la sección de stats del hero:
```html
<!-- ELIMINAR COMPLETAMENTE este stat: -->
<div class="stat">
  <span class="stat__number">16+</span>
  <span class="stat__label">Años exp. operativa</span>
</div>

<!-- REEMPLAZAR POR: -->
<div class="stat">
  <span class="stat__number">2025</span>
  <span class="stat__label">Bootcamp 4Geeks</span>
</div>
```

### 5.2 — Limpiar la sección "Proyectos Destacados" de Home

La homepage NO debe mostrar todos los proyectos. Solo los 2 más impactantes con un CTA claro.

**CONSERVAR solo:**
1. TrackFlow (estado: En desarrollo — cambiar a "Proyecto actual")
2. Talk to the Machine (con link a la demo en Vercel — ver Fase 6)

**ELIMINAR de home:** ClawMate y Cinema Seat Manager (estos van en /proyectos/)

**Texto de enlace al final:**
```html
<div class="projects-cta">
  <a href="/proyectos/" class="btn btn--outline">
    Ver todos los proyectos con demos →
  </a>
</div>
```

### 5.3 — Añadir sección "Por qué trabajar conmigo" (nueva, entre hero y proyectos)

```html
<section class="why-me">
  <div class="section__inner">
    <div class="why-me__grid">
      
      <div class="why-me__item">
        <span class="why-me__icon">🎯</span>
        <h3>Orientado a resultados</h3>
        <p>No solo entrego código — entrego soluciones que funcionan para tu negocio.</p>
      </div>

      <div class="why-me__item">
        <span class="why-me__icon">⚡</span>
        <h3>Stack moderno</h3>
        <p>Next.js, FastAPI, Python, n8n, Composio. Tecnología actual, no legado.</p>
      </div>

      <div class="why-me__item">
        <span class="why-me__icon">🤝</span>
        <h3>Comunicación clara</h3>
        <p>Propuesta detallada, actualizaciones frecuentes y presupuesto cerrado antes de empezar.</p>
      </div>

      <div class="why-me__item">
        <span class="why-me__icon">🌍</span>
        <h3>Disponible globalmente</h3>
        <p>Trabajo remoto internacional. Madrid, Barcelona o donde lo necesites.</p>
      </div>

    </div>
  </div>
</section>
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━
## FASE 6 — PROYECTOS: DEMOS EN VIVO (VERCEL)
## ━━━━━━━━━━━━━━━━━━━━━━━━

### 6.1 — Proyectos a desplegar en Vercel

| Proyecto | Repo | Tipo | Variables de entorno necesarias |
|----------|------|------|--------------------------------|
| Talk to the Machine | github.com/4GeeksAcademy/Jesteban1983-talk-to-the-machine | Next.js | `GROQ_API_KEY` |
| Cinema Seat Manager | (ver repo en GitHub) | Vite + TypeScript | Ninguna |
| TrackFlow | github.com/4GeeksAcademy/Jesteban1983-TrackFlow | Next.js + FastAPI | En desarrollo |

### 6.2 — Pasos para desplegar Talk to the Machine en Vercel

```bash
# 1. Clonar el repositorio localmente
git clone https://github.com/4GeeksAcademy/Jesteban1983-talk-to-the-machine.git
cd Jesteban1983-talk-to-the-machine

# 2. Verificar que funciona localmente
npm install
npm run dev

# 3. Asegurarse de que el proyecto tiene:
#    - next.config.js o next.config.ts
#    - Un archivo .env.example con: GROQ_API_KEY=

# 4. En el repo de GitHub:
#    - Hacer fork a tu cuenta personal (Jesteban1983)
#    - O crear un repo nuevo: jonathanesteban1983/talk-to-the-machine

# 5. En Vercel (vercel.com):
#    - "Add New Project"
#    - Importar desde GitHub
#    - Framework: Next.js (autodetectado)
#    - En "Environment Variables" añadir: GROQ_API_KEY = [tu clave de Groq]
#    - Deploy
#    
#    URL resultante: talk-to-the-machine-xxx.vercel.app
#    Configurar dominio personalizado: demo-chat.jonathanesteban.dev (opcional)
```

### 6.3 — Pasos para desplegar Cinema Seat Manager en Vercel

```bash
# Si el proyecto usa Vite:
# 1. Verificar que package.json tiene:
{
  "scripts": {
    "build": "vite build",
    "preview": "vite preview"
  }
}

# 2. En Vercel:
#    - Framework: Vite (autodetectado)
#    - Build Command: npm run build
#    - Output Directory: dist
#    - Sin variables de entorno
#    Deploy

# URL: cinema-seat-xxx.vercel.app
```

### 6.4 — Actualizar tarjetas de proyectos en /proyectos/index.html

```html
<!-- TALK TO THE MACHINE — añadir/actualizar botón de demo -->
<a href="https://[URL-VERCEL-TALK-TO-MACHINE]" 
   class="project-card__demo" 
   target="_blank" 
   rel="noopener">
  🚀 Demo en vivo →
</a>

<!-- CINEMA SEAT MANAGER — añadir/actualizar botón de demo -->
<a href="https://[URL-VERCEL-CINEMA]" 
   class="project-card__demo"
   target="_blank"
   rel="noopener">
  🎬 Probar demo →
</a>
```

### 6.5 — Añadir sección de Stack tecnológico visual a /proyectos/

```html
<!-- Añadir al inicio de /proyectos/, después del hero -->
<section class="tech-stack">
  <div class="section__inner">
    <p class="tech-stack__label">Tecnologías que uso en mis proyectos</p>
    <div class="tech-stack__grid">
      <!-- Cada badge con logo e nombre -->
      <span class="tech-badge">⚛️ React</span>
      <span class="tech-badge">▲ Next.js</span>
      <span class="tech-badge">🐍 Python</span>
      <span class="tech-badge">⚡ FastAPI</span>
      <span class="tech-badge">🗄️ PostgreSQL</span>
      <span class="tech-badge">☁️ Supabase</span>
      <span class="tech-badge">⚙️ n8n</span>
      <span class="tech-badge">🔗 Composio</span>
      <span class="tech-badge">🤖 OpenClaw</span>
      <span class="tech-badge">🐳 Docker</span>
      <span class="tech-badge">▲ Vercel</span>
    </div>
  </div>
</section>
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━
## FASE 7 — NUEVA PÁGINA /servicios/automatizacion/ (ampliar)
## ━━━━━━━━━━━━━━━━━━━━━━━━

**La página ya existe. Ampliarla con 2 secciones nuevas:**

### 7.1 — Sección n8n (añadir anchor `#n8n`)

```html
<section id="n8n" class="automation-section">
  <div class="section__inner">
    
    <div class="automation-header">
      <img src="/assets/img/logos/n8n-logo.svg" alt="n8n" class="automation-logo" width="60">
      <div>
        <h2>Automatización con <em>n8n</em></h2>
        <p>n8n es una plataforma open-source de automatización de flujos de trabajo. Sin escribir código, conecto tus aplicaciones y diseño procesos que se ejecutan solos.</p>
      </div>
    </div>

    <div class="automation-examples">
      <h3>Ejemplos de flujos que puedo construir</h3>
      <div class="examples-grid">
        
        <div class="example-card">
          <span class="example-card__num">01</span>
          <h4>Captación automática de leads</h4>
          <p>Un formulario de contacto dispara: notificación en Slack, registro en Notion/Airtable, email personalizado al lead y tarea en tu CRM.</p>
        </div>

        <div class="example-card">
          <span class="example-card__num">02</span>
          <h4>Sincronización de inventario</h4>
          <p>Cuando el stock en tu tienda cae por debajo del mínimo, se genera automáticamente un pedido y se notifica al proveedor por email.</p>
        </div>

        <div class="example-card">
          <span class="example-card__num">03</span>
          <h4>Gestión de incidencias IT</h4>
          <p>Un email de soporte se clasifica automáticamente, se asigna prioridad y se registra en el sistema de tickets sin intervención humana.</p>
        </div>

        <div class="example-card">
          <span class="example-card__num">04</span>
          <h4>Informes automáticos</h4>
          <p>Cada lunes a las 9:00, se genera un informe de métricas de la semana y se envía por email al equipo directivo.</p>
        </div>

      </div>
    </div>

  </div>
</section>
```

### 7.2 — Sección Composio (añadir anchor `#composio`)

```html
<section id="composio" class="automation-section automation-section--alt">
  <div class="section__inner">

    <div class="automation-header">
      <img src="/assets/img/logos/composio-logo.svg" alt="Composio" class="automation-logo" width="60">
      <div>
        <h2>Integraciones con <em>Composio</em></h2>
        <p>Composio es la capa de integración que conecta agentes de IA con más de 150 herramientas. Permite a un agente IA leer emails, crear eventos en Calendar, publicar en Slack o editar archivos en Drive — de forma autónoma.</p>
      </div>
    </div>

    <div class="composio-integrations">
      <h3>Herramientas disponibles para conectar</h3>
      <div class="integrations-tags">
        <span>📧 Gmail</span>
        <span>📅 Google Calendar</span>
        <span>📁 Google Drive</span>
        <span>💬 Slack</span>
        <span>📱 Telegram</span>
        <span>📋 Notion</span>
        <span>🔧 GitHub</span>
        <span>📊 Airtable</span>
        <span>🛒 Shopify</span>
        <span>📞 Twilio</span>
        <span>➕ +140 más</span>
      </div>
    </div>

    <div class="composio-use-case">
      <h3>Caso de uso real — ClawMate</h3>
      <p>Mi proyecto ClawMate conecta un agente IA (OpenClaw) con Gmail, Calendar, Drive y Telegram mediante Composio MCP. El agente puede leer emails, agendar reuniones, buscar archivos y enviar mensajes — sin intervención humana.</p>
      <a href="/proyectos/clawmate/" class="btn btn--primary">Ver el proyecto completo →</a>
    </div>

  </div>
</section>
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━
## FASE 8 — MEJORAS GENERALES DE DISEÑO
## ━━━━━━━━━━━━━━━━━━━━━━━━

### 8.1 — Añadir sección de "Estado actual / Disponibilidad" en Home

```html
<!-- Añadir justo antes del footer o bajo el hero -->
<div class="availability-banner">
  <div class="section__inner">
    <div class="availability-banner__inner">
      <div class="availability-dot"></div>
      <span><strong>Disponible para proyectos:</strong> Acepto nuevos clientes a partir de [FECHA]. Tiempo de respuesta: &lt;24h.</span>
      <a href="/contacto/">Empecemos →</a>
    </div>
  </div>
</div>
```

```css
.availability-banner {
  background: rgba(74,222,128,0.06);
  border-top: 1px solid rgba(74,222,128,0.2);
  border-bottom: 1px solid rgba(74,222,128,0.2);
  padding: 14px 0;
}
.availability-banner__inner {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.875rem;
}
.availability-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4ade80;
  box-shadow: 0 0 0 4px rgba(74,222,128,0.2);
  animation: pulse 2s infinite;
  flex-shrink: 0;
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 4px rgba(74,222,128,0.2); }
  50% { box-shadow: 0 0 0 8px rgba(74,222,128,0.05); }
}
```

### 8.2 — Correcciones de alineación global del contenido

Verificar que TODO el contenido usa el mismo `max-width` y márgenes que el navbar:

```css
/* Variable global de contenido */
:root {
  --content-max: 1200px;
  --content-pad: 24px;
}

/* Aplicar a TODOS los contenedores de sección */
.section__inner,
.container,
.hero__inner,
.page-wrapper,
.footer__inner {
  max-width: var(--content-max);
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--content-pad);
  padding-right: var(--content-pad);
  box-sizing: border-box;
}

/* En móvil, reducir padding */
@media (max-width: 640px) {
  :root { --content-pad: 16px; }
}
```

### 8.3 — Footer: actualizar links

En el footer, **mover** el link de Certificaciones a dentro de "Sobre Mí":
```html
<!-- ANTES (footer navigation): -->
<a href="/certificaciones/">Certificaciones</a>

<!-- DESPUÉS: -->
<a href="/sobre-mi/#certificaciones">Formación & Certificaciones</a>
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━
## FASE 9 — SEO & META-DATOS
## ━━━━━━━━━━━━━━━━━━━━━━━━

### 9.1 — Actualizar meta-tags en todas las páginas

| Página | Title nuevo | Description nueva |
|--------|-------------|-------------------|
| `/` | `Jonathan Esteban \| Desarrollador Web & Soporte IT · Madrid` | `Desarrollador web (4Geeks) y técnico IT con experiencia en soporte. Automatización con n8n y Composio. Proyectos reales con demos.` |
| `/servicios/` | `Servicios Web, Automatización IA y Soporte IT \| Jonathan Esteban` | `Desarrollo web, automatización con n8n y Composio, y soporte IT presencial en Madrid y Barcelona.` |
| `/servicios/automatizacion/` | `Automatización con n8n, Composio y Agentes IA \| Jonathan Esteban` | `Flujos n8n, integraciones Composio y agentes OpenClaw. Automatiza tu negocio sin código.` |
| `/sobre-mi/` | `Sobre Mí & Certificaciones \| Jonathan Esteban` | `Desarrollador web en formación (4Geeks Madrid) y técnico IT. Certificaciones en frontend, backend y ciberseguridad.` |
| `/proyectos/` | `Portfolio de Proyectos con Demos \| Jonathan Esteban` | `TrackFlow, ClawMate, Talk to the Machine. Demos en vivo, código en GitHub.` |

### 9.2 — Añadir Schema.org `Person` en el head de la homepage

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Jonathan Esteban Barona",
  "url": "https://jonathanesteban.dev",
  "jobTitle": "Desarrollador Web & Técnico IT",
  "description": "Desarrollador web en formación con experiencia en soporte IT. Automatización con n8n y Composio.",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Madrid",
    "addressCountry": "ES"
  },
  "sameAs": [
    "https://github.com/Jesteban1983",
    "https://linkedin.com/in/jonathanesteban"
  ]
}
</script>
```

---

## ━━━━━━━━━━━━━━━━━━━━━━━━
## FASE 10 — QA Y CHECKLIST FINAL
## ━━━━━━━━━━━━━━━━━━━━━━━━

El agente debe verificar cada punto antes de dar el trabajo por terminado:

### ✅ Contenido
- [ ] "16+ años" eliminado de **todas** las páginas (home, servicios, sobre-mi, meta-tags)
- [ ] Experiencia descrita como "soporte IT" y "bootcamp en curso"
- [ ] Stats del hero son verídicos
- [ ] "100% Clientes satisfechos" eliminado o cambiado a "100% Compromiso con la calidad"

### ✅ Navbar
- [ ] Solo existe UN bloque `<nav>` en cada página
- [ ] El navbar está alineado al mismo `max-width` que el contenido
- [ ] El dropdown de Servicios funciona y muestra 3 columnas
- [ ] El dropdown se cierra al hacer click fuera y con Escape
- [ ] El menú hamburger funciona en móvil
- [ ] "Certificaciones" NO aparece como ítem principal del navbar

### ✅ Servicios
- [ ] La página `/servicios/` tiene 3 bloques claramente separados: Desarrollo, Automatización, Soporte IT
- [ ] Cada bloque tiene su propio anchor (`#desarrollo`, `#automatizacion`, `#soporte`)
- [ ] Los servicios de n8n y Composio son visibles y tienen su propia card con badge "NUEVO"
- [ ] La calculadora de presupuesto sigue funcionando

### ✅ Sobre Mí
- [ ] La sección de Certificaciones está integrada dentro de `/sobre-mi/`
- [ ] La URL `/certificaciones/` redirige a `/sobre-mi/#certificaciones`
- [ ] El historial laboral tiene fechas coherentes

### ✅ Proyectos
- [ ] Talk to the Machine tiene link a demo en Vercel
- [ ] Cinema Seat Manager tiene link a demo en Vercel
- [ ] Los botones "Demo" abren en nueva pestaña con `target="_blank"`
- [ ] Los filtros de categoría (Web, Backend, Automatización) siguen funcionando

### ✅ Homepage
- [ ] Solo 2 proyectos destacados (no todos)
- [ ] Sección "Por qué trabajar conmigo" añadida
- [ ] Banner de disponibilidad visible
- [ ] Sin redundancia con la página de Proyectos

### ✅ Diseño
- [ ] El contenido de todas las páginas está alineado al mismo contenedor
- [ ] Los márgenes y paddings son consistentes en desktop y móvil
- [ ] Las tarjetas de servicio tienen hover effect
- [ ] Las tarjetas nuevas de n8n y Composio tienen badge "NUEVO"

### ✅ SEO
- [ ] Meta-descriptions actualizadas en todas las páginas
- [ ] Schema.org Person en el homepage
- [ ] Canonical URLs correctas
- [ ] Sin keywords falsas ("16 años de experiencia")

---

## 📁 ÁRBOL DE ARCHIVOS MODIFICADOS

```
/
├── index.html                         ← Fase 1, 5
├── assets/
│   └── css/
│       └── main.css                   ← Fase 2, 3, 4, 5, 8
│   └── js/
│       └── navbar.js                  ← Fase 2 (nuevo archivo)
├── servicios/
│   └── index.html                     ← Fase 1, 3
│   └── automatizacion/
│       └── index.html                 ← Fase 7
├── proyectos/
│   └── index.html                     ← Fase 6
├── sobre-mi/
│   └── index.html                     ← Fase 1, 4
└── certificaciones/
    └── index.html                     ← Fase 4 (solo redirección)
```

---

## 🔑 CREDENCIALES Y ACCESOS QUE NECESITAS

Antes de empezar, ten a mano:
- [ ] Acceso al repositorio GitHub del sitio web
- [ ] Cuenta en Vercel (vercel.com) — gratis
- [ ] API Key de Groq (groq.com) para el proyecto Talk to the Machine
- [ ] Acceso al proveedor de hosting/despliegue del sitio principal

---

## 💡 RECOMENDACIONES ADICIONALES (para futuras iteraciones)

1. **Añadir testimonios** — Aunque sean de compañeros de bootcamp o proyectos académicos, ayudan a generar confianza.
2. **Blog técnico** — Un artículo mensual sobre n8n, automatización o proyectos posiciona muy bien en SEO.
3. **Sección "Open to work"** — Si aún buscas empleo además de clientes freelance, un banner discreto lo comunica.
4. **Google Analytics 4** — Instalar seguimiento para saber qué páginas visitan más tus futuros clientes.
5. **Formulario de contacto funcional** — Verificar que el serverless function del formulario funciona correctamente.
6. **Lighthouse score** — Ejecutar `npx lighthouse https://jonathanesteban.dev` y corregir los warnings de performance y accesibilidad.

---

*Documento generado para ejecución por agente IA — jonathanesteban.dev*  
*Fecha de auditoría: Agosto 2026*  
*Páginas analizadas: `/`, `/servicios/`, `/proyectos/`, `/sobre-mi/`, `/certificaciones/`*
