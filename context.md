# 🌐 Master Architectural Specification — jonathanesteban.dev (v3.0 Multi-Page Corporate Portal)

> **Dominio Oficial:** https://jonathanesteban.dev  
> **Hosting & Serverless:** Netlify (Git-integrated deployment with Netlify Serverless Functions)  
> **Arquitectura:** Sitio Multi-Página (MPA) Profesional con Hojas de Datos JSON, Serverless API y Tailwind CSS  
> **Seguridad & Cumplimiento:** 100% de Secreta en `.env` / Netlify Env Vars, Integración OAuth TikTok/Meta, RGPD, Callback de Eliminación de Datos  
> **Autor:** Jonathan Esteban Barona — Full-Stack Developer, AI Engineer & Digital Operations Specialist  
> **Última actualización:** 2026-08-09

---

## 📋 Tabla de Contenidos

1. [Visión General y Posicionamiento de Mercado](#1-visión-general-y-posicionamiento-de-mercado)
2. [Estructura Exacta del Proyecto (`site/`)](#2-estructura-exacta-del-proyecto-site)
3. [Seguridad y Gestión de Secretos (.env & Serverless)](#3-seguridad-y-gestión-de-secretos-env--serverless)
4. [Rutas y Contenido Detallado por Página](#4-rutas-y-contenido-detallado-por-página)
5. [Módulos Interactivos y JavaScript (`assets/js/`)](#5-módulos-interactivos-y-javascript-assetsjs)
6. [Datasets JSON (`assets/data/`)](#6-datasets-json-assetsdata)
7. [Netlify Serverless Functions (`functions/`)](#7-netlify-serverless-functions-functions)
8. [Cumplimiento Legal y OAuth (Meta & TikTok Automation)](#8-cumplimiento-legal-y-oauth-meta--tiktok-automation)
9. [Estrategia SEO + GEO (Generative Engine Optimization)](#9-estrategia-seo--geo-generative-engine-optimization)
10. [Configuración de Despliegue en Netlify (`netlify.toml`)](#10-configuración-de-despliegue-en-netlify-netlifytoml)
11. [Checklist de Calidad y Producción](#11-checklist-de-calidad-y-producción)

---

## 1. Visión General y Posicionamiento de Mercado

Este proyecto transiciona `jonathanesteban.dev` de una landing page monolítica a una **Plataforma Corporativa Multi-Página de Alto Nivel**. Su propósito es presentar a Jonathan Esteban Barona como un **Full-Stack Developer, AI Engineer y Gestor de Operaciones Digitales** de primer nivel, capaz de ofrecer soluciones tecnológicas avanzadas para empresas en España (Barcelona/Madrid) y clientes internacionales en modalidad remota.

### Objetivos Clave

1. **Arquitectura Multi-Página (MPA):** 15+ sub-rutas limpias (`/servicios/`, `/proyectos/`, `/soporte-it/`, `/faq/`, etc.) que demuestran solidez técnica y estructura empresarial.
2. **Automatización Social Media (TikTok & Meta APIs):** Cumplir con los requerimientos estrictos de verificación de aplicaciones para TikTok Developer Console y Meta for Developers (Política de Privacidad, Términos de Servicio, Callback de Eliminación de Datos y URLs de Redirección OAuth).
3. **Cero Secretos Expuestos:** Todos los tokens, API keys y endpoints de webhooks (n8n, Telegram, SendGrid, OAuth App Secrets) residen únicamente en variables de entorno procesadas por **Netlify Functions**.
4. **Experiencia de Cliente Interactiva:** Incluye Calculadora de Presupuestos, Filtro de Proyectos por Tecnología, Centro de Ayuda e Interactivo FAQ, y Demo App en vivo.
5. **Máximo Rendimiento SEO + GEO:** Optimización tanto para buscadores tradicionales (Google/Bing) como para Motores Generativos de IA (ChatGPT, Perplexity, Claude, AI Overviews) mediante JSON-LD estructurado múltiple.

---

## 2. Estructura Exacta del Proyecto (`site/`)

El proyecto debe seguir estrictamente la siguiente jerarquía de archivos dentro del directorio `site/`:

```
site/
├── index.html                                # Homepage / Portal corporativo principal
├── servicios/
│   └── index.html                            # Catálogo completo de servicios + Calculadora
├── proyectos/
│   ├── index.html                            # Portfolio interactivo con filtros
│   ├── demo-app/
│   │   └── index.html                        # App interactiva de demostración en vivo
│   └── casos/
│       ├── portfolio-redesign/
│       │   └── index.html                    # Estudio de Caso 1: Rediseño de Plataforma
│       ├── landing-negocio/
│       │   └── index.html                    # Estudio de Caso 2: High-Conversion Lead Engine
│       └── automatizacion-leads/
│           └── index.html                    # Estudio de Caso 3: Pipeline de IA con n8n & OpenClaw
├── certificaciones/
│   └── index.html                            # Credenciales, 4Geeks Academy & Certificados
├── soporte-it/
│   └── index.html                            # Operaciones Digitales, Soporte IT & Mantenimiento
├── sobre-mi/
│   └── index.html                            # Biografía profesional, valores & historia
├── contacto/
│   └── index.html                            # Formulario de contacto avanzado + agendamiento
├── faq/
│   └── index.html                            # Centro de ayuda & FAQ interactivo
├── privacy-policy/
│   └── index.html                            # Política de Privacidad (Cumplimiento RGPD/Meta/TikTok)
├── terms-of-service/
│   └── index.html                            # Términos y Condiciones de Uso
├── data-deletion/
│   └── index.html                            # Instrucciones y confirmación de eliminación de datos de usuario
├── auth/
│   ├── tiktok/
│   │   └── callback/
│   │       └── index.html                    # Landing de procesamiento OAuth TikTok
│   └── facebook/
│       └── callback/
│           └── index.html                    # Landing de procesamiento OAuth Facebook/Meta
├── gracias/
│   └── index.html                            # Confirmación de conversión / Lead capturado
├── assets/
│   ├── css/
│   │   ├── tokens.css                         # Design tokens, variables CSS & Tailwind setup
│   │   ├── base.css                           # Reset, tipografía & reglas base
│   │   ├── layout.css                         # Grids, contenedores, headers & footers
│   │   ├── components.css                     # Cards, botones, badges, modales & calculadoras
│   │   ├── pages.css                          # Estilos específicos por sección
│   │   └── legal.css                          # Maquetación para documentos legales
│   ├── js/
│   │   ├── main.js                            # Inicialización global & boostrap de la app
│   │   ├── nav.js                             # Menú responsive, active state & scroll headers
│   │   ├── theme.js                           # Toggle Dark/Light mode con localStorage
│   │   ├── faq.js                             # Acordeón de FAQ con filtro de búsqueda
│   │   ├── filters.js                         # Filtrado dinámico de proyectos & servicios
│   │   ├── form.js                            # Validación & envío asíncrono de formularios
│   │   ├── calculator.js                      # Calculadora interactiva de presupuestos
│   │   ├── tracking.js                        # Event tracking & analítica respetuosa con privacidad
│   │   └── app-demo.js                        # Lógica de la aplicación interactiva de demostración
│   ├── data/
│   │   ├── projects.json                      # Dataset estructurado de proyectos y estudios de caso
│   │   ├── certificates.json                  # Dataset estructurado de certificaciones y cursos
│   │   ├── services.json                      # Dataset estructurado de servicios y paquetes
│   │   └── faq.json                           # Dataset estructurado de preguntas frecuentes
│   ├── img/                                   # Fotografía profesional WebP, logos, diagramas, OG
│   ├── icons/                                 # SVGs vectoriales de tecnologías y servicios
│   └── docs/
│       └── domain-verification/               # Archivos de verificación para TikTok/Meta Console
├── functions/
│   ├── contact-submit.js                      # Netlify Function: Procesar formulario de contacto
│   ├── notify-owner.js                        # Netlify Function: Notificación inmediata vía Telegram
│   ├── autoresponse.js                        # Netlify Function: Respuesta automática por Email
│   ├── tiktok-oauth-callback.js               # Netlify Function: Token exchange para TikTok API
│   ├── facebook-oauth-callback.js             # Netlify Function: Token exchange para Meta API
│   ├── data-deletion-request.js               # Netlify Function: Endpoint de eliminación de datos Meta/TikTok
│   └── webhook-n8n.js                         # Netlify Function: Conexión segura con workflows n8n
├── robots.txt                                 # Directivas SEO y acceso explícito a bots de IA
├── sitemap.xml                                # Mapa del sitio XML con las 15+ URLs
└── favicon.ico                                # Favicon multirresolución
```

---

## 3. Seguridad y Gestión de Secretos (.env & Serverless)

### Regla de Oro de Seguridad
**Ningún token de API, client secret, clave de Telegram o webhook privado puede existir en el código fuente frontend (HTML, CSS o JS).**

### `.env` (Configuración en servidor / Netlify Environment Variables)

```env
# === SERVIDOR & ENTORNOS ===
NODE_ENV=production
SITE_URL=https://jonathanesteban.dev

# === FORMULARIO & EMAIL (Server-side Only) ===
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxx
CONTACT_RECIPIENT_EMAIL=joonathanesteban@gmail.com
SENDER_EMAIL_NO_REPLY=joonathanesteban@gmail.com

# === TELEGRAM NOTIFICATIONS ===
TELEGRAM_BOT_TOKEN=7890123456:AAXxxxxxxxxxxxxxxxxxxxxxxxxxxx
TELEGRAM_CHAT_ID=123456789

# === AUTOMATIZACIÓN n8n WORKFLOWS ===
N8N_WEBHOOK_LEADS_URL=https://n8n.jonathanesteban.dev/webhook/lead-entry
N8N_WEBHOOK_SECRET=secret_n8n_token_889900

# === TIKTOK DEVELOPER API OAUTH ===
TIKTOK_CLIENT_KEY=awxxxxxxxxxxxxxx
TIKTOK_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TIKTOK_REDIRECT_URI=https://jonathanesteban.dev/auth/tiktok/callback/

# === META / FACEBOOK DEVELOPER OAUTH ===
FACEBOOK_APP_ID=123456789012345
FACEBOOK_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FACEBOOK_REDIRECT_URI=https://jonathanesteban.dev/auth/facebook/callback/

# === GOOGLE SITE VERIFICATION (Public) ===
VITE_GOOGLE_SITE_VERIFICATION=m7HiJ34wfzUNV
```

### `.env.example` (Plantilla de repositorio público)

```env
# Archivo de ejemplo para configuración en entorno local y CI/CD
NODE_ENV=development
SITE_URL=http://localhost:8888

SENDGRID_API_KEY=tu_sendgrid_key_aqui
CONTACT_RECIPIENT_EMAIL=tu_email@dominio.com
SENDER_EMAIL_NO_REPLY=no-reply@tudominio.com

TELEGRAM_BOT_TOKEN=tu_telegram_bot_token
TELEGRAM_CHAT_ID=tu_telegram_chat_id

N8N_WEBHOOK_LEADS_URL=https://tu-n8n.com/webhook/endpoint
N8N_WEBHOOK_SECRET=tu_webhook_secret

TIKTOK_CLIENT_KEY=tu_tiktok_client_key
TIKTOK_CLIENT_SECRET=tu_tiktok_client_secret
TIKTOK_REDIRECT_URI=https://jonathanesteban.dev/auth/tiktok/callback/

FACEBOOK_APP_ID=tu_facebook_app_id
FACEBOOK_APP_SECRET=tu_facebook_app_secret
FACEBOOK_REDIRECT_URI=https://jonathanesteban.dev/auth/facebook/callback/

VITE_GOOGLE_SITE_VERIFICATION=tu_codigo_verification
```

---

## 4. Rutas y Contenido Detallado por Página

### 4.1 Home (`site/index.html`)
- **Propósito:** Hub central y presentación ejecutiva de la marca personal.
- **Secciones:**
  1. **Header/Nav:** Menú corporativo sticky con navegación a todas las sub-páginas, toggle dark/light y botón CTA "Contactar".
  2. **Hero Section:** Headline de alto impacto ("Desarrollo Full-Stack, Ingeniería de IA y Automatización Digital"), badge de estado "Disponible para proyectos", métricas en vivo (16+ años experiencia, 4/6 hitos 4Geeks, 10+ proyectos), foto profesional y CTAs principales.
  3. **Resumen de Servicios:** Grid con los 4 pilares (Full-Stack, APIs REST, Agentes IA, Soporte IT) con enlace a `/servicios/`.
  4. **Proyectos Destacados:** Cards interactivas con tag de tecnologías, enlaces a demostraciones y enlace a `/proyectos/`.
  5. **Diferenciador & Método:** Por qué combinar desarrollo tradicional con Ingeniería de IA y gestión operativa real reduce tiempos y costes.
  6. **Testimonios / Credenciales:** Resumen del bootcamp 4Geeks Academy y certificaciones destacadas.
  7. **CTA Final & Formulario Rápido:** Formulario directo conectado a Netlify Function `/api/contact-submit`.

### 4.2 Servicios (`site/servicios/index.html`)
- **Propósito:** Desglose comercial completo de la oferta tecnológica y calculadora interactiva.
- **Secciones:**
  1. **Catálogo de Servicios:**
     - *Desarrollo Web Full-Stack:* Next.js, React, TypeScript, HTML5/CSS3 moderno.
     - *APIs REST & Arquitectura Backend:* Python, FastAPI, Pydantic, SQLModel, PostgreSQL, Supabase.
     - *Ingeniería de IA & Agentes Autónomos:* Agentes OpenClaw, herramientas MCP Composio, automatización de workflows.
     - *Automatización de Procesos & Social Media:* Integration de APIs TikTok/Meta, n8n, pipelines de video y leads.
  2. **Calculadora Interactiva de Presupuesto (`calculator.js`):** Permite al usuario seleccionar el tipo de proyecto, funcionalidades requeridas, nivel de urgencia y recibir una estimación orientativa instantánea con botón de envío de propuesta.

### 4.3 Portfolio de Proyectos (`site/proyectos/index.html`)
- **Propósito:** Demostración práctica de casos de éxito y repositorios de código.
- **Funcionalidades:**
  - **Filtros por Categoría (`filters.js`):** Todos, Full-Stack, Backend & APIs, Agentes IA, Frontend UI.
  - **Grid Dinámico:** Renderizado desde `assets/data/projects.json`.
  - **Proyectos Incluidos:**
    - *TrackFlow (Sistema de Gestión de Inventario)* — FastAPI + Supabase + Next.js.
    - *ClawMate (Agente Personal de IA)* — OpenClaw + Composio MCP + Integración Google APIs.
    - *Voice Command API* — FastAPI + Audio Processing + REST endpoints.
    - *Auth System Full-Stack* — FastAPI + JWT + OAuth2 + Password Reset Flow.
    - *Talk to the Machine* — Next.js + Groq API + LLaMA 3.
    - *Cinema Seat Manager* — TypeScript + Vite + DOM API.
    - *EduTrack Data Audit* — PostgreSQL + Supabase + SQL avanzado.
  - **Enlaces a Estudios de Caso y Demo Live:** Botones hacia `/proyectos/casos/...` y `/proyectos/demo-app/`.

### 4.4 Demo App en Vivo (`site/proyectos/demo-app/index.html`)
- **Propósito:** Aplicación interactiva embebida que demuestra habilidades avanzadas de Frontend en TypeScript/JavaScript y consumo de APIs.
- **Lógica (`app-demo.js`):** Panel interactivo de gestión donde los visitantes pueden probar la manipulación de estado en tiempo real, filtros de datos y simulación de procesamiento asistido por IA.

### 4.5 Estudios de Caso (`site/proyectos/casos/`)
- **Rutas:**
  - `/proyectos/casos/portfolio-redesign/index.html` — Caso de estudio sobre transformación de arquitectura web estática a MPA optimizada para IA.
  - `/proyectos/casos/landing-negocio/index.html` — Caso de estudio sobre construcción de landings de alta conversión con backend serverless.
  - `/proyectos/casos/automatizacion-leads/index.html` — Caso de estudio sobre integración de workflows de IA (OpenClaw + n8n + Telegram) para captura y calificación de leads.

### 4.6 Certificaciones & Formación (`site/certificaciones/index.html`)
- **Propósito:** Acreditación académica e historia de aprendizaje continuo.
- **Contenido:**
  - **4Geeks Academy Madrid (Bootcamp AI Engineering):** Progreso detallado (71% completado, 194/273 tareas, 4/6 hitos).
  - **Grid de Certificaciones Oficiales:**
    1. *Frontend con HTML5, CSS3 y JavaScript* — Fundación Adecco (30h).
    2. *Bases de Datos* — Fundación Adecco (30h).
    3. *Introducción a Java SE* — Fundación Adecco (30h).
    4. *Desarrollo Back-End (Básico)* — Ministerio de Trabajo, Perú (30h, Nota: 17/20).
    5. *Diseño Web con HTML5 + CSS* — Fundación Telefónica Movistar (30h).
    6. *Ciberseguridad Básica* — ESIC Business & Marketing School.
  - Renderizado dinámico desde `assets/data/certificates.json`.

### 4.7 Soporte IT & Operaciones Digitales (`site/soporte-it/index.html`)
- **Propósito:** Presentación de la trayectoria de 16+ años en soporte técnico, logística y gestión operativa.
- **Servicios:** Mantenimiento de infraestructuras IT, reparación de equipos, redes locales, administración VPS/Linux, gestión de bandejas de entrada empresariales, transcripción y data entry profesional.

### 4.8 Sobre Mí (`site/sobre-mi/index.html`)
- **Propósito:** Biografía profesional completa, valores, cronología de carrera e idiomas (Español nativo / Inglés técnico).

### 4.9 Contacto (`site/contacto/index.html`)
- **Propósito:** Punto principal de conversión con formulario validado en cliente (`form.js`) y procesado en servidor (`contact-submit.js`).
- **Campos:** Nombre, Email, Teléfono/WhatsApp (opcional), Servicio de interés, Presupuesto estimado, Mensaje.
- **Feedback:** Indicadores en tiempo real de envío, estados de carga y pantalla de redirección a `/gracias/`.

### 4.10 Centro de Ayuda e Interactivo FAQ (`site/faq/index.html`)
- **Propósito:** Resolución de dudas comunes de clientes y optimización GEO para motores de IA.
- **Funcionalidades (`faq.js`):** Buscador en tiempo real de preguntas frecuentes y filtro por categorías (Proyectos, Pagos, Tecnologías, Garantías).

### 4.11 Páginas Legales & Cumplimiento OAuth (`site/privacy-policy/`, `site/terms-of-service/`, `site/data-deletion/`)
- **Páginas indispensables para la aprobación de aplicaciones en Meta for Developers y TikTok Developer Center.**
- **Privacy Policy:** Cláusulas completas RGPD/LOPD-GDD, tratamientos de datos, derechos ARCO-POL, uso de cookies.
- **Terms of Service:** Condiciones de contratación, propiedad intelectual, uso de automatizaciones.
- **Data Deletion Instructions:** Guía paso a paso para que usuarios que hayan autorizado la app de Facebook/TikTok soliciten la eliminación de sus datos, junto a confirmación del endpoint automático `/api/data-deletion-request`.

### 4.12 OAuth Callbacks (`site/auth/tiktok/callback/`, `site/auth/facebook/callback/`)
- Páginas de aterrizaje amigables para el usuario tras completar el flujo de autorización OAuth. Muestran mensaje de confirmación y envían el código de autorización al servidor de forma segura sin exponer credenciales.

### 4.13 Página de Gracias (`site/gracias/index.html`)
- Landing de confirmación tras envío exitoso del formulario de contacto o solicitud de presupuesto.

---

## 5. Módulos Interactivos y JavaScript (`assets/js/`)

El sitio utiliza JavaScript Vanilla modular optimizado (ES6 modules):

1. **`main.js`:** Punto de entrada que inicializa los componentes según la página activa.
2. **`nav.js`:** Controla el menú hamburguesa móvil, el efecto glassmorphism al hacer scroll y el resalte del link activo.
3. **`theme.js`:** Administra el cambio entre modo oscuro (`dark`) y claro (`light`) mediante clases en `<html>` y persistencia en `localStorage`.
4. **`faq.js`:** Maneja la apertura/cierre de acordeones FAQ y el filtro de búsqueda en directo.
5. **`filters.js`:** Filtra los elementos del portfolio de proyectos según la categoría seleccionada sin recargar la página.
6. **`form.js`:** Realiza la validación HTML5 + JS de los formularios de contacto y envía los datos via `fetch` a las Netlify Functions (`/api/contact-submit`).
7. **`calculator.js`:** Lógica de cálculo interactivo de tarifas y requisitos de proyectos.
8. **`tracking.js`:** Registro de eventos de conversión (respetuoso con la privacidad, sin cookies de terceros).
9. **`app-demo.js`:** Lógica de la aplicación interactiva embebida en `/proyectos/demo-app/`.

---

## 6. Datasets JSON (`assets/data/`)

### 6.1 `projects.json`
```json
[
  {
    "id": "trackflow",
    "title": "TrackFlow — Sistema de Gestión de Inventario",
    "category": "backend",
    "featured": true,
    "description": "Sistema completo de inventario con API REST FastAPI, PostgreSQL/Supabase, autenticación JWT y backoffice Next.js.",
    "tags": ["Python", "FastAPI", "PostgreSQL", "Supabase", "Next.js"],
    "github": "https://github.com/4GeeksAcademy/Jesteban1983-TrackFlow.git",
    "case_study_url": "/proyectos/casos/landing-negocio/",
    "status": "En desarrollo"
  },
  {
    "id": "clawmate",
    "title": "ClawMate — Agente Personal de IA",
    "category": "ai",
    "featured": true,
    "description": "Agente autónomo integrado con OpenClaw y Composio MCP para automatización de Gmail, Calendar, Drive y Telegram.",
    "tags": ["OpenClaw", "Composio MCP", "Python", "Google APIs"],
    "status": "Completado"
  }
]
```

### 6.2 `certificates.json`
```json
[
  {
    "id": "cert-adecco-frontend",
    "title": "Frontend con HTML5, CSS3 y JavaScript",
    "issuer": "Fundación Adecco",
    "date": "Noviembre 2025",
    "hours": "30h"
  },
  {
    "id": "cert-4geeks-bootcamp",
    "title": "AI Engineering — Full Stack + IA",
    "issuer": "4Geeks Academy Madrid",
    "date": "2026",
    "status": "71% Completado (194/273 tareas)"
  }
]
```

### 6.3 `services.json`
```json
[
  {
    "id": "fullstack",
    "title": "Desarrollo Web Full-Stack",
    "description": "Aplicaciones y sitios web a medida con Next.js, React, Tailwind CSS y arquitectura limpia.",
    "icon": "code"
  },
  {
    "id": "api-backend",
    "title": "APIs REST & Arquitectura Backend",
    "description": "Servicios backend robustos con FastAPI, Python, PostgreSQL y autenticación segura JWT.",
    "icon": "server"
  }
]
```

### 6.4 `faq.json`
```json
[
  {
    "question": "¿Qué servicios ofrece Jonathan Esteban?",
    "answer": "Desarrollo web Full-Stack (React/Next.js), APIs REST con FastAPI, creación de Agentes de IA autónomos (OpenClaw), automatización de procesos y soporte técnico especializado.",
    "category": "servicios"
  }
]
```

---

## 7. Netlify Serverless Functions (`functions/`)

Ubicadas en la carpeta `functions/` del proyecto. Se ejecutan en el entorno seguro de Netlify:

### 7.1 `functions/contact-submit.js`
- **Ruta invocada:** `/api/contact-submit`
- **Lógica:**
  1. Verifica que la solicitud sea `POST`.
  2. Valida la presencia de honeypot anti-spam (`_gotcha`). Si contiene texto, rechaza silenciosamente.
  3. Procesa y sanitiza los campos `name`, `email`, `subject`, `message`.
  4. Invoca internamente a `notify-owner.js` (notificación Telegram) y `autoresponse.js` (email de confirmación).
  5. Envía los datos al webhook de n8n (`N8N_WEBHOOK_LEADS_URL`).
  6. Retorna respuesta JSON `{ success: true, message: "Mensaje recibido correctamente" }`.

### 7.2 `functions/notify-owner.js`
- Envía una alerta instantánea al Telegram privado de Jonathan (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) detallando el nuevo prospecto.

### 7.3 `functions/autoresponse.js`
- Envía un correo electrónico profesional de confirmación al usuario que completó el formulario utilizando la API de SendGrid.

### 7.4 `functions/tiktok-oauth-callback.js`
- **Ruta invocada:** `/api/tiktok-oauth-callback`
- Recibe el `code` de autorización devuelto por TikTok, realiza el token exchange usando `TIKTOK_CLIENT_KEY` y `TIKTOK_CLIENT_SECRET` en servidor, guardando el token de forma segura sin exponerlo al navegador.

### 7.5 `functions/facebook-oauth-callback.js`
- **Ruta invocada:** `/api/facebook-oauth-callback`
- Procesa el token exchange para la app de Meta/Facebook usando `FACEBOOK_APP_ID` y `FACEBOOK_APP_SECRET`.

### 7.6 `functions/data-deletion-request.js`
- **Ruta invocada:** `/api/data-deletion-request`
- Endpoint exigido por Meta for Developers para solicitudes de eliminación de datos de usuario. Recibe la `signed_request`, la valida, registra la solicitud de borrado y devuelve la URL de confirmación y el código de seguimiento exigido por Facebook.

### 7.7 `functions/webhook-n8n.js`
- Puente autenticado mediante token secreto (`N8N_WEBHOOK_SECRET`) para transferir eventos desde la web a la instancia de automatización n8n.

---

## 8. Cumplimiento Legal y OAuth (Meta & TikTok Automation)

Para permitir que Jonathan ejecute bots y automatizaciones de video/leads en TikTok y Facebook/Instagram, la web cumple con todos los requisitos de verificación de desarrolladores:

1. **Dominio Propio Verificado:** `https://jonathanesteban.dev` con archivo de verificación en `site/assets/docs/domain-verification/`.
2. **Política de Privacidad Transparente (`/privacy-policy/`):** Define de forma explícita el uso de datos procedentes de APIs de Meta y TikTok.
3. **Página de Eliminación de Datos (`/data-deletion/`):** Ofrece tanto un formulario/instrucción clara al usuario como la URL del endpoint `/api/data-deletion-request`.
4. **Callbacks de OAuth Seguros:** Puntos de entrada oficial para redirección tras autenticación en TikTok (`/auth/tiktok/callback/`) y Facebook (`/auth/facebook/callback/`).

---

## 9. Estrategia SEO + GEO (Generative Engine Optimization)

### 9.1 Stacked JSON-LD Schemas (Renderizados en las páginas clave)

#### En `index.html` (Homepage):
- `Person` Schema (Datos de Jonathan Esteban, habilidades, alumni de 4Geeks Academy).
- `WebSite` Schema (Información del sitio corporativo).
- `Organization` Schema (Marca profesional freelance).
- `ItemList` Schema (Catálogo de proyectos destacados).

#### En `site/faq/index.html`:
- `FAQPage` Schema con todas las preguntas y respuestas estructuradas para que motores como Google AI Overviews o Perplexity las citen como respuesta directa.

#### En `site/servicios/index.html`:
- `Service` Schema listando cada servicio comercial ofrecido.

### 9.2 `robots.txt` (`site/robots.txt`)
```txt
User-agent: *
Allow: /

# Permitir explícitamente rastreadores de motores de IA para GEO
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: https://jonathanesteban.dev/sitemap.xml
```

### 9.3 `sitemap.xml` (`site/sitemap.xml`)
Contiene las 15+ URLs del sitio con sus correspondientes etiquetas `<lastmod>`, `<changefreq>` y `<priority>`.

---

## 10. Configuración de Despliegue en Netlify (`netlify.toml`)

```toml
[build]
  publish = "site"
  functions = "functions"

# === HEADERS DE SEGURIDAD Y PRIVACIDAD ===
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"
    Content-Security-Policy = "default-src 'self'; script-src 'self' 'unsafe-inline' https://unpkg.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' https://api.netlify.com; frame-ancestors 'none'"

# === REGLAS DE REDIRECCIÓN Y RUTAS DE API ===
[[redirects]]
  from = "/api/contact-submit"
  to = "/.netlify/functions/contact-submit"
  status = 200

[[redirects]]
  from = "/api/tiktok-oauth-callback"
  to = "/.netlify/functions/tiktok-oauth-callback"
  status = 200

[[redirects]]
  from = "/api/facebook-oauth-callback"
  to = "/.netlify/functions/facebook-oauth-callback"
  status = 200

[[redirects]]
  from = "/api/data-deletion-request"
  to = "/.netlify/functions/data-deletion-request"
  status = 200

# Redirección 301 del subdominio de Netlify al dominio propio
[[redirects]]
  from = "https://jonathanesteban.netlify.app/*"
  to = "https://jonathanesteban.dev/:splat"
  status = 301
  force = true
```

---

## 11. Checklist de Calidad y Producción

- [ ] Todas las 15+ páginas creadas en la carpeta `site/` con enlaces internos válidos.
- [ ] Ninguna clave secreta presente en código frontend (todas en `.env` / Netlify Functions).
- [ ] Formulario de contacto funcionando asíncronamente con notificación a Telegram.
- [ ] Páginas legales (`privacy-policy`, `terms-of-service`, `data-deletion`) listas para revisión de apps en Meta y TikTok.
- [ ] Callbacks OAuth configurados para recibir tokens de forma segura en backend serverless.
- [ ] Calculadora de presupuesto interactiva funcionando en `/servicios/`.
- [ ] Filtro de proyectos funcionando sin recarga en `/proyectos/`.
- [ ] Schemas JSON-LD (Person, WebSite, FAQPage, Service) validados en Google Rich Results Test.
- [ ] `robots.txt` y `sitemap.xml` actualizados con el dominio `jonathanesteban.dev`.
- [ ] Netlify Functions desplegadas y respondiendo HTTP 200 en las rutas `/api/*`.

---

*Esta especificación maestra define el estándar definitivo para la construcción de jonathanesteban.dev.*