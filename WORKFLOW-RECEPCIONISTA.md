# RECEPCIONISTA IA — Plano de Implementación (propuesta para flecos)

> **Estado:** ✔️ En construcción (Fase 1: formulario → agente → aprobación Telegram).
> **Principio rector:** la IA redacta, TÚ apruebas con 1 clic antes de que algo salga.
> **Regla anti-fraude:** el agente NO responde a todo. Distingue y decide (ver §2bis).

---

## 1. Qué es (una frase)
Un **recepcionista IA en n8n** que escucha los mensajes que te llegan (formulario web,
correo y WhatsApp), los **entiende** con contexto tuyo de verdad (servicios, precios,
garantía de 15 días, CV real) y te prepara la respuesta para que la **apruebes tú**
en Telegram antes de que se envíe al cliente.

## 2. Principio: NO es un sistema de autorespuesta
El agente NO lanza plantillas. Con LLM *anclado a tu conocimiento*:
- Lee la intención (incidencia vs. presupuesto vs. instalación) → elige el servicio.
- Redacta en tu tono (cercano, directo, sin jerga).
- Nunca inventa cifras ni promete lo que no haces (regla 10 del plan).
- Si no está seguro, **no responde**: lo deriva a ti con el mensaje original.

## 3. Canales (los 3 con su nivel de "listo hoy")
| Canal | Disparador | Estado | Bloqueante |
|---|---|---|---|
| **Web (formulario)** | Netlify Function proxy → webhook n8n | 🟢 Montable hoy en local | Probar con `netlify dev` (no `http.server`) |
| **Correo** | Gmail trigger en n8n (poll a `joonathanesteban@gmail.com`) | 🟡 Requiere conectar Gmail a n8n | Aprobación OAuth de Google (es tu cuenta, tú la autorizas) |
| **WhatsApp** | WhatsApp Business (tienes la cuenta) — ⏸ **PAUSADO** | 🔴 En espera: solo opciones GRATUITAS hasta alcanzar volumen | No hay envío masivo gratuito real; se documentan las alternativas para retomar |

## 4. Arquitectura del workflow (workflow-base)
```
[Disparador]
  ├─ (Web) Netlify Function -> POST a webhook n8n
  ├─ (Gmail) Trigger: correo nuevo -> n8n
  └─ (WhatsApp) Meta webhook -> n8n
        │
        ▼
 [1. PRE-PROCESO] Limpiar mensaje + detectar canal/remitente
        ▼
 [2. AGENTE INICIAL] LLM con contexto embebido:
     • CV-DATA.md (tu experiencia real)
     • Los 6 servicios + precios base (MARKET-ANALYSIS.md)
     • Garantía 15 días
     • FAQ (respuestas a dudas frecuentes)
     → devuelve JSON: { intención, servicio, respuesta (sin enviar), dudas? }
        ▼
 [3. CLASIFICACIÓN] — el agente DECIDE, no responde a todo
     ┌─ ✅ LEAD REAL (incidencia de un usuario/empresa real) → prepara borrador
     ├─ ⚠️ FRAUDE/PHISHING (patrones de estafa, enlaces maliciosos,
     │     urgencia falsa, "te pago por adelantado", extraños cifras) → NUNCA
     │     responde: lo marca y te lo notifica para que decidas (reportar/bloquear)
     ├─ 😐 PERSONAL/IRRELEVANTE (amigo, familiar, spam) → MUESTRA pero NO contesta
     └─ 🤷 DUDA REAL → NO inventa: lo deriva a TI con el mensaje original
        ▼
 [4. APROBACIÓN HUMANA] Bot de Telegram (el que ya tienes):
     📩 *Borrador para [cliente]*
     "Hola, gracias por escribir… [respuesta redactada]"
     [✅ Aprobar y enviar]  [✏️ Editar]  [❌ Rechazar]
        ▼
 [5. ENVÍO SEGÚN CANAL]
     • Correo → Gmail (tu cuenta) → responder
     • WhatsApp → Cloud API → responder
     • Web-form → correo a ti + notificación
        ▼
 [6. MEMORIA] Guardar conversación por cliente/email (para no repetir)
```

## 5. El "agente inicial que lee y responde según tu experiencia"
En n8n se modela con un nodo **HTTP Request** hacia tu LiteLLM (localhost:4000)
o directamente al modelo, con un **system prompt construido** desde tus datos:
```
Eres el recepcionista de Jonathan Esteban (soporte IT, Barcelona).
Esto es lo que OFRECES (usa SIEMPRE precios y servicios reales):
- Servicio 1: Helpdesk N1 … (precio: ver MARKET-ANALYSIS)
- Servicio 2: Mantenimiento/Reparación PC …
- …
- Garantía: TODOS los servicios incluyen 15 días desde la entrega.
- Experiencia real (CV-DATA): locutorios 2007-2012, voluntariado 2024-2026…
NO inventes cifras. NO prometas plazos exactos que no controles.
Si no puedes responder con seguridad → {"needs_human": true}
Responde en español, tono cercano, 2-3 frases, y termina pidiendo el dato que
falta (modelo de equipo, barrio, horario).
```
El JSON devuelto deja claro cuándo el borrador está **listo para aprobar** y cuándo
necesita tu ojo → alimenta el botón de Telegram.

## 6. Seguridad (fiel a la Fase 5 del plan)
- El navegador **nunca ve la URL del webhook de n8n**: el form llama a tu dominio
  → Netlify Function → n8n (secret en `.env` de Netlify, no en el cliente).
- **Cabeceras duras** en `netlify.toml` (CSP + HSTS) — se añaden en esta fase.

## 2bis. Distinguir qué SÍ se contesta (anti-fraude y anti-spam)
**Regla de oro: el agente no responde a todo.** Cada mensaje pasa por una clasificación
de confianza ANTES de preparar borrador. El agente devuelve siempre un JSON con
`classificacion` y `justificacion` (para que tú veas POR QUÉ decide).

| Señal | Clasificación | Acción del agente |
|---|---|---|
| Habla de un servicio real, equipo, incidencia o presupuesto concreto | ✅ LEAD REAL | Prepara borrador y pide aprobación |
| `Factura por adelantado`, `Pago en segundos`, urgencia falsa, enlace raro, "soy un oficial", cifras extrañas, promesas de dinero fácil | ⚠️ FRAUDE/PHISHING | **NO responde**: notifica a TI, conserva el mensaje original |
| Amigo/familiar/fuera de contexto del negocio, o spam (ofertas, SEO masivo) | 😐 NO COMERCIAL | Muestra pero NO contesta |
| Pide algo que no está en tu conocimiento (precio raro, garantía que no das) | 🤷 DUDA REAL | **No inventa**: deriva a TI con el mensaje original |
| Mensaje en otro idioma, muy corto, sin señal clara | 🤷 AMBIGUO | Prepara borrador conservador y pide aprobación (tú decides) |

**Reglas d**e obligado cumplimiento del agente:
1. **Nunca** responde a fraude/spam — solo lo señala.
2. **Nunca** inventa precios, plazos ni servicios que no estén en tu contexto.
3. **Siempre** incluye justificación de su clasificación (para auditoría).
4. Si hay el menor riesgo de daño (mensaje personal, tema delicado), **no contesta**: te lo pasa.

## 7. Cómo se conectan los servicios (URLs y envs)
- **n8n está en Docker con red `host`** en tu VPS y expuesto en `https://n8n.jonathanesteban.dev` (ya responde 200).
- **El webhook de producción** (cuando se active) será:
  `https://n8n.jonathanesteban.dev/webhook/recepcionista-leads`
- Las **Netlify Functions corren en la nube de Netlify**, NO en tu VPS: por eso la variable
  de producción **no puede ser `localhost:5678`**. En Netlify Configuración → Env vars:
  - `N8N_WEBHOOK_LEADS_URL` = `https://n8n.jonathanesteban.dev/webhook/recepcionista-leads`
  - `N8N_WEBHOOK_SECRET` = `un-secreto-largo` (mismo valor que inyectarás en n8n)
- El contenedor n8n ya tiene `WEBHOOK_URL=https://n8n.jonathanesteban.dev/` y `GENERIC_TIMEZONE=Europe/Madrid` => los webhooks se generan en la URL pública por defecto.
- **n8n → LiteLLM**: ambos en red `host` => el nodo HTTP llama `http://localhost:4000/v1` (funciona).
- En **pruebas locales** (netlify dev) sí usamos `localhost:5678`, pero NUNCA en producción.

## 7. Qué creo / qué dejo "apuntado" (fase 1)
### Creo en local (verificable, sin push):
- `astro-portfolio/netlify/functions/contact-recepcionista.js` — proxy form → n8n.
- `astro-portfolio/netlify/functions/_shared/` — helpers de rate-limit + validación.
- Edición de `src/pages/contacto/index.astro` para **apuntar a tu endpoint** (con fallback
  a Formspree si el proxy falla, para no romper producción).
- Refuerzo de `netlify.toml` con `Content-Security-Policy` y `Strict-Transport-Security`.
- `FISCALIZACION.md` (7 puntos, adaptado a esta arquitectura).
- `docs/WORKFLOW-RECEPCIONISTA.md` — documento maestro de los 3 canales + cómo conectar
  Gmail y WhatsApp cuando quieras.

### Dejo documentado (no ejecutable aún por regla sin-push ni por trámites externos):
- Import del workflow n8n (`workflow-recepcionista.json`) — listo para importar.
- Pasos de conexión de **Gmail** (OAuth) y **WhatsApp** (Meta) con sus bloqueantes.

## 8. Qué NO hago (a propósito)
- NO desplego Netlify Functions hasta que acabes de revisar (tu regla).
- NO conecto WhatsApp hasta que tengas el número verificado (se documenta).
- NO reemplazo Formspree de golpe: el form tendrá **fallback** para no dejar el
  formulario roto si el proxy aún no está en producción.

## 9. Validación que haré antes de entregarte
- `npm run build` sigue OK.
- Pruebo la función en local con **`netlify dev`** → envío un form de prueba →
  compruebo que NO aparece ninguna URL de n8n en el cliente y que el webhook recibe.
- Te dejo el checklist `FISCALIZACION.md` para que lo firmes con 1 ✅ en local.

## 10. Tu decisión (para arrancar)
- [ ] **OK, monta la Fase 1 (formulario → agente → aprobación Telegram)** — empiezo ya.
- [ ] OK pero **solo el documento** `WORKFLOW-RECEPCIONISTA.md` primero (sin tocar código).
- [ ] Cambia algo del diseño (canales, tono, modo de aprobación, orden) antes de escribir.