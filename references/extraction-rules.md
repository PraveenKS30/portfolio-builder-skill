# Extraction rules

How to turn each input type into the structured profile object without fabricating or losing nuance.

## General principles

- **Quote, don't paraphrase, when possible.** If the user wrote a great line about themselves, use it. Don't replace strong specific writing with generic synonyms.
- **Never fabricate metrics.** If a bullet says "improved performance" without a number, leave it without a number and flag for follow-up. Inventing a "30% improvement" that the user can't defend is worse than a vague bullet.
- **Flag gaps, don't fill them.** Missing employer name, vague date, missing project link — surface in the gap analysis, not patched silently.
- **Preserve seniority signals.** Title changes within a company are achievements. Reporting to executives, leading X people, owning P&L of $X — these matter and should land in the profile.

## Common fabrication traps to avoid

These are the failure modes that show up most often. Read this list before starting extraction.

**Trap: filling in missing job locations.** If the user didn't say where Stripe was, the location is empty. Do NOT default to "Remote" or "San Francisco" or anything else. Empty is correct.

**Trap: padding tech stacks with adjacent tools.** If the user listed a project's tech as "Next.js, React, GPT-4 API," that's the tech list. Do NOT add "Stripe" because SaaS tools usually use Stripe, or "Postgres" because Next.js apps usually use Postgres. Only what they said.

**Trap: changing the metric while keeping the spirit.** "A few hundred users" is not the same as "500+ GitHub stars." Different number, different unit, different platform. Keep the user's exact phrasing.

**Trap: adding plausible-sounding bullets to fill out a role.** If the user gave one bullet for a role, the role has one bullet. Don't write "Collaborated with cross-functional teams to deliver high-impact features" because it sounds normal — it's filler and it's invented.

**Trap: turning work experience into projects.** If the user mentioned a product they worked on while at a company (e.g. "led design for FigJam at Figma"), it goes in the experience section under that role. It does NOT also go in the projects section unless the user explicitly listed it as a separate project.

**Trap: rewriting vague bullets to sound more accomplished.** "Worked on ETA prediction models" is the user's bullet. Keep it as is, and flag it in the gap analysis. Do not rewrite it to "Developed and shipped ETA prediction models powering ride-time estimates" — every word added is a fabrication.

**Trap: dropping social links because the resume has no slot for them.** If the user provided a Behance, GitHub, Twitter, or website link, it must appear somewhere in the output. The resume header line and the portfolio footer are both fine targets. Don't silently drop links.

## LinkedIn (PDF export or pasted text)

LinkedIn URLs cannot be reliably fetched — block-listed by their CDN. If the user gives only a URL, ask them to paste the text or attach the PDF export instead.

When parsing a LinkedIn export:
- The first block is usually identity (name, headline, location). The headline LinkedIn auto-suggests is often weak — note it but don't lock to it; the user often wants something tighter.
- "Experience" entries are reverse-chronological. Each entry has company, title, dates, location, and a description. The descriptions are often a wall of text — split them on bullet points or sentence boundaries to populate `achievements`.
- "Skills" on LinkedIn are user-claimed. Mark them as `technical` only if they appear in actual experience descriptions or projects too. Otherwise treat them as soft signals and don't promote to the skills section without evidence.
- Recommendations and endorsements are useful for the gap analysis (e.g., "you have 12 recommendations — pull a quote for the testimonials section") but don't go into the profile by default.

## Existing resume (PDF, DOCX, plain text)

- Extract section by section. Don't try to parse the entire doc as one blob.
- Resume bullets are usually already in good shape — preserve them as `achievements` rather than rewriting. Rewriting is a separate explicit step the user has to ask for.
- Watch for inconsistencies between the resume and LinkedIn (different titles, different dates) — these go in the gap analysis.

## GitHub

If the user gives a GitHub username:
- Try to fetch the public profile (just the README) — but if you can't, ask them to either paste their repo list or describe their top 3-5 projects.
- For each non-fork repo with a description and any stars or recent activity, add to `projects`. Use the repo description; tech stack from the language breakdown.
- Pinned repos are the user's own selection of what they consider their best — prioritize those if you can identify them.
- The GitHub bio is sometimes a goldmine for `value_prop` — short, written by the user, opinionated.

## Twitter/X, YouTube, Medium, Dev.to, Behance

These mostly populate `writing`, `social_proof`, and `links`. If the user has a meaningful following or output (e.g., 50+ articles, 10k+ followers, regular speaking), surface that in `social_proof` — it's worth a callout on the portfolio.

## Raw notes / brain-dump

Treat raw notes as the highest-priority source — the user took the time to write something specific, so it almost always contains the unique value prop or the bullet points they want emphasized. Read carefully and:
- Pull out specific projects, achievements, or claims and try to find supporting evidence in the other sources.
- If a claim has no source, ask the user before including it. Don't drop user-provided info silently.

## Conflicts

When two sources disagree (e.g., LinkedIn says "Senior Engineer" but the resume says "Staff Engineer"):
- Use the most recent / most authoritative source — usually the resume for titles, since it's what the person actively maintains.
- Flag the conflict in the gap analysis so the user can resolve it.
- Never silently pick one and discard the other.
