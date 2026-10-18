# FISCALIZACION.md — Recepcionista IA (Fase 1)

> **Qué es:** checklist NO técnico para que verifiques (sin leer código) que la
> fase 1 del recepcionista IA es segura y hace solo lo que promete.
> **Cómo usarlo:** marca ✅ solo cuando lo hayas comprobado tú en local.
> **Regla:** nada se activa en producción sin tu visto bueno (sin push).

---

## Los 7 puntos (adaptados a esta arquitectura)

### 1. ✅ El formulario sigue funcionando aunque el agente falle
- [ ] Con el proxy "apagado" (sin webhook), el envío del form **cae a Formspree**
      (tu correo sigue llegando igual que hoy).
- [ ] Con el proxy activo, el mensaje llega al workflow n8n (y TÚ lo apruebas en Telegram).

### 2. ✅ No se expone ningún secreto en el navegador
- [ ] En la página de contacto (botón derecho → Ver código fuente) **no aparece**:
      la URL de n8n, el secreto compartido ni la API key de LiteLLM.
- [ ] El formulario solo llama a `/.netlify/functions/…` (relativa, sin host ni secretos).

### 3. ✅ Los bots no contaminan
- [ ] Envías un form rellenando el campo oculto `company_site` → se finge éxito pero
      **NO se reenvía a ninguna parte** (ni n8n ni correo).
- [ ] Envías 4+ formularios seguidos desde la misma IP → a partir del 4º te avisa
      "Demasiados envíos" (rate limit).

### 4. ✅ Fraude / spam: el agente NO responde a todo
- [ ] Envías un mensaje tipo phising ("te pago por adelantado", "soy un oficial",
      urgencia falsa) → en Telegram te aparece **⚠️ FRAUDE — NO responder** y NO hay borrador.
- [ ] Envías un mensaje de un amigo/familiar fuera de contexto → **NO se responde**, solo se muestra.
- [ ] Envías un mensaje real de un cliente (incidencia/presupuesto) → genera **borrador**
      y te pide aprobación con botones.

### 5. ✅ El agente NO inventa
- [ ] Con un mensaje pidiendo algo que no está en su contexto (precio que no existe,
      garantía que no das) → te lo **deriva a ti** con una duda, nunca inventa la cifra.
- [ ] Cualquier borrador que produzca lleva SIEMPRE tu OK (botón) antes de salir.

### 6. ✅ El webhook n8n no es público de verdad
- [ ] Accedes a `https://n8n.jonathanesteban.dev/webhook/recepcionista-leads` en el
      navegador → NO devuelve datos (solo el proxy autorizado con secreto puede enviar).
- [ ] En `netlify.toml` están activas las cabeceras de seguridad (CSP + HSTS) y no
      encontraste ninguna URL de n8n en el código del navegador (punto 2).

### 7. ✅ Tú controlas el envío final
- [ ] Ningún mensaje se responde al cliente sin que **apruebes** en Telegram.
- [ ] Los botones de Telegram son: **✅ Aprobar y enviar** / **❌ Descartar** — no existe
      "enviar en automático".

---

## Firmado

- [ ] He verificado los 7 puntos en local (`netlify dev`).
- [ ] Autorizo activar la Fase 1 en producción (proxoy + webhook + botones Telegram).

**Fecha:** ______________  **Firma:** ______________

---

## Qué NO está incluido (decisión consciente)
- WhatsApp — ⏸ **pausado** hasta encontrar opción gratuita de verdad con volumen de
  clientes (tienes WhatsApp Business; se documentan las opciones para reanudar).
- Gmail — 🟡 pendiente de conectar OAuth en n8n (es tu cuenta, tú la autorizas).
- Envío automático — ❌ no existe: todo pasa por aprobación humana.