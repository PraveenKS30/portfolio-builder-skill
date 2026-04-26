# portfolio-builder

A Claude skill that turns your reference materials — LinkedIn, existing resume, GitHub, social links, raw notes — into a polished single-file HTML portfolio website and a matching Markdown resume.

Three theme options. No fabrication. Built-in gap analysis that flags weak bullets and missing pieces instead of papering over them.

---

## Why this exists

Most "AI resume builders" cheerfully invent metrics, pad your tech stacks with adjacent tools, and rewrite your vague bullets into confident-sounding fiction. That looks great until you have to defend it in an interview.

This skill takes a different approach. It treats your inputs as ground truth, only emits what you actually said, and explicitly flags every weak spot so *you* can decide whether to fill it in or leave it. It also produces a real portfolio site — not a generic template — in one of three distinct themes tuned for different professional vibes.

## What you get

Out of the box, the skill produces:

- **`portfolio.html`** — a single self-contained HTML file. CSS embedded, only Google Fonts loaded externally. Mobile-responsive. Drop it on GitHub Pages, Vercel, your own domain, anywhere.
- **`resume.md`** — an ATS-friendly Markdown resume. Easy to edit, easy to convert to PDF, easy to keep under version control.

Plus a Portfolio Health Report in the chat that flags missing metrics, vague bullets, and gaps relative to your industry.

## Themes

| Theme | Vibe | Good for |
|-------|------|----------|
| **minimal-light** | Clean serif headings, off-white background, lots of whitespace | Consultants, writers, PMs, generalists |
| **dark-tech** | Terminal-inspired dark mode with monospace accents and subtle neon | Engineers, ML / infra, hackers |
| **creative-bold** | Vibrant colors, large display type, asymmetric layout | Designers, marketers, founders, creatives |

If you don't pick one, the skill picks based on your domain. Swap themes by re-running with a different `--theme`.

## Quick start

### Install

Copy this folder into your local Claude skills directory and rename it to `portfolio-builder/`. The skill loader will pick it up.

Or, package it as a `.skill` file:

```bash
python -m scripts.package_skill portfolio-builder/
```

Then drag the resulting `portfolio-builder.skill` into Claude.

### Use

Once installed, just describe what you want:

```
Build me a portfolio from my LinkedIn export and GitHub.
Use the dark-tech theme.

[paste LinkedIn text]
GitHub: github.com/myhandle
Email: me@example.com
```

The skill will:

1. Extract a structured profile from your inputs
2. Show you a gap analysis (missing metrics, vague bullets, weak spots)
3. Confirm or pick a theme
4. Generate the portfolio HTML + resume Markdown
5. Hand off the files with a short summary

## Inputs

Pass any combination — partial inputs are fine:

- **LinkedIn** — exported PDF or pasted text. URLs alone aren't reliably fetchable; LinkedIn blocks scrapers.
- **Existing resume** — PDF, DOCX, or plain text
- **GitHub** — username or profile URL
- **Social links** — Twitter/X, YouTube, Medium, Dev.to, Behance, personal site
- **Raw notes** — bullet points, brain-dumps, or just a description of what you do

The more you give it, the better the output. But it works with surprisingly little.

## How it differs from other AI resume tools

### It doesn't make things up

The skill ships with explicit "fabrication trap" rules and concrete examples of what *not* to do. A few from the reference docs:

- If you said "worked on ETA prediction models," the output says exactly that — not "Developed and shipped ETA prediction models powering ride-time estimates."
- If you said your project has "a few hundred users," the output says "a few hundred users" — not "500+ GitHub stars" (different metric, different platform, different number).
- If you didn't say where your previous job was located, the location field stays empty — not silently filled with "Remote" or "San Francisco."
- If you listed a project's tech as "Next.js, React," the output doesn't add "Stripe" or "Postgres" because those are common adjacencies.

### It flags weakness instead of hiding it

The Portfolio Health Report categorizes gaps by severity:

```
🔴 Critical
- Lyft role: "worked on ETA prediction models" — no metrics, no scope, no impact
- No LinkedIn link — standard for any 2026 job search

🟡 Moderate
- Stripe and Lyft locations missing
- Stripe missing tech stack

🟢 Minor
- Date format inconsistent across roles
```

This gives you the chance to fill gaps before publishing — which is the only way to actually fix them.

### It looks like a portfolio, not a template

The three themes are visually distinct and intentional, not Bootstrap reskins. The dark-tech theme has a working terminal-window header. The creative-bold theme has neo-brutalist offset shadows and decorative blobs. The minimal-light theme leans into typography with Fraunces and generous whitespace.

## Project structure

```
portfolio-builder/
├── SKILL.md                          # Main skill instructions for Claude
├── README.md                         # This file
├── HOW-TO-INSTALL.md                 # Quick install instructions
├── assets/
│   └── themes/
│       ├── minimal-light.html        # Light, serif, whitespace-heavy
│       ├── dark-tech.html            # Dark, monospace, terminal vibe
│       └── creative-bold.html        # Bold colors, display type
├── references/
│   ├── profile-schema.md             # In-memory profile JSON shape
│   ├── extraction-rules.md           # How to extract without fabricating
│   ├── gap-analysis.md               # Health report checklist
│   └── resume-template.md            # Markdown resume conventions + ATS rules
├── scripts/
│   └── render_portfolio.py           # Profile JSON + theme → portfolio.html + resume.md
└── evals/
    └── evals.json                    # Test cases (3 personas)
```

## Theme template tokens

Themes use simple `{{ token }}` placeholders that the render script substitutes. If you want to add a fourth theme, copy one of the existing templates and use the same tokens:

| Token | What it becomes |
|-------|------------------|
| `{{ name }}` | Full name |
| `{{ title }}` | Current title |
| `{{ location }}` | City, Country |
| `{{ value_prop }}` | One-line value prop |
| `{{ bio }}` | 3-4 sentence about-me |
| `{{ email }}` | Contact email |
| `{{ cta_github }}`, `{{ cta_linkedin }}`, `{{ cta_email }}` | Pre-rendered CTA buttons |
| `{{ experience_items }}` | Rendered experience timeline |
| `{{ skills_blocks }}` | Rendered skills section |
| `{{ project_cards }}` | Rendered project cards |
| `{{ writing_section }}` | Optional writing/talks section |
| `{{ footer_links }}` | Footer link list |

If a profile field is missing, the renderer inserts an HTML comment like `<!-- ADD: professional headshot here -->` rather than leaving the section blank or fabricating content.

## Update workflow

When you have new info — a shipped project, a new cert, a promotion — just tell the skill:

```
Just shipped a new project: telemetry-dashboard.
Open source, github.com/me/telemetry-dashboard, in TypeScript and Rust.
```

It merges the update into the structured profile, re-runs the renderer, and tells you:

- What changed
- Which sections were affected
- Any new gaps the update revealed

## Standalone use of the render script

The render script can also be run directly without going through Claude. Build a profile JSON file matching the schema in `references/profile-schema.md`, then:

```bash
python scripts/render_portfolio.py \
    --profile path/to/profile.json \
    --theme   dark-tech \
    --out-dir path/to/output/
```

This is handy for hooking the skill into a CI pipeline that rebuilds your portfolio whenever you push a profile update.

## Roadmap ideas

These aren't promised features — just suggestions for where this could go:

- **Print-friendly HTML resume** alongside the Markdown one
- **PDF export** (via WeasyPrint or Playwright)
- **Themes for specific industries** (academic CV, design case-study layout, founder/operator)
- **Content sync** — pull GitHub README projects automatically, refresh on each build
- **Internationalization** — date formats, address conventions, photo norms by region

PRs welcome.

## Contributing

This skill is opinionated about a few things:

- **No fabrication.** If a contribution makes the skill fill in details the user didn't provide, it's a regression.
- **Concrete over abstract.** The skill instructions teach by example, not by command. New rules should follow that pattern.
- **Themes should be distinctive.** No more bland generic-template themes; each one needs a clear point of view.

To test changes, the `evals/evals.json` file has three personas you can re-run as regression tests.

## Built with

The skill itself is plain Markdown + a small Python helper. No framework, no build step, no dependencies beyond stdlib Python 3 for the optional render script.

The themes use Google Fonts only — Fraunces + Inter for minimal-light, JetBrains Mono + Inter for dark-tech, DM Serif Display + Space Grotesk for creative-bold.

## License

MIT. Use it, fork it, ship your own version. Attribution appreciated but not required.
