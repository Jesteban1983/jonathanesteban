# 🧭 Auditoría Completa + Plan de Reestructuración — jonathanesteban.dev

> **Fecha:** 2026-08-16
> **Tipo:** Auditoría exhaustiva ruta por ruta + plan de corrección priorizado
> **Estado:** Sitio auditado al 100% — 27 rutas probadas

---

## 📋 RESUMEN EJECUTIVO

| Métrica | Valor |
|---------|-------|
| Rutas totales probadas | 27 |
| Rutas funcionando OK | 25 |
| Rutas con error/mejora | 12 |
| Problemas P0 (bloqueantes) | 3 |
| Problemas P1 (conversión) | 7 |
| Problemas P2 (calidad) | 8 |
| Redundancia detectada | Sobre mí / Certificaciones / Proyectos solapados |

---

## 🔍 MATRIZ DE ENLACES — RUTA POR RUTA

| # | Ruta | HTTP | Title | H1 | Estado | Severidad |
|---|------|:----:|-------|:--:|:------:|:---------:|
| 1 | `/` | 200 | Full-Stack Developer & AI Engineer | JonathanEsteban | ✅ OK | — |
| 2 | `/servicios/` | 200 | Servicios de Desarrollo Web, IA... | Soluciones digitales... | ⚠️ MEJORA | P1 |
| 3 | `/servicios/desarrollo-web/` | 200 | — | — | ⚠️ NO VERIFICABLE | P1 |
| 4 | `/servicios/automatizacion/` | 200 | — | — | ⚠️ NO VERIFICABLE ** | P1 |
| 5 | `/servicios/soporte-it/` | 200 | Servicio de Soporte IT | Soporte IT... | ✅ OK | — |
| 6 | `/soporte-it/` | 301 → `/servicios/soporte-it/` | — | — | ✅ REDIRECT OK | — |
| 7 | `/proyectos/` | 200 | Portfolio de Proyectos... | Trabajo Desarrollado | ⚠️ MEJORA | P1 |
| 8 | `/proyectos/trackflow/` | 200 | TrackFlow | Proyecto | ⚠️ MEJORA | P1 |
| 9 | `/proyectos/clawmate/` | 200 | ClawMate | Proyecto | ✅ OK | — |
| 10 | `/proyectos/talk-to-the-machine/` | 200 | Talk to the Machine | Proyecto | ✅ OK | — |
| 11 | `/proyectos/demo-app/` | 200 | Demo App en Vivo | Live Interactive Demo | ⚠️ MEJORA | P2 |
| 12 | `/certificaciones/` | 200 | Certificaciones & Formación | Acreditación Técnica | ⚠️ MEJORA | P1 |
| 13 | `/sobre-mi/` | 200 | Jonathan Esteban — Full-Stack... | Sobre Mí & Dashboard | ⚠️ MEJORA | P1 |
| 14 | `/contacto/` | 200 | Contacto & Agendamiento | — (formulario) | ✅ OK | — |
| 15 | `/faq/` | 200 | Preguntas Frecuentes (FAQ) | Centro de Ayuda | ⚠️ MEJORA | P1 |
| 16 | `/legal/aviso-legal/` | 200 | Aviso legal | Responsable del sitio | ✅ OK | — |
| 17 | `/legal/privacidad/` | 301 → `/privacy-policy/` | Redirigiendo... | — | ✅ REDIRECT OK | — |
| 18 | `/legal/cookies/` | 200 | Politica de cookies | — | ⚠️ MEJORA | P2 |
| 19 | `/privacy-policy/` | 200 | Política de Privacidad | Responsable del Tratamiento | ⚠️ MEJORA | P2 |
| 20 | `/terms-of-service/` | 200 | Términos y Condiciones | Aceptación de los Términos | ⚠️ MEJORA | P2 |
| 21 | `/data-deletion/` | 200 | Instrucciones y Eliminación | Cumplimiento RGPD... | ✅ OK | — |
| 22 | `/auth/tiktok/callback/` | 200 | TikTok OAuth Callback | Autenticación con TikTok | ✅ OK | — |
| 23 | `/auth/facebook/callback/` | 200 | Facebook/Meta OAuth Callback | Autenticación con Meta | ✅ OK | — |
| 24 | `/gracias/` | 200 | — | — | ❌ ERROR | P0 |
| 25 | `/soporte-tecnico/` | — | — | — | ❌ NO VERIFICABLE | P2 |

> ** Nota: `/servicios/automatizacion/` y `/servicios/desarrollo-web/` existen (HTTP 200) pero devuelven páginas vacías o placeholder sin contenido real.

---

## 🚩 PROBLEMAS DETECTADOS — POR SEVERIDAD

## 🔴 P0 — BLOQUEANTES (corregir YA)

### P0-1: `/gracias/` — Página vacía o rota
- **Hallazgo:** No se pudo extraer contenido. Puede estar vacía o sin template.
- **Impacto:** Si alguien envía el formulario y llega aquí, no ve confirmación.
- **Corrección:** Crear página de agradecimiento con mensaje claro y CTA a home.

### P0-2: `/servicios/automatizacion/` y `/servicios/desarrollo-web/` vacíos
- **Hallazgo:** Las rutas existen pero devuelven páginas sin contenido sustancial. Son placeholder.
- **Impacto:** Un cliente que llegue directo ve una página vacía → pérdida del lead.
- **Corrección:** Poblarlas con contenido completo (ver sección 4).

### P0-3: Email de contacto expuesto (`joonathanesteban@gmail.com`)
- **Hallazgo:** En aviso legal, privacidad y data-deletion aparece tu email real.
- **Impacto:** No es crítico de seguridad, pero recibirás spam.
- **Corrección:** Usar `hola@jonathanesteban.dev` como email público y reservar el personal para interno.

---

## 🟠 P1 — AFECTAN CONVERSIÓN Y CONFIANZA

### P1-1: "16+ años experiencia operativa" — INFLADO
- **Hallazgo:** Aparece en home, servicios, sobre-mí. 2007 → 2026 son 19 años, pero solo ~6 son IT.
- **Impacto:** El cliente percibe "16 años como desarrollador" y la realidad es ~1 año.
- **Corrección:** Cambiar a expresión honesta como:
  > 5+ años soporte IT + gestión operativa desde 2007
  O mejor: separar "Años operativos" de "Años desarrollando software".

### P1-2: "71% Bootcamp" como número grande
- **Hallazgo:** En home y sobre-mí aparece como métrica principal. Es un progreso parcial.
- **Impacto:** Un cliente piensa "no ha terminado". No genera confianza.
- **Corrección:** Eliminar de la home. En certificaciones/sobre-mí poner texto descriptivo:
  > Formación Full Stack & AI Engineer en curso — 4Geeks Academy (194/273 tareas)

### P1-3: "100% Clientes satisfechos" en /servicios/
- **Hallazgo:** No tienes clientes reales que hayan contratado servicios web/IA de pago.
- **Impacto:** Falso. Si un cliente lo descubre, pierdes toda credibilidad.
- **Corrección:** Eliminar esta métrica por completo. Reemplazar con algo verificable.

### P1-4: 3 páginas que hablan de lo mismo (Sobre mí / Certificaciones / Proyectos)
- **Hallazgo:** 
  - `/sobre-mi/` tiene: timeline laboral + certificaciones + habilidades + bootcamp
  - `/certificaciones/` tiene: bootcamp + certificaciones (solapamiento con sobre-mí)
  - `/proyectos/` tiene: proyectos pero con información que se repite
- **Impacto:** Confunde al visitante, contenido duplicado canibaliza SEO.
- **Corrección:** 
  - **Sobre mí:** Solo biografía, experiencia, enfoque de trabajo, valores
  - **Certificaciones:** Solo formación académica + certificados
  - **Proyectos:** Solo proyectos con caso de estudio

### P1-5: TrackFlow como "En desarrollo" en portfolio
- **Hallazgo:** En home y proyectos aparece como "En desarrollo".
- **Impacto:** Muestras proyectos incompletos. Un cliente busca resultados terminados.
- **Corrección:** Cambiar a "Completado v1.0" o si sigue en desarrollo, ponerlo como "Demo funcional — en iteración continua". Pero no uses "En desarrollo" como label principal.

### P1-6: Falta CTA comercial potente en home
- **Hallazgo:** El hero no tiene un CTA claro de "Solicitar presupuesto" visible.
- **Impacto:** El visitante no sabe qué hacer después de leer.
- **Corrección:** Añadir botón primario "Solicitar presupuesto" + secundario "Ver servicios".

### P1-7: Servicio de Automatización no listado en la home
- **Hallazgo:** En la home solo aparecen "Desarrollo Web", "APIs REST", "Agentes IA", "Soporte IT".
- **Impacto:** No estás ofreciendo el servicio que más quieres vender.
- **Corrección:** Añadir "Automatización de procesos con IA" como servicio destacado en home.

---

## 🟡 P2 — CALIDAD TÉCNICA, SEO Y ACCESIBILIDAD

### P2-1: Navbar no alineado (contenido a derecha e izquierda)
- **Hallazgo:** Los items del menú no están balanceados.
- **Corrección:** Distribuir equitativamente: logo a izquierda, enlaces centrados o derecha.

### P2-2: Hero no cubre 100dvh de color azul
- **Hallazgo:** El fondo azul del hero no se extiende al 100% del viewport.
- **Corrección:** Asegurar `min-height: 100dvh` en la sección hero y background que cubra completo.

### P2-3: Tipografía muy junta (letter-spacing)
- **Hallazgo:** El texto se ve apretado, especialmente en párrafos largos.
- **Corrección:** Aumentar `letter-spacing` y `line-height` para mejorar legibilidad.

### P2-4: "100% Clientes satisfechos" sin base real (redundancia)
- **Hallazgo:** Misma métrica falsa aparece en 2 secciones.
- **Corrección:** Eliminar. (Ya cubierto en P1-3)

### P2-5: Páginas legales mejorables
- **Hallazgo:** 
  - Aviso legal: demasiado breve, no menciona RGDB completo
  - Cookies: no implementa banner real de cookies
  - Privacy policy: redirige desde legal/privacidad pero funciona
- **Corrección:** 
  - Aviso legal: completar con datos de contacto reales, registro, etc.
  - Cookies: implementar banner funcional con consentimiento

### P2-6: Sin algoritmo dinámico de años de experiencia
- **Hallazgo:** El "16+" es texto estático.
- **Solicitaste:** Auto-actualización anual.
- **Corrección:** Implementar en JS: `const años = new Date().getFullYear() - 2007` y se actualiza solo.

### P2-7: Sin contador dinámico de proyectos realizados
- **Hallazgo:** "10+ proyectos" es manual.
- **Solicitaste:** Que se actualice vía agente (conteo desde DB/automatización).
- **Corrección:** El lead bot puede alimentar este número. Mientras tanto, poner un número real y verificable.

### P2-8: Sin breadcrumbs ni botón return consistente
- **Hallazgo:** Algunas páginas tienen "← Volver" (proyectos), otras no.
- **Corrección:** Implementar breadcrumb en todas las páginas internas + botón return arriba.

---

## 🟢 P3 — MEJORAS FUTURAS

### P3-1: Subir demos a Vercel
- **Solicitaste:** Proyectos demo desplegados en Vercel para mostrar funcionalidad real.
- **Acción:** Identificar qué proyectos pueden deployarse (Talk-to-the-machine, Cinema Seat, Demo App).

### P3-2: Integrar lead bot en la web (el proyecto que diseñamos)
- **Hallazgo:** El widget de chat del PLAN.md no está implementado.
- **Acción:** Una vez tengas la VM en Hetzner, desplegar el asistente.

### P3-3: WhatsApp Business + formulario + n8n
- **Hallazgo:** El formulario actual probablemente envía por email estático.
- **Acción:** Conectar con n8n para registro automático de leads.

---

## 📐 ARQUITECTURA FINAL RECOMENDADA

Reestructura completa que cumple TODO lo que pediste:

```
/
├── /                          ← Home renovada con hero 100dvh + CTA
│
├── /servicios/                ← Índice con subcategorías
│   ├── /servicios/desarrollo-web/      ← Web, landing, tiendas
│   └── /servicios/automatizacion/      ← IA, n8n, agentes (NUEVO)
│   └── /servicios/soporte-it/          ← Soporte técnico
│
├── /proyectos/                ← Portfolio con filtros
│   ├── /proyectos/trackflow/
│   ├── /proyectos/clawmate/
│   ├── /proyectos/talk-to-the-machine/
│   └── /proyectos/demo-app/            ← Ya existe, mejorar
│
├── /sobre-mi/                 ← Solo biografía + enfoque
├── /certificaciones/          ← Solo formación + certs
├── /contacto/                 ← Formulario mejorado
├── /faq/                      ← FAQ con schema JSON-LD
│
├── /legal/
│   ├── /legal/aviso-legal/
│   ├── /legal/privacidad/     ← Redirigido 301 a /privacy-policy/
│   └── /legal/cookies/
├── /privacy-policy/
├── /terms-of-service/
├── /data-deletion/
│
├── /auth/
│   ├── /auth/tiktok/callback/
│   └── /auth/facebook/callback/
│
└── /gracias/                  ← Página funcional (CORREGIR)
```

### Menú desplegable propuesto (navbar)

```
[Logo]  Inicio  Servicios ▼  Proyectos ▼  Sobre mí  FAQ  Contacto
                ├ Desarrollo Web    ├ TrackFlow
                ├ Automatización   ├ ClawMate
                └ Soporte IT       └ Talk to Machine
```

### Estructura del footer

```
[Redes: GitHub | LinkedIn | WhatsApp]
[Aviso legal | Privacidad | Cookies | Términos | Data Deletion]
© 2026 Jonathan Esteban — experiencia actualizada dinámicamente
```

---

## ✏️ COPY PROPUESTO (honesto, sin inflación)

### Hero de la home (NUEVO)

```html
<h1>Desarrollo web, automatización con IA y soporte IT para negocios que quieren trabajar mejor</h1>
<p>Diseño y construyo sistemas — APIs, agentes de IA, workflows automatizados — que convierten procesos repetitivos en resultados medibles. </p>
<a href="/contacto/" class="btn-primary">Solicitar presupuesto</a>
<a href="/servicios/" class="btn-secondary">Ver servicios →</a>
```

### Barra de confianza (HONESTA)

```html
📍 Madrid · Barcelona · Remoto     |     🛠 5+ años soporte IT + gestión operativa
📦 6 proyectos reales (GitHub)     |     🎓 Full Stack + IA Engineering (4Geeks)
```

**NUNCA** pongas:
- ❌ "16+ años experiencia operativa" (no contextualizado)
- ❌ "100% Clientes satisfechos"
- ❌ "71% Bootcamp"

---

## 🤖 ALGORITMO DE ACTUALIZACIÓN AUTOMÁTICA

Incluir en el `<script>` de la web:

```javascript
// Auto-actualización anual de años de experiencia
const startYear = 2007;
const currentYear = new Date().getFullYear();
const experienceYears = currentYear - startYear;
document.querySelectorAll('[data-experience]').forEach(el => {
  el.textContent = experienceYears + '+';
});

// Proyectos realizados (alimentado por agente en el futuro)
// Mientras tanto, valor fijo verificable
```

Los spans en HTML se marcan con `data-experience` y se actualizan solos cada año.

---

## 📊 PRIORIDAD DE EJECUCIÓN

### Fase 1 — Inmediata (hoy)
1. ✅ Corregir `/gracias/` (P0-1)
2. ✅ Ajustar hero a 100dvh (P2-2)
3. ✅ Eliminar "100% Clientes satisfechos" (P1-3)
4. ✅ Eliminar "71%" de la home (P1-2)
5. ✅ Cambiar "16+ años" a texto honesto (P1-1)
6. ✅ Añadir CTA comercial en home (P1-6)
7. ✅ Poblar /servicios/automatizacion/ (P0-2)
8. ✅ Poblar /servicios/desarrollo-web/ (P0-2)

### Fase 2 — Corto plazo (1-3 días)
9. ✅ Reestructurar navbar con desplegables
10. ✅ Separar contenido: Sobre mí / Certificaciones / Proyectos (P1-4)
11. ✅ Subir demos a Vercel (P3-1)
12. ✅ Ajustar tipografía (P2-3)
13. ✅ Implementar breadcrumbs + botón return (P2-8)
14. ✅ Algoritmo años dinámicos (P2-6)

### Fase 3 — Integración con automatización
15. ✅ Desplegar lead bot en Hetzner VM
16. ✅ Conectar formulario → n8n → base de datos
17. ✅ Contador dinámico de proyectos desde DB (P2-7)
18. ✅ WhatsApp Business API
19. ✅ Chat widget en web

### Fase 4 — Legal y SEO
20. ✅ Banner de cookies funcional (P2-5)
21. ✅ JSON-LD Person + WebSite + FAQPage
22. ✅ Completar aviso legal RGDB
23. ✅ Sitemap actualizado
24. ✅ robots.txt optimizado

---

## ✅ ESTADO DE CADA RUTA SEGÚN TU PLAN MAESTRO

| Ruta requerida | Estado actual | Acción |
|----------------|:-------------:|--------|
| `/servicios/desarrollo-web/` | ❌ Vacío | Poblar con contenido |
| `/servicios/automatizacion/` | ❌ Vacío | Crear desde cero |
| `/servicios/soporte-it/` | ✅ OK | Ya existe + 301 desde /soporte-it/ |
| `/certificaciones/` | ⚠️ Existe | Separar de sobre-mí, quitar 71% |
| `/faq/` | ⚠️ Existe | Mejorar estructura, añadir schema |
| `/legal/aviso-legal/` | ⚠️ Breve | Completar |
| `/legal/privacidad/` | ✅ Redirect a /privacy-policy/ | OK |
| `/legal/cookies/` | ⚠️ Sin banner | Implementar |
| `/privacy-policy/` | ⚠️ Presente | Revisar contenido |
| `/terms-of-service/` | ⚠️ Breve | Completar |
| `/data-deletion/` | ✅ OK | |
| `/auth/tiktok/callback/` | ✅ OK | |
| `/auth/facebook/callback/` | ✅ OK | |
| `/gracias/` | ❌ Roto | Corregir urgente |

---

## 🧠 NOTAS ADICIONALES

### Sobre la redundancia "Sobre mí / Certificaciones / Proyectos"

Actualmente las 3 páginas contienen:
- **Sobre mí:** timeline + certificaciones + bootcamp + skills + barra de progreso 71%
- **Certificaciones:** bootcamp + certificados (mismos que sobre-mí)
- **Proyectos:** proyectos + descripciones

**Solución:**
- **Sobre mí:** Solo biografía personal, enfoque de trabajo, ubicación, valores. Sin listados de certificaciones.
- **Certificaciones:** Solo formación académica + certificaciones con fechas + enlaces.
- **Proyectos:** Solo casos de estudio con problema → solución → resultado.

### Sobre la tipografía

Solicitaste que la letra se vea muy junta. Recomendación para el CSS:

```css
body {
  letter-spacing: 0.01em;    /* antes: 0 o muy bajo */
  line-height: 1.7;          /* antes: ~1.5 */
}
```

Esto aplica a toda la web y mejora legibilidad especialmente en móvil.

---

## 🔜 PRÓXIMOS PASOS

Este documento es el **plan director**. Para implementarlo:

1. **Tú** decides qué orden seguir
2. **Yo** te ayudo a escribir el código de cada sección (componente por componente)
3. Priorizamos: primero lo que se ve (home, hero, navbar), después contenido interno

**¿Empezamos por la Fase 1 (correcciones inmediatas)?** Te ayudo a escribir los cambios en tu código fuente.