# Jonathan Esteban — Portfolio Personal

> Full Stack Developer & Gestor de Operaciones Digitales · Barcelona, España

Portfolio profesional de una sola página construido con HTML5, CSS3 y JavaScript vanilla. Sin frameworks, sin dependencias de build — desplegable en cualquier servidor estático con un solo archivo.

---

## Vista previa

```
https://jonathanesteban.github.io/portfolio
```

---

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Estructura | HTML5 semántico |
| Estilos | CSS3 con Custom Properties (variables) |
| Lógica | JavaScript ES2022 vanilla |
| Iconos | Lucide Icons v0.x (CDN) |
| Tipografía | Google Fonts — Instrument Serif + Inter |
| Formulario | Formspree (endpoint externo) |
| Despliegue | GitHub Pages |

---

## Estructura del proyecto

```
portfolio/
├── index.html              ← Archivo principal (todo inline)
├── assets/
│   └── foto-jonathan.jpg   ← Foto de perfil (280×280px mínimo)
└── README.md
```

Todo el CSS y el JavaScript están embebidos dentro de `index.html`. No hay paso de compilación.

---

## Configuración antes de publicar

### 1. Foto de perfil

Coloca tu foto en `./assets/foto-jonathan.jpg`. Requisitos:

- Formato: JPG o WebP
- Tamaño mínimo: 280 × 280 px
- Relación de aspecto: 1:1 (cuadrada)
- Peso recomendado: menos de 150 KB

Si la imagen no existe o falla al cargar, el sitio muestra automáticamente las iniciales **JE** como fallback.

### 2. Formspree — formulario de contacto

El formulario envía mensajes vía [Formspree](https://formspree.io). Para activarlo:

1. Crea una cuenta gratuita en formspree.io
2. Crea un nuevo formulario y copia tu ID (formato: `xabc1234`)
3. Reemplaza `XXXXXXXX` en dos lugares del archivo `index.html`:

```html
<!-- Línea ~700: atributo action del <form> -->
<form action="https://formspree.io/f/XXXXXXXX" method="POST" ...>

<!-- Línea ~730: fetch en el script -->
fetch('https://formspree.io/f/XXXXXXXX', {
```

El plan gratuito de Formspree permite 50 envíos al mes sin tarjeta de crédito.

### 3. Links de GitHub

Los links de proyectos apuntan a:

```
https://github.com/jonathanesteban/trackflow
https://github.com/jonathanesteban/cinema-seat-manager
https://github.com/jonathanesteban/talk-to-the-machine
```

Si tus repositorios tienen una URL distinta, búscalos en `index.html` por `project-card__link` y actualiza los `href`.

---

## Despliegue en GitHub Pages

```bash
# 1. Crea el repositorio en GitHub (nombre sugerido: portfolio)
# 2. Clona y añade los archivos
git clone https://github.com/jonathanesteban/portfolio.git
cd portfolio
cp /ruta/a/tu/index.html .
mkdir assets && cp /ruta/a/tu/foto.jpg assets/foto-jonathan.jpg

# 3. Sube los cambios
git add .
git commit -m "feat: portfolio inicial"
git push origin main

# 4. Activa GitHub Pages
# GitHub → Settings → Pages → Source: Deploy from branch → main → / (root)
```

El sitio quedará disponible en `https://jonathanesteban.github.io/portfolio` en 1-2 minutos.

---

## Secciones del portfolio

| Sección | Descripción |
|---------|-------------|
| Hero | Presentación, foto, stats animados y CTAs |
| Sobre mí | Bio bilingüe (ES/EN), idiomas y competencias |
| Skills | Stack técnico dividido en 3 grupos |
| Experiencia | Timeline cronológico con logros cuantificados |
| Proyectos | Tarjetas con links a GitHub y estado del proyecto |
| Certificaciones | 6 certificaciones con emisor y fecha |
| Servicios | 6 servicios freelance disponibles |
| Contacto | Info de contacto + formulario funcional |

---

## Características técnicas

**Dark / Light mode**
El tema se detecta automáticamente desde `prefers-color-scheme`. El botón en la navegación permite cambiarlo manualmente. Los colores están gestionados por CSS Custom Properties en dos bloques `:root` separados.

**Animaciones de scroll**
Las secciones aparecen con una transición `fade-in` usando `IntersectionObserver`. Compatible con `prefers-reduced-motion`: si el usuario tiene activada esa preferencia del sistema, las animaciones se desactivan automáticamente.

**Contador animado**
Los tres números del hero (16+, 6, 3) se animan con easing cubic cuando entran en el viewport por primera vez.

**Responsive**
Tres breakpoints: escritorio (>1024px), tablet (768-1024px) y móvil (<768px). En móvil el avatar se oculta y aparece un menú hamburguesa con overlay de pantalla completa.

**Accesibilidad WCAG AA**
- Skip link activo y visible al recibir foco con teclado
- `role="main"` explícito en `<main>`
- Todos los botones icon-only tienen `aria-label` descriptivo
- El `aria-label` del theme toggle se actualiza dinámicamente
- El menú móvil se cierra con la tecla `Escape`
- Todas las imágenes decorativas tienen `aria-hidden="true"`

**Performance**
- `<link rel="preload">` para Google Fonts
- `fetchpriority="high"` + `loading="eager"` en la imagen del hero (above the fold)
- `{ passive: true }` en el listener de scroll
- Un solo archivo HTML — cero peticiones de CSS/JS propios

---

## Proyectos incluidos

### TrackFlow — Sistema Logístico
Sistema de gestión logística con algoritmo de búsqueda A* para optimización de rutas. Implementa la función de Harrington para scoring, inmutabilidad estricta en TypeScript y principio Open/Closed.

**Stack:** TypeScript · A* Algorithm · Vite

### Cinema Seat Manager
Gestor interactivo de reserva de butacas de cine. Lógica de reservas, validación de rango, búsqueda de asientos contiguos y visualización del mapa de sala.

**Stack:** TypeScript · DOM API · Vite

### Talk to the Machine
Chat con inteligencia artificial conectado a Groq API usando LLaMA 3 como modelo de lenguaje. Interfaz conversacional en tiempo real.

**Stack:** Next.js · Groq API · LLaMA 3

---

## Dependencias externas (CDN)

```html
<!-- Lucide Icons — solo se usa si hay elementos con data-lucide -->
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js" defer></script>

<!-- Google Fonts — Inter + Instrument Serif -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300..700
            &family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
```

Ninguna de estas dependencias es crítica para el funcionamiento del sitio. Si los CDNs fallan, el sitio sigue siendo funcional con fuentes del sistema.

---

## Personalización rápida

Para adaptar el portfolio a otro desarrollador, los únicos valores que necesitas cambiar son:

```
Nombre:      "Jonathan Esteban"         → buscar y reemplazar en index.html
Email:       joonathanesteban@gmail.com → 3 ocurrencias
LinkedIn:    /in/jonathanesteban        → 2 ocurrencias
GitHub user: /jonathanesteban/          → 3 ocurrencias (links de proyectos)
Ciudad:      Barcelona                  → 4 ocurrencias
Formspree:   XXXXXXXX                   → 2 ocurrencias
```

---

## Licencia

Código disponible para uso personal y educativo.
Desarrollado como proyecto de formación en **4Geeks Academy, Barcelona** · 2025–2026.

---

*Construido sin frameworks. Un archivo. Cero pasos de build.*