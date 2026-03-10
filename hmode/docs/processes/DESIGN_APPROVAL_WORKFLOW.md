# Design Approval Workflow
<!-- File UUID: 8f3a9c2d-4e7b-4f8a-9d2e-1c5a8b3f7d9e -->

## Overview

Enforced multi-gate design workflow for Phase 6 (Design) ensuring human approval at critical checkpoints.

**Flow:**
```
Sitemap (IA Agent) → Approval Gate 1 → Lo-Fi Mocks (UX Agent) → Approval Gate 2 → Hi-Fi Mocks (UX Agent)
```

**When to Use:**
- Phase 6 (Design) of SDLC
- Production projects requiring formal design review
- Projects with external stakeholders

**When NOT to Use:**
- SPIKE mode (throwaway prototypes)
- Internal tools with no design requirements
- Prototype/exploration projects (unless requested)

---

## 1.0 WORKFLOW STAGES

### Stage 1: Information Architecture (Sitemap)

**Trigger:** Entering Phase 6 with design approval workflow enabled

**Process:**
1. Spawn `information-architecture-agent` with design brief
2. Agent outputs:
   - Navigation hierarchy (YAML or diagram)
   - User flow diagrams (Mermaid)
   - Sitemap with page relationships
   - Content groupings
3. Save output to `docs/design/01-information-architecture.md`
4. **MANDATORY:** Proceed to Approval Gate 1

**No Skipping:** IA must be approved before lo-fi mocks begin.

---

### Stage 2: Approval Gate 1 - IA Review

**Trigger:** IA artifacts generated

**Process:**
1. Present IA deliverables to stakeholder:
   ```
   ═══════════════════════════════════════════════════════════
     APPROVAL GATE 1: INFORMATION ARCHITECTURE
   ═══════════════════════════════════════════════════════════

   Generated Artifacts:
   [1] docs/design/01-information-architecture.md
   [2] Navigation hierarchy diagram
   [3] User flow diagrams

   Review Status: PENDING
   ```

2. Invoke approval tool:
   ```
   /approval request
   ```

3. Wait for human approval decision:
   - **APPROVED** → Proceed to Stage 3
   - **REJECTED** → Return to Stage 1 with feedback
   - **CHANGES REQUESTED** → Modify IA, re-submit to Gate 1

**Exit Criteria:**
- ✅ Navigation structure approved
- ✅ User flows approved
- ✅ Sitemap signed off
- ✅ Content hierarchy confirmed

**Enforcement:**
- Stage 3 CANNOT begin until Gate 1 status = APPROVED
- All IA changes must be re-approved

---

### Stage 3: Lo-Fi Mockups

**Trigger:** Approval Gate 1 passed

**Process:**
1. Spawn `ux-component-agent` with IA specification
2. Agent instructions:
   ```
   Create lo-fi wireframes (grayscale, placeholder content):
   - NO final colors (use grayscale)
   - NO final copy (use lorem ipsum or [placeholder])
   - NO final images (use placeholder boxes)
   - FOCUS: Layout, spacing, component structure
   ```

3. Agent outputs:
   - HTML wireframes (Tailwind, grayscale palette)
   - Component structure notes
   - Layout rationale
4. Save to `docs/design/02-lofi-wireframes/`
5. **MANDATORY:** Proceed to Approval Gate 2

**Design System Constraints:**
- Use design tokens for spacing (ENFORCE)
- Use grayscale variants of design tokens
- Maintain visual hierarchy (H1 > H2 > Body)

---

### Stage 4: Approval Gate 2 - Lo-Fi Review

**Trigger:** Lo-fi wireframes generated

**Process:**
1. Present wireframes to stakeholder:
   ```
   ═══════════════════════════════════════════════════════════
     APPROVAL GATE 2: LO-FI WIREFRAMES
   ═══════════════════════════════════════════════════════════

   Generated Artifacts:
   [1] docs/design/02-lofi-wireframes/*.html
   [2] Component structure documentation
   [3] Layout rationale

   Review Status: PENDING
   ```

2. Invoke approval tool:
   ```
   /approval request
   ```

3. Wait for human approval decision:
   - **APPROVED** → Proceed to Stage 5
   - **REJECTED** → Return to Stage 3 with feedback
   - **CHANGES REQUESTED** → Modify wireframes, re-submit to Gate 2
   - **BACK TO IA** → Return to Stage 1 (major structural changes)

**Exit Criteria:**
- ✅ Layout approved
- ✅ Component structure approved
- ✅ Spacing/hierarchy approved
- ✅ User flow visually validated

**Enforcement:**
- Stage 5 CANNOT begin until Gate 2 status = APPROVED
- Major layout changes require re-approval

---

### Stage 5: Hi-Fi Mockups

**Trigger:** Approval Gate 2 passed

**Process:**
1. Spawn `ux-component-agent` with approved lo-fi wireframes
2. Agent instructions:
   ```
   Convert lo-fi wireframes to hi-fi mockups:
   - Apply full design system colors (design tokens ONLY)
   - Add final copy (replace placeholders)
   - Add final images/icons
   - Add micro-interactions (hover states, etc.)
   - Polish typography and visual details
   ```

3. Agent outputs:
   - HTML mockups (full fidelity)
   - Design system compliance report
   - Asset manifest (images, icons)
4. Save to `docs/design/03-hifi-mockups/`
5. Create validation report using `@design-system/examples/VALIDATION_REPORT`
6. **MANDATORY:** Final approval before Phase 7

**Design System Enforcement:**
- ❌ NO raw hex colors
- ✅ Use hsl(var(--token)) exclusively
- ✅ Validate against design system checklist
- ✅ Include asset metadata headers

---

### Stage 6: Final Design Sign-Off

**Trigger:** Hi-fi mockups generated

**Process:**
1. Present final mockups:
   ```
   ═══════════════════════════════════════════════════════════
     FINAL DESIGN SIGN-OFF
   ═══════════════════════════════════════════════════════════

   Generated Artifacts:
   [1] docs/design/03-hifi-mockups/*.html
   [2] Design system validation report
   [3] Asset manifest

   Review Status: PENDING
   ```

2. Invoke approval tool:
   ```
   /approval request
   ```

3. Wait for human approval decision:
   - **APPROVED** → Advance to Phase 7 (Test)
   - **REJECTED** → Return to Stage 5 with feedback
   - **CHANGES REQUESTED** → Modify mockups, re-submit to Stage 6
   - **BACK TO LO-FI** → Return to Stage 3 (major changes)

**Exit Criteria:**
- ✅ Visual design approved
- ✅ Copy approved
- ✅ Design system compliance confirmed
- ✅ All stakeholders signed off

**Enforcement:**
- Phase 7 CANNOT begin until final sign-off
- Changes to approved designs require re-approval

---

## 2.0 ENFORCEMENT MECHANISMS

### 2.1 Pre-Stage Checks

**Before Stage 1 (IA):**
```
✓ Phase 6 (Design) active
✓ Design brief exists
✓ Persona confirmed (from Phase 2)
✓ Selected solution documented (from Phase 5)
```

**Before Stage 3 (Lo-Fi):**
```
✓ Approval Gate 1 status = APPROVED
✓ IA artifacts exist in docs/design/01-*
```

**Before Stage 5 (Hi-Fi):**
```
✓ Approval Gate 2 status = APPROVED
✓ Lo-fi artifacts exist in docs/design/02-*
```

**Before Phase 7 (Test):**
```
✓ Final design sign-off status = APPROVED
✓ Hi-fi artifacts exist in docs/design/03-*
✓ Design system validation passed
```

### 2.2 Approval Tracking

**File:** `.project-approvals.yaml`

```yaml
design_workflow:
  enabled: true
  gates:
    - gate_id: gate_1_ia
      stage: information_architecture
      status: pending | approved | rejected | changes_requested
      approved_by: user_email
      approved_at: timestamp
      artifacts:
        - docs/design/01-information-architecture.md
      feedback: []

    - gate_id: gate_2_lofi
      stage: lofi_wireframes
      status: pending | approved | rejected | changes_requested
      approved_by: user_email
      approved_at: timestamp
      artifacts:
        - docs/design/02-lofi-wireframes/*.html
      feedback: []

    - gate_id: final_signoff
      stage: hifi_mockups
      status: pending | approved | rejected | changes_requested
      approved_by: user_email
      approved_at: timestamp
      artifacts:
        - docs/design/03-hifi-mockups/*.html
      feedback: []
```

**Update Mechanism:**
- After each approval decision, update `.project-approvals.yaml`
- Check file before proceeding to next stage
- Reject advancement if prior gate not approved

### 2.3 Violation Responses

**If Stage 3 attempted without Gate 1 approval:**
```
Cannot proceed to lo-fi wireframes:
- Gate 1 (IA Review) status: PENDING
- Required: APPROVED

Options:
[1] Request approval for current IA
[2] Revise IA based on feedback
[3] View approval status
```

**If Stage 5 attempted without Gate 2 approval:**
```
Cannot proceed to hi-fi mockups:
- Gate 2 (Lo-Fi Review) status: PENDING
- Required: APPROVED

Options:
[1] Request approval for current wireframes
[2] Revise wireframes based on feedback
[3] View approval status
```

**If Phase 7 attempted without final sign-off:**
```
Cannot advance to Phase 7 (Test):
- Final design sign-off status: PENDING
- Required: APPROVED

Options:
[1] Request final design approval
[2] Revise hi-fi mockups based on feedback
[3] View approval status
```

---

## 3.0 ENABLING THE WORKFLOW

### 3.1 Per-Project Opt-In

**When to Enable:**
- User explicitly requests design approval workflow
- Production projects (automatically enabled)
- Projects with `project_type: production` in `.project`

**How to Enable:**

1. During Phase 6 entry, ask:
   ```
   Enable formal design approval workflow?

   [1] Yes - Require approval at each stage (IA → Lo-Fi → Hi-Fi)
   [2] No - Single approval after final design
   [3] Skip - Generate designs without approval (SPIKE mode only)
   ```

2. If [1], create `.project-approvals.yaml` with design_workflow.enabled = true

3. Proceed to Stage 1

### 3.2 Automatic Enablement

**Triggers:**
- `.project` has `project_type: production`
- User mentions "formal design review" or "stakeholder approval"
- User references external stakeholders or clients

**Announcement:**
```
Detected production project - enabling formal design approval workflow.

This will require approval at:
  1. Information architecture (sitemap, navigation)
  2. Lo-fi wireframes (layout, structure)
  3. Hi-fi mockups (final design)

Continue? [Y/n]
```

### 3.3 Skipping Workflow

**Allowed When:**
- SPIKE mode (throwaway prototypes)
- Explicit user override: "skip design approvals"
- Prototype/exploration project type

**Not Allowed When:**
- Production projects (hard requirement)
- Workflow already enabled and partially complete

---

## 4.0 APPROVAL TOOL INTEGRATION

### 4.1 Invoking Approval

**Command:** `/approval request`

**Parameters:**
- `gate_id`: gate_1_ia | gate_2_lofi | final_signoff
- `artifacts`: List of files to review
- `context`: Brief description of what's being approved

**Example:**
```
/approval request gate_1_ia docs/design/01-information-architecture.md "Navigation structure and user flows for e-commerce checkout"
```

### 4.2 Approval Response

**User sees:**
```
═══════════════════════════════════════════════════════════
  APPROVAL REQUEST: Information Architecture
═══════════════════════════════════════════════════════════

Artifacts:
[1] Open: docs/design/01-information-architecture.md
[2] View: Navigation diagram
[3] View: User flow diagrams

Decision:
[1] Approve - Proceed to lo-fi wireframes
[2] Request changes - Provide feedback and re-submit
[3] Reject - Return to requirements/research
```

**AI receives:**
- Approval decision
- Feedback (if changes requested)
- Timestamp and approver

### 4.3 Tracking Approval State

**Read approval status:**
```python
import yaml

with open('.project-approvals.yaml') as f:
    approvals = yaml.safe_load(f)

gate_1_status = approvals['design_workflow']['gates'][0]['status']

if gate_1_status != 'approved':
    raise DesignWorkflowViolation("Gate 1 not approved")
```

**Update approval status:**
```python
approvals['design_workflow']['gates'][0].update({
    'status': 'approved',
    'approved_by': 'user@example.com',
    'approved_at': '2026-02-02T10:30:00Z',
    'feedback': []
})

with open('.project-approvals.yaml', 'w') as f:
    yaml.dump(approvals, f)
```

---

## 5.0 INTEGRATION WITH SDLC

### 5.1 Phase 6 Entry Point

**Before:** Phase 6 started with design generation
**After:** Phase 6 checks if design approval workflow enabled

**Modified Phase 6 flow:**
```
Enter Phase 6 → Check project type
                ↓
         Production/approval requested?
                ↓
              YES ↓         NO ↓
      Enable workflow    Standard design
                ↓              ↓
         Stage 1 (IA)    Generate designs
                ↓              ↓
         Gate 1          Single approval
                ↓              ↓
         Stage 3         Advance to Phase 7
         (Lo-Fi)
                ↓
         Gate 2
                ↓
         Stage 5
         (Hi-Fi)
                ↓
         Final Sign-Off
                ↓
         Advance to Phase 7
```

### 5.2 Gate Check Function

**Add to core utilities:**

```python
# File: hmode/shared/libs/sdlc_gates.py
# File UUID: 3d7f8a2e-9c4b-4f1a-8e3d-2a6f9b3c7d5e

def check_design_gate(gate_id: str) -> bool:
    """
    Check if a design approval gate has been passed.

    Args:
        gate_id: gate_1_ia | gate_2_lofi | final_signoff

    Returns:
        True if gate approved, False otherwise

    Raises:
        DesignGateNotApproved: If gate not approved with instructions
    """
    import yaml
    from pathlib import Path

    approval_file = Path('.project-approvals.yaml')

    if not approval_file.exists():
        # No approval workflow enabled
        return True

    with open(approval_file) as f:
        approvals = yaml.safe_load(f)

    if not approvals.get('design_workflow', {}).get('enabled'):
        return True

    for gate in approvals['design_workflow']['gates']:
        if gate['gate_id'] == gate_id:
            if gate['status'] == 'approved':
                return True
            else:
                raise DesignGateNotApproved(
                    f"Gate {gate_id} not approved. Status: {gate['status']}"
                )

    # Gate not found - not yet reached
    return True
```

### 5.3 Invocation Pattern

**Before spawning UX agent:**
```python
from shared.libs.sdlc_gates import check_design_gate, DesignGateNotApproved

try:
    check_design_gate('gate_1_ia')  # Before lo-fi
    # Proceed to spawn UX agent for lo-fi
except DesignGateNotApproved as e:
    print(f"Cannot proceed: {e}")
    print("Options:")
    print("[1] Request approval for current IA")
    print("[2] Revise IA based on feedback")
```

---

## 6.0 EXAMPLE WALKTHROUGH

### Scenario: E-commerce Checkout Redesign

**Phase 5 Complete:**
- Selected solution: Multi-step checkout with guest option
- Tech stack: Next.js, Tailwind, Stripe
- Advancing to Phase 6 (Design)

**Phase 6 Entry:**
```
Entering Phase 6 - Design

Detected: project_type = production
Enabling formal design approval workflow.

Workflow stages:
  1. Information Architecture → Approval Gate 1
  2. Lo-Fi Wireframes → Approval Gate 2
  3. Hi-Fi Mockups → Final Sign-Off

Continue? [Y/n]
```

**Stage 1: IA Generation**
```
Spawning information-architecture-agent...

Agent task:
- Design sitemap for checkout flow
- Map user journey (cart → payment → confirmation)
- Define navigation structure

Output: docs/design/01-information-architecture.md
```

**Generated IA includes:**
- Cart page
- Shipping info page
- Payment page
- Order confirmation page
- Guest vs. logged-in user flows

**Gate 1: Approval Request**
```
═══════════════════════════════════════════════════════════
  APPROVAL GATE 1: INFORMATION ARCHITECTURE
═══════════════════════════════════════════════════════════

Review artifacts:
[1] Open: docs/design/01-information-architecture.md

Decision? [approve/changes/reject]
```

**User response:** "approve"

**Stage 3: Lo-Fi Wireframes**
```
Gate 1 approved ✓
Proceeding to Stage 3: Lo-Fi Wireframes

Spawning ux-component-agent...

Agent task:
- Generate grayscale wireframes for 4 pages
- Use placeholder content
- Focus on layout and structure

Output: docs/design/02-lofi-wireframes/*.html
```

**Gate 2: Approval Request**
```
═══════════════════════════════════════════════════════════
  APPROVAL GATE 2: LO-FI WIREFRAMES
═══════════════════════════════════════════════════════════

Review artifacts:
[1] Open: docs/design/02-lofi-wireframes/cart.html
[2] Open: docs/design/02-lofi-wireframes/shipping.html
[3] Open: docs/design/02-lofi-wireframes/payment.html
[4] Open: docs/design/02-lofi-wireframes/confirmation.html

Decision? [approve/changes/reject]
```

**User response:** "changes - Add order summary sidebar on all pages"

**Revision:**
```
Gate 2 status: changes_requested
Feedback: Add order summary sidebar on all pages

Revising wireframes...
[Updated 4 wireframes]

Re-submitting to Gate 2...
```

**User response:** "approve"

**Stage 5: Hi-Fi Mockups**
```
Gate 2 approved ✓
Proceeding to Stage 5: Hi-Fi Mockups

Spawning ux-component-agent...

Agent task:
- Convert wireframes to full-fidelity mockups
- Apply design system colors
- Add final copy and images
- Polish interactions

Output: docs/design/03-hifi-mockups/*.html
```

**Final Sign-Off:**
```
═══════════════════════════════════════════════════════════
  FINAL DESIGN SIGN-OFF
═══════════════════════════════════════════════════════════

Review artifacts:
[1] Open: docs/design/03-hifi-mockups/cart.html
[2] Open: docs/design/03-hifi-mockups/shipping.html
[3] Open: docs/design/03-hifi-mockups/payment.html
[4] Open: docs/design/03-hifi-mockups/confirmation.html
[5] View: Design system validation report

Decision? [approve/changes/reject]
```

**User response:** "approve"

**Phase 7 Advancement:**
```
Final design sign-off approved ✓

Phase 6 (Design) complete.
Ready to advance to Phase 7 (Test).

Proceed? [Y/n]
```

---

## 7.0 SUMMARY

**Key Points:**

1. **Three-Stage Approval:** IA → Lo-Fi → Hi-Fi
2. **Enforcement:** Cannot skip stages without approval
3. **Tracking:** `.project-approvals.yaml` maintains state
4. **Integration:** Built into Phase 6 of SDLC
5. **Opt-In:** Automatic for production, optional for prototypes
6. **Flexible:** Can request changes or reject at any gate

**Benefits:**

- Catches structural issues early (IA review)
- Validates layout before investing in visuals (Lo-Fi)
- Ensures stakeholder buy-in before implementation
- Reduces rework in later phases
- Creates audit trail of design decisions

**Related Files:**
- `@processes/PHASE_6_DESIGN` - Phase 6 overview
- `@design-system/MANAGEMENT_GUIDELINES` - Design system rules
- `hmode/shared/libs/sdlc_gates.py` - Gate checking utilities
- `.project-approvals.yaml` - Per-project approval state
