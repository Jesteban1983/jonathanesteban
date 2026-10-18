// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

import mdx from '@astrojs/mdx';

import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://jonathanesteban.dev',
  output: 'static',
  trailingSlash: 'always',

  vite: {
    plugins: [tailwindcss()]
  },

  integrations: [
    mdx(),
    sitemap({
      // Páginas sin valor SEO (gracias, OAuth callbacks, redirección)
      filter: (page) => !/\/(gracias|auth|certificaciones)\//.test(page),
      changefreq: 'monthly',
      priority: 0.7,
      lastmod: new Date(),
    }),
  ]
});