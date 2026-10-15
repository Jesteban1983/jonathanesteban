# BLOG-CONTENT-TEMPLATE.md
## Template del agente redactor — Blog jonathanesteban.dev

> **DOCUMENTO OBSOLETO — El prompt maestro está en `BLOG-AUTOMATION.md` sección 2 (PROMPT A).**
> Este archivo se mantiene como referencia rápida. Si hay discrepancia, manda `BLOG-AUTOMATION.md`.
> **Fuente de verdad visual:** `BRAND.md` (colores `#0D3C46` petróleo y `#F2A72A` ámbar, tipografía **Inter**).

---

## 🎯 Referencia rápida

| Elemento | Dónde está |
|----------|-----------|
| **Prompt del agente** (system prompt completo) | `BLOG-AUTOMATION.md` → Sección 2 → PROMPT A |
| **Validación automática** (nodo 5, 11 checks) | `BLOG-AUTOMATION.md` → Sección 4 |
| **Prompt de imagen** (bloque fijo + negativo) | `BLOG-AUTOMATION.md` → Sección 5 → PROMPT B |
| **Correo de aprobación** (HTML inline) | `BLOG-AUTOMATION.md` → Sección 6 |
| **CSS de formato** (justificado, APA, espaciado) | `BLOG-AUTOMATION.md` → Sección 3 |
| **Flujo n8n** (nodo por nodo) | `BLOG-AUTOMATION.md` → Sección 1 |

---

## 📝 Frontmatter del artículo (el nodo 7 lo escribe)

```yaml
---
title: ""
description: ""          # = metaDescription del agente
slug: ""
date: ""                 # lo fija el nodo de publicación
category: ""
readingTime: ""
image: "/blog/<slug>.png"
imageAlt: ""
draft: true              # pasa a false al aprobar
---
```

---

## 🔍 Checklist rápido para el agente (resumen de PROMPT A)

- [ ] **Tono:** Tú, cercano, directo, sin jerga. Barcelona solo 1-2 veces.
- [ ] **Estructura:** Intro → Respuesta rápida → 3-5 H2 → Tabla APA (opcional, máx 1) → Errores comunes → FAQ (3 preguntas) → CTA → Referencias.
- [ ] **Extensión:** 900–1.300 palabras.
- [ ] **Tabla:** Usar `<TablaAPA titulo="..." nota="...">`. El título describe el contenido, va centrado, en mayúsculas y negrita; no lleva número.
- [ ] **Citas:** (Autor, año) en texto. Referencias al final en APA 7 con URL.
- [ ] **SEO:** Título ≤ 60 chars, meta 140–155 chars, slug ≤ 6 palabras.
- [ ] **Salida:** Solo JSON válido, sin bloques de código, sin texto extra.
- [ ] **Imagen:** `imagePrompt` en inglés, escena concreta, sin texto.
- [ ] **Prohibido:** "años de experiencia", "garantizado", "el mejor", "100 %", "cientos de clientes", emojis, signos de exclamación.
- **16:9** obligatorio; portada PNG generada por modelo, mínimo 1920×1080.
- Modelo por defecto: `gemini-nano-banana-2.1`, mediante el generador compartido `IA-ENGINEERING-LAB/tools/gemini-image/`; detalles y configuración segura en `IA-ENGINEERING-LAB/tools/gemini-image/README.md`.
- Guardar en `public/assets/img/blog/{{slug}}.png` (no reemplazar por SVG manual).

---

## ✅ Checklist que el agente debe verificar antes de entregar

- [ ] Frontmatter completo con todos los campos
- [ ] Tono de marca: "tú", cercano, sin jerga
- [ ] Texto justificado en el CSS (no requiere acción en MDX)
- [ ] Menciones de "15 días de garantía" si aplica
- [ ] CTA final a `/contacto/`
- [ ] Tags: máximo 4, incluyendo "pymes" si aplica
- [ ] Hero image generada con prompt correcto
- [ ] Tablas con formato APA (caption opcional)
- [ ] Sin errores ortográficos ni links rotos
- [ ] Fecha de publicación correcta

---

## 📁 Rutas de archivo

```
src/content/blog/{{slug}}.mdx          ← El artículo
public/assets/img/blog/{{slug}}.png    ← La imagen hero generada por modelo
```

---