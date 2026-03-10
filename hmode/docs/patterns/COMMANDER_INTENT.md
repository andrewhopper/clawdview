# Commander's Intent Pattern

<!-- File UUID: 7f3c4a2b-9e1d-4f8a-b6c3-5d7e8f9a0b1c -->

## Overview

**Commander's Intent** is a military decision-making framework adapted for universal planning and execution. It provides clear, concise objectives that enable autonomous execution and adaptive decision-making when conditions change.

Originally developed for military operations, this pattern applies to any complex planning scenario: organizing events, managing construction projects, planning expeditions, coordinating weddings, launching businesses, or responding to crises.

## Four Key Components

### 1.0 Purpose (The "Why")
The overarching reason for the operation. Answers: "Why are we doing this?"

**Characteristics:**
- Single sentence when possible
- Links to broader strategic goals
- Provides context for all decisions
- Unchanging despite tactical adjustments
- Works in tandem with constraints to define mission scope

**Examples:**
```
Purpose: Create memorable celebration within budget (wedding)
Purpose: Restore health certification before health board review (restaurant)
Purpose: Secure remote beach location for optimal surf conditions (expedition)
Purpose: Complete kitchen modernization before holiday season (renovation)
Purpose: Establish forward operating base for humanitarian relief (military)
```

### 2.0 Key Tasks (The "What")
Essential activities that MUST be completed to achieve success. These are the non-negotiable outcomes.

**Characteristics:**
- 3-7 concrete tasks
- Measurable or verifiable
- Critical path items only
- Listed in priority order

**Examples:**
```
Wedding Planning Key Tasks:
1. Venue secured and deposit paid
2. Core vendors contracted (catering, photography, music)
3. Guest accommodations arranged
4. Ceremony and reception timeline finalized

Construction Project Key Tasks:
1. Building permits obtained and approved
2. Foundation poured and inspected
3. Structural framing completed and verified
4. Systems (electrical, plumbing) installed and tested

Surf Expedition Key Tasks:
1. Destination selected based on swell forecast
2. Accommodations booked near quality breaks
3. Ground transportation arranged
4. Emergency medical access confirmed
```

### 3.0 End State (The "Done")
Description of desired conditions upon mission completion. Defines what success looks like for all actors (friendly forces, enemy forces, terrain/environment).

**Characteristics:**
- Concrete, observable conditions
- Defines success criteria
- Describes system state, not activities
- Often includes what should NOT exist

**Examples:**
```
Wedding End State:
- 150 guests attended ceremony and reception
- Event proceeded according to timeline without major issues
- Venue returned in acceptable condition
- Photography captured all key moments
- Budget variance within 5% of plan

Kitchen Renovation End State:
- All appliances installed and operational
- Electrical and plumbing pass final inspection
- Cabinets, countertops, and backsplash completed to quality standards
- Family can prepare full meals without temporary facilities
- No building code violations

Expedition End State:
- Team arrived at destination safely
- Quality surf sessions occurred at target breaks
- All team members returned without injury
- Equipment performed reliably throughout trip
- Budget maintained within planned allocation
```

### 4.0 Constraints (The "Boundaries")
Restrictions imposed by higher command that limit freedom of action. Constraints define the boundaries within which the team must operate. Derived from military doctrine, constraints are **non-negotiable** and come from authorities such as product owners, tech leads, security teams, or organizational policies.

**Characteristics:**
- Non-negotiable restrictions
- Imposed by higher authority
- Define boundaries of acceptable solutions
- Must be explicit and measurable
- Interact with decision authority to define freedom within boundaries

**Types of Constraints:**

#### 4.1 Proscriptive Constraints (MUST DO)
Actions or requirements that are **mandatory**. These are things that **must be included** or **must be done** in any solution.

**Examples:**
```
Wedding Proscriptive Constraints:
- Must accommodate vegetarian and gluten-free dietary requirements
- Must comply with venue regulations (noise, decorations, alcohol)
- Must provide accessible facilities for guests with mobility limitations
- Must maintain liability insurance throughout event

Construction Proscriptive Constraints:
- Must obtain all required building permits before starting work
- Must use licensed electrician and plumber for systems work
- Must pass inspections at each major milestone
- Must maintain worksite safety protocols and signage

Expedition Proscriptive Constraints:
- Must carry emergency satellite communication device
- Must file trip plan with local authorities before departure
- Must maintain travel insurance for all team members
- Must follow Leave No Trace principles in protected areas
```

#### 4.2 Prohibitive Constraints (CANNOT DO)
Actions that are **forbidden**. These define what is **off-limits** and cannot be done under any circumstances.

**Examples:**
```
Wedding Prohibitive Constraints:
- Cannot exceed venue capacity (fire code: max 200 people)
- Cannot serve alcohol to minors
- Cannot play amplified music after 10 PM (noise ordinance)
- Cannot exceed total budget of $50,000
- Cannot modify venue structure (drilling, painting)

Construction Prohibitive Constraints:
- Cannot begin work before 7 AM or after 7 PM (city ordinance)
- Cannot remove load-bearing walls without engineer approval
- Cannot disturb asbestos-containing materials without certified abatement
- Cannot block emergency vehicle access to neighboring properties
- Cannot excavate without utility location verification

Expedition Prohibitive Constraints:
- Cannot enter restricted conservation areas without permits
- Cannot exceed weight limits for chartered aircraft
- Cannot travel without required vaccinations and medications
- Cannot deviate from approved route in hostile territory
```

#### 4.3 Resource/Logistical Constraints
Limitations on available resources including budget, personnel, infrastructure, or technical capabilities.

**Examples:**
```
Wedding Resource Constraints:
- Budget: Total cost cannot exceed $50,000 (deposits, vendors, venue)
- Personnel: Must plan and execute with 2 coordinators and family volunteers
- Venue capacity: Must accommodate exactly 150 guests
- Timeline: Must complete planning within 6 months
- Vendor availability: Limited to vendors available on selected date

Construction Resource Constraints:
- Budget: Project cost limited to $120,000 (materials, labor, permits)
- Labor: Must complete with 2-person crew and subcontractors
- Materials: Subject to current lumber and steel prices and availability
- Equipment: Limited to contractor's existing tools and rented equipment
- Timeline: Must complete before winter freeze (November 15)

Expedition Resource Constraints:
- Budget: $3,000 per person for 10-day trip (flights, lodging, equipment)
- Team size: Limited to 6 people (vehicle and accommodation capacity)
- Equipment: Must use existing surf gear and camping equipment
- Medical: First aid kit and emergency evacuation insurance only
```

#### 4.4 Temporal/Environmental Constraints
Time-based limitations and environmental conditions that must be respected.

**Examples:**
```
Wedding Temporal Constraints:
- Ceremony must begin at 4 PM (venue contract)
- Setup must complete by 2 PM (vendor access window)
- Event must conclude by 11 PM (venue curfew)
- Final payments due 2 weeks before event

Construction Temporal Constraints:
- Foundation must cure for 7 days before framing begins
- Rough inspections must pass before closing walls
- Must complete weatherproofing before rainy season (October)
- Cannot work on holidays (no inspector availability)

Environmental Constraints:
- Weather: Must account for seasonal rain and temperature
- Site conditions: Limited vehicle access on narrow residential street
- Neighborhood: Must minimize noise and dust impact on neighbors
- Utilities: Must coordinate shutoffs with occupants' schedules
```

#### 4.5 Constraints vs. Decision Authority

Constraints and decision authority work together to define operational freedom:

| Aspect | Constraints | Decision Authority |
|--------|-------------|-------------------|
| **What it defines** | Boundaries and limits | Freedom within boundaries |
| **Source** | Higher command/authority | Delegated by commander |
| **Negotiable** | No (non-negotiable) | Yes (can be adjusted) |
| **Examples** | "Cannot modify schema" | "Choose any ORM library" |
| **Purpose** | Prevent prohibited actions | Enable autonomous decisions |
| **Relationship** | Defines the box | Defines freedom inside box |

**Interaction Example:**
```yaml
# Wedding Planning: Constraints define the boundaries
constraints:
  - Cannot exceed venue capacity of 200 (prohibitive)
  - Must accommodate dietary restrictions (proscriptive)
  - Must complete setup by 2 PM (temporal)

# Decision authority defines freedom WITHIN those boundaries
decision_authority:
  autonomous:
    - Seating arrangement within capacity limits
    - Menu selection that meets dietary requirements
    - Decoration choices that don't damage venue
  requires_approval:
    - Adding guests beyond initial count
    - Major changes to ceremony timeline
    - Substituting different venue

# Construction: Constraints define the boundaries
constraints:
  - Cannot remove load-bearing walls (prohibitive)
  - Must obtain building permits (proscriptive)
  - Must complete before November 15 (temporal)

# Decision authority defines freedom WITHIN those boundaries
decision_authority:
  autonomous:
    - Cabinet hardware and finish selection
    - Work schedule optimization
    - Subcontractor selection from approved list
  requires_approval:
    - Layout changes affecting plumbing locations
    - Upgrading materials beyond budget
    - Timeline extensions
```

The executor has **full autonomy** to make decisions within the constrained space, but **cannot violate** the constraints even with approval.

## Component Relationship Matrix

The four components work together to define complete mission guidance:

| Component | Role | Answers | Changeability | Source |
|-----------|------|---------|---------------|--------|
| **Purpose** | Strategic objective | Why are we doing this? | Fixed (unchanging) | Leader/Project Owner |
| **Key Tasks** | Critical activities | What must be done? | Semi-fixed (can adapt) | Leader/Project Manager |
| **End State** | Success criteria | What does done look like? | Fixed (defines success) | Leader/Stakeholders |
| **Constraints** | Boundaries | What limits our options? | Non-negotiable | Higher authority (legal, budget, regulations) |

### How They Interact:

```
Purpose (WHY)
    ↓
    Defines scope and motivation
    ↓
Key Tasks (WHAT) ←→ Constraints (BOUNDARIES)
    ↓                   ↓
    Tasks must         Constraints limit
    achieve purpose    acceptable tasks
    ↓                   ↓
End State (DONE)
    ↓
    Observable success criteria
```

**Example of Interaction:**
```yaml
# Wedding Planning Example
purpose: "Create memorable celebration within budget"
# Purpose sets the strategic goal

key_tasks:
  - Venue secured and contracts signed
  - Core vendors booked (catering, photography, music)
  - Guest accommodations arranged
  - Ceremony and reception planned
# Tasks define WHAT must be accomplished

constraints:
  - Cannot exceed $50,000 total budget
  - Cannot exceed venue capacity of 150 guests
  - Must accommodate dietary restrictions
  - Must complete planning within 6 months
# Constraints LIMIT acceptable approaches

end_state:
  - 150 guests attended and enjoyed celebration
  - Event completed within budget
  - All vendors delivered contracted services
  - No venue damage or regulatory violations
# End state defines MEASURABLE success (influenced by all above)
```

## When to Use Commander's Intent

### ✅ USE When:
1. **Complex Multi-Step Operations:** Projects requiring 5+ steps or multiple decision points
2. **Uncertain Environments:** When exact approach may need adaptation mid-execution (weather, supply chain disruptions, changing conditions)
3. **Delegation to Teams:** Coordinating specialists who need autonomy (vendors, subcontractors, team leads)
4. **Ambiguous Goals:** Stakeholder provides objective but not detailed specifications
5. **Multi-Phase Projects:** Work spanning planning, execution, and completion phases
6. **Emergency Operations:** Crisis response or urgent situations requiring rapid adaptation
7. **Remote Coordination:** When leader cannot supervise every detail (expeditions, distributed teams)
8. **High-Stakes Events:** Weddings, conferences, launches where failure isn't acceptable

**Examples:**
- ✅ Planning a 150-person wedding with multiple vendors
- ✅ Managing a construction project with supply chain risks
- ✅ Coordinating a multi-week expedition with uncertain weather
- ✅ Organizing a conference with 500+ attendees
- ✅ Leading a military operation in hostile territory
- ✅ Responding to restaurant health inspection violations
- ✅ Launching a new retail store location

### ❌ DON'T USE When:
1. **Simple Linear Tasks:** "Pick up groceries" or "change lightbulb" - just do it
2. **Fully Specified Work:** Instructions provide exact steps with no decisions needed
3. **Trivial Operations:** Booking a single hotel, making a phone call, sending an email
4. **Pure Information Gathering:** Research with no execution component

## Integration with Any Project Lifecycle

Commander's Intent applies throughout the lifecycle of any project, from initial conception through final delivery. The pattern remains the same; only the focus shifts.

### Planning Phase: Initial Intent Definition
```yaml
# Wedding Planning (Conception Phase)
purpose: "Create memorable celebration within budget"
key_tasks:
  - Guest list finalized with headcount
  - Budget allocated across major categories
  - Venue options researched and shortlisted
  - Date range identified based on availability
end_state: "Clear plan with venue secured, budget allocated, and timeline established"
constraints:
  - Must research within 2-month timeline
  - Cannot make deposits before budget approval
  - Must consult with both families on major decisions
  - Budget research limited to $500 for travel and consultations
```

### Execution Phase: Build Intent
```yaml
# Construction (Build Phase)
purpose: "Complete kitchen addition before winter"
key_tasks:
  - Foundation poured and inspected
  - Framing completed and weatherproofed
  - Systems (electrical, plumbing) installed and tested
  - Interior finishes completed to quality standards
end_state: "Kitchen fully functional with all inspections passed"
constraints:
  - Must complete weatherproofing before October 15 (rainy season)
  - Cannot exceed $120,000 budget
  - Cannot block driveway access for more than 4 hours
  - Must use licensed contractors for electrical and plumbing
```

### Completion Phase: Finalization Intent
```yaml
# Expedition (Wrap-up Phase)
purpose: "Complete surf trip and return team safely"
key_tasks:
  - All equipment accounted for and packed
  - Accommodations settled and checked out
  - Return transportation confirmed
  - Team debriefed on trip outcomes
end_state: "Team home safely with positive experience and lessons documented"
constraints:
  - Must depart location by checkout time (10 AM)
  - Cannot leave damaged equipment unreported
  - Must stay within remaining budget for return travel
  - Cannot miss return flights (non-refundable tickets)
```

## Pattern Template

```markdown
## Commander's Intent

**Purpose:** [Single sentence describing the "why"]

**Key Tasks:**
1. [Critical task 1]
2. [Critical task 2]
3. [Critical task 3]
4. [Optional task 4]
5. [Optional task 5]

**End State:**
- [Observable condition 1]
- [Observable condition 2]
- [Observable condition 3]
- [What should NOT exist]

**Constraints:**
- Proscriptive: [Must do X, Must use Y]
- Prohibitive: [Cannot do X, Cannot change Y]
- Resource: [Budget limit, Team size, Infrastructure]
- Temporal: [Deadline, Deployment windows]
- Environmental: [Network conditions, Compliance requirements]

**Decision Authority:**
- Autonomous: [What agent can decide within constraints]
- Requires approval: [What needs human approval]
```

## Examples by Domain

### 1.0 Crisis Response (Restaurant Health Violation)
```yaml
purpose: "Restore health certification before 48-hour deadline"
key_tasks:
  - All cited violations identified and understood
  - Critical violations corrected (temperature control, cross-contamination)
  - Staff trained on proper food handling procedures
  - Re-inspection scheduled and passed
end_state: |
  - Health certificate restored and posted
  - No remaining violations on record
  - Staff demonstrates proper procedures
  - Documentation shows compliance with regulations
  - Restaurant reopens for normal operation
constraints:
  proscriptive:
    - Must correct all critical violations before re-inspection
    - Must document all corrective actions taken
    - Must retrain all food handlers on violations
    - Must use approved cleaning and sanitizing products
  prohibitive:
    - Cannot serve food to customers during correction period
    - Cannot use unapproved equipment or procedures
    - Cannot reopen without passing re-inspection
    - Cannot exceed $5,000 emergency repair budget
  resource:
    - Must complete with existing staff
    - Limited to equipment already on premises or immediately available
    - Emergency budget: $5,000 maximum
  temporal:
    - Must pass re-inspection within 48 hours
    - Cannot delay beyond deadline (forced closure)
    - Staff retraining must complete before re-inspection
decision_authority:
  autonomous:
    - Specific cleaning procedures and products
    - Staff training schedule and methods
    - Minor equipment repairs or replacements
    - Documentation format
  requires_approval:
    - Major equipment purchases over $1,000
    - Structural modifications
    - Decision to temporarily close dining room
    - Hiring temporary staff
```

### 2.0 Event Planning (Wedding Coordination)
```yaml
purpose: "Create memorable celebration within budget"
key_tasks:
  - Venue secured with deposit and contract signed
  - Core vendors contracted (catering, photography, music, flowers)
  - Guest accommodations arranged for out-of-town attendees
  - Ceremony and reception timeline finalized and communicated
  - Day-of coordination team briefed and prepared
end_state: |
  - 150 guests attended ceremony and reception
  - Event proceeded according to timeline without major disruptions
  - All contracted vendors delivered services as agreed
  - Photography captured all requested moments
  - Venue returned in acceptable condition
  - Total cost within 5% of $50,000 budget
constraints:
  proscriptive:
    - Must accommodate vegetarian and gluten-free dietary needs
    - Must provide accessible facilities for mobility-limited guests
    - Must comply with venue regulations (decorations, noise, alcohol)
    - Must maintain liability insurance throughout planning and event
    - Must provide transportation for guests from hotel to venue
  prohibitive:
    - Cannot exceed venue capacity (max 200, planned for 150)
    - Cannot serve alcohol to minors
    - Cannot play amplified music after 10 PM (venue noise ordinance)
    - Cannot exceed total budget of $50,000
    - Cannot modify venue structure or landscaping
  resource:
    - Budget: $50,000 total (venue $8K, catering $18K, photo $5K, other $19K)
    - Planning team: 2 coordinators plus family volunteers
    - Timeline: 6 months from engagement to wedding date
    - Venue capacity: 150 guests (max 200)
  temporal:
    - Planning must complete within 6 months
    - Vendor contracts must be signed 3 months before event
    - Final headcount due to caterer 2 weeks before event
    - Setup must complete by 3 PM, ceremony at 5 PM
    - Event must conclude by 11 PM (venue curfew)
decision_authority:
  autonomous:
    - Decoration selections and color scheme
    - Music playlist within genre preferences
    - Seating arrangements
    - Menu selections that meet dietary requirements
    - Timeline adjustments within venue constraints
  requires_approval:
    - Adding guests beyond 150 count
    - Budget reallocation between major categories (>$2,000)
    - Changing venue or date
    - Major ceremony or reception format changes
    - Vendor substitutions for core services
```

### 3.0 Destination Selection (Surf Expedition Planning)
```yaml
purpose: "Identify optimal surf destination for December trip"
key_tasks:
  - Multiple destinations evaluated for wave conditions in December
  - Swell forecasts and seasonal patterns analyzed
  - Accessibility, safety, and logistics assessed for each option
  - Cost comparison completed for top 3 destinations
  - Top recommendation validated with local surf reports
end_state: |
  - Clear recommendation with pros/cons for each option
  - Wave quality expectations documented for time of year
  - Cost breakdown completed for top choice
  - Accommodation and transportation feasibility confirmed
  - Team consensus achieved on destination selection
constraints:
  proscriptive:
    - Must evaluate wave conditions for intermediate surfers
    - Must assess safety and medical access
    - Must validate seasonal swell patterns with multiple sources
    - Must confirm surf break accessibility (walking/boat/etc)
    - Must research local regulations and permit requirements
  prohibitive:
    - Cannot select destination without consistent December swell
    - Cannot exceed $3,000 per person total trip budget
    - Research cannot take longer than 3 weeks
    - Cannot select locations requiring advanced technical skills
    - Cannot choose destinations with travel warnings
  resource:
    - Budget: $3,000 per person (6 people total)
    - Research time: 3 weeks maximum
    - Team: 6 intermediate surfers
    - Equipment: Existing boards and wetsuits
  temporal:
    - Research must complete within 3 weeks
    - Trip must occur in December (only available window)
    - Booking deadline: 8 weeks before departure (price increases)
    - Decision needed before booking window closes
decision_authority:
  autonomous:
    - Research sources and methodology
    - Evaluation criteria and scoring
    - Accommodation options within budget
    - Presentation format for recommendation
  requires_approval:
    - Final destination selection
    - Budget allocation between flights/accommodation/activities
    - Travel insurance and emergency plans
    - Commitment to non-refundable bookings
```

### 4.0 Home Improvement (Kitchen Renovation)
```yaml
purpose: "Modernize kitchen to increase home value while family lives in house"
key_tasks:
  - Design approved by family and meets building codes
  - Demolition completed with minimal dust containment breach
  - Plumbing and electrical systems upgraded and inspected
  - Cabinets, countertops, appliances installed and functional
  - Final inspection passed and certificate of occupancy issued
end_state: |
  - Kitchen fully functional for daily family meal preparation
  - All building inspections passed (rough, final)
  - Appliances installed and operational
  - Finishes completed to agreed quality standards
  - No building code violations
  - Project completed within 10% of $120,000 budget
  - Family can prepare meals without temporary kitchen by holidays
constraints:
  proscriptive:
    - Must obtain building permit before starting work
    - Must use licensed electrician and plumber for systems work
    - Must pass rough inspection before closing walls
    - Must maintain one operational sink at all times
    - Must contain dust to kitchen area (family living in home)
    - Must provide 48-hour notice before water/power shutoffs
  prohibitive:
    - Cannot remove load-bearing walls without engineer approval
    - Cannot work before 7 AM or after 7 PM (city noise ordinance)
    - Cannot block emergency egress from home
    - Cannot exceed $120,000 budget
    - Cannot disrupt family meals (must maintain makeshift kitchen)
    - Cannot leave work site unsecured overnight (family safety)
  resource:
    - Budget: $120,000 (demo $5K, cabinets $35K, counters $15K, appliances $12K, labor $40K, contingency $13K)
    - Labor: 2-person crew plus licensed subcontractors
    - Timeline: 8 weeks for completion
    - Equipment: Contractor's tools plus rentals (dumpster, scaffolding)
  temporal:
    - Must complete before November 20 (family hosting Thanksgiving)
    - Rough inspection must occur before closing walls (2-week window)
    - Final inspection must occur after all work complete
    - Cannot work on weekends (family needs peace)
    - Foundation work must cure for specified time before proceeding
decision_authority:
  autonomous:
    - Cabinet hardware selection within style guide
    - Work schedule optimization within hour restrictions
    - Dust containment methods
    - Subcontractor selection from approved list
    - Minor design adjustments that don't affect layout
  requires_approval:
    - Layout changes affecting plumbing or electrical locations
    - Material upgrades that exceed budget allocations
    - Timeline extensions beyond November 20
    - Structural modifications
    - Changes requiring permit amendments
```

## Usage with Specialized Teams

### Delegating to Specialists with Commander's Intent

Commander's Intent enables effective delegation to specialists by providing clear objectives while preserving their autonomy to execute within their expertise.

```markdown
# Wedding Coordination: Delegating to Florist

## Commander's Intent for Floral Design

**Purpose:** Create cohesive floral design that complements venue and season

**Key Tasks:**
1. Design centerpieces for 15 reception tables
2. Create ceremony arrangements (altar, aisle markers)
3. Provide bouquets for wedding party (bride, 4 bridesmaids)
4. Design boutonnieres for groom and groomsmen

**End State:**
- All floral arrangements delivered and set up by 3 PM
- Colors complement burgundy and gold theme
- Designs appropriate for fall season
- All arrangements fresh and properly hydrated
- Within allocated $3,500 budget

**Constraints:**
- Proscriptive: Must use seasonal flowers, Must deliver by 3 PM setup deadline
- Prohibitive: Cannot use lilies (bride allergic), Cannot exceed $3,500 budget
- Resource: $3,500 budget allocation
- Temporal: Setup complete by 3 PM on wedding day

**Decision Authority:**
- Autonomous: Specific flower selections, arrangement styles, vase choices, design details
- Requires approval: Major color deviations, budget increases, delivery time changes
```

### Intent Cascade (Leader → Multiple Specialists)

```yaml
# Parent Intent (Construction Project Manager)
purpose: "Complete kitchen renovation before holiday deadline"
key_tasks:
  - Demolition and preparation completed safely
  - Systems (electrical, plumbing) installed and inspected
  - Cabinets and countertops installed professionally
  - Final inspection passed and space ready for use
constraints:
  - Must complete by November 20
  - Cannot exceed $120,000 budget
  - Must maintain family access to home
  - Must pass all building inspections

# Child Intent 1 (Electrician)
purpose: "Upgrade kitchen electrical to code for modern appliances"
key_tasks:
  - Install dedicated 240V circuit for range
  - Add GFCI outlets near sink and counters
  - Install under-cabinet lighting circuits
  - Pass rough electrical inspection
constraints:
  - Must follow current electrical code
  - Must coordinate power shutoffs with family (48hr notice)
  - Cannot exceed $8,000 allocated budget
  - Must complete before cabinet installation (Week 4)

# Child Intent 2 (Plumber)
purpose: "Relocate plumbing for new island and prep for appliances"
key_tasks:
  - Cap old sink location plumbing
  - Rough-in island sink and dishwasher connections
  - Install new gas line for range
  - Pass rough plumbing inspection
constraints:
  - Must maintain one working sink in home during work
  - Must coordinate water shutoffs with family (48hr notice)
  - Cannot exceed $6,500 allocated budget
  - Must complete before flooring installation (Week 5)

# Child Intent 3 (Cabinet Installer)
purpose: "Install custom cabinets according to design"
key_tasks:
  - Install base cabinets level and secure
  - Install upper cabinets with proper support
  - Install hardware and adjust doors/drawers
  - Prepare for countertop templating
constraints:
  - Must follow manufacturer installation specs
  - Must work within existing floor/wall dimensions
  - Cannot exceed 2-week installation window (Weeks 5-6)
  - Must be complete before countertop fabricator arrives
```

## Handling Ambiguity

### When Purpose is Clear, Tasks are Vague
```yaml
# Stakeholder: "Make the wedding more memorable"

purpose: "Create exceptional guest experience that exceeds expectations"

# ASK STAKEHOLDER TO CLARIFY KEY TASKS:
# [1] Focus on unique entertainment (live band, photo booth, surprises)
# [2] Focus on exceptional food/beverage (cocktail hour, premium menu)
# [3] Focus on personalization (custom favors, video montage, décor)
# [4] Comprehensive experience upgrade (all touchpoints)

# After clarification, define key tasks based on answer
```

### When Purpose is Vague, Tasks are Clear
```yaml
# Homeowner: "Install new countertops in the kitchen"

# INFER PURPOSE, CONFIRM WITH HOMEOWNER:
purpose: "Modernize kitchen to increase home value"  # Assumed
# OR
purpose: "Replace damaged countertops for functional use"  # Practical

key_tasks:  # Clear from request
  - Remove old countertops and dispose properly
  - Template new countertop dimensions
  - Fabricate and install new countertops
  - Seal and finish edges
```

### When Both are Vague
```yaml
# Client: "The restaurant needs improvement"

# ASK CLARIFYING QUESTIONS:
# 1. What problem are customers experiencing? [slow service/poor food quality/ambiance]
# 2. What metric are we trying to improve? [revenue/reviews/repeat customers]
# 3. What's in scope? [menu redesign/staff training/interior renovation]

# Then construct intent based on answers
```

## Validation Checklist

Before executing with Commander's Intent, verify:

**Purpose:**
- [ ] Answers "Why are we doing this?"
- [ ] Single, clear objective
- [ ] Links to user or business value
- [ ] Would make sense to stakeholder

**Key Tasks:**
- [ ] 3-7 concrete tasks listed
- [ ] Each task is measurable or verifiable
- [ ] Critical path only (no nice-to-haves)
- [ ] Ordered by priority or dependency

**End State:**
- [ ] Observable conditions (not activities)
- [ ] Defines success for all actors
- [ ] Includes "what should NOT exist"
- [ ] Could be verified by another person

**Constraints:**
- [ ] All constraint types considered (proscriptive, prohibitive, resource, temporal)
- [ ] Each constraint is specific and measurable
- [ ] Source/authority for constraints identified
- [ ] Constraints are truly non-negotiable
- [ ] No conflict between constraints

**Decision Authority:**
- [ ] Clear what agent can decide alone
- [ ] Clear what requires human approval
- [ ] Aligns with SDLC phase gates
- [ ] Decision authority respects constraints (no conflicts)

## Benefits of Commander's Intent

### For Executors (Team Members, Contractors, Specialists):
1. **Autonomy:** Clear objective enables independent decision-making within expertise
2. **Adaptability:** Can adjust tactics when obstacles arise without constant check-ins
3. **Focus:** Distinguishes critical tasks from optional work
4. **Verification:** End state provides clear success criteria
5. **Boundaries:** Constraints prevent costly mistakes and violations
6. **Empowerment:** Know exactly where they have authority vs. need approval

### For Leaders (Project Managers, Coordinators, Commanders):
1. **Trust:** Understand what team will do and why without micromanaging
2. **Control:** Clear approval points for critical decisions
3. **Diagnosis:** Easy to identify where execution diverged from plan
4. **Communication:** Shared language for discussing objectives across specialties
5. **Risk Management:** Constraints encode policies and prevent violations
6. **Scalability:** Can delegate effectively to multiple specialists simultaneously

### For Organizations (Projects, Teams, Systems):
1. **Traceability:** Intent documented for all operations and phases
2. **Coordination:** Multiple specialists aligned to same objective
3. **Continuity:** New team member can continue if original person unavailable
4. **Learning:** Analyze success/failure against intent for future projects
5. **Compliance:** Constraints ensure regulatory and policy adherence
6. **Knowledge Transfer:** Intent documentation becomes institutional knowledge

### Benefits of Explicit Constraints:
1. **Prevent Violations:** Stop agents before they break critical rules (schema changes, PII leaks)
2. **Faster Decisions:** Agent knows immediately what's off-limits without asking
3. **Encode Wisdom:** Capture organizational knowledge about what doesn't work
4. **Reduce Rework:** Prevent solutions that would be rejected in review
5. **Enable Autonomy:** Clearer boundaries = more freedom within them

## Anti-Patterns

### ❌ Too Prescriptive (Micromanagement)
```yaml
# Wedding Florist Intent - TOO PRESCRIPTIVE
purpose: "Create floral arrangements"
key_tasks:
  - Buy exactly 24 red roses from Trader Joe's on Oak Street
  - Cut stems to exactly 8 inches at 45-degree angle
  - Arrange 3 roses per vase in triangle formation
  - Place vase exactly 12 inches from table center
# PROBLEM: No room for florist expertise, might as well do it yourself
```

### ❌ Too Vague (No Direction)
```yaml
# Construction Project - TOO VAGUE
purpose: "Make things better"
key_tasks:
  - Improve stuff in the kitchen
  - Fix problems
  - Add features
# PROBLEM: Contractor has no clear objective or success criteria
```

### ❌ Conflicting Objectives
```yaml
# Wedding Planning - CONFLICTING
purpose: "Create lavish celebration while minimizing costs"
key_tasks:
  - Hire celebrity entertainment
  - Serve premium 5-course meal
  - Invite 300 guests
  - Reduce budget by 75%
# PROBLEM: Purpose contains competing priorities that can't coexist
```

### ❌ No End State
```yaml
# Kitchen Renovation - NO SUCCESS CRITERIA
purpose: "Improve kitchen"
key_tasks:
  - Replace some cabinets
  - Update countertops
  - Maybe upgrade appliances
# PROBLEM: No definition of success - how do we know when it's "done"?
```

### ❌ Vague Constraints
```yaml
# Restaurant Opening - VAGUE CONSTRAINTS
purpose: "Open new restaurant location"
constraints:
  - "Keep costs reasonable"
  - "Move pretty quickly"
  - "Don't cut too many corners"
# PROBLEM: Constraints too vague to be actionable or enforceable
```

### ❌ Conflicting Constraints
```yaml
# Conference Planning - IMPOSSIBLE CONSTRAINTS
purpose: "Host world-class technology conference"
constraints:
  - Must accommodate 5,000 attendees
  - Must complete planning in 2 weeks
  - Cannot hire any staff
  - Cannot exceed $10,000 budget
  - Must achieve 95% satisfaction rating
# PROBLEM: Constraints are mathematically impossible to satisfy together
```

## Relationship to Project Phases

Commander's Intent is **orthogonal to project phases** - it applies at any stage of any project type:

| Project Stage | Intent Focus | Common Constraints | Example Domain |
|---------------|--------------|-------------------|----------------|
| Conception/Planning | Research and validation intent | Budget for planning, timeline, no commitments yet | Wedding venue research |
| Investigation | Information gathering and analysis | Use approved methods, document findings | Surf destination evaluation |
| Design/Architecture | Detailed planning and specification | Follow industry standards, get stakeholder approval | Kitchen layout design |
| Vendor/Team Selection | Evaluation and contracting | Use approved vendors, budget limits, background checks | Contractor hiring |
| Preparation | Setup and staging | Permit requirements, safety protocols, coordination | Construction site prep |
| Execution/Build | Active implementation | No disruption to operations, maintain safety, daily progress | Restaurant buildout |
| Inspection/Testing | Quality verification | Pass all inspections, meet standards, document results | Building final inspection |
| Completion/Handoff | Final delivery and closeout | Complete punch list, training, documentation | Event day execution |
| Optimization/Refinement | Improvement after delivery | Maintain stability, limited scope, budget constraints | Post-wedding vendor reviews |
| Crisis Response | Emergency remediation | Minimal changes, rapid action, safety first | Health violation correction |

**Key Principle:** Commander's Intent defines **what to achieve**, project phases define **when and how to think about it**.

**Constraints Across Phases:**
- **Early phases (Planning, Research):** Constraints focus on research scope, timeline, budget for planning, stakeholder approval
- **Middle phases (Design, Selection):** Constraints focus on standards compliance, regulatory requirements, review gates
- **Late phases (Build, Execution):** Constraints focus on operational limits (no disruption, safety, resource availability)
- **Crisis/Emergency:** Constraints are strictest (minimal changes, rapid response, regulatory compliance, safety paramount)

## Practical Implementation

### Documentation Format

Commander's Intent should be documented and shared with all stakeholders and executors. Here's a recommended format:

```yaml
# Wedding Planning Intent Document
version: 1.0
created: 2025-06-01
updated: 2025-08-15
project: "Smith-Johnson Wedding"

purpose: "Create memorable celebration within budget"

key_tasks:
  - id: task-1
    description: "Venue secured with deposit and contract signed"
    priority: 1
    status: completed
    owner: "Lead Coordinator"
  - id: task-2
    description: "Core vendors contracted (catering, photography, music)"
    priority: 2
    status: in_progress
    owner: "Vendor Coordinator"
  - id: task-3
    description: "Guest accommodations arranged for out-of-town attendees"
    priority: 3
    status: pending
    owner: "Guest Services Coordinator"

end_state:
  conditions:
    - "150 guests attended ceremony and reception"
    - "Event proceeded according to timeline without major disruptions"
    - "All contracted vendors delivered services as agreed"
    - "Venue returned in acceptable condition"
    - "Total cost within 5% of $50,000 budget"

constraints:
  proscriptive:
    - "Must accommodate vegetarian and gluten-free dietary needs"
    - "Must comply with venue regulations (decorations, noise, alcohol)"
    - "Must provide accessible facilities for mobility-limited guests"
  prohibitive:
    - "Cannot exceed venue capacity (max 200, planned for 150)"
    - "Cannot serve alcohol to minors"
    - "Cannot play amplified music after 10 PM"
    - "Cannot exceed total budget of $50,000"
  resource:
    - "Budget: $50,000 total allocation"
    - "Team: 2 coordinators plus family volunteers"
    - "Timeline: 6 months planning period"
  temporal:
    - "Vendor contracts must be signed 3 months before event"
    - "Final headcount due 2 weeks before event"
    - "Setup must complete by 3 PM, ceremony at 5 PM"

decision_authority:
  autonomous:
    - "Decoration selections and color scheme"
    - "Music playlist within genre preferences"
    - "Seating arrangements"
  requires_approval:
    - "Adding guests beyond 150 count"
    - "Budget reallocation between major categories"
    - "Changing venue or date"

status: active
project_manager: "Sarah Johnson"
stakeholders: ["Bride", "Groom", "Both Families"]
parent_intent: null
child_intents: ["florist-intent", "catering-intent", "photography-intent"]
```

### Communication Tools

**Briefing Format:**
When briefing team members or vendors, use this structure:
1. State the purpose (the "why")
2. List key tasks (the "what")
3. Describe end state (the "done")
4. Clarify constraints (the "boundaries")
5. Define decision authority (the "freedom")

**Status Updates:**
Regular check-ins should reference:
- Which key tasks are complete
- Progress toward end state
- Any constraints being challenged
- Decisions made autonomously vs. requiring approval

**Delegation Pattern:**
When delegating to specialists:
```markdown
INTENT BRIEFING FOR [SPECIALIST]

Purpose: [Why this work matters to overall objective]

Your Key Tasks:
1. [Task 1]
2. [Task 2]
3. [Task 3]

Success Looks Like:
- [Observable condition 1]
- [Observable condition 2]

Your Constraints:
- Must: [Proscriptive constraints]
- Cannot: [Prohibitive constraints]
- Resources: [Budget, time, materials]
- Timeline: [Deadlines]

Your Decision Authority:
- You Decide: [Areas of autonomy]
- Get Approval For: [Escalation points]

Questions before you begin?
```

## Further Reading

### Military Doctrine (Origin of Pattern)
- U.S. Army Field Manual 6-0 (Mission Command) - Defines Commander's Intent framework
- NATO Allied Joint Publication AJP-5 (Operational Planning) - Chapter 3: Mission Analysis and Constraints
- U.S. Marine Corps MCDP 1 (Warfighting) - Mission tactics and constraint management

### Leadership and Management
- "Turn The Ship Around!" by L. David Marquet (intent-based leadership in Navy submarine)
- "Team of Teams" by General Stanley McChrystal (decentralized command, lessons from Iraq)
- "Extreme Ownership" by Jocko Willink & Leif Babin (decentralized command in SEAL teams)

### Project Management
- "A Guide to the Project Management Body of Knowledge (PMBOK)" - PMI standards
- "PRINCE2" - Structured project management methodology
- "Critical Chain" by Eliyahu M. Goldratt (constraint management in projects)

### Event Planning and Coordination
- "The Wedding Planner's Guide to Delegation" - Managing vendor teams with clear intent
- "Event Management Body of Knowledge" - Professional event coordination standards

### Construction Management
- "Construction Management Fundamentals" by Kraig Knutson (delegation and coordination)
- "Lean Construction" by Glenn Ballard (constraint-based planning)

### Risk and Constraint Management
- "The Checklist Manifesto" by Atul Gawande (using constraints to prevent failures)
- NASA Systems Engineering Handbook - Constraint management in complex systems
- "Managing Risk in Construction Projects" - Proactive constraint identification

### Expedition and Adventure Planning
- "Mountaineering: The Freedom of the Hills" - Planning and leading backcountry expeditions
- "Deep Survival" by Laurence Gonzales (decision-making under uncertainty)
- "The Ledge" by Jim Davidson (leadership and intent in mountain rescue)

---

**File UUID:** 7f3c4a2b-9e1d-4f8a-b6c3-5d7e8f9a0b1c
**Version:** 2.0
**Last Updated:** 2026-02-12
**Owner:** Claude Code / Hopper Labs
