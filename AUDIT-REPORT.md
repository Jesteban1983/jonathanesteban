# AUDIT-REPORT

Fecha: 2026-08-10
Proyecto auditado: jonathanesteban.dev (codigo local + validacion de navegacion en produccion)

## 1) Alcance y evidencia ejecutada

- Inventario completo de rutas y enlaces desde archivos HTML locales.
- Matriz de enlaces exportada: LINK-MATRIX.csv (511 filas).
- Prueba real en navegador sobre https://jonathanesteban.dev en desktop y viewport movil 390x844 para menu y enlaces principales.
- Verificacion de rutas minimas obligatorias en codigo local (site/**/index.html).
- Revision de formulario frontend + endpoint serverless.
- Revision de sitemap, robots y redirecciones Netlify.
- Escaneo de secretos en frontend/backend con patrones de API keys y tokens.

## 2) Resultado global

- Estado general: MEJORA
- Criticos P0 corregidos en codigo local: SI
- Riesgos pendientes de verificacion manual externa (NO VERIFICABLE): lector de pantalla real NVDA/VoiceOver, metricas Lighthouse, validacion de paneles TikTok/Meta.

## 3) Matriz final obligatoria (hallazgos principales)

| ID | Area | URL/archivo | Hallazgo | Estado | Severidad | Correccion aplicada | Evidencia |
|---|---|---|---|---|---|---|---|
| AUD-001 | Rutas | /servicios/desarrollo-web/ | Ruta requerida ausente | ERROR | P0 | Ruta creada con contenido comercial y CTA | Comprobacion en LINK-MATRIX.csv |
| AUD-002 | Rutas | /servicios/automatizacion/ | Ruta requerida ausente | ERROR | P0 | Ruta creada con alcance, exclusiones y aprobacion humana | Comprobacion en LINK-MATRIX.csv |
| AUD-003 | Rutas | /servicios/soporte-it/ | Ruta canonica requerida ausente | ERROR | P0 | Ruta creada; soporte consolidado en URL canonica | Comprobacion en LINK-MATRIX.csv |
| AUD-004 | SEO | /soporte-it/ | Duplicidad potencial de servicio Soporte IT | MEJORA | P1 | Redireccion y canonica a /servicios/soporte-it/ | Cambios en site/soporte-it/index.html y netlify.toml |
| AUD-005 | Rutas | /proyectos/trackflow/ | Ruta requerida ausente | ERROR | P0 | Ruta creada con estructura de caso y CTA | Comprobacion en LINK-MATRIX.csv |
| AUD-006 | Rutas | /proyectos/clawmate/ | Ruta requerida ausente | ERROR | P0 | Ruta creada con permisos, limites y aprobacion humana | Comprobacion en LINK-MATRIX.csv |
| AUD-007 | Rutas | /proyectos/talk-to-the-machine/ | Ruta requerida ausente | ERROR | P0 | Ruta creada con utilidad, limitaciones y CTA | Comprobacion en LINK-MATRIX.csv |
| AUD-008 | Legal | /legal/aviso-legal/ | Ruta legal requerida ausente | ERROR | P0 | Pagina legal creada | Comprobacion en LINK-MATRIX.csv |
| AUD-009 | Legal | /legal/privacidad/ | Ruta legal requerida ausente | ERROR | P0 | Alias legal implementado y coherencia con /privacy-policy/ | Comprobacion en LINK-MATRIX.csv |
| AUD-010 | Legal | /legal/cookies/ | Ruta legal requerida ausente | ERROR | P0 | Pagina de cookies creada | Comprobacion en LINK-MATRIX.csv |
| AUD-011 | Accesibilidad menu | site/assets/js/nav.js | Menu movil sin aria-controls/escape/foco robusto | ERROR | P0 | aria-controls automatico, cierre con Escape, foco al primer enlace y retorno de foco | Diff en nav.js |
| AUD-012 | Formulario | site/contacto/index.html | Campos incompletos para flujo comercial exigido | ERROR | P0 | Se agregaron telefono, servicio, negocio, presupuesto, plazo y consentimientos separados | Diff en contacto/index.html |
| AUD-013 | Formulario | site/assets/js/form.js | Validacion y estados de error/success limitados | MEJORA | P1 | Validacion nativa + mensajes accesibles role=alert/status + anti doble envio | Diff en form.js |
| AUD-014 | Seguridad formulario | functions/contact-submit.js | Validacion servidor insuficiente | ERROR | P0 | Validacion estricta, longitud de mensaje, consentimiento obligatorio y sanitizado basico | Diff en contact-submit.js |
| AUD-015 | Seguridad formulario | functions/contact-submit.js | Sin rate limiting basico | ERROR | P0 | Rate limit por IP en ventana temporal | Diff en contact-submit.js |
| AUD-016 | SEO | site/sitemap.xml | Sitemap desactualizado y sin nuevas canonicas | MEJORA | P2 | Sitemap actualizado con rutas canonicas y nuevas rutas de servicios/proyectos/legal | Diff en sitemap.xml |
| AUD-017 | SEO | site/sitemap.xml | URL de soporte legacy en sitemap | MEJORA | P2 | Eliminada URL legacy /soporte-it/ del sitemap | Diff en sitemap.xml |
| AUD-018 | SEO/Arquitectura | site/proyectos/index.html | Taxonomia de filtros no alineada con requerimiento | MEJORA | P2 | Filtros: Todos, Web, Backend/API, Automatizacion, Agentes IA, Herramientas internas | Diff en proyectos/index.html |
| AUD-019 | JS filtros | site/assets/js/filters.js | No soportaba multietiqueta por proyecto | MEJORA | P2 | Soporte para categorias multiples separadas por coma | Diff en filters.js |
| AUD-020 | Seguridad | functions + site | Exposicion de secretos en codigo auditado | OK | - | No se detectaron claves/tokens en texto plano con patrones comunes | Busqueda rg sin resultados |
| AUD-021 | Verificacion rutas minimas | LINK-MATRIX.csv | Cobertura de rutas obligatorias | OK | - | 22/22 rutas minimas presentes en codigo local | LINK-MATRIX.csv |
| AUD-022 | Rendimiento | proyecto completo | Lighthouse movil/escritorio | NO VERIFICABLE | P2 | Se intento con Lighthouse CLI y PageSpeed API; bloqueado por entorno (Chrome headless) y cuota 429 | logs de ejecucion en terminal |
| AUD-023 | Accesibilidad SR | proyecto completo | Prueba NVDA/VoiceOver manual | NO VERIFICABLE | P1 | Requiere ejecucion humana con lector de pantalla real | Limitacion de entorno |
| AUD-024 | OAuth/TikTok/Meta | /auth/tiktok/callback/ y /auth/facebook/callback/ | Coincidencia exacta con paneles developer externos | NO VERIFICABLE | P1 | Rutas existen, pero no se puede validar panel externo desde codigo local | Requiere acceso a consolas TikTok/Meta |

## 4) Resultado de inventario de enlaces

- Archivo: LINK-MATRIX.csv
- Filas: 511
- Resultado actual: 511 OK, 0 ERROR, 0 CRITICO (auditoria estatica local)

## 5) Cambios aplicados (archivos)

- functions/contact-submit.js
- netlify.toml
- site/assets/js/filters.js
- site/assets/js/form.js
- site/assets/js/nav.js
- site/contacto/index.html
- site/proyectos/index.html
- site/servicios/index.html
- site/sitemap.xml
- site/soporte-it/index.html
- site/legal/aviso-legal/index.html
- site/legal/privacidad/index.html
- site/legal/cookies/index.html
- site/proyectos/trackflow/index.html
- site/proyectos/clawmate/index.html
- site/proyectos/talk-to-the-machine/index.html
- site/servicios/desarrollo-web/index.html
- site/servicios/automatizacion/index.html
- site/servicios/soporte-it/index.html
- scripts/qa_audit.py
- .github/workflows/qa-audit.yml

## 6) Riesgos residuales y siguiente validacion recomendada

- Ejecutar Lighthouse real en deploy (mobile + desktop) y anexar metricas LCP/CLS/INP/TBT.
- Ejecutar pruebas manuales con NVDA/VoiceOver sobre menu, formularios, errores y confirmaciones.
- Validar en TikTok/Meta Developer que Redirect URI y URLs legales coinciden exactamente con las configuradas.
- Probar envio extremo-a-extremo del formulario en Netlify Functions (exito/error/red/429) con datos ficticios.

## 7) Paso 1 ejecutado (QA final adicional)

- Se ejecuto comprobacion HTTP real en produccion para 23 rutas clave y se guardo evidencia en reports/live-routes.json.
- Resultado actual en produccion: 9 rutas nuevas responden 404 (servicios/* nuevos, proyectos/* nuevos y legal/* nuevos), lo que confirma que los cambios aun no estan desplegados en el dominio.
- Se intento ejecutar Lighthouse CLI con Chromium (incluyendo ruta binaria directa y modo no interactivo), pero fallo por imposibilidad de conexion al proceso Chrome en este entorno.
- Se intento PageSpeed Insights API como alternativa, pero devolvio HTTP 429 por limite de cuota.

Estado del paso 1: EJECUTADO con evidencia de QA funcional/HTTP en produccion, pendiente de metricas Lighthouse hasta disponer de entorno compatible o tras despliegue.

## 8) Paso 2 ejecutado (automatizacion CI)

- Se creo scripts/qa_audit.py con validaciones criticas automatizadas:
	- existencia de rutas minimas obligatorias,
	- enlaces internos sin roturas,
	- title/h1/canonical por pagina,
	- reglas de sitemap para canonicidad de Soporte IT y exclusion de callbacks OAuth.
- Se creo .github/workflows/qa-audit.yml para ejecutar estas validaciones en cada push y pull_request.
- Ejecucion local verificada: pass (0 fallos, 0 warnings).

Estado del paso 2: COMPLETADO.
