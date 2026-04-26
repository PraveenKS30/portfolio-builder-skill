# Installing portfolio-builder

This folder is the complete portfolio-builder skill, ready to install.

## Option A — Install as a `.skill` file (recommended)

Run the included packager once to produce a `.skill` file that can be installed via the Claude UI:

```
python "C:\Users\c2pra\OneDrive\Documents\Claude\Projects\Personal Portfolio\package-portfolio-builder.py"
```

This produces `portfolio-builder.skill` in the same folder. Drag it into Claude (or use the install dialog) to install.

## Option B — Copy the folder into your skills directory

The skill is a normal folder with a `SKILL.md` and supporting files. Copy this entire `portfolio-builder-skill/` folder into your local skills directory and rename it to `portfolio-builder/`. The skill loader will pick it up.

## Using the skill

Once installed, just describe what you want:

- "Build me a portfolio website from this LinkedIn..."
- "Rewrite my resume from this background..."
- "Make a personal site with the dark-tech theme..."

You can pass any combination of: LinkedIn export, existing resume, GitHub username, social links, raw notes. The skill will run a gap analysis, confirm a theme with you (or pick one), and produce a single-file `portfolio.html` plus a Markdown `resume.md`.

## Themes

- **minimal-light** — clean serif headings, off-white background. Default for consultants, writers, PMs.
- **dark-tech** — terminal-inspired dark theme. Default for engineers and ML/infra.
- **creative-bold** — vibrant playful theme with display type. Default for designers and creatives.

## Updating

Tell the skill what changed ("just shipped X," "got a cert in Y," "got promoted to Z") and it'll merge the new info and re-render.
