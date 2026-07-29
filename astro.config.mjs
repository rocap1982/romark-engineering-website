import { defineConfig } from 'astro/config';
import node from '@astrojs/node';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// Deploy targets that serve the site from a sub-path (e.g. a GitHub Pages
// project site) set these at build time. Unset means "served from the domain
// root", which is the production configuration.
const site = process.env.SITE_URL ?? 'https://romarkengineering.co.uk';
const base = process.env.BASE_PATH ?? '/';

export default defineConfig({
  site,
  base,
  output: 'static',
  adapter: node({ mode: 'standalone' }),
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()]
  }
});
