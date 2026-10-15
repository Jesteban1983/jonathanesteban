# BRAND.md — Identidad de Marca Jonathan Esteban
**Fecha:** 2026-10-11
**Propósito:** Manual de marca para jonathanesteban.dev — identidad visual que representa a **Jonathan como persona**, no al servicio actual. El logo es reutilizable aunque el negocio cambie.

---

## 🎯 Filosofía de marca

| Atributo | Descripción |
|----------|-------------|
| **Tono** | Cercano, directo, sin jerga técnica innecesaria |
| **Personalidad** | Resolutivo, honesto, humano — "te explico qué pasó y cómo evitarlo" |
| **Diferenciador** | No eres una empresa anónima con call center. Eres Jonathan, un técnico real que atiende a personas reales |
| **Audiencia** | Pymes, autónomos, mayores, teletrabajadores, comercios locales — personas que necesitan ayuda IT y quieren a alguien de confianza |

---

## 🎨 Paleta de colores

| Variable CSS | Color | Hex | Uso |
|-------------|-------|-----|-----|
| `--color-primary` | Verde azulado oscuro | `#0D3C46` | Fondo de logo, títulos, header, botones principales |
| `--color-primary-light` | Verde azulado medio | `#1A5A6A` | Hovers, variantes de primary |
| `--color-accent` | Ámbar/dorado | `#F2A72A` | Acentos, CTAs, detalles destacados, iconos |
| `--color-accent-light` | Ámbar claro | `#F5C04A` | Hovers de acento, backgrounds sutiles |
| `--color-neutral-900` | Gris profundo | `#0F172A` | Texto principal |
| `--color-neutral-600` | Gris medio | `#475569` | Texto secundario, meta |
| `--color-neutral-100` | Gris claro | `#F1F5F9` | Fondos de fondo, secciones alternas |
| `--color-bg` | Blanco | `#FFFFFF` | Fondo principal |

### Modo oscuro
Los mismos colores se invierten con fondo oscuro y texto claro. El acento teal funciona igual de bien en ambos modos:

| Contexto | Light | Dark |
|----------|-------|------|
| Fondo | `#FFFFFF` | `#0D3C46` |
| Texto principal | `#0D3C46` | `#F1F5F9` |
| Superficie | `#F1F5F9` | `#1A5A6A` |

### Regla de uso
- **Primary (verde azulado):** máx. 60% del diseño (fondo de logo, header, títulos, secciones principales)
- **Accent (ámbar):** máx. 15% del diseño (botones, enlaces, detalles) — para que destaque
- **Neutrales:** texto, fondos secundarios, bordes

---

## 🔤 Tipografía

| Uso | Fuente | Google Fonts | Fallback |
|-----|--------|-------------|----------|
| **Titulares** | **Inter** (pesos: 700, 800) | ✅ Sí | system-ui, sans-serif |
| **Cuerpo** | **Inter** (pesos: 400, 500, 600) | ✅ Sí | system-ui, sans-serif |
| **Monospace** (código) | JetBrains Mono | ✅ Sí | monospace |

**¿Por qué Inter?**
- Legible en pantalla incluso en tamaños pequeños
- Muy neutral — no compite con el contenido, lo sirve
- Funciona igual en español (acentos, ñ) que en inglés
- Compatible con Tailwind (`font-sans` por defecto)

### Tamaños recomendados

| Elemento | Tamaño | Peso |
|----------|--------|------|
| H1 (hero) | `text-5xl` (48px) | 800 |
| H2 (sección) | `text-3xl` (30px) | 700 |
| H3 (card) | `text-xl` (20px) | 600 |
| Cuerpo | `text-base` (16px) | 400 |
| Meta / pequeño | `text-sm` (14px) | 400 |
| CTA / botón | `text-base` (16px) | 600 |

---

## 🎨 Logos definitivos (diseñados por Jonathan)

### Logo Icono — `logo-icono.svg` / `logo-icono.png`
Monograma "JE" con fondo verde azulado oscuro (`#0D3C46`), letras blancas y detalle ámbar (`#F2A72A`). Un círculo ámbar al final de la E aporta el toque distintivo.

**Usos:** Favicon, avatar redes sociales, marca de agua, cabeceras de documento.

### Logo Horizontal — `logo-horizontal.svg` / `logo-horizontal.png`
Monograma + nombre "Jonathan Esteban" en una línea horizontal.

**Usos:** Header del sitio web, tarjetas de visita, firma de email.

### Logo Horizontal con Descriptor — `logo-horizontal-descriptor.svg`
Monograma + nombre + "soporte informático en Barcelona".

**Usos:** Hero de la home, secciones principales del sitio, perfiles profesionales.

### Logo Horizontal Blanco — `logo-horizontal-blanco.svg`
Versión invertida: monograma blanco sobre fondo oscuro, texto en blanco.

**Usos:** Fondos oscuros, footer, modo oscuro del sitio.

---

## 📐 Reglas de uso del logo

### Espacio de seguridad
- Mínimo: el ancho de la "J" en todas direcciones alrededor del logo
- Nunca colocar texto, imágenes u otros elementos dentro del espacio de seguridad

### Tamaño mínimo
- Versión completa (con tagline): 200px de ancho
- Solo wordmark: 120px de ancho
- Monograma: 32px de ancho (favicon)

### Versiones
- **Versión completa:** Logo + tagline (para header y hero)
- **Versión simplificada:** Solo wordmark (para footer, mobile)
- **Monograma:** Solo iniciales (para favicon, avatar)
- **Un color (oscuro):** Para fondos claros (`currentColor` con `color=#1E3A5F`)
- **Un color (claro):** Para fondos oscuros (`currentColor` con `color=#FFFFFF`)

### Qué NO hacer con el logo
- No estirar, comprimir ni rotar
- No cambiar los colores del logo
- No añadir sombras, gradientes ni efectos
- No usar sobre fondos que no contrasten
- No separar el monograma en "J" y "E" por separado

---

## 🗣️ Tono de voz

| Principio | Qué significa | Ejemplo (bien) | Ejemplo (mal) |
|-----------|---------------|----------------|---------------|
| **Cercano** | Hablas como persona, no como empresa | "Te ayudo a poner tu PC a punto" | "Ofrecemos soluciones integrales de IT" |
| **Directo** | Vas al grano, sin rodeos | "Se te ha roto el portátil? Te lo miro" | "¿Está experimentando una disrupción en sus dispositivos?" |
| **Sin jerga** | Explicas en cristiano | "TCP/IP es el idioma que usan los ordenadores para hablar entre ellos en la red" | "Protocolo de capa 3 del modelo OSI" |
| **Honesto** | Dices lo que sabes y lo que no | "Esto no lo he visto antes, pero lo investigo" | "Por supuesto, soy experto en todo" |

### Reglas de copywriting
- **Tratar de "tú"** siempre (nunca "usted", nunca "vos")
- **Frases cortas.** Una idea por frase.
- **No prometer lo que no está en el CV.** Si no tienes 15 años de experiencia, no lo pongas.
- **Garantía de 15 días** mencionada siempre que se hable de precio.
- **Zona de cobertura:** "Barcelona y área metropolitana sur (presencial) / toda España (remoto)"

---

## 📁 Archivos de marca

| Archivo | Descripción |
|---------|-------------|
| `brand/logo-icono.svg` | Monograma "JE" (favicon, avatar) |
| `brand/logo-icono.png` | Exportación PNG del monograma |
| `brand/logo-horizontal.svg` | Logo horizontal (monograma + nombre) |
| `brand/logo-horizontal.png` | Exportación PNG del horizontal |
| `brand/logo-horizontal-descriptor.svg` | Logo horizontal + "soporte informático en Barcelona" |
| `brand/logo-horizontal-blanco.svg` | Versión invertida para fondos oscuros |
| `BRAND.md` | Este documento — manual de marca completo |

---

**Autorrevisión:** ✅ 3 conceptos de logo definidos, paleta con 5 colores + variantes oscuras, 2 tipografías Google Fonts con justificación, reglas de uso detalladas, espacio de seguridad, versiones, tono de voz coherente con el perfil real del CV.

**ESPERANDO APROBACIÓN FASE 2 — ¿Qué concepto de logo eliges? (1: Monograma, 2: Wordmark, 3: Icono)**