# BLOG-AUTOMATION.md

## Contenido del blog automatizado con n8n — jonathanesteban.dev

> **Para qué sirve:** es el documento que se le entrega al agente en la Fase 4 del plan. Contiene, listos para pegar: el prompt del agente redactor, el prompt de imagen, las reglas de formato (justificado, APA), el flujo de n8n nodo por nodo y la plantilla del correo de aprobación.
> **Fuente de verdad visual:** `BRAND.md` (colores `#0D3C46` petróleo y `#F2A72A` ámbar, tipografía **Inter**). Si algo de aquí contradice a `BRAND.md`, manda `BRAND.md`.
> **Regla de oro:** nada se publica sin que Jonathan pulse "Aprobar" en su correo.

---

## 1. Flujo de n8n (nodo por nodo)

```
[1 Schedule: días 1 y 15, 09:00 Europe/Madrid]
        ↓
[2 Tema: lee la siguiente fila "pendiente" del banco de temas]
        ↓
[3 Anti-duplicados: lista los .mdx existentes (GitHub) y compara slug/título]
        ↓
[4 AGENTE REDACTOR  ←→ herramientas: buscar_web, leer_url]      (Prompt A)
        ↓
[5 VALIDACIÓN (Code): esquema, formato, APA, frases prohibidas]
        ├─ falla → vuelve al nodo 4 con la lista de errores (máx. 2 reintentos)
        ↓
[6 IMAGEN: modelo de imagen con el prompt del agente + bloque de estilo] (Prompt B)
        ├─ resolución < 1600×900 o falla → reintento (máx. 2)
        ↓
[7 BORRADOR: commit a /content/blog/drafts/<slug>.mdx + imagen]
        ↓
[8 CORREO: Markdown→HTML + "Aprobar / Cancelar" con espera de respuesta]   (sección 6)
        ├─ Aprobar → [9 PUBLICAR]: mueve a /content/blog/<slug>.mdx (draft:false, fecha),
        │             dispara el build de Netlify, marca el tema "publicado",
        │             envía correo "Publicado: <URL>"
        └─ Cancelar / sin respuesta en 48 h → el borrador queda en /drafts/,
                      tema "revisar", correo "No publicado"
[Error Trigger] → correo a Jonathan con el nodo que falló
```

**Notas de implementación**

- **Banco de temas:** Google Sheets o Data Table de n8n, columnas: `tema`, `keyword`, `intencion` (informativa / guía / comparativa), `estado` (pendiente / publicado / revisar), `fecha`.
- **Modelo del agente:** el orquestador (DeepSeek V4 Flash). Es redacción, no la capa de seguridad, así que no requiere la restricción de la Fase 5.
- **Aprobación:** usa la operación **"Send and Wait for Response"** del nodo de Gmail con tipo "Approve or Disapprove" y *Limit Wait Time* = 48 h (comprueba que tu versión de n8n la incluye). Genera enlaces de un solo uso y no hay que construir tokens propios. Si no estuviera disponible: nodo Wait en modo webhook + token aleatorio de un solo uso con caducidad.
- **Credenciales:** solo en el almacén de credenciales de n8n. Ninguna clave en prompts, repositorio ni correos.
- **Camino manual (Cognito Forms):** el formulario entra por webhook, salta los nodos 2–5, pasa por 6 (opcional, si no sube imagen) y 7, y termina con un correo con botón "Cancelar publicación" válido 10 minutos antes del build.

---

## 2. PROMPT A — Agente redactor (system prompt)

```
# ROL
Eres el redactor técnico del blog de Jonathan Esteban, técnico de soporte
informático en Barcelona. Escribes artículos útiles, verificados y claros para
personas y pequeños negocios que no son técnicos.

# CONTEXTO (variables de n8n)
- Tema: {{ $json.tema }}
- Palabra clave principal: {{ $json.keyword }}
- Intención de búsqueda: {{ $json.intencion }}
- Año actual: {{ $now.year }}
- Artículos ya publicados (evita repetir enfoque): {{ $json.existentes }}

# REGLAS DE HONESTIDAD (inquebrantables)
1. Cada dato, cifra, versión de software o norma debe salir de una fuente que HAYAS
   consultado con las herramientas. Si no puedes verificarlo, no lo escribas.
2. Prohibido inventar estadísticas, precios, estudios, citas o URLs.
3. Prohibido hablar de la experiencia de Jonathan con cifras ("X años de experiencia",
   "cientos de clientes") ni atribuirle certificaciones. Nada de "garantizado al 100 %",
   "el mejor", "siempre", "nunca" sin sustento.
4. Si mencionas software o hardware, comprueba cuál es la versión vigente en {{ $now.year }}
   antes de afirmarlo. No des por "nuevo" lo que ya no lo es.
5. No des instrucciones que puedan dañar equipos, vulnerar cuentas ajenas o saltarse
   licencias. En seguridad, solo defensa y buenas prácticas.
6. Si el tema exige un profesional (salud, asesoría legal, reparación eléctrica), dilo.

# TONO
Español de España, tuteo, cercano y directo. Explica cualquier término técnico la primera
vez que aparece. Frases cortas. Sin relleno, sin exageraciones, sin tecnicismos
innecesarios. Menciona Barcelona solo 1 o 2 veces y solo cuando aporte (p. ej. el CTA).

# ESTRUCTURA DEL ARTÍCULO (en este orden; el título H1 lo pinta la plantilla, NO lo incluyas)
1. Introducción (80–120 palabras): el problema que el lector reconoce + qué va a lograr.
2. "Respuesta rápida" (2–3 frases): la respuesta directa, para quien solo quiere eso.
3. Desarrollo: entre 3 y 5 secciones H2 (con H3 solo si hace falta).
   - Cada H2 empieza con una frase que responde la pregunta de esa sección.
   - Procedimientos: lista numerada, un paso = una acción.
   - Enumeraciones: lista con viñetas, mínimo 3 elementos, redacción paralela.
4. Tabla APA: solo si una comparación o un dato ordenado aporta de verdad. Máximo 1.
5. "Errores comunes" o "Cuándo conviene llamar a un técnico" (honesto, sin presionar).
6. "Preguntas frecuentes": 3 preguntas reales con respuesta de 2–4 frases. Cada pregunta va en su propio párrafo, en negrita; la respuesta empieza debajo, en un párrafo independiente (nunca en la misma línea o párrafo).
7. Conclusión + CTA (2–3 frases). Invita a contactar. Si hablas de un servicio, puedes
   mencionar la garantía de 15 días desde la entrega; no prometas nada más.
8. "Referencias" en APA 7 (ver reglas).
Extensión del cuerpo: 900–1.300 palabras.

# FORMATO DEL TEXTO
- Markdown/MDX. Párrafos de 2 a 5 frases; una idea por párrafo.
- Sin negritas decorativas: negrita solo para el término clave de cada sección (máx. 1 por párrafo).
- Sin emojis, sin MAYÚSCULAS enfáticas, sin signos de exclamación.
- Los puntos de una lista terminan igual (todos con punto o ninguno).
- Números: coma decimal (3,5); separador de miles con punto desde 10.000.

# TABLAS (formato APA 7, adaptado a web)
Usa SIEMPRE este componente, con una línea en blanco antes y después de la tabla interna:

<TablaAPA numero="1" titulo="Comparación de [lo comparado] en [contexto]" nota="Elaboración propia a partir de Autor (año).">

| Criterio | Opción A | Opción B |
|---|---|---|
| Dato | valor | valor |

</TablaAPA>

- Título en minúscula salvo la primera palabra y nombres propios, sin punto final.
- Encabezados de columna cortos. Sin celdas vacías (usa "—" si no aplica).
- Numeración correlativa. Cita la tabla en el texto ("como muestra la Tabla 1").
- La nota siempre empieza por la fuente de los datos. Sin colores ni iconos en celdas.

# CITAS Y REFERENCIAS (APA 7)
- En el texto: (Autor, año) o Autor (año). Para organizaciones: (Microsoft, 2025).
- Sección final "Referencias": una por línea, orden alfabético, con URL activa.
  Formato: Autor. (Año, día mes). *Título en cursiva*. Sitio. URL
- Mínimo 2 referencias, preferiblemente fuentes oficiales (fabricante, documentación,
  organismos públicos). Solo las que hayas leído de verdad.

# SEO Y RESPUESTA DIRECTA
- Keyword principal: en el slug, en el título, en el primer párrafo y en un H2 (natural).
- Título ≤ 60 caracteres. Meta descripción 140–155 caracteres, con beneficio concreto.
- Slug: minúsculas, sin tildes, guiones, ≤ 6 palabras.
- Redacta las FAQ de forma que cada respuesta se entienda sola, sin el resto del texto.

# SALIDA
Devuelve SOLO este JSON válido (sin texto antes ni después, sin bloques de código):
{
  "slug": "",
  "title": "",
  "metaDescription": "",
  "keywordPrincipal": "",
  "keywordsSecundarias": [],
  "categoria": "",
  "tiempoLectura": "",
  "resumenCorreo": "2-3 frases para el correo de aprobación",
  "markdown": "cuerpo completo (sin frontmatter y sin H1)",
  "referencias": [{ "apa": "", "url": "" }],
  "imagePrompt": "escena concreta en inglés (ver reglas de imagen), sin texto en la imagen",
  "imageAlt": "descripción accesible de la imagen, 100-125 caracteres, en español",
  "autoverificacion": {
    "datosVerificados": true,
    "fuentesConsultadas": 0,
    "palabras": 0,
    "tablaIncluida": false
  }
}
```

---

## 3. Reglas de formato visual (el agente de la Fase 4 las implementa en la web)

Todo el contenido vive dentro de `<article class="blog-post">`. **Hereda la fuente (Inter, según `BRAND.md`) y el tamaño base del resto de la página**: no se declara ni otra fuente ni otro tamaño para el cuerpo.

**Requisito:** el `<html>` debe llevar `lang="es"`; sin eso `hyphens: auto` no corta bien las palabras y el justificado deja huecos.

```
/* blog.css */
.blog-post { font-family: inherit; font-size: inherit; line-height: 1.75; color: inherit; }

/* Texto justificado: párrafos y elementos de lista */
.blog-post :where(p, li) {
  text-align: justify;
  text-justify: inter-word;
  hyphens: auto;
  -webkit-hyphens: auto;
  overflow-wrap: break-word;
}

/* Espaciado entre párrafos y puntos */
.blog-post p            { margin: 0 0 1.25em; }
.blog-post :where(ul, ol) { margin: 0 0 1.5em; padding-left: 1.5em; }
.blog-post li           { margin: 0 0 .6em; }
.blog-post li > :where(ul, ol) { margin: .6em 0 0; }

/* Títulos: misma familia, alineados a la izquierda (no se justifican) */
.blog-post h2 { margin: 2.25em 0 .75em; text-align: left; }
.blog-post h3 { margin: 1.75em 0 .6em;  text-align: left; }

/* Tabla APA 7: sin líneas verticales; solo 3 líneas horizontales */
.apa-table { margin: 2em 0; overflow-x: auto; }
.apa-table .apa-num   { margin: 0; font-weight: 700; text-align: left; }
.apa-table .apa-title { margin: 0 0 .6em; font-style: italic; text-align: left; }
.apa-table table {
  width: 100%; border-collapse: collapse; font-size: inherit;
  border-top: 1px solid currentColor; border-bottom: 1px solid currentColor;
  font-variant-numeric: tabular-nums;
}
.apa-table th, .apa-table td { border: 0; padding: .45em .8em; text-align: left; hyphens: none; }
.apa-table thead th { font-weight: 400; text-align: center; border-bottom: 1px solid currentColor; }
.apa-table thead th:first-child { text-align: left; }
.apa-table td.num { text-align: center; }
.apa-table .apa-note { margin: .6em 0 0; text-align: left; }
```

Componente (adapta al stack decidido en la Fase 1; ejemplo en React/MDX):

```
export function TablaAPA({ numero, titulo, nota, children }) {
  return (
    <figure className="apa-table">
      <p className="apa-num">Tabla {numero}</p>
      <p className="apa-title">{titulo}</p>
      {children}
      {nota && <p className="apa-note"><em>Nota.</em> {nota}</p>}
    </figure>
  );
}
```

**Frontmatter que escribe el nodo 7** (a partir del JSON del agente):

```
---
title: ""
description: ""          # = metaDescription
slug: ""
date: ""                 # lo fija el nodo de publicación
category: ""
readingTime: ""
image: "/blog/<slug>.png"
imageAlt: ""
draft: true              # pasa a false al aprobar
---
```

> **Nota sobre APA:** APA 7 está pensado para trabajos académicos (doble espacio, Times New Roman). Aquí se aplica lo que es transferible a web: numeración y título de tablas, ausencia de líneas verticales, nota con fuente, citas en texto y referencias. La tipografía y el espaciado siguen la marca.

---

## 4. Validación automática (nodo 5, Code)

Rechaza el borrador y devuelve la lista de errores al agente si falla cualquiera de estas comprobaciones:

| # | Comprobación |
|---|--------------|
| 1 | JSON válido con todos los campos del esquema |
| 2 | `title` ≤ 60 caracteres y `metaDescription` entre 140 y 155 |
| 3 | `markdown` sin H1 (`# `) y sin frontmatter |
| 4 | Entre 900 y 1.300 palabras |
| 5 | Entre 3 y 5 encabezados H2, y existen las secciones "Preguntas frecuentes" y "Referencias" |
| 6 | Si hay tabla: usa `<TablaAPA>` con `numero`, `titulo` y `nota`, y la tabla está citada en el texto |
| 7 | Al menos 2 referencias y todas las `url` responden con HTTP 200 |
| 8 | Ninguna frase prohibida: "años de experiencia", "garantizado", "el mejor", "100 %", "cientos de clientes" |
| 9 | Sin emojis ni signos de exclamación |
| 10 | `slug` no existe ya en el repositorio |
| 11 | `imagePrompt` en inglés y sin pedir texto dentro de la imagen |

---

## 5. PROMPT B — Imagen de portada

**Requisitos de calidad:** 16:9, salida 2K preferida y mínimo 1600×900. Debe parecer una imagen editorial del año en curso (`$now.year`), no de stock genérico. El nodo 6 rechaza imágenes menores de 1600×900.

**Modelo recomendado:** `gemini-nano-banana-2.1` (Nano Banana 2.1) por Gemini API. La documentación vigente lo recomienda para proyectos nuevos; genera 16:9 hasta 4K y equilibra calidad con coste/latencia. `gemini-3-pro-image` queda como alternativa premium para casos especiales de máxima consistencia visual. Configura `IMAGE_MODEL` en n8n para poder cambiar de modelo sin editar el flujo. No instalar un modelo local en el VPS actual: no hay driver NVIDIA operativo y la GTX 850M no es adecuada para inferencia moderna de imágenes.

**Instalación segura:** habilitar Gemini API y crear una clave en Google AI Studio. Para ejecutar el script local, guardarla en `astro-portfolio/.env` como `GEMINI_API_KEY=...` (el `.env` está ignorado por Git). En n8n usar su almacén de credenciales/secretos, no reutilizar ni exponer el `.env` local. No incluir la clave en prompts, query strings, logs o correos. Configurar un límite de gasto/cuota en el proveedor y comprobar la tarifa vigente antes de producción. La llamada de prueba y la generación están bloqueadas hasta añadir esa credencial.

**Generador común del laboratorio:** la herramienta principal está en `IA-ENGINEERING-LAB/tools/gemini-image/generate_image.py`; su clave compartida vive en `IA-ENGINEERING-LAB/.env` (ver `.env.example`). El wrapper `astro-portfolio/scripts/generate_blog_image.py` agrega estilo del blog y delega la generación a la herramienta común. Dependencias instaladas una sola vez desde `tools/gemini-image/requirements.txt`. El wrapper guarda en `public/assets/img/blog/<slug>.png` y exige PNG mínimo de 1600×900.

La configuración global (modelo, tamaño y formato por defecto) está documentada en `tools/gemini-image/README.md`; no duplicar credenciales por proyecto. No compartir ni subir el `.env` global.

Ejemplo de ejecución desde la raíz del laboratorio:

```sh
python3 -m venv .venv-image
. .venv-image/bin/activate
pip install -r tools/gemini-image/requirements.txt
python 08-proyectos/it-support-portfolio/astro-portfolio/scripts/generate_blog_image.py --slug ordenador-lento --scene "A modern slim laptop with a visible SSD upgrade kit and a contemporary Wi-Fi 7 router on a tidy Mediterranean home-office desk; show the practical computer-performance troubleshooting theme through the hardware, with soft daylight and no people."
```

Para n8n, el nodo de generación debe usar una credencial protegida y solicitar los mismos parámetros (`16:9`, `2K`, formato PNG). Guardar primero como borrador, validar el binario (PNG y al menos 1600×900) y solo asociarlo/publicarlo después de la aprobación humana. Evitar exponer la clave directamente en nodos Code o expresiones. Si el nodo HTTP estándar no puede guardar la respuesta de imagen binaria de Interactions, usar un servicio auxiliar autenticado o un nodo Gemini mantenido; probar la versión de n8n antes de implementar, pues la API de imagen no se confirma configurada en el compose actual.

El prompt final que se envía al modelo es: **escena del agente + bloque de estilo fijo**.

```
[ESCENA — la escribe el agente en "imagePrompt", en inglés]
Ejemplo: A slim modern laptop and a Wi-Fi 7 router on a clean desk beside a window,
soft morning light, a technician's hands out of focus in the background.

[BLOQUE DE ESTILO FIJO — se concatena siempre]
Premium editorial photograph, 16:9, shot on a full-frame camera, 35mm lens, shallow
depth of field, natural soft light. Contemporary {{ $now.year }} technology: current-generation
slim laptops, AI-era workstation, Wi-Fi 7 equipment, NVMe drives, modern smartphone,
clean cable management. Calm Mediterranean workspace. Color grading dominated by deep
petrol teal (#0D3C46) shadows with one small warm amber (#F2A72A) accent light that echoes
the brand. High detail, sharp focus on the subject, realistic materials, uncluttered
composition with generous negative space on the left third for the title overlay.

[NEGATIVOS — se concatenan siempre]
No text, no letters, no numbers, no logos, no watermarks, no brand names, no recognizable
faces, no people looking at the camera, no cartoon look, no clip-art, no binary-code rain,
no hooded hacker, no glowing padlock hologram, no CRT monitors, no floppy disks, no outdated
hardware, no low-resolution look, no oversaturation, no plastic skin.
```

**Reglas:**

- Sin personas reconocibles, para no mostrar "clientes" o "trabajos" que no existen.
- Cada imagen debe ilustrar el tema concreto (un router, un disco, un portátil), no una metáfora vaga.
- Una sola portada por artículo. Si el artículo incluye figuras internas, se numeran "Figura 1" en APA (número en negrita, título en cursiva arriba y *Nota.* abajo).
- El nodo 7 guarda la imagen en `/public/blog/<slug>.png` y el texto alternativo viene de `imageAlt`.

---

## 6. Correo de aprobación (nodo 8)

**Asunto:** `Aprobar borrador: {{title}}`

**Cuerpo (HTML con estilos en línea; el nodo Markdown convierte el artículo completo):**

```
<div style="max-width:640px;margin:0 auto;font-family:Inter,Arial,sans-serif;color:#0D3C46;line-height:1.7">
  <p style="margin:0 0 4px;font-size:13px">Borrador para aprobar · {{tiempoLectura}} · {{palabras}} palabras</p>
  <h1 style="margin:0 0 16px;font-size:24px">{{title}}</h1>
  <img src="{{imageUrl}}" alt="{{imageAlt}}" style="width:100%;border-radius:12px;margin:0 0 16px">
  <p style="margin:0 0 8px"><strong>Resumen:</strong> {{resumenCorreo}}</p>
  <p style="margin:0 0 20px;font-size:14px">
    Meta descripción: {{metaDescription}}<br>
    Fuentes consultadas: {{fuentesConsultadas}} · Validación automática: superada
  </p>

  <!-- BOTONES: los genera "Send and Wait for Response" (Aprobar / Cancelar). Caduca en 48 h. -->

  <hr style="border:0;border-top:1px solid #D9E2E4;margin:24px 0">
  <div style="text-align:justify;font-size:16px">{{ articuloHTML }}</div>
  <hr style="border:0;border-top:1px solid #D9E2E4;margin:24px 0">
  <p style="font-size:13px">Si no respondes en 48 horas, el borrador NO se publica y queda guardado en /drafts/.</p>
</div>
```

**Qué revisar antes de pulsar "Aprobar"** (checklist de Jonathan):

- [ ] Los datos y versiones son correctos y las referencias existen.
- [ ] No hay promesas ni cifras de experiencia que no estén en tu CV.
- [ ] La tabla (si la hay) está bien: sin líneas verticales, con número, título y nota.
- [ ] La imagen es nítida, actual y no tiene texto raro.
- [ ] El tono suena a ti: cercano, claro, sin exageraciones.

---

## 7. Criterios de aceptación de esta fase

1. Un borrador automático completa el ciclo: tema → texto → imagen → correo → aprobación → publicado, una vez de extremo a extremo.
2. Un borrador cancelado queda en `/drafts/` y **no** aparece en la web.
3. Si no se responde en 48 h, no se publica nada.
4. En la web publicada: texto justificado, misma fuente y tamaño que el resto del sitio, espaciado correcto entre párrafos y viñetas, tabla APA sin líneas verticales.
5. La validación del nodo 5 rechaza de verdad un borrador defectuoso (prueba con uno a propósito).
6. Ningún secreto aparece en el repositorio, en el correo ni en los logs de n8n.