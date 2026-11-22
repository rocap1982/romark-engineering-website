// PLAN-004 (22/11/2026): /blank-development/ merged into /cad/. Permanent redirect keeps any ranking it earned.
import type { APIRoute } from 'astro';

export const prerender = false;

export const GET: APIRoute = ({ redirect }) => redirect('/cad/', 301);
