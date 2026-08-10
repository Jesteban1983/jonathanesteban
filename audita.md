# Prompt maestro: auditar y corregir `jonathanesteban.dev`

## 0. Instrucciones de uso

Copia este documento completo en tu agente de desarrollo. El agente debe ejecutar la auditoría, corregir el código y entregar evidencia verificable.

No debe limitarse a leer la home ni asumir que una ruta funciona porque aparece en el menú. Debe probar la web con navegador real en escritorio y móvil, auditar el DOM renderizado, abrir cada enlace y comprobar las rutas públicas.

---

## 1. Rol del agente

Actúa como:

- Auditor técnico.
- Desarrollador frontend.
- Especialista en UX y conversión.
- Especialista en SEO técnico.
- Especialista en accesibilidad WCAG 2.2 nivel AA.
- Especialista en formularios y seguridad web.
- Especialista en integraciones OAuth con TikTok y Meta.

Tu misión es transformar `https://jonathanesteban.dev` en la web oficial y comercial de una agencia de:

- Desarrollo web.
- Automatización de procesos.
- Workflows con n8n.
- Agentes de IA.
- Integraciones con APIs.
- Soporte IT.
- Reparación y configuración informática.

La web debe funcionar como:

1. Portfolio técnico.
2. Sitio comercial para captar clientes.
3. Catálogo de servicios contratables.
4. Muestra de calidad técnica.
5. Web oficial para futuras integraciones con TikTok, Facebook/Meta, WhatsApp Business y YouTube.

---

## 2. Reglas obligatorias

### 2.1 Verificar antes de corregir

- Usa navegador real en escritorio y móvil.
- Inspecciona el DOM después de ejecutar JavaScript.
- Abre el menú hamburguesa.
- Extrae todos los enlaces visibles y generados dinámicamente.
- Haz clic en cada enlace interno.
- Prueba los enlaces externos sin ejecutar acciones destructivas.
- Abre cada URL pública directamente.
- Verifica los formularios con datos ficticios.
- Comprueba los estados de éxito y error.
- No declares que algo funciona sin probarlo.
- No declares que una página existe solo porque aparece en el menú.

### 2.2 Seguridad durante la auditoría

- No muestres API keys, tokens, cookies, sesiones ni contraseñas.
- No incluyas secretos en capturas ni reportes.
- Si encuentras un secreto, informa del archivo y severidad, pero no de su valor.
- No envíes mensajes reales a clientes.
- Usa cuentas, emails y teléfonos de prueba.
- No publiques contenido en redes sociales.
- No elimines datos ni despliegues cambios destructivos sin autorización.

### 2.3 Honestidad sobre el contenido

- No inventes clientes, resultados, certificaciones, precios ni testimonios.
- No presentes una formación en curso como certificación terminada.
- No presentes un proyecto de cliente como propio sin confirmación.
- No prometas aprobación de TikTok, Meta o WhatsApp.
- No describas funcionalidades que no existan en la demo o el producto.
- Si algo no puede comprobarse, usa el estado `NO VERIFICABLE`.

---

## 3. Contexto de la marca

### 3.1 Posicionamiento actual

La web presenta a Jonathan Esteban como:

> Full-Stack Developer & AI Engineer

Mensaje base:

> Construyo sistemas —APIs, automatizaciones, agentes de IA— que resuelven problemas reales de negocio.

Ubicación:

- Madrid y Barcelona, España.
- Remoto internacional.

### 3.2 Proyectos actuales

Conserva y revisa estos proyectos:

- **TrackFlow:** sistema de gestión de inventario con FastAPI, JWT, PostgreSQL, Next.js y Supabase.
- **ClawMate:** agente de IA con OpenClaw y Composio MCP.
- **Talk to the Machine:** chat conversacional con Groq API, LLaMA 3 y Next.js.

### 3.3 Servicios que deben poder contratarse

- Desarrollo de webs corporativas.
- Landing pages.
- Tiendas online básicas.
- Rediseño y mantenimiento web.
- Automatización de formularios y leads.
- Integraciones con CRM, email y APIs.
- Workflows con n8n.
- Agentes de IA.
- Soporte técnico remoto o presencial, si realmente se ofrece.
- Configuración y optimización de ordenadores.
- Instalación de software con licencia legítima.
- Reparación informática con diagnóstico previo.

---

## 4. Arquitectura final obligatoria

Usa esta arquitectura como referencia:

```text
/
├── /servicios/
│   ├── /servicios/desarrollo-web/
│   ├── /servicios/automatizacion/
│   └── /servicios/soporte-it/
├── /proyectos/
│   ├── /proyectos/trackflow/
│   ├── /proyectos/clawmate/
│   └── /proyectos/talk-to-the-machine/
├── /certificaciones/
├── /sobre-mi/
├── /contacto/
├── /faq/
├── /legal/aviso-legal/
├── /legal/privacidad/
├── /legal/cookies/
├── /privacy-policy/
├── /terms-of-service/
├── /data-deletion/
├── /auth/tiktok/callback/
├── /auth/facebook/callback/
└── /gracias/
```

### 4.1 Regla de soporte IT

Soporte IT es un servicio dentro de Servicios. Usa una única URL canónica:

```text
/servicios/soporte-it/
```

No crees simultáneamente:

```text
/soporte-it/
/servicios/soporte-tecnico/
```

si ambas páginas tienen el mismo objetivo y contenido. Esto sería redundante, confundiría al usuario y podría dividir la relevancia SEO entre varias URLs.

Si esas rutas ya existen:

1. Conserva la página más completa en `/servicios/soporte-it/`.
2. Redirige las URLs antiguas mediante 301.
3. Actualiza todos los enlaces internos.
4. Elimina las URLs antiguas del sitemap.
5. Añade canonical a `/servicios/soporte-it/`.
6. Comprueba que no existan cadenas de redirección.

Solo crea páginas adicionales si tienen una intención distinta, por ejemplo:

```text
/servicios/reparacion-ordenadores-barcelona/
/servicios/mantenimiento-informatico-empresas/
```

Estas páginas solo se justifican si realmente tienen público, oferta y contenido diferentes.

---

## 5. Fase 1: inventario del sitio

Construye un inventario completo de todas las rutas, enlaces, assets y formularios.

### 5.1 Matriz de enlaces

Entrega una tabla con estas columnas:

| Campo | Contenido |
|---|---|
| ID | Identificador del hallazgo |
| URL de origen | Página donde aparece el enlace |
| Texto visible | Texto o `aria-label` |
| URL destino | Destino final |
| Tipo | Interno, externo, ancla, descarga u OAuth |
| Visible desktop | Sí/No |
| Visible móvil | Sí/No |
| Requiere JavaScript | Sí/No |
| HTTP final | Código de respuesta |
| Redirecciones | Cadena completa |
| Title | Título de destino |
| H1 | H1 de destino |
| Canonical | URL canónica |
| Resultado | OK, MEJORA, ERROR, CRÍTICO o NO VERIFICABLE |
| Evidencia | Prueba ejecutada |

### 5.2 Rutas mínimas

Comprueba estas rutas, aunque no aparezcan indexadas:

```text
/
/servicios/
/servicios/desarrollo-web/
/servicios/automatizacion/
/servicios/soporte-it/
/proyectos/
/proyectos/trackflow/
/proyectos/clawmate/
/proyectos/talk-to-the-machine/
/certificaciones/
/sobre-mi/
/contacto/
/faq/
/legal/aviso-legal/
/legal/privacidad/
/legal/cookies/
/privacy-policy/
/terms-of-service/
/data-deletion/
/auth/tiktok/callback/
/auth/facebook/callback/
/gracias/
```

Si una ruta no existe:

- Comprueba si existe una alternativa.
- No dupliques contenido.
- Crea la ruta si es necesaria.
- Si no es necesaria, documenta por qué no se crea.

---

## 6. Fase 2: menú hamburguesa

### 6.1 Pruebas móviles

Usa al menos un viewport aproximado de `390x844`.

Comprueba:

- El botón existe.
- El botón tiene nombre accesible.
- Es realmente un `<button>`.
- Tiene `aria-expanded`.
- Tiene `aria-controls`.
- Cambia `aria-expanded` al abrir y cerrar.
- El menú aparece dentro del viewport.
- El foco entra correctamente al menú.
- Escape cierra el menú.
- Al seleccionar una ruta, el menú se cierra.
- El foco vuelve al botón al cerrar.
- No queda un overlay bloqueando el contenido.
- No hay scroll horizontal.
- Todos los enlaces se pueden usar con teclado.

### 6.2 Menú principal

Debe incluir:

```text
Inicio
Servicios
Proyectos
Certificaciones
Sobre mí
Contacto
FAQ
```

Soporte IT debe aparecer como servicio dentro de Servicios o como enlace directo a `/servicios/soporte-it/`, pero no como una página duplicada.

### 6.3 Footer

Debe mostrar enlaces visibles a:

```text
Aviso legal
Privacidad
Cookies
Terms of Service
Data Deletion
Contacto
GitHub
LinkedIn
```

No dejes las páginas legales únicamente dentro del menú hamburguesa.

---

## 7. Fase 3: auditoría de la home

### 7.1 Hero

El hero debe explicar en pocos segundos:

- Quién eres.
- Qué construyes.
- Para quién.
- Qué problema resuelves.
- Qué acción debe realizar el visitante.

Si no existe una propuesta comercial clara, usa esta base adaptándola al contenido real:

**Título:**

> Desarrollo web, automatización y agentes de IA para negocios que quieren trabajar mejor.

**Subtítulo:**

> Diseño y construyo webs, integraciones y sistemas automatizados que convierten tareas repetitivas en procesos simples, medibles y escalables.

**CTA primaria:**

> Solicitar presupuesto

**CTA secundaria:**

> Ver servicios

Conserva `Full-Stack Developer & AI Engineer` como descriptor profesional, pero no como única propuesta comercial.

### 7.2 Secciones recomendadas

Orden sugerido:

1. Header.
2. Hero.
3. Barra de confianza.
4. Servicios.
5. Cómo trabajo.
6. Proyectos destacados.
7. Resultados o beneficios verificables.
8. Certificaciones y formación.
9. FAQ resumida.
10. CTA final.
11. Footer legal.

### 7.3 Barra de confianza

Usa únicamente datos reales:

- Ubicación.
- Años de experiencia operativa, explicados correctamente.
- Proyectos realizados.
- Tecnologías.
- Formación en curso o completada.
- Disponibilidad remota.

No presentes una barra de progreso como si fuera una certificación.

---

## 8. Fase 4: servicios

### 8.1 Índice `/servicios/`

Debe ser una página comercial que permita entender y contratar los servicios.

Cada servicio debe incluir:

- Cliente ideal.
- Problema que resuelve.
- Resultado esperado.
- Entregables.
- Exclusiones.
- Plazo orientativo.
- Precio desde o proceso de presupuesto.
- CTA.
- FAQ específica.

### 8.2 Desarrollo web

Ruta:

```text
/servicios/desarrollo-web/
```

Debe explicar:

- Web corporativa.
- Landing page.
- Tienda online básica.
- Rediseño.
- Mantenimiento.
- Integración de formularios.
- CTA contextual a `/contacto/?service=desarrollo-web`.

### 8.3 Automatización y agentes

Ruta:

```text
/servicios/automatizacion/
```

Debe explicar:

- Automatización de formularios.
- Captura y cualificación de leads.
- Integración con email y CRM.
- Workflows n8n.
- Agentes de IA.
- APIs y herramientas externas.
- Aprobación humana para acciones sensibles.
- CTA contextual a `/contacto/?service=automatizacion`.

### 8.4 Soporte IT

Ruta única:

```text
/servicios/soporte-it/
```

Debe explicar:

- Diagnóstico informático.
- Soporte remoto.
- Soporte presencial solo si realmente se ofrece.
- Configuración y optimización.
- Instalación de software legítimo.
- Mantenimiento preventivo.
- Reparación básica con diagnóstico.
- Protección de datos antes de intervenir.
- CTA contextual a `/contacto/?service=soporte-it`.

Incluye esta advertencia cuando corresponda:

> Antes de intervenir en un equipo se revisará el estado de los datos y se recomendará una copia de seguridad cuando exista riesgo de pérdida.

No prometas recuperación de datos garantizada.

---

## 9. Fase 5: portfolio y casos

### 9.1 Índice `/proyectos/`

Debe permitir filtrar por:

```text
Todos
Web
Backend/API
Automatización
Agentes IA
Herramientas internas
```

### 9.2 Plantilla de cada caso

Cada proyecto debe tener:

```text
Título
Tipo de proyecto
Estado real
Contexto
Problema
Objetivo
Solución
Arquitectura
Stack
Decisiones clave
Resultado verificable
Limitaciones
Siguiente fase
CTA: Quiero algo similar
```

### 9.3 TrackFlow

Comprueba:

- Si está en desarrollo o terminado.
- Si es proyecto propio, demo o cliente.
- Que el enlace GitHub funciona.
- Que no expone secretos.
- Que los beneficios descritos son verificables.
- Que tiene CTA contextual.

### 9.4 ClawMate

Comprueba:

- Qué tareas ejecuta realmente.
- Qué servicios conecta.
- Qué permisos necesita.
- Qué acciones requieren aprobación humana.
- Qué datos procesa.
- Que no se usa “autónomo” como promesa absoluta.
- Que no aparecen credenciales ni datos reales.

### 9.5 Talk to the Machine

Comprueba:

- Que la demo funciona.
- Que no expone claves de Groq.
- Que tiene manejo de errores.
- Que limita abusos.
- Que explica su utilidad empresarial.
- Que tiene CTA para solicitar un sistema similar.

---

## 10. Fase 6: certificaciones y formación

Ruta:

```text
/certificaciones/
```

Para cada elemento muestra solo información real:

```text
Nombre
Institución
Estado
Fecha
Tecnologías
Enlace o evidencia
```

Si 4Geeks está en curso, utiliza una redacción como:

> Formación Full Stack & AI Engineer en curso — 4Geeks Academy.

No la presentes como certificación terminada ni uses “71 % Bootcamp” sin contexto.

---

## 11. Fase 7: Sobre mí

Ruta:

```text
/sobre-mi/
```

Debe incluir:

- Quién eres.
- Experiencia operativa.
- Formación actual.
- Perfil técnico.
- Enfoque de trabajo.
- Madrid, Barcelona y remoto.
- Diferencia entre experiencia operativa y experiencia como desarrollador.

No conviertas “16+ años de experiencia operativa” en “16 años de experiencia como desarrollador” si no es exacto.

---

## 12. Fase 8: contacto y formulario

Ruta:

```text
/contacto/
```

### 12.1 Campos

```text
Nombre
Email
Teléfono opcional
Servicio
Tipo de negocio
Presupuesto orientativo
Plazo
Mensaje
Consentimiento para responder
Consentimiento separado para WhatsApp
Honeypot anti-spam
```

### 12.2 Flujo

```text
Formulario
  ↓
Validación del navegador
  ↓
Endpoint seguro
  ↓
Validación del servidor
  ↓
Resend o Brevo
  ↓
Email interno
  ↓
Confirmación al cliente
  ↓
Webhook n8n/CRM opcional
```

### 12.3 Seguridad

- No uses `mailto:` como flujo principal.
- No expongas claves API en JavaScript del navegador.
- Valida siempre también en servidor.
- Añade rate limiting.
- Usa honeypot o CAPTCHA accesible.
- Escapa contenido HTML.
- Limita el tamaño del mensaje.
- Registra el consentimiento.
- No envíes WhatsApp posterior sin consentimiento adecuado.

### 12.4 Pruebas

Prueba con datos ficticios:

- Envío correcto.
- Campos obligatorios vacíos.
- Email inválido.
- Doble clic.
- Error del proveedor de email.
- Error de red.
- Pantalla móvil.
- Lector de pantalla.
- Mensaje de éxito.
- Mensaje de error.

---

## 13. Fase 9: FAQ

Ruta:

```text
/faq/
```

Debe responder:

- Qué servicios ofreces.
- Cómo empieza un proyecto.
- Qué necesitas del cliente.
- Plazos orientativos.
- Forma de pago.
- Mantenimiento.
- Soporte remoto y presencial.
- Licencias de software.
- Protección de datos.
- Cómo solicitar presupuesto.
- Cómo funciona la automatización con n8n.
- Cuándo interviene una persona.

Usa datos estructurados `FAQPage` únicamente si las preguntas y respuestas están visibles en la página y son reales.

---

## 14. Fase 10: páginas legales

### 14.1 Rutas

```text
/legal/aviso-legal/
/legal/privacidad/
/legal/cookies/
/privacy-policy/
/terms-of-service/
/data-deletion/
```

Puedes mostrar el contenido en español y mantener aliases en inglés para las plataformas, siempre que las URLs configuradas carguen contenido real, público y coherente.

### 14.2 Privacy Policy

Debe describir realmente:

- Responsable del tratamiento.
- Datos recogidos.
- Formularios.
- Email.
- WhatsApp.
- TikTok.
- Facebook/Meta.
- YouTube.
- n8n.
- Hosting.
- APIs de IA.
- Finalidades.
- Base legal.
- Conservación.
- Derechos.
- Eliminación.
- Contacto.
- Tokens OAuth, si se almacenan.

### 14.3 Terms of Service

Debe incluir:

- Descripción del sitio o aplicación.
- Uso permitido.
- Contenido del usuario.
- Propiedad intelectual.
- Integraciones de terceros.
- Responsabilidad del usuario.
- Limitaciones del servicio.
- Suspensión.
- Cambios.
- Contacto.
- Ley aplicable.

### 14.4 Data Deletion

Debe explicar:

1. Qué datos pueden eliminarse.
2. Cómo solicitar la eliminación.
3. Qué información debe aportar la persona para localizar los datos.
4. Plazo de gestión.
5. Qué datos pueden conservarse por obligación legal.
6. Cómo se confirmará la eliminación.

Si Meta requiere callback técnico, implementa también el endpoint correspondiente.

---

## 15. Fase 11: TikTok, Meta y OAuth

### 15.1 TikTok

Comprueba:

- Web URL.
- Terms of Service URL.
- Privacy Policy URL.
- Dominio verificado.
- Redirect URI exacto.
- HTTPS.
- Parámetro `state`.
- Manejo de errores.
- No exposición de tokens.

Ruta propuesta:

```text
/auth/tiktok/callback/
```

### 15.2 Facebook/Meta

Comprueba:

- App Domains.
- Privacy Policy URL.
- Terms URL si corresponde.
- Data Deletion URL.
- Data Deletion Callback.
- Callback OAuth.
- HTTPS.
- Política accesible y coherente.

Ruta propuesta:

```text
/auth/facebook/callback/
```

No marques ningún requisito como cumplido solo porque la ruta exista. Debe cargar correctamente y coincidir exactamente con la configuración del panel de desarrolladores.

---

## 16. Fase 12: SEO técnico

### 16.1 SEO por página

Para cada página comprueba:

- Intención de búsqueda principal.
- `title` único.
- `meta description` única.
- Un solo `h1`.
- Jerarquía correcta de headings.
- Texto real en el DOM.
- Enlaces `<a href>` rastreables.
- Canonical.
- Open Graph.
- Twitter/X card.
- `lang="es"`.
- Alt de imágenes.
- URL limpia.
- Breadcrumbs cuando aporten orientación.

### 16.2 Evitar canibalización

- Una intención principal por URL.
- Una única página principal para soporte IT: `/servicios/soporte-it/`.
- No mantener dos páginas con el mismo servicio.
- Redireccionar URLs antiguas.
- Eliminar duplicados del sitemap.
- Usar canonical en la URL definitiva.
- Revisar enlaces internos para que apunten a la URL canónica.

### 16.3 Home sugerida

Si refleja el contenido real, puedes usar:

```html
<title>Jonathan Esteban | Desarrollo web, automatización y soporte IT</title>
<meta name="description" content="Desarrollo web, automatización con n8n, agentes de IA y soporte informático para negocios y profesionales en España y remoto internacional.">
```

### 16.4 Indexación

Comprueba:

- `robots.txt`.
- `sitemap.xml`.
- Sitemap con solo URLs canónicas.
- Callbacks OAuth fuera del sitemap.
- Páginas privadas fuera del índice.
- Redirecciones 301 correctas.
- No existen cadenas o bucles de redirección.
- Las páginas importantes son alcanzables mediante enlaces internos.

### 16.5 Datos estructurados

Usa JSON-LD solo con datos verdaderos:

- `Person` para Jonathan.
- `Organization` o `ProfessionalService` si la agencia está realmente definida.
- `WebSite`.
- `BreadcrumbList`.
- `FAQPage` solo con FAQ visible.
- `SoftwareApplication` solo para demos que realmente sean aplicaciones.

No inventes valoraciones, precios, reseñas, clientes ni resultados.

---

## 17. Fase 13: accesibilidad para personas ciegas

Implementa y prueba **WCAG 2.2 nivel AA**, con especial atención a lectores de pantalla, navegación no visual, teclado, zoom, contraste y formularios.

### 17.1 Estructura semántica

- Usa un único `h1` descriptivo por página.
- Mantén jerarquía lógica `h2` y `h3`.
- No uses headings solo para obtener tamaño visual.
- Usa `header`, `nav`, `main`, `section`, `article` y `footer` correctamente.
- Añade `Saltar al contenido principal` al inicio.
- Usa `<nav aria-label="Navegación principal">`.
- Marca la página actual con `aria-current="page"`.
- Define títulos de página únicos y descriptivos.
- No ocultes contenido esencial solo mediante CSS o imágenes.

### 17.2 Menú y teclado

- El botón de menú debe ser `<button>`.
- Debe tener nombre accesible.
- Debe actualizar `aria-expanded`.
- Debe asociarse al menú con `aria-controls`.
- Al abrir, mueve el foco al primer enlace.
- Al cerrar, devuelve el foco al botón.
- Escape debe cerrar el menú.
- El foco debe ser visible.
- Tab, Enter y Shift+Tab deben permitir recorrer todo.
- No uses `aria-hidden` sobre contenido que tenga foco.
- El orden del foco debe coincidir con el orden visual y lógico.

### 17.3 Imágenes e iconos

- Toda imagen informativa tiene `alt` descriptivo.
- Toda imagen decorativa usa `alt=""`.
- No pongas información esencial solo en imágenes.
- Iconos decorativos con `aria-hidden="true"`.
- Iconos interactivos con nombre accesible.
- Capturas de proyectos con texto alternativo útil.
- No repitas en `alt` el texto visible inmediatamente al lado.

### 17.4 Enlaces y botones

- Usa texto descriptivo: `Ver caso de TrackFlow` en vez de `Ver más`.
- No uses `href="#"` sin comportamiento real.
- No uses `div` como botón.
- Diferencia semánticamente enlaces y botones.
- Indica si un enlace abre una pestaña nueva.
- Usa `rel="noopener noreferrer"` cuando corresponda.

### 17.5 Formularios

- Cada campo tiene `<label>` asociado mediante `for` e `id`.
- Indica los campos obligatorios.
- No dependas solo del placeholder.
- Usa `fieldset` y `legend` para grupos.
- Usa `autocomplete` apropiado.
- Vincula instrucciones con `aria-describedby`.
- Vincula errores con el campo.
- No señales errores solo con color.
- Al enviar con errores, enfoca el resumen o primer campo inválido.
- Anuncia éxito con `role="status"`.
- Anuncia errores importantes con `role="alert"` sin exceso de interrupciones.
- Comprueba el formulario con lector de pantalla.

### 17.6 Pruebas con lector de pantalla

Cuando estén disponibles, prueba:

- NVDA + Firefox o Chrome en Windows.
- VoiceOver + Safari en macOS o iOS.

Documenta:

- Lectura del título de cada página.
- Navegación por headings.
- Navegación por landmarks.
- Navegación por enlaces.
- Navegación por botones.
- Apertura y cierre del menú.
- Lectura de tarjetas de proyectos.
- Lectura de campos del formulario.
- Lectura de errores.
- Lectura de confirmación de envío.
- Orden del foco.

### 17.7 Zoom, contraste y movimiento

- Prueba zoom al 200 %.
- Prueba reflow al 400 % cuando sea aplicable.
- Comprueba contraste de texto y controles.
- No uses color como único indicador.
- Respeta `prefers-reduced-motion`.
- No uses carruseles automáticos sin controles accesibles.
- Comprueba que el foco no quede oculto.

No consideres suficiente una puntuación de Lighthouse. La prueba manual con lector de pantalla es obligatoria para encontrar problemas de orden, nombres, foco y anuncios.

---

## 18. Fase 14: rendimiento

Ejecuta Lighthouse o equivalente en móvil y escritorio.

Registra valores reales de:

- Performance.
- Accessibility.
- Best Practices.
- SEO.
- LCP.
- CLS.
- INP o TBT.
- Peso total.
- Imágenes.
- Fuentes.
- Scripts bloqueantes.

No inventes puntuaciones. Incluye la fecha y configuración de la prueba.

---

## 19. Fase 15: seguridad

Busca y corrige:

- API keys en frontend.
- Tokens OAuth en repositorios.
- Archivos `.env` públicos.
- Datos reales de clientes.
- Emails o teléfonos en capturas.
- XSS en contenido dinámico.
- Formularios sin validación servidor.
- CORS innecesariamente abierto.
- Ausencia de headers básicos.
- Dependencias vulnerables.
- Enlaces a paneles internos.

Si encuentras un secreto:

1. No lo incluyas.
2. Identifica archivo, línea aproximada y severidad sin revelar valor.
3. Solicita confirmación antes de revocarlo si no tienes autorización.
4. Recomienda rotación.
5. Revisa el historial Git.
6. Corrige el origen.

---

## 20. Correcciones prioritarias

### P0 — bloquea lanzamiento o revisión de plataforma

- Formulario roto.
- Falta de Privacy Policy.
- Falta de Terms of Service.
- Falta de Data Deletion.
- Secreto expuesto.
- Callback OAuth inválido.
- Enlace crítico roto.
- Menú inaccesible.

### P1 — afecta conversión y confianza

- Falta CTA de presupuesto.
- Servicios poco claros.
- Proyectos sin caso de negocio.
- Falta FAQ.
- Falta página de contacto.
- Información contradictoria.
- Soporte IT duplicado.

### P2 — calidad técnica

- SEO incompleto.
- Canonicals incorrectos.
- Sitemap desactualizado.
- Falta de datos estructurados apropiados.
- Problemas de contraste.
- Alt deficientes.
- Problemas de foco.
- Lighthouse bajo.

### P3 — mejoras futuras

- Dashboard de leads.
- n8n conectado al formulario.
- WhatsApp Business.
- CRM.
- Multiidioma.
- Automatización comercial.

---

## 21. Matriz final obligatoria

Entrega una tabla con este formato:

| ID | Área | URL/archivo | Hallazgo | Estado | Severidad | Corrección aplicada | Evidencia |
|---|---|---|---|---|---|---|---|
| AUD-001 | Menú | `/` | Enlace Servicios | OK | — | — | Prueba móvil |
| AUD-002 | Legal | `/privacy-policy/` | No carga | ERROR | P0 | Página corregida | HTTP + navegador |

Estados permitidos:

```text
OK
MEJORA
ERROR
CRÍTICO
NO VERIFICABLE
```

Severidades:

```text
P0: bloquea lanzamiento o revisión de plataforma
P1: afecta conversión, confianza o funcionamiento principal
P2: afecta calidad técnica, SEO o accesibilidad no bloqueante
P3: mejora futura
```

---

## 22. Criterios de aceptación

La tarea solo se considera terminada cuando:

- Todas las rutas del menú fueron abiertas.
- Todos los enlaces internos fueron probados.
- No quedan enlaces críticos rotos.
- Existe una única página canónica para Soporte IT.
- La home tiene CTA comercial.
- Los servicios son comprensibles y contratables.
- Los proyectos tienen problema, solución, resultado y CTA.
- El formulario funciona con datos de prueba.
- El email interno llega correctamente.
- No se exponen secretos.
- Privacy Policy carga.
- Terms of Service carga.
- Data Deletion carga.
- Los callbacks tienen implementación o estado documentado.
- El footer tiene enlaces legales visibles.
- SEO básico está configurado.
- El menú funciona con teclado.
- La web funciona con lector de pantalla.
- Los formularios son accesibles.
- Se probó zoom y reflow.
- Lighthouse fue ejecutado y reportado.
- Se entregó matriz enlace por enlace.
- Se entregaron evidencias reales.

---

## 23. Orden de ejecución

Ejecuta el trabajo en este orden:

1. Inventario y rastreo.
2. Prueba del menú.
3. Prueba de todas las rutas.
4. Auditoría de contenido.
5. Auditoría legal.
6. Auditoría del formulario.
7. Auditoría de TikTok y Meta.
8. Auditoría SEO.
9. Auditoría de accesibilidad.
10. Auditoría de rendimiento.
11. Auditoría de seguridad.
12. Correcciones P0.
13. Correcciones P1.
14. Correcciones P2.
15. Pruebas de regresión.
16. Informe final.

No rediseñes antes de terminar el inventario. No elimines páginas sin documentarlo. No cierres la tarea con recomendaciones genéricas: entrega pruebas concretas.

---

## 24. Prompt operativo resumido

```text
Audita y corrige https://jonathanesteban.dev como web oficial de una agencia de desarrollo web, automatización, n8n, agentes IA y soporte IT.

Usa navegador real en escritorio y móvil. Abre el menú hamburguesa, extrae todos los enlaces del DOM renderizado, prueba cada ruta y crea una matriz con URL de origen, texto, destino, HTTP, redirecciones, title, h1, canonical, visibilidad móvil, resultado y evidencia.

Usa una única página canónica para soporte IT:
/servicios/soporte-it/

No mantengas /soporte-it/ ni /servicios/soporte-tecnico/ con contenido duplicado. Si existen, consolida, redirige con 301, actualiza enlaces y elimina duplicados del sitemap.

Audita y corrige:
- Home y propuesta comercial.
- Menú y footer.
- Servicios.
- Proyectos y casos.
- Certificaciones.
- Sobre mí.
- Contacto y formulario.
- FAQ.
- Aviso legal, privacidad y cookies.
- Terms of Service.
- Data Deletion.
- Callbacks TikTok y Facebook.
- SEO técnico.
- Accesibilidad WCAG 2.2 AA.
- Lectores de pantalla NVDA/VoiceOver.
- Teclado, foco, headings, landmarks, alt, labels y errores.
- Zoom 200 %, reflow, contraste y movimiento.
- Rendimiento.
- Seguridad y secretos.

No inventes información. No muestres credenciales. Marca como NO VERIFICABLE lo que no puedas comprobar.

Corrige primero P0, después P1 y P2. Ejecuta pruebas de regresión. Entrega AUDIT-REPORT.md y LINK-MATRIX.csv con la matriz enlace por enlace, severidad, corrección aplicada y evidencia real.
```

---

## 25. Fuentes técnicas de referencia

Usa como referencia técnica:

- WCAG 2.2 del W3C para accesibilidad y compatibilidad con tecnologías de asistencia.
- WAI sobre cambios y criterios de WCAG 2.2.
- Google Search Central para SEO técnico y rastreo.
- Google Search Central para datos estructurados.
- TikTok Developer Guidelines y requisitos de URL.
- Meta Data Deletion Callback.

