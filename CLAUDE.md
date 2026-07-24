---
project: romark-engineering-website
status: active
---

# Agent Operating Manual

This repository uses the **Fluid Build System (FBS)** — a governance framework for AI-assisted development with progressive disclosure, approval gates, and drift control.

## Project Context

**Romark Engineering** — Precision engineering & sheet metal fabrication company in Stanford-Le-Hope, Essex. Website rebuild from WordPress to Astro.

- **Current site**: https://engineeringessex.co.uk/ (WordPress/Salient theme, 35 pages)
- **Target framework**: Astro 5 (static + hybrid for contact form)
- **Styling**: Tailwind CSS v4 via @tailwindcss/vite
- **Language**: TypeScript (strict)
- **Email**: TBD (Resend API or similar for contact form)
- **Hosting**: TBD (Railway, Cloudflare Pages, or similar)

### Key Directories (target structure)

- `src/pages/` — Astro page routes (~35 pages: 9 services, 6 core, ~20 SEO landing)
- `src/layouts/Layout.astro` — Master layout with head/nav/footer/SEO
- `src/data/services.json` — Service definitions (9 services)
- `src/data/equipment.json` — Equipment catalog
- `src/data/seo-pages.json` — SEO landing page content (~20 pages)
- `src/pages/api/` — Server routes (contact form)
- `public/images/` — Static images (gallery, logo)
- `src/styles/global.css` — Tailwind v4 theme tokens

### Commands

- `npm run dev` — Start dev server
- `npm run build` — Production build
- `npm start` — Run production server

### Business Details

- Phone: 01375 673 447 / 01375 640 037
- Location: Stanford-Le-Hope, Essex
- Industries: Automotive, power generation, architectural
- Services: Laser profiling, folding/pressing, fabrication/welding, CNC machining, milling, turning, sheet metal, blank development, CAD

## Resume fast (read in order)

1. `PROJECT_STATUS.md` — fastest snapshot of current state
2. `docs/sprints/CURRENT_STATUS.md` — what's happening now
3. `.claude/skills/` — load only the relevant skills (2-4 max)
4. `.claude/agents/` — specialized subagents (verifier, test-runner, debugger, + 6 reviewers for --deep mode)
5. `docs/audits/active/` — unresolved P0/P1 drift findings

## Cross-company & personal context (HQ hub)

Rob's master context hub is **`rocap1982/hq`** — the map of all repos across Romark, Wallers, and personal projects, plus standing rules and identity files.

- Need context beyond this repo? Add `rocap1982/hq` to the session and start at its `INDEX.md`.
- Learned a durable cross-company or personal fact this session? Record it in `hq` (`companies/` or `personal/`) — not only in this repo's session logs.
- Hub rule: pointers, not copies — never duplicate this repo's live state into `hq`.

## Governance (non-negotiable)

- If a change impacts canonical contracts (schemas/API/DB/business rules), create a **plan** in `docs/plans/` and wait for explicit approval before implementing.
- Contract changes follow the full pipeline:

```
/new-idea          → explore architecture and design
/review-idea-doc   → validate idea completeness
/new-plan          → formalize contract changes
/review-plan-doc   → validate plan format and completeness
/check-plan        → deep feasibility review against codebase
  ⏸ wait for explicit user approval
/new-sprint        → create agent-executable work plan
/review-sprint-doc → validate sprint doc before building
/start-sprint      → execute the work plan
/check-sprint      → deep code review after implementation
/review-sprint     → verification gates + close-out → stage: done
```

- `/review-sprint` supports `--deep` for parallel reviewer subagents (architecture, security, performance, data integrity, test quality, docs governance)

## Workflows

- **Small fixes** (1-3 files): follow `.claude/rules/workflow-small-fixes.md`
- **Sprints** (planned work): follow `.claude/rules/workflow-sprints.md`
- **Audits** (drift checks): follow `.claude/rules/workflow-audits.md`

## Progressive disclosure

- Load only what you need. Don't read the entire repo.
- Skills are loaded on demand — descriptions are always in context, full content loads when invoked.
- Keep context lean: prefer 2-4 relevant skills over broad repo-wide reading.

## Session checkpoints

At the start of meaningful work:
- State which status docs you read (`PROJECT_STATUS.md`, `docs/sprints/CURRENT_STATUS.md`).
- State which skill(s) you loaded.

At the end of a session (or use `/close-session`):
- State whether a new skill should be created/updated.
- State whether an audit, plan, or roadmap update is required.

## Documentation (two modes)

- **Install Documentation (one-time)**: establish the repo's canonical documentation set via `/install-documentation`.
- **Ongoing Documentation (per sprint)**: when features or contracts change, load the `documentation-governance` skill and update the correct canonical docs before marking sprint stage `done`.

## Keep documentation minimal

- Don't create new docs for one-off fixes.
- Prefer updating the single snapshot (`PROJECT_STATUS.md`) + existing sprint/audit docs.
