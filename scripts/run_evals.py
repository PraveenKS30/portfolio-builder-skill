#!/usr/bin/env python3
"""Run lightweight renderer checks for the portfolio-builder skill."""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RENDERER = ROOT / "scripts" / "render_portfolio.py"
TMP_ROOT = Path("C:/tmp") if Path("C:/tmp").exists() else ROOT


CASES = [
    {
        "id": "maya-dark-tech",
        "theme": "dark-tech",
        "profile": {
            "identity": {
                "name": "Maya Chen",
                "title": "Staff ML Engineer",
                "location": "San Francisco, CA",
                "value_prop": "I build ML systems that ship - and keep shipping at scale.",
                "bio": "Staff ML engineer focused on real-time inference platforms and reliable training systems.",
            },
            "links": {
                "email": "maya@mayachen.dev",
                "github": "https://github.com/mayachen-ml",
                "linkedin": "https://linkedin.com/in/mayachen-ml",
            },
            "experience": [
                {
                    "company": "Vega AI",
                    "title": "Staff ML Engineer",
                    "dates": "Aug 2022 - Present",
                    "location": "San Francisco, CA",
                    "achievements": [
                        "Built and shipped a real-time feature platform serving 12B daily inferences across recommendations, search, and ads. Cut p99 latency from 280ms to 65ms."
                    ],
                    "tech": ["Python", "PyTorch", "Ray", "Kubernetes"],
                },
                {
                    "company": "Stripe",
                    "title": "Senior ML Engineer",
                    "dates": "2019 - 2022",
                    "achievements": ["Built fraud detection models that prevented an estimated $40M in losses annually"],
                },
                {
                    "company": "Lyft",
                    "title": "ML Engineer",
                    "dates": "2017 - 2019",
                    "achievements": ["Worked on ETA prediction models"],
                },
            ],
            "projects": [
                {
                    "name": "pyvecindex",
                    "description": "Fast vector index for Python, 800 stars on GitHub",
                    "repo": "https://github.com/mayachen-ml/pyvecindex",
                    "highlight": True,
                }
            ],
        },
        "must_contain": ["Maya Chen", "Staff ML Engineer", "$40M in losses annually", "pyvecindex"],
        "must_not_contain": ["Remote", "500+ GitHub stars"],
    },
    {
        "id": "jordan-creative-bold",
        "theme": "creative-bold",
        "profile": {
            "identity": {
                "name": "Jordan Park",
                "title": "Senior Product Designer",
                "location": "Brooklyn, NY",
                "bio": "Product designer focused on AI writing surfaces and collaborative tools.",
            },
            "links": {
                "email": "hi@jordanpark.design",
                "website": "https://jordanpark.design",
                "twitter": "https://twitter.com/jordandesigns",
                "other": [{"label": "Behance", "url": "https://behance.net/jordanpark"}],
            },
            "experience": [
                {
                    "company": "Notion",
                    "title": "Senior Product Designer",
                    "dates": "2023 - Present",
                    "achievements": ["Bumped activation rate of new AI users from 12% to 31%."],
                }
            ],
            "social_proof": {"followers": {"twitter": "18k"}},
        },
        "must_contain": ["Jordan Park", "12% to 31%", "behance.net/jordanpark", "18k followers on twitter"],
        "must_not_contain": ["github"],
    },
    {
        "id": "sam-default-dev",
        "theme": "dark-tech",
        "profile": {
            "identity": {
                "name": "Sam Rivera",
                "title": "Junior Developer",
                "location": "Austin, TX",
                "headline": "Frontend developer building practical tools for educators and teams.",
            },
            "links": {"email": "sam@samrivera.dev", "github": "https://github.com/samrivera"},
            "education": [{"degree": "B.S. Computer Science", "institution": "UT Austin", "year": "2024"}],
            "projects": [
                {
                    "name": "QuizForge",
                    "description": "SaaS tool that helps teachers generate quiz questions from lesson plans. Has 40 paying customers.",
                    "tech": ["GPT-4", "React", "Next.js"],
                    "link": "https://quizforge.app",
                    "highlight": True,
                },
                {
                    "name": "imgcli",
                    "description": "CLI tool for resizing images with a few hundred users.",
                    "repo": "https://github.com/samrivera/imgcli",
                },
            ],
        },
        "must_contain": ["Sam Rivera", "QuizForge", "40 paying customers", "imgcli"],
        "must_not_contain": ["LinkedIn"],
    },
]


def run_case(case):
    tmp = Path(tempfile.mkdtemp(prefix=f"portfolio-eval-{case['id']}-", dir=TMP_ROOT))
    try:
        profile_path = tmp / "profile.json"
        profile_path.write_text(json.dumps(case["profile"], indent=2), encoding="utf-8")
        subprocess.run(
            [
                sys.executable,
                str(RENDERER),
                "--profile",
                str(profile_path),
                "--theme",
                case["theme"],
                "--out-dir",
                str(tmp),
            ],
            check=True,
            cwd=str(ROOT),
            stdout=subprocess.DEVNULL,
        )
        output = (tmp / "portfolio.html").read_text(encoding="utf-8")
        output += "\n" + (tmp / "resume.md").read_text(encoding="utf-8")
        failures = []
        for expected in case["must_contain"]:
            if expected not in output:
                failures.append(f"missing {expected!r}")
        for forbidden in case["must_not_contain"]:
            if forbidden in output:
                failures.append(f"unexpected {forbidden!r}")
        if "{{" in output or "}}" in output:
            failures.append("unreplaced template token")
        return failures
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    failed = False
    for case in CASES:
        failures = run_case(case)
        if failures:
            failed = True
            print(f"FAIL {case['id']}: " + "; ".join(failures))
        else:
            print(f"PASS {case['id']}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
