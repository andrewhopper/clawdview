# SDLC WorkflowNet Diagram

## Petri Net Visualization

```
Legend:
  ○  = Place (condition/state)
  │  = Transition (action)
  →  = Arc (flow)
  ◆  = XOR-split (exclusive choice)
  ●  = Token

                                    SDLC 9-Phase WorkflowNet
═══════════════════════════════════════════════════════════════════════════════

    ●
    ○ p_idle (source)
    │
    │ t_start
    ↓
    ○ p_seed_done ─────────────────────────────────────────────────────┐
    │                                                                   │
    │ t_research [g: seed_doc_complete]                                 │
    ↓                                                                   │
    ○ p_research_done                                                   │
    │                                                                   │
    │ t_check_feasibility_required                                      │
    ↓                                                                   │
    ○ p_feasibility_required                                            │
    │                                                                   │
    ◆────────────────────────────┬─────────────────────────┐            │
    │                            │                         │            │
    │ t_feasibility              │ t_skip_feasibility      │            │
    │ [g: project_type ==        │ [g: project_type !=     │            │
    │     'production']          │     'production']       │            │
    ↓                            ↓                         │            │
    └────────────○───────────────┘                         │            │
                 p_feasibility_done                        │            │
                 │                                         │            │
                 │ t_expansion [g: feasibility_go]         │            │
                 ↓                                         │            │
                 ○ p_expansion_done                        │            │
                 │                                         │            │
                 │ t_analysis                              │            │
                 ↓                                         │            │
                 ○ p_analysis_done                         │   Phase    │
                 │                                         │  Numbers   │
                 │ t_selection                             │            │
                 ↓                                         │    1       │
                 ○ p_selection_done                        │            │
                 │                                         │    2       │
                 │ t_check_requirements_required           │            │
                 ↓                                         │   2.5      │
                 ○ p_requirements_required                 │            │
                 │                                         │    3       │
    ◆────────────┴────────────────┬────────────────────────┤            │
    │                             │                        │    4       │
    │ t_requirements              │ t_skip_requirements    │            │
    │ [g: project_type ==         │ [g: project_type !=    │    5       │
    │     'production']           │     'production']      │            │
    ↓                             ↓                        │   5.5      │
    └─────────────○───────────────┘                        │            │
                  p_requirements_done                      │    6       │
                  │                                        │            │
                  │ t_design [g: selection_complete]       │    7       │
                  ↓                                        │            │
                  ○ p_design_done                          │    8       │
                  │                                        │            │
                  │ t_test_design [g: design_approved]     │   8.5      │
                  ↓                                        │            │
                  ○ p_test_design_done                     │    9       │
                  │                                        │            │
                  │ t_implementation [g: tests_written     │            │
                  │                   AND tests_fail]      └────────────┘
                  ↓
                  ○ p_implementation_done
                  │
                  │ t_check_qa_required
                  ↓
                  ○ p_qa_required
                  │
    ◆─────────────┴───────────────┬────────────────────────┐
    │                             │                        │
    │ t_qa                        │ t_skip_qa              │
    │ [g: has_web_ui == true]     │ [g: has_web_ui ==      │
    │                             │     false]             │
    ↓                             ↓                        │
    └─────────────○───────────────┘                        │
                  p_qa_done                                │
                  │                                        │
                  │ t_refinement [g: qa_complete OR skip]  │
                  ↓                                        │
                  ○ p_refinement_done                      │
                  │                                        │
                  │ t_complete [g: all_tests_pass]         │
                  ↓                                        │
                  ○ p_complete (sink)                      │
                                                           │
═══════════════════════════════════════════════════════════╧═══════════════════
```

## Soundness Analysis

### Workflow Net Properties

| Property | Status | Notes |
|----------|--------|-------|
| Single source place | ✓ | `p_idle` |
| Single sink place | ✓ | `p_complete` |
| All nodes on path i→o | ✓ | All places/transitions reachable |
| No dead transitions | ✓ | Every transition has enabling path |

### Soundness Verification

**Definition:** A WF-net is sound if:
1. For every marking M reachable from initial marking, there exists a firing sequence to final marking
2. Final marking has exactly 1 token in sink, 0 elsewhere
3. No dead transitions (every transition can fire in some reachable marking)

**Verification:**

```
Initial marking:    M₀ = { p_idle: 1 }
Final marking:      Mf = { p_complete: 1 }

Path Analysis (Production + Web/UI project):
M₀ → t_start → { p_seed_done: 1 }
   → t_research → { p_research_done: 1 }
   → t_check_feasibility_required → { p_feasibility_required: 1 }
   → t_feasibility → { p_feasibility_done: 1 }
   → t_expansion → { p_expansion_done: 1 }
   → t_analysis → { p_analysis_done: 1 }
   → t_selection → { p_selection_done: 1 }
   → t_check_requirements_required → { p_requirements_required: 1 }
   → t_requirements → { p_requirements_done: 1 }
   → t_design → { p_design_done: 1 }
   → t_test_design → { p_test_design_done: 1 }
   → t_implementation → { p_implementation_done: 1 }
   → t_check_qa_required → { p_qa_required: 1 }
   → t_qa → { p_qa_done: 1 }
   → t_refinement → { p_refinement_done: 1 }
   → t_complete → Mf

Path Analysis (Prototype + CLI project):
M₀ → t_start → { p_seed_done: 1 }
   → t_research → { p_research_done: 1 }
   → t_check_feasibility_required → { p_feasibility_required: 1 }
   → t_skip_feasibility → { p_feasibility_done: 1 }  // SKIP 2.5
   → t_expansion → { p_expansion_done: 1 }
   → t_analysis → { p_analysis_done: 1 }
   → t_selection → { p_selection_done: 1 }
   → t_check_requirements_required → { p_requirements_required: 1 }
   → t_skip_requirements → { p_requirements_done: 1 }  // SKIP 5.5
   → t_design → { p_design_done: 1 }
   → t_test_design → { p_test_design_done: 1 }
   → t_implementation → { p_implementation_done: 1 }
   → t_check_qa_required → { p_qa_required: 1 }
   → t_skip_qa → { p_qa_done: 1 }  // SKIP 8.5
   → t_refinement → { p_refinement_done: 1 }
   → t_complete → Mf
```

**Result: SOUND** ✓

- All paths lead to `p_complete` with exactly 1 token
- XOR-splits have mutually exclusive guards (exactly one path taken)
- No deadlock possible (all markings can reach final)
- No dead transitions (all transitions fire in some scenario)

## Token Flow Example

**Scenario:** Production Web/UI project

```
Time  | Firing              | Token Location        | Context
──────┼─────────────────────┼───────────────────────┼─────────────────────
t=0   | (initial)           | ● p_idle              | project_type=production
t=1   | t_start             | ● p_seed_done         | has_web_ui=true
t=2   | t_research          | ● p_research_done     |
t=3   | t_check_feas...     | ● p_feasibility_req   |
t=4   | t_feasibility       | ● p_feasibility_done  | guard: production ✓
t=5   | t_expansion         | ● p_expansion_done    |
...   | ...                 | ...                   |
t=14  | t_qa                | ● p_qa_done           | guard: has_web_ui ✓
t=15  | t_refinement        | ● p_refinement_done   |
t=16  | t_complete          | ● p_complete          | DONE
```

## GetEnabledTransitions Output

At `p_test_design_done` (Phase 7 complete):

```yaml
enabled_set:
  case_id: "sdlc-case-001"
  current_marking: { p_test_design_done: 1 }
  transitions:
    - id: t_implementation
      name: "Phase 8: Implementation"
      is_enabled: true
      all_guards_passed: true  # tests_written AND tests_fail
      priority: 90
      action_type: task
      requires_human: false
      priority_factors:
        - { name: "forward_progress", modifier: +20 }
        - { name: "only_option", modifier: +20 }
```

At `p_qa_required` (Phase 8 complete, web project):

```yaml
enabled_set:
  case_id: "sdlc-case-001"
  current_marking: { p_qa_required: 1 }
  context: { has_web_ui: true }
  transitions:
    - id: t_qa
      name: "Phase 8.5: QA Validation"
      is_enabled: true
      all_guards_passed: true  # has_web_ui == true
      priority: 85
      action_type: task
      requires_human: false
    - id: t_skip_qa
      name: "Skip QA (non-visual)"
      is_enabled: false
      blocking_reason: "Guard failed: has_web_ui == false"
      priority: 0
```
