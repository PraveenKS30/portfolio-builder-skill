---
name: portfolio-builder
description: >-
  Build a personal portfolio website and matching resume from a person's reference materials (LinkedIn, existing resume, GitHub, social links, raw notes). Use this skill whenever the user wants to create, generate, build, or refresh a portfolio site, personal website, dev portfolio, designer portfolio, or wants to turn their LinkedIn/resume/GitHub into a portfolio. Also use when the user wants to write or rewrite their resume from existing background info, asks for a "personal site," "portfolio," "developer site," or wants help packaging their professional identity. The skill produces a single-file HTML portfolio (in one of three themes: minimal-light, dark-tech, or creative-bold) plus a Markdown resume the user can edit. Trigger even when the user only mentions one of the inputs (e.g. "make a portfolio from my LinkedIn") or only one of the outputs (e.g. "rewrite my resume").
---

# Portfolio Builder

Take messy reference material about a person — a LinkedIn export, a resume PDF, a GitHub username, a few links, some notes — and turn it into a polished single-file HTML portfolio website plus a Markdown resume the person can edit and reuse. The skill is opinionated about quality (specific bullets, quantified results, no filler) and about look-and-feel (three distinct themes, no generic templates).

## When this skill applies

Use this skill any time the user is trying to package their professional identity for the world: building a portfolio site, refreshing their resume from raw background info, turning a LinkedIn into a personal site, or asking for "something I can send to recruiters." Don't wait for the user to say the word "portfolio" — if they describe the problem ("I need a personal website, here's my LinkedIn and GitHub") that's enough.

If the user only wants the resume, still use this skill — produce just the Markdown resume and skip the portfolio build. If the user only wants the website, do the inverse. The default when they want both (or are ambiguous) is to produce both.

## The workflow at a glance

1. **Collect inputs.** Take whatever the user has (URLs, PDFs, .txt, raw notes pasted in chat). Don't insist on a specific format.
2. **Extract a structured profile.** Pull out identity, experience, skills, education, projects, and links into one in-memory JSON object.
3. **Run a gap analysis.** Surface missing or weak areas, inconsistencies, and quick wins. Show this to the user before building anything — it informs how aggressively the skill should fill gaps vs. flag them.
4. **Confirm theme.** Show the three theme options and let the user pick. If they don't pick, default based on the person's domain (engineer → dark-tech, designer/creative → creative-bold, everyone else → minimal-light).
5. **Generate the portfolio HTML and resume markdown.** Use the helper script in `scripts/render_portfolio.py` plus the theme template in `assets/themes/`.
6. **Hand off the files** with a short summary of what was generated and what's still missing (placeholder comments in the HTML, gaps in the resume).

The user may come back later with new info ("I just shipped a new project," "I got promoted") — re-run steps 2 → 5 with the new data merged in.

## Step 1 — Collect inputs

Ask once at the start: "What do you have for me? Any of these are useful — LinkedIn (URL or exported PDF), existing resume, GitHub/Twitter/personal site, or just a brain-dump of your background." Don't gate progress on a complete set — partial inputs are normal.

If the user provides a URL the skill cannot fetch (LinkedIn especially blocks scrapers), don't pretend you read it. Tell them honestly that LinkedIn's URL isn't directly accessible and ask them to either paste the relevant text or export their profile to PDF.

## The single most important rule: don't invent

This is the rule the skill stands or falls on, so it's worth being explicit. The user is going to put their name on whatever this skill produces. If the output contains a metric, employer, project detail, or skill they can't defend in an interview, the skill has hurt them, not helped them.

**Concretely, this means:**

- If the source says "worked on ETA prediction models," the output says exactly that — not "Developed and shipped ETA prediction models powering ride-time estimates" (the second version made up "shipped," "powering," and "ride-time estimates").
- If the source says a project has "a few hundred users," the output says "a few hundred users" — not "500+ GitHub stars" (different metric, different number, different platform).
- If the source doesn't say where Stripe was, the location field stays empty or is omitted — not silently filled with "Remote" or "San Francisco".
- If the source lists a project's tech as "Next.js, React" the output doesn't add "Stripe" or "Postgres" because those are common adjacencies.

The temptation is strong — fabricated bullets sound more polished, fabricated tech stacks make profiles look more complete, and fabricated locations make resumes look filled out. Resist all of it. The user will catch it, and it destroys trust.

**Three cheap tests before writing any output line:**

1. *Is this exact phrase or fact in the source material?* If not, leave it out or replace with a placeholder.
2. *Could the user defend this in an interview?* If they couldn't say "yes I built that with X tech and got Y result" without lying, take it out.
3. *Am I rephrasing or am I extending?* Light rephrasing for tone is fine ("worked on" → "contributed to" is gray area but OK). Adding new claims is not.

When something is missing or vague, the right response is to flag it in the gap analysis (see step 3) so the user can fill it in — not to paper over it with plausible-sounding filler.

## Step 2 — Extract a structured profile

Build an internal JSON object with this shape. Don't show the JSON to the user — it's the working representation. See `references/profile-schema.md` for the full schema and edge cases.

```
{
  "identity": { "name", "title", "location", "headline", "value_prop" },
  "links":    { "email", "github", "linkedin", "twitter", "website", "other": [] },
  "experience": [ { "company", "title", "dates", "achievements": [ ... ] } ],
  "skills":     { "technical": [], "domain": [], "soft": [] },
  "education":  [ { "degree", "institution", "year" } ],
  "certifications": [ ... ],
  "projects":   [ { "name", "description", "tech": [], "link" } ],
  "writing":    [ { "title", "venue", "link" } ],
  "social_proof": { "followers", "speaking", "press" }
}
```

When extracting, follow the rules in `references/extraction-rules.md` — particularly: never fabricate metrics, flag vague entries instead of inventing detail, and preserve the user's voice if they wrote in first person.

## Step 3 — Gap analysis

Before generating anything, surface what's missing or weak. **This is where vague bullets, missing metrics, and dropped links go.** When the user reads the report they should see all the things you noticed could use more detail — that's the value of the gap analysis. If you "improve" a vague bullet silently and don't mention it, you've removed the user's ability to choose between leaving it vague or filling it in properly.

For each role, scan every bullet and explicitly call out:
- Bullets that lack metrics ("worked on X")
- Bullets with weak verbs ("helped," "involved in," "contributed to")
- Roles missing tech stack
- Missing job locations or dates

Use this format (it reads cleanly in chat and gives the user a chance to fill gaps before the build):

```
## Portfolio Health Report

🔴 Critical
- [item] — [why it matters]

🟡 Moderate
- [item]

🟢 Minor
- [item]

## Inconsistencies
- [field] differs between [source A] and [source B]

## Opportunities
- [missing keyword / project that should be highlighted / link that's missing]
```

See `references/gap-analysis.md` for the full checklist of things to look for, including industry-specific keywords (e.g., for AI/ML work, flag missing terms like "agents," "RAG," "evals," "MCP").

After showing the report, ask: "Want to fill any of these in before I build, or should I generate now and use placeholders?"

## Step 4 — Confirm the theme

Three themes ship with this skill. Each lives in `assets/themes/`:

- **minimal-light** — clean serif headings, lots of whitespace, off-white background. Good default for consultants, writers, PMs, generalists.
- **dark-tech** — dark background, monospace accents, subtle neon highlight color. Good for engineers, ML/AI folks, infra people.
- **creative-bold** — vibrant colors, large display type, asymmetric layout. Good for designers, marketers, founders, creative roles.

Show the three options to the user with one-line descriptions. If they don't have a preference, pick a default based on the profile's domain and explain the choice. Don't overthink it — they can re-run with a different theme in 30 seconds.

## Step 5 — Generate

Use the script:

```
python scripts/render_portfolio.py \
    --profile <path-to-profile.json> \
    --theme <minimal-light|dark-tech|creative-bold> \
    --out-dir <output-directory>
```

This produces two files in the output directory:
- `portfolio.html` — single self-contained HTML file (CSS embedded, only CDN-loaded fonts allowed)
- `resume.md` — Markdown resume following the conventions in `references/resume-template.md`

The script handles theme rendering and missing-field placeholders automatically. If a field is missing, the script inserts an HTML comment like `<!-- ADD: professional headshot -->` rather than leaving the section blank or fabricating content.

To use the script, first save the structured profile to a JSON file in a working directory, then call the script. Example:

```
mkdir -p /tmp/portfolio-build
cat > /tmp/portfolio-build/profile.json << 'EOF'
{ ...the profile object... }
EOF
python scripts/render_portfolio.py \
    --profile /tmp/portfolio-build/profile.json \
    --theme dark-tech \
    --out-dir /tmp/portfolio-build/
```

If the script is unavailable for any reason (different environment, permissions), fall back to reading the relevant theme template directly from `assets/themes/<theme>.html` and rendering it inline — the templates use `{{ token }}` placeholders that map 1:1 to the profile schema.

## Step 6 — Hand off

When done, give the user:

1. **Direct paths/links to both files** (not the JSON, just `portfolio.html` and `resume.md`).
2. **A short summary of what was generated** — number of roles, projects, theme used.
3. **A short list of what's still missing** — every `<!-- ADD: ... -->` placeholder in the portfolio + any flagged gaps from step 3.
4. **A "what's next" suggestion** — usually one or two of: add a headshot, write project case studies, connect a GitHub readme, swap themes to compare.

Don't write a long postamble explaining what's in the files — they can open them.

## Update mode

If the user comes back with new info ("I just got a cert in X," "I shipped Y," "I got promoted to Z"), don't rebuild from scratch — merge the new data into the structured profile and re-run the renderer. Tell the user explicitly:

```
What changed: <one line>
Sections updated: <portfolio sections + resume sections>
New gaps revealed: <if any>
```

## Quality bars

These are non-negotiable because they're what separates a generic portfolio from one that gets the user a callback:

- **Action verbs.** Every resume bullet starts with one (Built, Shipped, Led, Reduced, Designed). No "Responsible for…"
- **Quantified results where possible.** Percentages, dollar amounts, time saved, scale. If the user didn't give numbers, flag it as a gap rather than inventing.
- **No vague claims.** "Strong communication skills" is filler. "Presented quarterly results to 200-person eng org" is evidence.
- **Don't fabricate.** If a metric, project, or skill isn't in the source material, it doesn't make it into the output. Better to leave a placeholder.
- **Specific, not generic.** Bios, headlines, project descriptions — write them so they could only describe this person, not anyone in the same role.

## Reference files

- `references/profile-schema.md` — full schema for the in-memory profile object, with edge cases
- `references/extraction-rules.md` — how to extract from each input type without fabricating
- `references/gap-analysis.md` — checklist for the health report, including domain-specific keywords
- `references/resume-template.md` — Markdown resume structure, ATS rules, and bullet-writing examples

## Bundled assets

- `assets/themes/minimal-light.html` — light theme template
- `assets/themes/dark-tech.html` — dark theme template
- `assets/themes/creative-bold.html` — bold/creative theme template

## Bundled scripts

- `scripts/render_portfolio.py` — takes profile JSON + theme name, writes portfolio.html and resume.md
