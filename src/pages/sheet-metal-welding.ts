// PLAN-004 (22/11/2026): /sheet-metal-welding/ merged into /fabrication-and-welding/. Permanent redirect keeps any ranking it earned.
import type { APIRoute } from 'astro';

export const prerender = false;

export const GET: APIRoute = ({ redirect }) => redirect('/fabrication-and-welding/', 301);
