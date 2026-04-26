# Profile schema

This is the in-memory representation the skill builds from the user's inputs. The render script reads this exact shape — keep it consistent. Missing fields are fine (the renderer handles them with placeholders); fabricated fields are not.

## Full schema

```json
{
  "identity": {
    "name": "Full name as it should appear on the site and resume",
    "title": "Current professional title (e.g. 'Senior ML Engineer')",
    "location": "City, Country (or 'Remote')",
    "headline": "One-line professional headline — what they want to be known for",
    "value_prop": "1-2 sentence value proposition. What makes them distinct.",
    "bio": "3-4 sentence about-me paragraph synthesized from inputs",
    "headshot_url": "Optional URL or local path to headshot image"
  },

  "links": {
    "email": "person@example.com",
    "github": "https://github.com/handle",
    "linkedin": "https://linkedin.com/in/handle",
    "twitter": "https://x.com/handle",
    "website": "https://existing-site.com",
    "youtube": "https://youtube.com/@handle",
    "medium": "https://medium.com/@handle",
    "other": [
      { "label": "Behance", "url": "..." }
    ]
  },

  "experience": [
    {
      "company": "Acme Corp",
      "title": "Senior Engineer",
      "dates": "Jan 2022 – Present",
      "location": "San Francisco, CA",
      "summary": "Optional one-line summary of the role",
      "achievements": [
        "Shipped X to Y users, reducing Z by N%",
        "Led team of N engineers building..."
      ],
      "tech": ["Python", "Kubernetes", "Postgres"]
    }
  ],

  "skills": {
    "technical": ["Python", "TypeScript", "PostgreSQL", "AWS"],
    "domain":    ["ML infrastructure", "Distributed systems"],
    "soft":      ["Cross-functional leadership", "Technical writing"]
  },

  "education": [
    {
      "degree": "B.S. Computer Science",
      "institution": "University of X",
      "year": "2018",
      "details": "Optional — honors, GPA if notable, relevant coursework"
    }
  ],

  "certifications": [
    { "name": "AWS Solutions Architect — Professional", "issuer": "AWS", "year": "2024" }
  ],

  "projects": [
    {
      "name": "Project name",
      "description": "1-2 sentences. What it does, who it's for, why it matters.",
      "tech": ["Next.js", "tRPC", "Postgres"],
      "link": "https://...",
      "repo": "https://github.com/...",
      "highlight": true
    }
  ],

  "writing": [
    { "title": "Article title", "venue": "Medium / personal blog / conference", "link": "https://..." }
  ],

  "social_proof": {
    "followers": { "twitter": 5000, "github": 200 },
    "speaking":  ["Talk title @ Conference 2024"],
    "press":     [{ "outlet": "...", "title": "...", "link": "..." }]
  }
}
```

## Edge cases and conventions

**Dates.** Use the form `Mon YYYY – Mon YYYY` or `Mon YYYY – Present`. If the source only gives years, use `YYYY – YYYY`. Don't normalize aggressively if the user wrote it differently — just be consistent within the profile.

**Achievements vs. responsibilities.** Achievements are what the person *did* with measurable impact. Responsibilities are what they were *supposed to* do. Always prefer achievements. If the source only has responsibilities, lift them but flag the role for follow-up in the gap analysis.

**Skills overlap.** Don't list the same skill in both `technical` and `domain`. If a skill is debatable (e.g., "system design"), put it under `domain`.

**Highlighted projects.** Mark 2-4 projects with `"highlight": true` if they're the strongest. The renderer can use this to decide layout (e.g., featured cards vs. list).

**Empty arrays vs. missing fields.** If a section legitimately doesn't apply (no certifications, no writing), use an empty array. Don't omit the key — the renderer checks for empty arrays to suppress empty sections.

**Links.** Always include the protocol (`https://`). For LinkedIn URLs, normalize to `https://linkedin.com/in/<handle>` form.

## What not to put in the profile

- Made-up metrics. If the user didn't give a number, don't invent one.
- Skills the user didn't claim and that aren't evidenced by their work.
- Inferred employer or project details the user didn't confirm.
- Anything from a URL you couldn't actually fetch.
