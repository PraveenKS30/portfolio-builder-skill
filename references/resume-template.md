# Resume template & writing rules

The skill produces a Markdown resume because it's the easiest format to edit, version, and convert later. The render script generates this from the profile object.

## Structure

```markdown
# {{ name }}

**{{ title }}** · {{ location }}
{{ email }} · {{ links.github }} · {{ links.linkedin }} · {{ links.website }}

---

## Summary

{{ 2-3 sentence tailored summary that mirrors the value_prop but reads as the
opening paragraph of a resume — what kind of work, what scale, what makes them
distinct. Use first person omitted (no "I"). }}

---

## Experience

### {{ company }} — {{ title }}
*{{ dates }} · {{ location }}*

- {{ achievement starting with action verb, with metric where possible }}
- {{ achievement }}
- {{ achievement }}

**Tech:** {{ tech list, comma-separated }}

### {{ next company }} — {{ title }}
...

---

## Skills

**Languages & Frameworks:** {{ technical skills }}
**Domain:** {{ domain skills }}
**Tools:** {{ relevant tools }}

---

## Projects

### {{ project name }} — [{{ link }}]({{ link }})
{{ 1-2 sentence description }}
*Tech: {{ tech }}*

---

## Education

**{{ degree }}** · {{ institution }} · {{ year }}
{{ optional details }}

---

## Certifications

- {{ name }} — {{ issuer }}, {{ year }}
```

## ATS rules

ATS = Applicant Tracking System. These parsers are dumb; respect them:

- **Use plain Markdown headings.** No fancy unicode characters in section titles.
- **No tables, no images, no two-column layouts.** They break parsers.
- **Spell out abbreviations on first use** (e.g., "Continuous Integration (CI)") so the parser indexes both terms.
- **Use the exact keywords from job descriptions.** If the target role says "Kubernetes," don't write "K8s."
- **Standard section names.** "Experience" not "Where I've Been." "Skills" not "Toolbox."

## Bullet writing examples

**Bad → Good** (use these as exemplars when rewriting):

Bad: *Worked on the search team to improve relevance.*
Good: *Shipped query rewriting model that improved top-3 click-through rate by 12% across 4M weekly searches.*

Bad: *Responsible for managing AWS infrastructure.*
Good: *Migrated 30+ services from EC2 to EKS, cutting infra costs 35% ($420k/year) and deploy time from 18min to 4min.*

Bad: *Helped redesign the onboarding flow.*
Good: *Led redesign of new-user onboarding (research → prototype → ship), increasing day-7 activation from 41% to 58%.*

Bad: *Strong communication and leadership skills.*
Good: *Mentored 4 junior engineers; two were promoted to mid-level within 18 months.*

Bad: *Used machine learning to solve business problems.*
Good: *Built and shipped recommendation model serving 50M users/day; A/B test showed +8% session length, +3% revenue.*

## Length

- Less than 5 years experience: 1 page
- 5-15 years: 1-2 pages, prefer 1
- 15+ years: 2 pages — never more

If a role is older than ~10 years and not directly relevant, compress it to one line ("Earlier roles at X, Y, Z — details on request").

## What to leave out

- Date of birth, marital status, photo (US/UK conventions; flag if user is in a market where these are expected)
- High school, unless it's the only education
- "References available upon request" — assumed
- Skills the user can't actually do at a senior-relevant level
