# 📊 Guía de Configuración: Google Sheets como Backend de Leads

Esta guía te permite recibir **todos los envíos del formulario de contacto directamente en una hoja de Google Sheets de forma 100% gratuita, sin límites mensuales y con tu diseño web intacto**.

---

## Opción 1 (Recomendada): Google Apps Script + Google Sheets

Con este método, tu formulario envía los datos a través de la función serverless de Netlify (`contact-recepcionista.js`), filtrando spam y guardando cada lead ordenadamente en tu hoja de cálculo.

### Paso 1: Crear la Hoja de Google Sheets
1. Entra en [Google Sheets](https://sheets.new) y crea una hoja de cálculo nueva.
2. Nómbrala, por ejemplo: **`Leads Web - jonathanesteban.dev`**.

---

### Paso 2: Abrir el editor de Google Apps Script
1. En el menú superior de tu hoja de cálculo, haz clic en **Extensiones** → **Apps Script**.
2. Borra el código que aparezca por defecto en `Código.gs` y pega el siguiente código:

```javascript
/**
 * Webhook para recepcionar leads de jonathanesteban.dev
 */
const WEBHOOK_SECRET = "CAMBIA_ESTO_POR_UNA_CLAVE_SEGURA"; // Ej: mi-clave-super-secreta-2026

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.tryLock(10000); // Evitar colisiones concurrentes

  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const data = JSON.parse(e.postData.contents);

    // Validar secreto si está configurado
    if (WEBHOOK_SECRET && data.secret !== WEBHOOK_SECRET) {
      return ContentService.createTextOutput(
        JSON.stringify({ status: 'error', message: 'Unauthorized' })
      ).setMimeType(ContentService.MimeType.JSON);
    }

    // Crear encabezados si la hoja está vacía
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        'Fecha',
        'Nombre',
        'Email',
        'Asunto',
        'Mensaje',
        'Acepta WhatsApp',
        'IP'
      ]);
      // Formato negrita al encabezado
      sheet.getRange(1, 1, 1, 7).setFontWeight('bold');
    }

    // Formatear fecha
    const fecha = new Date().toLocaleString('es-ES', { timeZone: 'Europe/Madrid' });

    // Añadir fila con el lead
    sheet.appendRow([
      fecha,
      data.name || '',
      data.email || '',
      data.subject || '',
      data.message || '',
      data.consentWhatsapp ? 'Sí' : 'No',
      data.ip || ''
    ]);

    // (Opcional) Notificación automática a tu correo de Gmail
    /*
    MailApp.sendEmail({
      to: Session.getActiveUser().getEmail(),
      subject: `[Nuevo Lead Web] ${data.subject || 'Incidencia'} - ${data.name}`,
      body: `Nuevo mensaje de ${data.name} (${data.email}):\n\n${data.message}\n\nWhatsApp: ${data.consentWhatsapp ? 'Sí' : 'No'}`
    });
    */

    return ContentService.createTextOutput(
      JSON.stringify({ status: 'success' })
    ).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(
      JSON.stringify({ status: 'error', error: err.message })
    ).setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}
```

---

### Paso 3: Implementar como Aplicación Web (Web App)
1. En la esquina superior derecha de Apps Script, pulsa en el botón azul **Implementar** (Deploy) → **Nueva implementación**.
2. Haz clic en el icono de engranaje (⚙️) al lado de "Seleccionar tipo" y elige **Aplicación web**.
3. Rellena los datos:
   - **Descripción:** `Webhook Leads Web`
   - **Ejecutar como:** `Yo (tu correo)`
   - **Quién tiene acceso:** `Cualquier usuario` (Anyone) *(Esencial para que Netlify pueda enviar datos sin requerir login de Google)*.
4. Haz clic en **Implementar**.
5. Autoriza los permisos de Google si te lo solicita.
6. **Copia la "URL de la aplicación web"**. Tendrá este formato:
   `https://script.google.com/macros/s/AKfycb.../exec`

---

### Paso 4: Añadir las variables de entorno
Añade las siguientes variables en **Netlify** (*Site configuration → Environment variables*) o en tu `.env` local para pruebas con `netlify dev`:

| Variable | Valor |
|---|---|
| `GOOGLE_SHEET_WEBHOOK_URL` | La URL de la aplicación web copiada en el Paso 3 |
| `GOOGLE_SHEET_SECRET` | La misma clave que pusiste en `WEBHOOK_SECRET` en el script |

¡Listo! A partir de ese momento, cada vez que un usuario envíe el formulario desde tu web:
1. Pasará por el filtro anti-spam y rate-limit de Netlify.
2. Se insertará de inmediato una nueva fila en tu Google Sheet.
3. El usuario verá la pantalla de confirmación `/gracias/`.

---

## Opción 2: Usar Google Forms Nativo (Headless)

Si prefieres vincularlo a un Google Form ya existente en vez de Apps Script:

1. Crea tu formulario en [Google Forms](https://forms.google.com).
2. Haz clic en los tres puntos ⋮ → **Obtener enlace previamente rellenado**.
3. Escribe texto de prueba en cada campo (ej. "NombreTest", "EmailTest") y dale a "Obtener enlace".
4. Copia el enlace en un editor de texto. Verás los parámetros `entry.123456789=NombreTest`.
5. En Netlify, configura:
   - `GOOGLE_FORM_ACTION_URL`: `https://docs.google.com/forms/u/0/d/e/[TU_ID_AQUÍ]/formResponse`
   - `GOOGLE_FORM_ENTRY_NAME`: `entry.123456789`
   - `GOOGLE_FORM_ENTRY_EMAIL`: `entry.987654321`
   - `GOOGLE_FORM_ENTRY_SUBJECT`: `entry.456789123`
   - `GOOGLE_FORM_ENTRY_MESSAGE`: `entry.789123456`
   - `GOOGLE_FORM_ENTRY_WHATSAPP`: `entry.654321987`
