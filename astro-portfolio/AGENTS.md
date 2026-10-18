## Reglas del proyecto (jonathanesteban.dev)

> Leer también `../MEMORY.md` (decisiones y errores previos), `../TOOLS.md` (comandos) y `../PLAN-SEO-GEO-v1.md` (plan vigente). Este bloque es idéntico en `AGENTS.md` y `CLAUDE.md`.

### Contexto
- Sitio de **soporte informático** (particulares, pymes, autónomos). Base: **L'Hospitalet de Llobregat**; servicio **a domicilio y en remoto**.
- Stack: Astro 7 (static) · Tailwind 4 · MDX · Netlify (Functions) · n8n · Leaflet.

### Reglas obligatorias
1. **Node ≥ 22.12:** `export PATH=/home/taisu/.nvm/versions/node/v24.20.0/bin:$PATH`. El Node del sistema (v18) no funciona.
2. **Privacidad:** nunca publicar la dirección de casa ni un pin exacto. Mostrar solo zona de cobertura.
3. **Copy:** nunca "sin local físico". Usar "servicio a domicilio y en remoto".
4. **Honestidad:** no inventar cifras, reseñas, clientes ni certificaciones. Fuente: `../CV-DATA.md`. Si falta un dato, escribir `NO VERIFICADO`.
5. **Mapa:** Esri World Street Map (sin API key). No usar CARTO ni Esri Dark Canvas. Dark mode = filtro CSS sobre `.leaflet-tile-pane`.
6. **SEO:** todo `<Layout>` lleva `title`, `description` y `canonical`; un único `<h1>`; páginas sin valor SEO (`gracias`, `auth`, redirecciones) con `noindex={true}` y fuera del sitemap (`astro.config.mjs`).
7. **Accesibilidad:** `id="main-content"` en cada `<main>`; imágenes con `alt`; no quitar el skip-link ni `:focus-visible`.
8. **Formulario:** único manejador = `<script>` de `src/pages/contacto/index.astro`. No reintroducir listeners en `public/assets/js/form.js`. Éxito → `/gracias/`.
9. **Archivos:** no borrar; mover a `deprecated/` y pedir confirmación. Los `.astro` pueden ser CRLF: no usar `sed` con `$`.
10. **Verificación:** `npm run build` sin errores antes de dar algo por terminado. El navegador integrado no funciona en este entorno; comprobar con `curl`/build.
11. **Memoria:** al terminar una tarea, añadir entrada en `../MEMORY.md`; si cambian comandos, `../TOOLS.md`.
12. **Fases:** seguir `../PLAN-SEO-GEO-v1.md`; no pasar de fase sin validación de Jonathan.

---

## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Documentation

Full documentation: https://docs.astro.build

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Using React, Vue, Svelte, or other framework components](https://docs.astro.build/en/guides/framework-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)
