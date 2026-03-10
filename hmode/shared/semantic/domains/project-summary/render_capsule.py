#!/usr/bin/env python3
"""
Capsule HTML Renderer - 10 Layout Variants
shadcn-inspired, clean white backgrounds.
"""

import yaml
import sys
from pathlib import Path
from datetime import datetime

LAYOUTS = {
    "a1b2c3d4": "minimal",      # Just name + tagline + benefit
    "e5f6g7h8": "card",         # Bordered card with sections
    "i9j0k1l2": "split",        # Two column layout
    "m3n4o5p6": "timeline",     # Vertical timeline style
    "q7r8s9t0": "magazine",     # Editorial style
    "u1v2w3x4": "dashboard",    # Metrics-focused
    "y5z6a7b8": "pitch",        # Investor pitch style
    "c9d0e1f2": "notion",       # Notion-like blocks
    "g3h4i5j6": "terminal",     # Developer/CLI aesthetic
    "k7l8m9n0": "poster",       # Bold poster style
}


def load_capsule(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def get_status_color(indicator: str) -> str:
    return {"green": "#22c55e", "yellow": "#eab308", "red": "#ef4444", "blue": "#3b82f6", "gray": "#9ca3af"}.get(indicator, "#9ca3af")


def render_all_layouts(capsule: dict, project_name: str) -> dict:
    """Render capsule in all 10 layout variants."""
    c = capsule
    core = c.get("core_benefit", "").strip()
    customer = c.get("customer", "")
    problem = c.get("problem", "").strip()
    alts = c.get("alternatives", [])
    solution = c.get("solution", "").strip()
    uvp = c.get("uvp", "")
    status = c.get("status", {})
    next_step = c.get("next_step", "")
    color = get_status_color(status.get("indicator", "gray"))
    label = status.get("label", "")
    pct = status.get("percent", 0)
    alt_names = " · ".join([a.get("name", "") for a in alts[:3]])

    base = f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{project_name}</title><style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;background:#fff;color:#0a0a0a;padding:2rem;line-height:1.5}}.c{{max-width:600px;margin:0 auto}}'''

    layouts = {}

    # a1b2c3d4 - minimal
    layouts["a1b2c3d4"] = base + f'''.n{{font-size:2rem;font-weight:600;letter-spacing:-.02em}}.t{{color:#737373;margin:.5rem 0 1.5rem}}.b{{color:#525252;font-size:1.05rem}}</style></head><body><div class="c"><h1 class="n">{project_name}</h1><p class="t">{uvp}</p><p class="b">{core}</p></div></body></html>'''

    # e5f6g7h8 - card
    layouts["e5f6g7h8"] = base + f'''.card{{border:1px solid #e5e5e5;border-radius:8px;padding:1.5rem}}.n{{font-size:1.5rem;font-weight:600}}.t{{color:#737373;font-size:.9rem;margin:.25rem 0 1rem}}.s{{display:flex;align-items:center;gap:.5rem;font-size:.8rem;color:#737373;margin-bottom:1rem}}.dot{{width:8px;height:8px;border-radius:50%;background:{color}}}.sec{{padding:1rem 0;border-top:1px solid #f5f5f5}}.l{{font-size:.7rem;color:#a3a3a3;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.25rem}}</style></head><body><div class="c"><div class="card"><h1 class="n">{project_name}</h1><p class="t">{uvp}</p><div class="s"><span class="dot"></span>{label} · {pct}%</div><div class="sec"><div class="l">Core Benefit</div>{core}</div><div class="sec"><div class="l">Next</div>{next_step}</div></div></div></body></html>'''

    # i9j0k1l2 - split
    layouts["i9j0k1l2"] = base + f'''.grid{{display:grid;grid-template-columns:1fr 1fr;gap:2rem}}@media(max-width:640px){{.grid{{grid-template-columns:1fr}}}}.n{{font-size:1.75rem;font-weight:600;margin-bottom:.5rem}}.t{{color:#737373}}.l{{font-size:.7rem;color:#a3a3a3;text-transform:uppercase;margin-bottom:.25rem}}.left{{border-right:1px solid #e5e5e5;padding-right:2rem}}@media(max-width:640px){{.left{{border:0;padding:0}}}}</style></head><body><div class="c"><div class="grid"><div class="left"><h1 class="n">{project_name}</h1><p class="t">{uvp}</p></div><div><div class="l">Core Benefit</div><p>{core}</p><br><div class="l">Next Step</div><p>{next_step}</p></div></div></div></body></html>'''

    # m3n4o5p6 - timeline
    layouts["m3n4o5p6"] = base + f'''.n{{font-size:1.5rem;font-weight:600}}.t{{color:#737373;margin:.25rem 0 1.5rem}}.item{{display:flex;gap:1rem;padding:1rem 0}}.line{{width:2px;background:#e5e5e5;position:relative}}.dot{{width:10px;height:10px;border-radius:50%;background:{color};position:absolute;left:-4px}}.l{{font-size:.7rem;color:#a3a3a3;text-transform:uppercase}}</style></head><body><div class="c"><h1 class="n">{project_name}</h1><p class="t">{uvp}</p><div class="item"><div class="line"><div class="dot"></div></div><div><div class="l">Benefit</div>{core}</div></div><div class="item"><div class="line"><div class="dot" style="background:#e5e5e5"></div></div><div><div class="l">Next</div>{next_step}</div></div></div></body></html>'''

    # q7r8s9t0 - magazine
    layouts["q7r8s9t0"] = base.replace("ui-sans-serif,system-ui,-apple-system,sans-serif", "Georgia,serif") + f'''.n{{font-size:2.5rem;font-weight:400;letter-spacing:-.02em}}.t{{font-size:1.2rem;color:#525252;margin:.5rem 0 2rem;font-style:italic}}.b{{font-size:1.1rem;line-height:1.7}}.f{{margin-top:2rem;padding-top:1rem;border-top:1px solid #e5e5e5;font-size:.75rem;color:#a3a3a3}}</style></head><body><div class="c"><h1 class="n">{project_name}</h1><p class="t">{uvp}</p><p class="b">{core}</p><div class="f">{label} · {pct}%</div></div></body></html>'''

    # u1v2w3x4 - dashboard
    layouts["u1v2w3x4"] = base + f'''.n{{font-size:1.25rem;font-weight:600}}.t{{color:#737373;font-size:.85rem}}.metrics{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1.5rem 0}}.m{{background:#fafafa;padding:1rem;border-radius:6px;text-align:center}}.mv{{font-size:1.5rem;font-weight:600;color:{color}}}.ml{{font-size:.7rem;color:#a3a3a3;text-transform:uppercase}}.sec{{background:#fafafa;padding:1rem;border-radius:6px;margin-top:1rem}}</style></head><body><div class="c"><h1 class="n">{project_name}</h1><p class="t">{uvp}</p><div class="metrics"><div class="m"><div class="mv">{pct}%</div><div class="ml">Progress</div></div><div class="m"><div class="mv">{len(alts)}</div><div class="ml">Alternatives</div></div><div class="m"><div class="mv" style="font-size:1rem">{label}</div><div class="ml">Status</div></div></div><div class="sec">{core}</div></div></body></html>'''

    # y5z6a7b8 - pitch
    layouts["y5z6a7b8"] = base + f'''.n{{font-size:2rem;font-weight:700;text-align:center}}.t{{text-align:center;color:#737373;margin:.5rem 0 2rem}}.box{{background:#fafafa;border-radius:8px;padding:1.5rem;margin:1rem 0}}.l{{font-size:.65rem;color:{color};text-transform:uppercase;letter-spacing:.1em;font-weight:600;margin-bottom:.5rem}}</style></head><body><div class="c"><h1 class="n">{project_name}</h1><p class="t">{uvp}</p><div class="box"><div class="l">The Problem</div>{problem}</div><div class="box"><div class="l">Our Solution</div>{core}</div><div class="box"><div class="l">Next Step</div>{next_step}</div></div></body></html>'''

    # c9d0e1f2 - notion
    layouts["c9d0e1f2"] = base + f'''.n{{font-size:2rem;font-weight:700}}.t{{color:#737373;margin-bottom:1.5rem}}.block{{padding:.75rem 1rem;margin:.5rem 0;border-radius:4px;background:#fafafa}}.block:hover{{background:#f5f5f5}}.l{{font-size:.7rem;color:#a3a3a3;margin-bottom:.25rem}}.tag{{display:inline-block;background:#e5e5e5;padding:.15rem .5rem;border-radius:4px;font-size:.75rem;margin-right:.25rem}}</style></head><body><div class="c"><h1 class="n">{project_name}</h1><p class="t">{uvp}</p><div class="block"><div class="l">Status</div><span class="tag" style="background:{color}20;color:{color}">{label}</span><span class="tag">{pct}%</span></div><div class="block"><div class="l">Core Benefit</div>{core}</div><div class="block"><div class="l">Next Step</div>{next_step}</div><div class="block"><div class="l">Customer</div>{customer}</div></div></body></html>'''

    # g3h4i5j6 - terminal
    layouts["g3h4i5j6"] = f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{project_name}</title><style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:ui-monospace,monospace;background:#fafafa;color:#0a0a0a;padding:2rem}}.c{{max-width:600px;margin:0 auto;background:#fff;border:1px solid #e5e5e5;border-radius:8px;overflow:hidden}}.bar{{background:#f5f5f5;padding:.5rem 1rem;border-bottom:1px solid #e5e5e5;font-size:.75rem;color:#737373}}.term{{padding:1.5rem;font-size:.9rem}}.cmd{{color:#737373}}.out{{margin:.5rem 0 1rem 1rem}}.g{{color:{color}}}</style></head><body><div class="c"><div class="bar">capsule — {project_name.lower().replace(" ","-")}</div><div class="term"><div class="cmd">$ cat project.info</div><div class="out"><strong>{project_name}</strong><br>{uvp}</div><div class="cmd">$ echo $CORE_BENEFIT</div><div class="out">{core}</div><div class="cmd">$ echo $STATUS</div><div class="out"><span class="g">●</span> {label} ({pct}%)</div><div class="cmd">$ cat next_step.txt</div><div class="out">{next_step}</div></div></div></body></html>'''

    # k7l8m9n0 - poster
    layouts["k7l8m9n0"] = base + f'''.n{{font-size:3rem;font-weight:800;letter-spacing:-.03em;line-height:1.1}}.t{{font-size:1.5rem;color:#525252;margin:1rem 0 2rem}}.b{{font-size:1rem;color:#737373;max-width:400px}}.tag{{display:inline-block;background:{color};color:#fff;padding:.25rem .75rem;border-radius:4px;font-size:.8rem;font-weight:600;margin-top:2rem}}</style></head><body><div class="c"><h1 class="n">{project_name}</h1><p class="t">{uvp}</p><p class="b">{core}</p><span class="tag">{label}</span></div></body></html>'''

    return layouts


def main():
    if len(sys.argv) < 2:
        print("Usage: python render_capsule.py <capsule.yaml> [project_name]")
        sys.exit(1)

    capsule_path = Path(sys.argv[1])
    project_name = sys.argv[2] if len(sys.argv) > 2 else capsule_path.parent.name

    if not capsule_path.exists():
        print(f"Error: {capsule_path} not found")
        sys.exit(1)

    capsule = load_capsule(capsule_path)
    layouts = render_all_layouts(capsule, project_name)

    output_dir = capsule_path.parent
    for uuid, html in layouts.items():
        output_path = output_dir / f".capsule-{uuid}.html"
        with open(output_path, "w") as f:
            f.write(html)
        print(f"Generated: {output_path} ({LAYOUTS[uuid]})")


if __name__ == "__main__":
    main()
