# Gap analysis checklist

Run through this before generating outputs. Anything that fails goes in the Portfolio Health Report. Severity guide: 🔴 Critical (will materially hurt them in a job search), 🟡 Moderate (worth fixing soon), 🟢 Minor (polish).

## Identity & headline

- 🔴 Missing professional headline or value prop
- 🔴 Headline is generic ("Software Engineer at X") with no positioning
- 🟡 No bio / about-me paragraph
- 🟡 No professional headshot referenced
- 🟢 Inconsistent capitalization or punctuation in name/title across sources

## Experience

For each role:
- 🔴 Bullets are responsibilities ("Responsible for...") rather than achievements
- 🔴 No metrics anywhere in the role
- 🟡 Vague verbs ("worked on", "helped with", "involved in")
- 🟡 No tech stack listed for engineering roles
- 🟢 Date format inconsistent with other roles

Across roles:
- 🔴 Unexplained gap longer than 6 months without context
- 🟡 Job titles or dates that differ between resume and LinkedIn
- 🟢 Reverse-chronological order broken

## Skills

- 🔴 Skills claimed but not evidenced anywhere in experience or projects
- 🟡 Skills section dominated by buzzwords with no specific tools
- 🟡 Stack heavily weighted toward outdated tech for their role (e.g., a "ML engineer" listing only scikit-learn and no modern frameworks)
- 🟢 Soft skills listed without supporting evidence

## Projects

- 🔴 No projects at all (critical for engineers, designers, anyone whose work is tangible)
- 🔴 Projects without links or any way to see the work
- 🟡 Project descriptions that don't explain what the project actually does
- 🟡 No tech stack listed
- 🟢 Fewer than 3 projects highlighted on portfolio

## Writing & content

- 🟡 Has a blog/Medium/YouTube but it's not linked anywhere
- 🟢 No content output at all (this is normal — only flag if their target role expects it, e.g., DevRel, founder, consultant)

## Links & social

- 🔴 No email or way to contact
- 🟡 GitHub link missing for engineers
- 🟡 LinkedIn link missing
- 🟢 Personal website not linked from other socials

## Domain-specific keyword gaps

Adjust based on the person's field. Flag missing terms as Opportunities (not Critical) — they're suggestions, not requirements:

**AI / ML / Agents work**
- Modern: agents, RAG, evals, fine-tuning, MCP, LLMOps, vector DBs, embeddings
- Frameworks: LangChain, LlamaIndex, vLLM, transformers
- Production: latency, cost-per-call, eval pipelines

**Data engineering**
- Modern: dbt, Snowflake, BigQuery, Databricks, Iceberg, lakehouse
- Streaming: Kafka, Flink, Materialize
- Quality: data contracts, observability

**Frontend**
- Modern: React 18+, Next.js App Router, RSC, Tailwind, Radix, shadcn/ui
- Performance: Core Web Vitals, LCP, INP
- Tooling: Vite, Turbopack, Bun

**Backend / infra**
- Modern: Kubernetes, Terraform, Pulumi, ArgoCD, gRPC
- Observability: OpenTelemetry, Prometheus, Grafana
- Cloud: specific services beyond just "AWS"

**Design**
- Modern: Figma, design systems, tokens, variants
- Process: research, prototyping, accessibility, WCAG
- Output: case studies (with metrics), shipped work

**Product management**
- Modern: discovery, opportunity solution trees, JTBD
- Metrics: north star, activation, retention, revenue
- Tools: Linear, Notion, Amplitude, Mixpanel

## Formatting the report

```
## Portfolio Health Report

🔴 Critical
- [item] — [one-line explanation of why it matters]
- [item] — [why]

🟡 Moderate
- [item]
- [item]

🟢 Minor
- [item]

## Inconsistencies
- [field/value] in [source A] vs. [source B]

## Opportunities
- [missing keyword] is standard in [their field] roles in 2026 — worth adding if the work supports it
- [missing project type] — [suggestion]
```

Keep each line short. The user is going to scan this, not read it.
