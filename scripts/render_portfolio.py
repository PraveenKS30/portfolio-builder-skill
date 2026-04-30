#!/usr/bin/env python3
"""
Render a portfolio HTML and Markdown resume from a structured profile JSON.

Usage:
    python render_portfolio.py \
        --profile path/to/profile.json \
        --theme   minimal-light|dark-tech|creative-bold \
        --out-dir path/to/output/

Outputs:
    <out-dir>/portfolio.html
    <out-dir>/resume.md
"""

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path

THEMES = {"minimal-light", "dark-tech", "creative-bold"}

# ---------- helpers ----------

def safe(d, *keys, default=""):
    """Safely walk a nested dict; return default if any key is missing."""
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur or cur[k] is None:
            return default
        cur = cur[k]
    return cur


def e(s):
    """Escape HTML entities, treating None as ''."""
    return escape(str(s)) if s is not None else ""


def cta(label, href, kind="cta-secondary"):
    if not href:
        return ""
    extra = "" if href.startswith("mailto:") else ' target="_blank" rel="noopener"'
    return f'<a class="cta {kind}" href="{e(href)}"{extra}>{e(label)}</a>'


def display_url(url):
    if not url:
        return ""
    return re.sub(r"^https?://", "", str(url)).rstrip("/")


# ---------- portfolio rendering ----------

def render_experience_items(experience, theme):
    if not experience:
        return "<!-- ADD: experience entries -->"
    parts = []
    for role in experience:
        bullets = "".join(f"<li>{e(b)}</li>" for b in role.get("achievements", []))
        if not bullets:
            bullets = "<li><!-- ADD: 3-5 bullet achievements for this role --></li>"
        tech = role.get("tech") or []
        tech_row = (
            f'<div class="tech-row">{e(", ".join(tech))}</div>' if tech else ""
        )

        if theme == "minimal-light":
            parts.append(f"""
<div class="timeline-item">
  <div class="timeline-dates">{e(role.get('dates', ''))}</div>
  <div>
    <div class="timeline-title">{e(role.get('title', ''))}</div>
    <div class="timeline-company">{e(role.get('company', ''))}{' · ' + e(role.get('location', '')) if role.get('location') else ''}</div>
    <ul class="timeline-bullets">{bullets}</ul>
    {tech_row}
  </div>
</div>""")
        else:
            parts.append(f"""
<div class="timeline-item">
  <div class="timeline-header">
    <div class="timeline-title">{e(role.get('title', ''))}</div>
    <div class="timeline-dates">{e(role.get('dates', ''))}</div>
  </div>
  <div class="timeline-company">{e(role.get('company', ''))}{' · ' + e(role.get('location', '')) if role.get('location') else ''}</div>
  <ul class="timeline-bullets">{bullets}</ul>
  {tech_row}
</div>""")
    return "\n".join(parts)


def render_skills_blocks(skills, theme):
    if not skills:
        return "<!-- ADD: skills -->"
    cats = [
        ("technical", "Technical"),
        ("domain", "Domain"),
        ("soft", "Soft skills"),
    ]
    parts = []
    for key, label in cats:
        items = skills.get(key) or []
        if not items:
            continue
        if theme == "minimal-light":
            parts.append(f"""
<div>
  <div class="skill-cat-title">{e(label)}</div>
  <div class="skill-list">{e(' · '.join(items))}</div>
</div>""")
        else:
            pills = "".join(f'<span class="skill-pill">{e(s)}</span>' for s in items)
            parts.append(f"""
<div class="skill-cat">
  <div class="skill-cat-title">{e(label)}</div>
  <div class="skill-pills">{pills}</div>
</div>""")
    return "\n".join(parts) or "<!-- ADD: skills -->"


def render_project_cards(projects, theme):
    if not projects:
        return "<!-- ADD: projects -->"
    parts = []
    ordered_projects = sorted(projects, key=lambda p: not bool(p.get("highlight")))
    for p in ordered_projects:
        tech = ", ".join(p.get("tech") or [])
        links = []
        if p.get("link"):
            links.append(f'<a href="{e(p["link"])}" target="_blank" rel="noopener">live →</a>')
        if p.get("repo"):
            links.append(f'<a href="{e(p["repo"])}" target="_blank" rel="noopener">code →</a>')
        links_html = " ".join(links) or "<!-- ADD: live link or repo -->"
        tech_html = f'<div class="project-tech">{e(tech)}</div>' if tech else ""
        featured = " featured" if p.get("highlight") else ""
        parts.append(f"""
<div class="project-card{featured}">
  <div class="project-name">{e(p.get('name', ''))}</div>
  <div class="project-desc">{e(p.get('description', ''))}</div>
  {tech_html}
  <div class="project-links">{links_html}</div>
</div>""")
    return "\n".join(parts)


def render_writing_section(writing, theme):
    if not writing:
        return ""  # entirely suppress section if empty
    items = "".join(
        f'<li><a href="{e(w.get("link", "#"))}" target="_blank" rel="noopener">{e(w.get("title", ""))}</a>'
        f'<span class="writing-venue">{e(w.get("venue", ""))}</span></li>'
        for w in writing
    )
    heading_num = '<span class="num">05</span>' if theme == "creative-bold" else ""
    return f"""
<section>
  <h2>{heading_num}Writing & talks</h2>
  <ul class="writing-list">{items}</ul>
</section>
"""


def render_footer_links(links):
    pieces = []
    for key, label in [
        ("github", "github"),
        ("linkedin", "linkedin"),
        ("twitter", "twitter"),
        ("youtube", "youtube"),
        ("medium", "medium"),
        ("website", "website"),
    ]:
        if links.get(key):
            pieces.append(f'<a href="{e(links[key])}" target="_blank" rel="noopener">{label}</a>')
    for other in links.get("other", []) or []:
        if other.get("url"):
            pieces.append(f'<a href="{e(other["url"])}" target="_blank" rel="noopener">{e(other.get("label", "link"))}</a>')
    return " · ".join(pieces) or "<!-- ADD: social links -->"


def render_headshot(identity):
    url = identity.get("headshot_url")
    if not url:
        return "<!-- ADD: professional headshot here if available -->"
    alt = identity.get("name") or "Professional headshot"
    return f'<img class="headshot" src="{e(url)}" alt="{e(alt)}" />'


def render_social_proof_section(social_proof, theme):
    if not social_proof:
        return ""

    items = []
    followers = social_proof.get("followers") or {}
    for network, count in followers.items():
        items.append(e(f"{count} followers on {network}"))
    for talk in social_proof.get("speaking") or []:
        items.append(e(talk))
    for press in social_proof.get("press") or []:
        outlet = press.get("outlet", "")
        title = press.get("title", "")
        label = " - ".join(filter(None, [outlet, title]))
        if press.get("link"):
            label = f'<a href="{e(press["link"])}" target="_blank" rel="noopener">{e(label or press["link"])}</a>'
        else:
            label = e(label)
        items.append(label)

    if not items:
        return ""

    heading_num = '<span class="num">05</span>' if theme == "creative-bold" else ""
    rendered = "".join(f"<li>{item}</li>" for item in items)
    return f"""
<section>
  <h2>{heading_num}Proof</h2>
  <ul class="proof-list">{rendered}</ul>
</section>
"""


def render_portfolio(profile, theme, template_path):
    template = Path(template_path).read_text(encoding="utf-8")

    identity = profile.get("identity", {})
    links = profile.get("links", {})
    name = identity.get("name", "")
    name_parts = name.split(" ", 1)
    name_first = name_parts[0] if name_parts else ""
    name_last = name_parts[1] if len(name_parts) > 1 else ""
    name_handle = re.sub(r"[^a-zA-Z0-9]", "", name).lower() or "portfolio"

    cta_github = cta("GitHub", links.get("github"))
    cta_linkedin = cta("LinkedIn", links.get("linkedin"))
    email = links.get("email", "")
    cta_email = cta("Email", f"mailto:{email}") if email else ""
    location = identity.get("location", "")

    replacements = {
        "{{ name }}": e(name) or "<!-- ADD: full name -->",
        "{{ name_first }}": e(name_first),
        "{{ name_last }}": e(name_last),
        "{{ name_handle }}": e(name_handle),
        "{{ title }}": e(identity.get("title", "")) or "<!-- ADD: professional title -->",
        "{{ location }}": e(location) or "<!-- ADD: location -->",
        "{{ value_prop }}": e(identity.get("value_prop", "") or identity.get("headline", "")) or "<!-- ADD: 1-2 sentence value proposition -->",
        "{{ bio }}": e(identity.get("bio", "")) or "<!-- ADD: 3-4 sentence about-me bio -->",
        "{{ email }}": e(email) or "<!-- ADD: contact email -->",
        "{{ headshot }}": render_headshot(identity),
        "{{ cta_github }}": cta_github,
        "{{ cta_linkedin }}": cta_linkedin,
        "{{ cta_email }}": cta_email,
        "{{ experience_items }}": render_experience_items(profile.get("experience", []), theme),
        "{{ skills_blocks }}": render_skills_blocks(profile.get("skills", {}), theme),
        "{{ project_cards }}": render_project_cards(profile.get("projects", []), theme),
        "{{ social_proof_section }}": render_social_proof_section(profile.get("social_proof", {}), theme),
        "{{ writing_section }}": render_writing_section(profile.get("writing", []), theme),
        "{{ footer_links }}": render_footer_links(links),
    }

    out = template
    for token, value in replacements.items():
        out = out.replace(token, value)
    unreplaced = sorted(set(re.findall(r"{{\s*[^}]+\s*}}", out)))
    if unreplaced:
        raise ValueError(f"Unreplaced template tokens: {', '.join(unreplaced)}")
    return out


# ---------- resume rendering ----------

def render_resume(profile):
    identity = profile.get("identity", {})
    links = profile.get("links", {})

    name = identity.get("name", "<!-- ADD: name -->")
    title = identity.get("title", "")
    location = identity.get("location", "")

    # Header line
    contact_parts = []
    if links.get("email"):
        contact_parts.append(links["email"])
    if links.get("github"):
        contact_parts.append(links["github"])
    if links.get("linkedin"):
        contact_parts.append(links["linkedin"])
    if links.get("website"):
        contact_parts.append(links["website"])
    if links.get("twitter"):
        contact_parts.append(links["twitter"])
    if links.get("youtube"):
        contact_parts.append(links["youtube"])
    if links.get("medium"):
        contact_parts.append(links["medium"])
    for other in links.get("other", []) or []:
        if other.get("url"):
            contact_parts.append(other["url"])

    lines = []
    lines.append(f"# {name}")
    lines.append("")
    header_meta = " · ".join(filter(None, [f"**{title}**" if title else "", location]))
    lines.append(header_meta if header_meta else "<!-- ADD: title and location -->")
    if contact_parts:
        lines.append(" · ".join(contact_parts))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    bio = identity.get("bio") or identity.get("value_prop") or "<!-- ADD: 2-3 sentence summary -->"
    lines.append(bio)
    lines.append("")
    lines.append("---")
    lines.append("")

    # Experience
    lines.append("## Experience")
    lines.append("")
    for role in profile.get("experience", []) or []:
        company = role.get("company", "")
        rtitle = role.get("title", "")
        dates = role.get("dates", "")
        loc = role.get("location", "")
        lines.append(f"### {company} — {rtitle}")
        meta = " · ".join(filter(None, [dates, loc]))
        if meta:
            lines.append(f"*{meta}*")
        lines.append("")
        achievements = role.get("achievements") or []
        if achievements:
            for a in achievements:
                lines.append(f"- {a}")
        else:
            lines.append("- <!-- ADD: 3-5 achievement bullets, lead with action verb, quantify if possible -->")
        tech = role.get("tech") or []
        if tech:
            lines.append("")
            lines.append(f"**Tech:** {', '.join(tech)}")
        lines.append("")
    if not profile.get("experience"):
        lines.append("<!-- ADD: experience -->")
        lines.append("")
    lines.append("---")
    lines.append("")

    # Skills
    skills = profile.get("skills") or {}
    if skills:
        lines.append("## Skills")
        lines.append("")
        if skills.get("technical"):
            lines.append(f"**Languages & Frameworks:** {', '.join(skills['technical'])}")
        if skills.get("domain"):
            lines.append(f"**Domain:** {', '.join(skills['domain'])}")
        if skills.get("soft"):
            lines.append(f"**Soft:** {', '.join(skills['soft'])}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Projects
    projects = profile.get("projects") or []
    if projects:
        lines.append("## Projects")
        lines.append("")
        ordered_projects = sorted(projects, key=lambda p: not bool(p.get("highlight")))
        for p in ordered_projects:
            link = p.get("link") or p.get("repo") or ""
            heading = f"### {p.get('name', '')}"
            if link:
                heading = f"### {p.get('name', '')} — [{display_url(link)}]({link})"
            lines.append(heading)
            if p.get("description"):
                lines.append(p["description"])
            if p.get("tech"):
                lines.append(f"*Tech: {', '.join(p['tech'])}*")
            lines.append("")
        lines.append("---")
        lines.append("")

    # Education
    education = profile.get("education") or []
    if education:
        lines.append("## Education")
        lines.append("")
        for ed in education:
            line = f"**{ed.get('degree', '')}** · {ed.get('institution', '')} · {ed.get('year', '')}"
            lines.append(line)
            if ed.get("details"):
                lines.append(ed["details"])
            lines.append("")
        lines.append("---")
        lines.append("")

    # Certifications
    certs = profile.get("certifications") or []
    if certs:
        lines.append("## Certifications")
        lines.append("")
        for c in certs:
            lines.append(f"- {c.get('name', '')} — {c.get('issuer', '')}, {c.get('year', '')}")
        lines.append("")

    social_proof = profile.get("social_proof") or {}
    proof_lines = []
    for network, count in (social_proof.get("followers") or {}).items():
        proof_lines.append(f"{count} followers on {network}")
    proof_lines.extend(social_proof.get("speaking") or [])
    for press in social_proof.get("press") or []:
        proof_lines.append(" - ".join(filter(None, [press.get("outlet", ""), press.get("title", "")])))
    if proof_lines:
        lines.append("## Social Proof")
        lines.append("")
        for item in proof_lines:
            lines.append(f"- {item}")
        lines.append("")

    return "\n".join(lines)


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True, help="Path to profile JSON file")
    ap.add_argument("--theme", required=True, choices=sorted(THEMES))
    ap.add_argument("--out-dir", required=True, help="Output directory")
    args = ap.parse_args()

    profile_path = Path(args.profile)
    if not profile_path.exists():
        print(f"Profile not found: {profile_path}", file=sys.stderr)
        sys.exit(1)

    profile = json.loads(profile_path.read_text(encoding="utf-8"))

    # Locate the theme template relative to this script's parent (skill root)
    skill_root = Path(__file__).resolve().parent.parent
    template_path = skill_root / "assets" / "themes" / f"{args.theme}.html"
    if not template_path.exists():
        print(f"Theme template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    portfolio_html = render_portfolio(profile, args.theme, template_path)
    resume_md = render_resume(profile)

    (out_dir / "portfolio.html").write_text(portfolio_html, encoding="utf-8")
    (out_dir / "resume.md").write_text(resume_md, encoding="utf-8")

    print(f"Wrote {out_dir / 'portfolio.html'}")
    print(f"Wrote {out_dir / 'resume.md'}")


if __name__ == "__main__":
    main()
