# 🌐 jonathanesteban.dev — Plataforma Corporativa Multi-Página & Serverless

> **Sitio Web Oficial:** [https://jonathanesteban.dev](https://jonathanesteban.dev)  
> **Autor:** Jonathan Esteban Barona — Full-Stack Developer, AI Engineer & Digital Operations Specialist  
> **Hosting:** Netlify (Git-integrated deployment)

---

## 🏗️ Arquitectura del Proyecto

El proyecto está estructurado como una **Plataforma Multi-Página (MPA)** modular con micro-servicios serverless:

```
.
├── site/                                      # Directorio público publicado en Netlify
│   ├── index.html                             # Homepage / Portal principal
│   ├── servicios/                             # Servicios comerciales & Calculadora de Presupuestos
│   ├── proyectos/                             # Portfolio interactivo con filtros por categoría
│   │   ├── demo-app/                          # App interactiva de demostración en vivo
│   │   └── casos/                             # Estudios de caso (portfolio-redesign, landing-negocio, automatizacion-leads)
│   ├── certificaciones/                       # Credenciales, 4Geeks Academy Madrid (71%) & Certificados
│   ├── soporte-it/                            # Operaciones Digitales & Mantenimiento IT
│   ├── sobre-mi/                              # Biografía profesional & propuesta de valor
│   ├── contacto/                              # Formulario de contacto asíncrono
│   ├── faq/                                   # Centro de Ayuda & FAQ interactivo (GEO / SEO)
│   ├── privacy-policy/                        # Política de Privacidad (Cumplimiento RGPD/Meta/TikTok)
│   ├── terms-of-service/                      # Términos y Condiciones del Servicio
│   ├── data-deletion/                         # Callback e instrucciones de eliminación de datos
│   ├── auth/                                  # Callbacks de autorización OAuth (TikTok & Facebook)
│   ├── gracias/                               # Landing de confirmación de conversión
│   ├── assets/
│   │   ├── css/                               # CSS modular (tokens, base, layout, components, pages, legal)
│   │   ├── js/                                # JS ES6 modular (main, nav, theme, faq, filters, form, calculator, tracking, app-demo)
│   │   ├── data/                              # Datasets JSON (projects, certificates, services, faq)
│   │   ├── img/                               # Imágenes WebP optimizadas y OpenGraph (1200x630)
│   │   ├── icons/                             # SVGs vectoriales de tecnologías y servicios
│   │   └── docs/domain-verification/          # Verificación de dominio Meta/TikTok
│   ├── robots.txt                             # Directivas SEO y acceso a bots de IA (GPTBot, PerplexityBot, ClaudeBot)
│   └── sitemap.xml                            # Mapa XML con las 15+ URLs del sitio
├── functions/                                 # Netlify Serverless Functions (backend aislado)
│   ├── contact-submit.js                      # Procesamiento de formulario de contacto & honeypot
│   ├── notify-owner.js                        # Notificaciones instantáneas a Telegram
│   ├── autoresponse.js                        # Emails de confirmación mediante SendGrid
│   ├── tiktok-oauth-callback.js               # Token exchange seguro para TikTok Developer Console
│   ├── facebook-oauth-callback.js             # Token exchange seguro para Meta for Developers
│   ├── data-deletion-request.js               # Endpoint de eliminación de datos firmado por Facebook/TikTok
│   └── webhook-n8n.js                         # Proxy autenticado a workflows n8n
├── .env                                       # Variables de entorno en producción (Gitignored)
├── .env.example                               # Plantilla de variables de entorno para desarrollo
├── .gitignore                                 # Protección de archivos sensibles (.env, node_modules)
├── netlify.toml                               # Configuración de despliegue, publish="site", functions="functions", CSP headers
└── context.md                                 # Especificación técnica maestra del proyecto (v3.0)
```

---

## � Flujo del Formulario de Contacto

El formulario en `/contacto/` sigue este pipeline completo:

```
Usuario envía → frontend (form.js) → /api/contact-submit (Netlify Function)
                                        ├── ✅ Validación (campos, email, longitud, honeypot)
                                        ├── 🚫 Rate limiting (8 solicitudes / 10 min por IP)
                                        ├── 📧 Email al propietario (Resend → SendGrid fallback)
                                        ├── ✉️ Auto-respuesta al usuario
                                        ├── 📱 Telegram notification
                                        └── 🔄 n8n webhook (opcional)
```

### Variables de Entorno Requeridas

| Variable | Obligatorio | Descripción |
|---|---|---|
| `RESEND_API_KEY` | Sí* | API key de Resend.com (proveedor email primario) |
| `SENDGRID_API_KEY` | Sí* | API key de SendGrid (fallback automático) |
| `TELEGRAM_BOT_TOKEN` | No | Token de @BotFather para notificaciones |
| `TELEGRAM_CHAT_ID` | No | Chat ID numérico para recibir notis |
| `N8N_WEBHOOK_LEADS_URL` | No | Webhook n8n para automatización de leads |
| `N8N_WEBHOOK_SECRET` | No | Secreto compartido para webhook |
| `SENDER_EMAIL_NO_REPLY` | No | Email remitente (default: joonathanesteban@gmail.com) |
| `RESEND_DOMAIN` | No | Dominio verificado en Resend (default: onboarding@resend.dev) |

> `*` Al menos un proveedor de email (Resend o SendGrid) debe configurarse para que funcione. Resend es gratuito hasta 100 emails/mes.

Las variables se configuran en el panel de Netlify: **Site Settings → Environment variables**.

---

## 🔒 Seguridad y Gestión de Secretos

- **Cero claves expuestas:** Ningún token de API, client secret u OAuth app secret se encuentra en el frontend.
- **Serverless Functions:** Todas las solicitudes a Telegram, SendGrid/Resend, n8n, Meta API o TikTok API son procesadas exclusivamente en backend mediante Netlify Functions (`functions/`).
- **Protección antispam:** Honeypot field invisible + rate limiting por IP.
- **Variables de Entorno:** Configuradas en el panel de Netlify (`Site Settings → Environment variables`). Copia `.env.example` como referencia.

---

## 🚀 Despliegue en Netlify

El despliegue es automático al enviar cambios a la rama `main` de GitHub. La configuración en `netlify.toml` indica:
- **Publish Directory:** `site`
- **Functions Directory:** `functions`

### Setup inicial

1. Conecta el repo en Netlify: **Add new site → Import from Git**
2. Configura las variables de entorno (ver tabla arriba)
3. Netlify detecta `netlify.toml` automáticamente
4. Primer deploy: `git push` a `main`

---

*Desarrollado para jonathanesteban.dev*