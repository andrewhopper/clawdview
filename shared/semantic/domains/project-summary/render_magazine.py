#!/usr/bin/env python3
"""
Capsule Magazine Renderer - Split layout with title/tags left, content right.
"""

import yaml
import sys
from pathlib import Path
from datetime import datetime
import subprocess


def load_capsule(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def get_git_hash() -> str:
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], text=True).strip()
    except:
        return "unknown"


def get_status_color(indicator: str) -> str:
    return {"green": "#22c55e", "yellow": "#eab308", "red": "#ef4444", "blue": "#3b82f6", "gray": "#9ca3af"}.get(indicator, "#9ca3af")


def render_magazine(capsule: dict, project_name: str, project_id: str, slug: str = "") -> str:
    c = capsule
    meta = c.get("_meta", {})
    core = c.get("core_benefit", "").strip()
    customer = c.get("customer", "")
    early_adopter = c.get("early_adopter", "")
    problem = c.get("problem", "").strip()
    alts = c.get("alternatives", [])
    solution = c.get("solution", "").strip()
    features = c.get("features", [])
    innovations = c.get("innovations", [])
    uvp = c.get("uvp", "")
    concept = c.get("high_level_concept", "")
    status = c.get("status", {})
    tags = c.get("tags", [])

    capsule_uuid = str(meta.get("uuid", ""))[:8]
    git_hash = get_git_hash()
    today = datetime.now().strftime("%b %d, %Y")

    # Build tags HTML
    tags_html = "".join([f'<span class="tag">{t}</span>' for t in tags[:5]])

    # Build alternatives HTML
    alts_html = "".join([f'<li><span>{a.get("name","")}</span><span class="gap">{a.get("gap","")}</span></li>' for a in alts])

    # Build features HTML
    features_html = "".join([f'<li>{f}</li>' for f in features])

    # Get diagram if available
    diagram_html = DIAGRAMS.get(slug, "")

    # Build innovations HTML
    innovations_html = ""
    for inn in innovations:
        innovations_html += f'''<div class="innovation">
            <div class="inn-title">{inn.get("title","")}</div>
            <div class="inn-desc">{inn.get("description","")}</div>
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: ui-sans-serif, system-ui, -apple-system, sans-serif;
            background: #fff;
            color: #000;
            padding: 3rem;
            line-height: 1.6;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 25% 75%;
            gap: 3rem;
        }}
        .left {{
            border-right: 1px solid #e5e5e5;
            padding-right: 2rem;
        }}
        .name {{
            font-size: 2.25rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            line-height: 1.1;
        }}
        .tagline {{
            font-size: 0.9rem;
            color: #666;
            margin-top: 0.75rem;
            line-height: 1.4;
        }}
        .ids {{
            margin-top: 1.5rem;
            font-size: 0.6rem;
            color: #bbb;
            font-family: ui-monospace, monospace;
        }}
        .ids div {{ margin-bottom: 0.2rem; }}
        .id-label {{ color: #999; }}
        .tags {{
            margin-top: 1.5rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.35rem;
        }}
        .tag {{
            font-size: 0.65rem;
            background: #f5f5f5;
            color: #666;
            padding: 0.2rem 0.5rem;
            border-radius: 3px;
        }}
        .right {{ padding-left: 1rem; }}
        .section {{ margin-bottom: 1.5rem; }}
        .label {{
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #999;
            font-weight: 500;
            margin-bottom: 0.35rem;
        }}
        .content {{
            font-size: 0.95rem;
            color: #333;
        }}
        .concept {{
            color: #666;
            font-style: italic;
        }}
        .customer-box {{
            color: #1e40af;
        }}
        .early {{ color: #666; font-size: 0.85rem; margin-top: 0.25rem; }}
        .alt-list {{
            list-style: none;
        }}
        .alt-list li {{
            display: flex;
            justify-content: space-between;
            padding: 0.3rem 0;
            font-size: 0.9rem;
        }}
        .gap {{ color: #666; font-size: 0.8rem; }}
        .feature-list {{
            list-style: none;
        }}
        .feature-list li {{
            padding: 0.2rem 0;
            font-size: 0.9rem;
        }}
        .feature-list li::before {{
            content: "— ";
            color: #999;
        }}
        .innovation {{
            margin-bottom: 0.5rem;
        }}
        .inn-title {{
            font-weight: 600;
            font-size: 0.9rem;
        }}
        .inn-desc {{
            font-size: 0.85rem;
            color: #666;
        }}
        .footer {{
            margin-top: 2.5rem;
            padding-top: 1rem;
            border-top: 1px solid #e5e5e5;
            font-size: 0.6rem;
            color: #ccc;
            display: flex;
            justify-content: space-between;
            font-family: ui-monospace, monospace;
        }}
        .diagram {{
            width: 100%;
            max-width: 400px;
            height: auto;
            margin: 0.5rem 0;
        }}
        .diagram-section {{
            background: #fafafa;
            padding: 1rem;
            border-radius: 6px;
            margin-bottom: 1.5rem;
        }}
        @media (max-width: 700px) {{
            .container {{ grid-template-columns: 1fr; gap: 2rem; }}
            .left {{ border-right: none; padding-right: 0; border-bottom: 1px solid #e5e5e5; padding-bottom: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="left">
            <h1 class="name">{project_name}</h1>
            <p class="tagline">{uvp}</p>
            <div class="ids">
                <div><span class="id-label">project</span> {project_id}</div>
                <div><span class="id-label">capsule</span> {capsule_uuid}</div>
            </div>
            <div class="tags">{tags_html}</div>
        </div>

        <div class="right">
            <div class="section">
                <div class="label">Concept</div>
                <div class="content concept">{concept}</div>
            </div>

            <div class="section">
                <div class="label">Customer</div>
                <div class="content customer-box">{customer}</div>
                {f'<div class="early">Early adopter: {early_adopter}</div>' if early_adopter else ''}
            </div>

            <div class="section">
                <div class="label">Problem</div>
                <div class="content">{problem}</div>
            </div>

            <div class="section">
                <div class="label">Solution</div>
                <div class="content">
                    <p>{solution}</p>
                    {f'<ul class="feature-list" style="margin-top:0.5rem">{features_html}</ul>' if features else ''}
                </div>
            </div>

            {f'<div class="diagram-section"><div class="label">How It Works</div>{diagram_html}</div>' if diagram_html else ''}

            <div class="section">
                <div class="label">Alternatives</div>
                <ul class="alt-list">{alts_html}</ul>
            </div>

            {f'<div class="section"><div class="label">Innovation</div><div class="content">{innovations_html}</div></div>' if innovations else ''}

            <div class="section">
                <div class="label">Benefit</div>
                <div class="content">{core}</div>
            </div>

            <div class="footer">
                <span>{git_hash}</span>
                <span>{today}</span>
            </div>
        </div>
    </div>
</body>
</html>'''


DIAGRAMS = {
    "frontgate": '''<svg viewBox="0 0 400 120" class="diagram">
        <rect x="10" y="45" width="70" height="30" fill="#f5f5f5" stroke="#ccc"/>
        <text x="45" y="65" text-anchor="middle" font-size="10">New File</text>
        <path d="M80 60 L120 60" stroke="#ccc" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="120" y="35" width="80" height="50" fill="#fef3c7" stroke="#eab308"/>
        <text x="160" y="55" text-anchor="middle" font-size="10">Frontgate</text>
        <text x="160" y="70" text-anchor="middle" font-size="8" fill="#666">Check Rules</text>
        <path d="M200 45 L240 25" stroke="#22c55e" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M200 75 L240 95" stroke="#ef4444" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="240" y="10" width="70" height="30" fill="#dcfce7" stroke="#22c55e"/>
        <text x="275" y="30" text-anchor="middle" font-size="10">Correct Path</text>
        <rect x="240" y="80" width="70" height="30" fill="#fef2f2" stroke="#ef4444"/>
        <text x="275" y="100" text-anchor="middle" font-size="10">Quarantine</text>
        <text x="220" y="20" font-size="8" fill="#22c55e">match</text>
        <text x="220" y="100" font-size="8" fill="#ef4444">no rule</text>
        <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#999"/></marker></defs>
    </svg>''',
    "gocoder": '''<svg viewBox="0 0 400 100" class="diagram">
        <rect x="10" y="35" width="60" height="30" fill="#eff6ff" stroke="#3b82f6"/>
        <text x="40" y="55" text-anchor="middle" font-size="10">Browser</text>
        <path d="M70 50 L100 50" stroke="#ccc" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="100" y="35" width="70" height="30" fill="#f5f5f5" stroke="#ccc"/>
        <text x="135" y="55" text-anchor="middle" font-size="10">WebSocket</text>
        <path d="M170 50 L200 50" stroke="#ccc" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="200" y="25" width="80" height="50" fill="#fef3c7" stroke="#eab308"/>
        <text x="240" y="45" text-anchor="middle" font-size="10">Container</text>
        <text x="240" y="60" text-anchor="middle" font-size="8" fill="#666">per user</text>
        <path d="M280 50 L310 50" stroke="#ccc" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="310" y="35" width="80" height="30" fill="#f5f3ff" stroke="#8b5cf6"/>
        <text x="350" y="55" text-anchor="middle" font-size="10">Claude Code</text>
        <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#999"/></marker></defs>
    </svg>''',
    "tts-cli": '''<svg viewBox="0 0 400 80" class="diagram">
        <rect x="10" y="25" width="70" height="30" fill="#f5f5f5" stroke="#ccc"/>
        <text x="45" y="45" text-anchor="middle" font-size="10">text.md</text>
        <path d="M80 40 L120 40" stroke="#ccc" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="120" y="20" width="80" height="40" fill="#fef3c7" stroke="#eab308"/>
        <text x="160" y="38" text-anchor="middle" font-size="10">tts convert</text>
        <text x="160" y="50" text-anchor="middle" font-size="8" fill="#666">ElevenLabs</text>
        <path d="M200 40 L240 40" stroke="#ccc" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="240" y="25" width="70" height="30" fill="#dcfce7" stroke="#22c55e"/>
        <text x="275" y="45" text-anchor="middle" font-size="10">audio.mp3</text>
        <path d="M310 40 L340 40" stroke="#ccc" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="340" y="25" width="50" height="30" fill="#eff6ff" stroke="#3b82f6"/>
        <text x="365" y="45" text-anchor="middle" font-size="10">S3</text>
        <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#999"/></marker></defs>
    </svg>''',
    "dementia-companion": '''<svg viewBox="0 0 400 120" class="diagram">
        <rect x="160" y="10" width="80" height="35" fill="#f5f3ff" stroke="#8b5cf6"/>
        <text x="200" y="25" text-anchor="middle" font-size="10">Voice AI</text>
        <text x="200" y="38" text-anchor="middle" font-size="8" fill="#666">cloned voice</text>
        <path d="M160 30 L90 55" stroke="#ccc" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M240 30 L310 55" stroke="#ccc" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="20" y="55" width="70" height="50" fill="#fef3c7" stroke="#eab308"/>
        <text x="55" y="75" text-anchor="middle" font-size="10">Patient</text>
        <text x="55" y="90" text-anchor="middle" font-size="8" fill="#666">phone call</text>
        <rect x="310" y="55" width="70" height="50" fill="#dcfce7" stroke="#22c55e"/>
        <text x="345" y="75" text-anchor="middle" font-size="10">Caregiver</text>
        <text x="345" y="90" text-anchor="middle" font-size="8" fill="#666">dashboard</text>
        <path d="M200 45 L200 55" stroke="#ccc" stroke-width="1" stroke-dasharray="3"/>
        <text x="200" y="70" text-anchor="middle" font-size="8" fill="#999">daily insights</text>
        <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#999"/></marker></defs>
    </svg>''',
}

CAPSULES = [
    ("projects/personal/active/tool-gocoder-web-agentic-coding-ui-like-claude-code-web-t9x2k-189/.capsule.yaml", "GoCoder", "t9x2k-189"),
    ("projects/personal/active/dementia-companion-fqong-001/.capsule.yaml", "Dementia Companion", "fqong-001"),
    ("projects/shared/active/service-tts-api-7k9b2-051/.capsule.yaml", "TTS CLI", "7k9b2-051"),
    ("projects/oss/active/proto-diagram-craft-5cfd2-001/.capsule.yaml", "Diagram Craft", "5cfd2-001"),
    ("projects/oss/active/proto-frontgate-02d7f-001/.capsule.yaml", "Frontgate", "02d7f-001"),
]


def main():
    for capsule_path, name, pid in CAPSULES:
        path = Path(capsule_path)
        if path.exists():
            capsule = load_capsule(path)
            slug = name.lower().replace(" ", "-")
            html = render_magazine(capsule, name, pid, slug)
            out = Path(f"/tmp/capsule-{slug}.html")
            out.write_text(html)
            print(f"Generated: {out}")
        else:
            print(f"Not found: {path}")


if __name__ == "__main__":
    main()
