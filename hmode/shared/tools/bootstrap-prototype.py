#!/usr/bin/env python3
"""
Bootstrap new prototypes following SDLC Phase 1 (SEED).

Creates planning documents only - no code until Phase 8+.
"""
# File UUID: a7f3b2c1-4d5e-6f7a-8b9c-0d1e2f3a4b5c

import argparse
import os
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path


def find_next_proto_number(base_dir: Path) -> int:
    """Find the next available prototype number."""
    proto_dirs = list(base_dir.glob("**/proto-[0-9]*"))

    if not proto_dirs:
        return 1

    numbers = []
    for path in proto_dirs:
        match = re.search(r'proto-(\d+)', path.name)
        if match:
            numbers.append(int(match.group(1)))

    return max(numbers) + 1 if numbers else 1


def generate_project_id(name: str, proto_num: int) -> str:
    """Generate project ID from name and number."""
    # Slugify name
    slug = name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug).strip('-')

    return f"proto-{proto_num:03d}-{slug}"


def generate_uuid() -> str:
    """Generate 8-char hex UUID."""
    return uuid.uuid4().hex[:8]


def infer_persona(purpose: str) -> str:
    """Infer target persona from purpose."""
    purpose_lower = purpose.lower()

    # Simple keyword-based inference
    if any(word in purpose_lower for word in ['coffee', 'starbucks', 'cafe', 'drink', 'order']):
        return "Coffee enthusiasts who want quick mobile ordering"
    elif any(word in purpose_lower for word in ['track', 'fitness', 'exercise', 'workout']):
        return "Fitness enthusiasts tracking their progress"
    elif any(word in purpose_lower for word in ['developer', 'code', 'programming', 'debug']):
        return "Software developers seeking productivity tools"
    elif any(word in purpose_lower for word in ['meal', 'food', 'nutrition', 'diet']):
        return "Health-conscious individuals tracking nutrition"
    elif any(word in purpose_lower for word in ['project', 'task', 'todo', 'manage']):
        return "Project managers coordinating team work"
    else:
        return "Users seeking to solve a specific problem efficiently"


def create_project_file(
    path: Path,
    name: str,
    project_id: str,
    project_uuid: str,
    description: str,
    purpose: str,
    classification: str,
) -> None:
    """Create .project YAML file."""
    today = datetime.now().strftime("%Y-%m-%d")

    content = f"""name: {name}
id: {project_id}
uuid: {project_uuid}
type: prototype
status: active
current_phase: 1
phase_name: SEED

description: {description}

purpose: |
  {purpose}

created: {today}
last_updated: {today}

classification: {classification}

tech_preferences: []
architecture_preferences: []

phases_completed: []
phases_in_progress:
  - phase: 1
    name: SEED
    started: {today}
    status: in_progress

notes: |
  - Starting with SDLC Phase 1 (SEED)
  - Need to define persona (WHO)
  - Will research existing solutions in Phase 2
"""

    path.write_text(content)


def create_readme(
    path: Path,
    name: str,
    project_id: str,
    purpose: str,
    persona: str,
) -> None:
    """Create README.md."""
    content = f"""# {name}

**Project ID:** {project_id}
**Phase:** 1 (SEED) - Concept Definition
**Status:** Active

## Overview

{purpose}

## Target User

**Persona:** {persona}

## Current Phase

**Phase 1: SEED** - Answering the 5 core questions:
1. What's the idea?
2. For who? (Persona)
3. What are they trying to do? (Intent)
4. How could they do it? (Solutions)
5. What needs to be built?

See `docs/PHASE-1-SEED.md` for details.

## Next Steps

1. Review and refine persona definition
2. Clarify user intent and goals
3. Move to Phase 2 (RESEARCH) to investigate existing solutions
4. **NO CODE YET** - Code comes in Phase 8+

## SDLC Progress

- [x] Phase 1: SEED (Current)
- [ ] Phase 2: RESEARCH
- [ ] Phase 3: EXPANSION
- [ ] Phase 4: ANALYSIS
- [ ] Phase 5: SELECTION
- [ ] Phase 6: DESIGN
- [ ] Phase 7: TEST
- [ ] Phase 8: IMPLEMENTATION
- [ ] Phase 9: REFINEMENT

---

**Note:** This prototype follows the 9-phase SDLC. No implementation code until Phase 8+.
"""

    path.write_text(content)


def create_phase1_doc(
    path: Path,
    name: str,
    purpose: str,
    persona: str,
) -> None:
    """Create docs/PHASE-1-SEED.md."""
    today = datetime.now().strftime("%Y-%m-%d")

    content = f"""# Phase 1: SEED

**Date:** {today}
**Status:** In Progress

## 1.0 The Core Idea

{purpose}

## 2.0 For Who? (Persona - REQUIRED)

**Target User:** {persona}

### Questions to Clarify

1. What is their current situation?
2. What are their pain points?
3. What is their technical comfort level?
4. What devices do they primarily use?
5. What is their context of use? (on-the-go, at desk, etc.)

## 3.0 What Are They Trying to Do? (Intent)

**Primary Intent:** [To be defined based on persona clarification]

### Sub-Goals

1. [To be defined]
2. [To be defined]
3. [To be defined]

## 4.0 How Could They Do It? (Solutions)

**Current Solutions:** [To be researched in Phase 2]

### Questions for Research

1. What existing solutions are available?
2. What are their strengths and weaknesses?
3. What gaps exist in current solutions?
4. What do users complain about most?

## 5.0 What Needs to Be Built?

**Requirements:** [To be defined after persona/intent clarification and research]

### Initial Thoughts

- [Add initial feature ideas]
- [Add technical considerations]
- [Add constraints or requirements]

---

## Next Actions

1. **Refine persona definition** - Interview or research target users
2. **Clarify intent and goals** - What are they really trying to accomplish?
3. **Move to Phase 2 (RESEARCH)** - Investigate existing solutions
4. **Document findings** - Create PHASE-2-RESEARCH.md

---

## Notes

- ⚠️ **NO CODE YET** - This is planning phase
- 🎯 Tech stack will be chosen in Phase 5 (SELECTION)
- 📋 Implementation happens in Phase 8+
"""

    path.write_text(content)


def main():
    parser = argparse.ArgumentParser(
        description="Bootstrap new prototype at Phase 1 (SEED)"
    )
    parser.add_argument("name", help="Prototype name (e.g., 'meal-tracker')")
    parser.add_argument("purpose", help="Brief purpose statement")
    parser.add_argument(
        "--classification",
        choices=["personal", "work", "shared", "oss", "unspecified"],
        default="personal",
        help="Project classification (default: personal)",
    )
    parser.add_argument(
        "--description",
        help="Brief description (default: same as purpose)",
    )

    args = parser.parse_args()

    # Setup paths
    repo_root = Path(__file__).parent.parent.parent
    projects_dir = repo_root / "projects" / args.classification

    # Find next proto number
    proto_num = find_next_proto_number(repo_root / "projects")

    # Generate identifiers
    project_id = generate_project_id(args.name, proto_num)
    project_uuid = generate_uuid()
    description = args.description or args.purpose

    # Infer persona
    persona = infer_persona(args.purpose)

    # Create directory structure
    proto_dir = projects_dir / project_id
    docs_dir = proto_dir / "docs"

    if proto_dir.exists():
        print(f"❌ Error: {proto_dir} already exists")
        sys.exit(1)

    docs_dir.mkdir(parents=True, exist_ok=True)

    # Create files
    create_project_file(
        proto_dir / ".project",
        args.name,
        project_id,
        project_uuid,
        description,
        args.purpose,
        args.classification,
    )

    create_readme(
        proto_dir / "README.md",
        args.name,
        project_id,
        args.purpose,
        persona,
    )

    create_phase1_doc(
        docs_dir / "PHASE-1-SEED.md",
        args.name,
        args.purpose,
        persona,
    )

    # Print summary
    print("✅ Created Prototype")
    print(f"📍 Phase 1 (SEED) - Concept Definition")
    print()
    print(f"📁 Location: {proto_dir.relative_to(repo_root)}")
    print(f"🎯 Purpose: {args.purpose}")
    print(f"👤 Target User: {persona}")
    print(f"🔖 Project ID: {project_id}")
    print(f"🆔 UUID: {project_uuid}")
    print()
    print("Files created:")
    print("- .project (Phase 1 tracking)")
    print("- README.md (Project overview)")
    print("- docs/PHASE-1-SEED.md (5 SDLC questions)")
    print()
    print("⚠️ No code yet - complete SDLC phases first")
    print("🔄 Tech stack will be chosen in Phase 5 (SELECTION)")
    print()
    print("=" * 70)
    print("⚠️  PERSONA CONFIRMATION REQUIRED BEFORE PHASE 2")
    print("=" * 70)
    print()
    print(f"I inferred the target user as: {persona}")
    print()
    print("Please confirm this persona is correct before moving to Phase 2 (RESEARCH).")
    print()
    print("Next steps:")
    print(f"1. cd {proto_dir.relative_to(repo_root)}")
    print("2. Review docs/PHASE-1-SEED.md")
    print("3. CONFIRM OR ADJUST the target persona")
    print("4. Only then move to Phase 2 (RESEARCH)")
    print()
    print("💡 Tip: Ask Claude to confirm before proceeding to Phase 2")


if __name__ == "__main__":
    main()
