# Flujo editorial n8n — Blog Automatizado

Este documento describe cómo se integra el pipeline de generación de artículos con n8n para automatizar el ciclo editorial completo.

## Arquitectura

```
n8n (Schedule Trigger)
  │
  ├─ [1] HTTP Request → webhook generación
  │     └─ Ejecuta: scripts/blog-workflow.sh generate
  │
  ├─ [★2] Correo de aprobación (opcional)
  │     └─ Envia draft a revisión editorial
  │
  ├─ [3] HTTP Request → webhook publicación
  │     └─ Ejecuta: scripts/blog-workflow.sh publish-all
  │
  └─ [4] HTTP Request → webhook build
        └─ Ejecuta: cd astro-portfolio && npm run build
```

## Requisitos previos

1. n8n corriendo (puerto 5678) — verificar con:
   ```bash
   curl -s http://localhost:5678/healthz  # debe responder
   ```

2. Webhook URL pública configurada (`WEBHOOK_URL` en docker-compose.yml).
   El workflow se apoya en nodos **Webhook** para recibir llamadas externas.

3. Scripts ejecutables:
   - `~/IA-ENGINEERING-LAB/08-proyectos/it-support-portfolio/astro-portfolio/scripts/blog-workflow.sh`
   - `~/IA-ENGINEERING-LAB/08-proyectos/it-support-portfolio/astro-portfolio/scripts/generate-blog-post.py`
   - `~/IA-ENGINEERING-LAB/08-proyectos/it-support-portfolio/astro-portfolio/scripts/blog-publish.sh`

## Workflow recomendado (3 nodos Webhook)

### ⚙️ 1. Disparador (Schedule Trigger)

| Parámetro | Valor |
|---|---|
| Trigger Times | `Cron: 0 9 * * 1,3,5` (Lun, Mie, Vie a las 9:00) |
| Timezone | `Europe/Madrid` |

Este trigger llama al webhook de generación.

### ⚙️ 2. Generar artículo (Execute Command)

Este nodo ejecuta el script que toma el siguiente tema pendiente y genera el artículo.

```
Comando: /bin/bash
Parámetros: -c "/home/taisu/IA-ENGINEERING-LAB/08-proyectos/it-support-portfolio/astro-portfolio/scripts/blog-workflow.sh generate --image"
```

- ⚡ Si el tópico bank se queda vacío, el script devuelve `{"error":"No hay temas pendientes"}`.
- Se puede añadir una condición para detener el flujo si hay error.

### ⚙️ 3. Enviar correo de aprobación (Email)

Una vez generado el draft, se envía un correo a Jonathan con template de aprobación.

**Asunto:** `✏️ Revisión: [título del artículo]`

**Cuerpo (HTML):**
```html
<p>Se ha generado un nuevo borrador:</p>
<ul>
  <li><strong>Título:</strong> {{ $json.title }}</li>
  <li><strong>Slug:</strong> {{ $json.slug }}</li>
  <li><strong>Palabras:</strong> {{ $json.wordCount }}</li>
</ul>
<p><a href="https://it-support.jonathanesteban.dev/blog/{{ $json.slug }}">Ver borrador</a></p>
<hr>
<h3>¿Aprobado?</h3>
<p>Responde a este correo o accede al webhook de publicación para confirmar.</p>
```

### ⚙️ 4. Webhook de publicación (Webhook)

Endpoint que recibe una llamada POST con JSON `{"action":"publish"}`.

```
Comando: /bin/bash
Parámetros: -c "/home/taisu/IA-ENGINEERING-LAB/08-proyectos/it-support-portfolio/astro-portfolio/scripts/blog-publish.sh"
```

- Publica todos los drafts pendientes, hace build, git commit y push.

### ⚙️ 5. Notificación (Telegram opcional)

Enviar mensaje a Telegram con el resultado de la publicación.

## Llamadas manuales (desde terminal)

```bash
# Ver siguiente tema
bash scripts/blog-workflow.sh next-topic

# Generar draft + imagen
bash scripts/blog-workflow.sh generate --image

# Listar drafts
bash scripts/blog-workflow.sh list-drafts

# Publicar todos los drafts
bash scripts/blog-publish.sh

# Publicar uno específico
bash scripts/blog-publish.sh <slug>

# Publicar desde n8n (vía blog-workflow.sh)
bash scripts/blog-workflow.sh publish-all
```

## Variables de entorno necesarias en n8n

Cuando los nodos Execute Command se ejecutan desde n8n, el entorno puede no heredar las variables de `~/.nova.env`. Soluciones:

1. **(Recomendada)** Añadir en el comando:
   ```bash
   set -a; . /home/taisu/.nova.env; set +a; bash scripts/blog-workflow.sh generate
   ```

2. **Configurar en docker-compose.yml** de n8n (volumen adicional):
   ```yaml
   volumes:
     - /home/taisu/.nova.env:/etc/nova.env:ro
   ```
   Y en el Entrypoint, hacer source de ese archivo.

## Topic Bank

El archivo `blog-topic-bank.csv` contiene la cola de temas. El script `next-topic` lee la primera línea en estado `pendiente` y la devuelve como JSON. Una vez publicado, `blog-publish.sh` marca automáticamente el tema como `publicado`.

**Formato:**
```csv
tema,keyword,keyword_intencion,intencion,estado
```
- `tema`: Título/tema del artículo
- `keyword`: Palabra clave principal
- `keyword_intencion`: Palabra clave long-tail
- `intencion`: informativa / guía práctica / comparativa / lista
- `estado`: pendiente / publicado / revisar