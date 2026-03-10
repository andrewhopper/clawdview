# Work Back Plan (WBP) Agent

<!-- File UUID: 8d4b5e9f-2c7a-4f1b-9e3d-6a8c7b9d0e2f -->

## Overview

**Work Back Plan (WBP)** is a reverse planning methodology that starts with the desired end state and works backward to the present, identifying critical milestones, dependencies, decision points, and potential failure modes along the way.

Also known as: Backward Planning, Reverse Planning, End-State Planning

## Core Principles

### 1.0 Start with the End
Define the precise end state first, then work backward to determine what must happen before that.

### 2.0 Critical Path Focus
Identify the longest chain of dependent activities - this determines minimum timeline.

### 3.0 Decision Points
Mark where choices must be made and what information is needed to make them.

### 4.0 Risk Mitigation
At each step backward, identify what could go wrong and how to prevent or recover.

## When to Invoke WBP Agent

### ✅ INVOKE When:
1. **Fixed Deadline:** "Need to open restaurant by March 1st", "Wedding date is June 15th" - timeline is constraint
2. **Complex Dependencies:** Multiple contractors, vendors, or stakeholders involved
3. **High Stakes:** Event launches, inspections, grand openings, expeditions to remote locations
4. **Unclear Path:** Multiple possible approaches, need to evaluate backward from goal
5. **Resource Planning:** Need to know when to start and what resources to commit
6. **Risk Assessment:** Want to identify failure modes before they occur
7. **Milestone Coordination:** Managing renovation during occupancy, coordinating with family availability
8. **Multi-Phase Projects:** Construction with weather constraints, conference with speaker dependencies

### ❌ DON'T INVOKE When:
1. **Simple Linear Task:** "Pick up dry cleaning" - just do it
2. **Exploratory Work:** Researching vacation destinations with no fixed dates
3. **Already Clear Forward Plan:** If you know exactly what to do next
4. **Trivial Operations:** Daily routines, basic household tasks

## WBP Template

```yaml
# Work Back Plan Template

end_state:
  description: "[Concrete, measurable outcome]"
  success_criteria:
    - "[Observable condition 1]"
    - "[Observable condition 2]"
  date: "[Target completion date/time]"
  owner: "[Who owns the end state]"

critical_path:
  # Start from end, work backward
  - milestone: "M5: End State Achieved"
    description: "[Final milestone description]"
    target_date: "[Date]"
    duration: "0d"
    owner: "[Owner]"

  - milestone: "M4: [Previous milestone]"
    description: "[What must be done before M5]"
    target_date: "[M5.date - duration]"
    duration: "[Time required]"
    dependencies: ["M3"]
    owner: "[Owner]"
    potential_issues:
      - issue: "[What could go wrong]"
        probability: "[low/medium/high]"
        impact: "[low/medium/high]"
        mitigation: "[How to prevent or recover]"

  - milestone: "M3: [Previous milestone]"
    description: "[What must be done before M4]"
    target_date: "[M4.date - duration]"
    duration: "[Time required]"
    dependencies: ["M2", "M1"]
    owner: "[Owner]"
    decision_point:
      question: "[What needs to be decided]"
      options: ["[Option A]", "[Option B]"]
      info_needed: "[What info is needed to decide]"
      deadline: "[When decision must be made]"
    potential_issues:
      - issue: "[What could go wrong]"
        probability: "[low/medium/high]"
        impact: "[low/medium/high]"
        mitigation: "[How to prevent or recover]"

  - milestone: "M2: [Earlier milestone]"
    # ... continue backward

  - milestone: "M1: Project Start"
    target_date: "[Calculated start date]"
    duration: "0d"

most_likely_course:
  description: "[Narrative of expected path from start to finish]"
  assumptions:
    - "[Assumption 1]"
    - "[Assumption 2]"

alternate_paths:
  - trigger: "[What event causes deviation]"
    path: "[How plan changes]"
    impact: "[Effect on timeline/resources]"

resource_requirements:
  - resource: "[Person/team/service]"
    needed_from: "[Date]"
    needed_until: "[Date]"
    allocation: "[hours/percentage]"

risks:
  # Prioritized by (probability × impact)
  - risk: "[Description]"
    probability: "[low/medium/high]"
    impact: "[low/medium/high]"
    score: "[1-9]"
    owner: "[Who monitors this]"
    indicators: ["[Early warning sign 1]", "[Early warning sign 2]"]
    mitigation: "[Proactive steps]"
    contingency: "[Reactive response if occurs]"

go_no_go_gates:
  - gate: "[Gate name]"
    date: "[Date]"
    criteria: ["[Must have 1]", "[Must have 2]"]
    decision_maker: "[Who decides]"
    if_no_go: "[What happens if we can't proceed]"

slack_buffer:
  total_duration: "[Critical path duration]"
  buffer_available: "[Time from start to deadline minus critical path]"
  buffer_allocation:
    - milestone: "[Milestone]"
      buffer: "[Buffer time]"
      reason: "[Why buffer needed here]"
```

## Example A: Wedding Planning WBP

```yaml
# Work Back Plan: Wedding Celebration

end_state:
  description: "Memorable wedding celebration executed within budget"
  success_criteria:
    - "Ceremony and reception completed successfully"
    - "All guests accommodated and fed"
    - "Photography captured all key moments"
    - "Event concluded on time and within budget"
  date: "2025-06-15 15:00"
  owner: "Bride & Groom"

critical_path:
  - milestone: "M8: Ceremony and Reception Completed"
    description: "Wedding concluded, guests departed, venue restored"
    target_date: "2025-06-15 22:00"
    duration: "7h"
    owner: "Wedding Coordinator"
    potential_issues:
      - issue: "Ceremony runs long, delays reception schedule"
        probability: "medium"
        impact: "medium"
        mitigation: "Build 15-minute buffer between ceremony and reception, rehearse ceremony timing"
      - issue: "Vendor no-show on day of event"
        probability: "low"
        impact: "critical"
        mitigation: "Confirm all vendors 48 hours before, maintain backup vendor contacts"

  - milestone: "M7: Final Walkthrough Completed"
    description: "Venue inspected, setup confirmed, all vendor access arranged"
    target_date: "2025-06-14 16:00"
    duration: "2h"
    dependencies: ["M6"]
    owner: "Wedding Coordinator"
    go_no_go_gate: true
    decision_point:
      question: "Is venue ready for event execution?"
      criteria:
        - "All setup requirements confirmed"
        - "Vendor access and timing coordinated"
        - "Backup plans in place for weather"
      decision_maker: "Wedding Coordinator"
      if_no_go: "Address critical gaps, may need to adjust day-of timeline"

  - milestone: "M6: All Vendors Confirmed and Final Payments Made"
    description: "Caterer, photographer, DJ, florist all confirmed for event date"
    target_date: "2025-06-01"
    duration: "1 week"
    dependencies: ["M5"]
    owner: "Bride & Groom"
    potential_issues:
      - issue: "Vendor cancellation within 2 weeks of event"
        probability: "low"
        impact: "high"
        mitigation: "Maintain backup vendor list, confirm all vendors 2 weeks prior"

  - milestone: "M5: Dress Alterations Completed"
    description: "Wedding dress fitted perfectly, ready to wear"
    target_date: "2025-05-15"
    duration: "3 weeks"
    dependencies: ["M4"]
    owner: "Bride"
    potential_issues:
      - issue: "Alterations require more time than expected"
        probability: "medium"
        impact: "medium"
        mitigation: "Schedule final fitting 4 weeks before wedding, not 2 weeks"

  - milestone: "M4: Menu Finalized with Caterer"
    description: "Full menu approved, dietary restrictions accommodated, tasting completed"
    target_date: "2025-04-15"
    duration: "2 weeks"
    dependencies: ["M3"]
    owner: "Bride & Groom"
    decision_point:
      question: "Buffet or plated service?"
      options: ["Buffet (lower cost, more variety)", "Plated (formal, predictable timing)", "Hybrid (stations + plated)"]
      info_needed: "Guest count finalized, venue logistics confirmed"
      deadline: "2025-04-15"

  - milestone: "M3: Guest List Finalized, Invitations Mailed"
    description: "All invitations sent, RSVP deadline set for 6 weeks before event"
    target_date: "2025-04-01"
    duration: "2 weeks"
    dependencies: ["M2"]
    owner: "Bride & Groom"
    potential_issues:
      - issue: "Guest count exceeds venue capacity"
        probability: "medium"
        impact: "high"
        mitigation: "Set realistic guest limit based on venue capacity, prioritize must-invite list"

  - milestone: "M2: Venue Selected and Deposit Paid"
    description: "Wedding venue secured, date reserved, contract signed"
    target_date: "2024-12-01"
    duration: "6 weeks"
    dependencies: ["M1"]
    owner: "Bride & Groom"
    potential_issues:
      - issue: "Preferred venue unavailable for desired date"
        probability: "medium"
        impact: "high"
        mitigation: "Have 3 venue options ready, be flexible on exact date (Sat vs Sun)"

  - milestone: "M1: Budget and Guest Count Determined"
    description: "Total budget set, expected guest count estimated, priorities defined"
    target_date: "2024-11-01"
    duration: "2 weeks"
    owner: "Bride & Groom"

most_likely_course:
  description: |
    Planning begins November 2024 with budget discussion and guest list brainstorming.
    Venue search starts immediately, with top venue secured by December 1st. Guest list
    finalized and invitations ordered in January 2025, mailed by April 1st. RSVP deadline
    is May 1st, providing 6 weeks notice to caterer. Menu tasting in March, final menu
    confirmed April 15th. Dress shopping in February, alterations completed by May 15th.
    All vendor final confirmations by June 1st. Final walkthrough June 14th. Wedding day
    June 15th starting at 3pm, reception until 10pm.
  assumptions:
    - "No major family conflicts on chosen date"
    - "Preferred venue available within budget"
    - "No vendor cancellations close to event"
    - "Weather cooperates (outdoor ceremony has indoor backup)"

alternate_paths:
  - trigger: "Venue unavailable for preferred date"
    path: "Adjust wedding date by 1-2 weeks OR select alternative venue"
    impact: "Timeline shifts by 2 weeks, some vendor availability may change"

  - trigger: "Guest count exceeds budget after RSVPs"
    path: "Adjust menu to lower-cost option OR reduce guest amenities"
    impact: "Menu changes require 2-week notice to caterer"

  - trigger: "Key vendor cancels within 2 weeks"
    path: "Activate backup vendor from pre-qualified list"
    impact: "May require style adjustments, possible increased cost"

resource_requirements:
  - resource: "Wedding Coordinator"
    needed_from: "2025-05-01"
    needed_until: "2025-06-15"
    allocation: "10 hours/week, 100% day-of"

  - resource: "Family Volunteers (Setup Team)"
    needed_from: "2025-06-14"
    needed_until: "2025-06-15"
    allocation: "6 people, 4 hours each"

  - resource: "Venue Event Manager"
    needed_from: "2025-06-14"
    needed_until: "2025-06-15"
    allocation: "100%"

risks:
  - risk: "Outdoor ceremony rained out"
    probability: "medium"
    impact: "high"
    score: 6
    owner: "Wedding Coordinator"
    indicators:
      - "Weather forecast 3 days prior"
      - "Backup indoor space availability"
    mitigation: "Book venue with indoor backup option, monitor weather starting 1 week before"
    contingency: "Activate indoor ceremony plan, adjust seating layout"

  - risk: "Guest count significantly higher than expected"
    probability: "medium"
    impact: "high"
    score: 6
    owner: "Bride & Groom"
    indicators:
      - "RSVP rate exceeds 80% (expected 70%)"
      - "Late RSVPs arriving"
    mitigation: "Set clear RSVP deadline, follow up with non-responders"
    contingency: "Adjust catering order by May 15th, use overflow seating plan"

  - risk: "Photographer cancellation"
    probability: "low"
    impact: "high"
    score: 3
    owner: "Bride"
    indicators:
      - "Photographer misses check-in calls"
      - "Suspicious communication patterns"
    mitigation: "Confirm photographer 2 weeks and 48 hours before event"
    contingency: "Have backup photographer contact ready, assign guest to capture iPhone photos"

go_no_go_gates:
  - gate: "Venue Confirmation"
    date: "2024-12-01"
    criteria:
      - "Venue contract signed"
      - "Date secured and deposit paid"
      - "Venue capacity matches guest list"
    decision_maker: "Bride & Groom"
    if_no_go: "Reconsider date, expand venue search, or reduce guest count"

  - gate: "Budget Check"
    date: "2025-05-01"
    criteria:
      - "Total committed expenses within 90% of budget"
      - "10% buffer remaining for surprises"
      - "All critical vendors booked"
    decision_maker: "Bride & Groom"
    if_no_go: "Cut optional elements (favors, extras) or reduce guest count"

  - gate: "Final Walkthrough"
    date: "2025-06-14"
    criteria:
      - "Venue setup confirmed"
      - "All vendors confirmed for correct time"
      - "Weather backup plan ready if needed"
    decision_maker: "Wedding Coordinator"
    if_no_go: "Address critical gaps, may need to adjust day-of timeline"

slack_buffer:
  total_duration: "7.5 months"
  critical_path_duration: "7 months"
  buffer_available: "2 weeks"
  buffer_allocation:
    - milestone: "M5: Dress Alterations"
      buffer: "1 week"
      reason: "Alterations often take longer than quoted"
    - milestone: "M6: Vendor Confirmations"
      buffer: "1 week"
      reason: "Buffer for vendor changes or last-minute adjustments"

  recommendation: "Buffer is adequate for wedding planning timeline"
```

## Example B: Home Renovation WBP

```yaml
# Work Back Plan: Kitchen Renovation

end_state:
  description: "Kitchen renovation completed before holidays"
  success_criteria:
    - "All appliances installed and operational"
    - "Final inspection passed, occupancy permitted"
    - "Kitchen fully functional for holiday cooking"
    - "Project completed within budget"
  date: "2025-11-20"
  owner: "Homeowner"

critical_path:
  - milestone: "M7: Final Inspection Passed"
    description: "Building inspector approves all work, occupancy permit issued"
    target_date: "2025-11-20"
    duration: "1 day"
    dependencies: ["M6"]
    owner: "General Contractor"
    potential_issues:
      - issue: "Inspector identifies code violations"
        probability: "medium"
        impact: "high"
        mitigation: "Schedule pre-inspection walkthrough 1 week before final inspection"

  - milestone: "M6: All Finishes Installed"
    description: "Countertops, backsplash, fixtures, flooring complete"
    target_date: "2025-11-13"
    duration: "1 week"
    dependencies: ["M5"]
    owner: "Finish Contractors"
    potential_issues:
      - issue: "Countertop fabrication delayed"
        probability: "medium"
        impact: "medium"
        mitigation: "Order countertops 4 weeks in advance, not 2 weeks"

  - milestone: "M5: Cabinets Installed, Rough-In Complete"
    description: "Cabinets mounted, plumbing and electrical rough-in inspected and approved"
    target_date: "2025-11-06"
    duration: "1 week"
    dependencies: ["M4"]
    owner: "Cabinet Installer, Licensed Plumber, Licensed Electrician"
    go_no_go_gate: true
    decision_point:
      question: "Did rough-in inspection pass?"
      criteria:
        - "Electrical rough-in approved"
        - "Plumbing rough-in approved"
        - "Cabinets level and secure"
      decision_maker: "General Contractor"
      if_no_go: "Correct violations, schedule re-inspection (adds 3-5 days)"

  - milestone: "M4: Demolition Complete, Walls Framed"
    description: "Old kitchen removed, new walls framed, ready for rough-in"
    target_date: "2025-10-30"
    duration: "1 week"
    dependencies: ["M3"]
    owner: "General Contractor"
    potential_issues:
      - issue: "Unexpected structural issues discovered"
        probability: "medium"
        impact: "high"
        mitigation: "Conduct pre-demo inspection, budget extra $2-3K for surprises"

  - milestone: "M3: Materials Ordered and Delivery Scheduled"
    description: "Cabinets, countertops, appliances, fixtures ordered with delivery dates"
    target_date: "2025-09-30"
    duration: "2 weeks"
    dependencies: ["M2"]
    owner: "Homeowner + General Contractor"
    potential_issues:
      - issue: "Material delivery delay due to supply chain"
        probability: "medium"
        impact: "high"
        mitigation: "Order materials 6 weeks in advance, identify alternative suppliers"

  - milestone: "M2: Contractor Selected, Contract Signed"
    description: "General contractor hired, scope and budget agreed, permits filed"
    target_date: "2025-09-15"
    duration: "3 weeks"
    dependencies: ["M1"]
    owner: "Homeowner"
    decision_point:
      question: "Which contractor to hire?"
      options: ["Lowest bid", "Best references", "Fastest timeline"]
      info_needed: "3+ contractor bids, reference checks, portfolio review"
      deadline: "2025-09-15"

  - milestone: "M1: Design Finalized, Permits Obtained"
    description: "Kitchen layout approved, all materials selected, building permits issued"
    target_date: "2025-08-25"
    duration: "4 weeks"
    owner: "Homeowner + Designer"
    potential_issues:
      - issue: "Permit approval delayed by city"
        probability: "medium"
        impact: "medium"
        mitigation: "Submit permits early, work with expediter if needed"

most_likely_course:
  description: |
    Design work begins late July 2025, finalized by August 25th with permits in hand.
    Contractor selection in September (3 bids, reference checks), signed by Sept 15th.
    Materials ordered by Sept 30th with 4-6 week lead times. Demo week of Oct 30th,
    rough-in first week of November, cabinets installed Nov 6th, finishes Nov 13th,
    final inspection Nov 20th. Kitchen ready for Thanksgiving Nov 27th.
  assumptions:
    - "No unexpected structural issues during demo"
    - "Material delivery on time (6-week lead time)"
    - "All inspections pass first try"
    - "Contractor availability aligns with timeline"

alternate_paths:
  - trigger: "Material delivery delayed 3+ weeks"
    path: "Adjust timeline OR source alternative materials"
    impact: "Project completion moves to Dec 15th"

  - trigger: "Structural issues discovered during demo"
    path: "Add structural remediation phase (1 week + $3-5K)"
    impact: "Pushes completion to Dec 1st"

  - trigger: "Rough-in inspection fails"
    path: "Correct violations, re-inspect (3-5 days)"
    impact: "Minor delay, may still hit Nov 20th with compressed finish schedule"

resource_requirements:
  - resource: "General Contractor"
    needed_from: "2025-10-30"
    needed_until: "2025-11-20"
    allocation: "100%"

  - resource: "Licensed Electrician"
    needed_from: "2025-10-30"
    needed_until: "2025-11-06"
    allocation: "50%"

  - resource: "Licensed Plumber"
    needed_from: "2025-10-30"
    needed_until: "2025-11-06"
    allocation: "50%"

  - resource: "Cabinet Installer"
    needed_from: "2025-11-06"
    needed_until: "2025-11-13"
    allocation: "100%"

risks:
  - risk: "Unexpected structural issues (rot, termites, outdated wiring)"
    probability: "medium"
    impact: "high"
    score: 6
    owner: "General Contractor"
    indicators:
      - "Home age over 30 years"
      - "Visible water damage or sagging"
    mitigation: "Budget $3-5K contingency, conduct pre-demo inspection"
    contingency: "Address structural issues before continuing, accept delayed timeline"

  - risk: "Material delivery delay"
    probability: "medium"
    impact: "high"
    score: 6
    owner: "Homeowner"
    indicators:
      - "Supplier quotes 6+ week lead time"
      - "Supply chain news mentions delays"
    mitigation: "Order materials 6 weeks in advance, identify backup suppliers"
    contingency: "Source alternative materials OR accept delayed completion"

  - risk: "Inspection failure requiring rework"
    probability: "medium"
    impact: "medium"
    score: 4
    owner: "General Contractor"
    indicators:
      - "Contractor unfamiliar with local code"
      - "Complex electrical or plumbing changes"
    mitigation: "Hire licensed electrician/plumber, schedule pre-inspection walkthrough"
    contingency: "Correct violations immediately, schedule re-inspection"

go_no_go_gates:
  - gate: "Design and Budget Approval"
    date: "2025-08-25"
    criteria:
      - "Design finalized and approved by homeowner"
      - "Budget confirmed and financing secured"
      - "Permits obtained from city"
    decision_maker: "Homeowner"
    if_no_go: "Revise design, secure financing, or delay project start"

  - gate: "Rough-In Inspection"
    date: "2025-11-06"
    criteria:
      - "Electrical rough-in passes inspection"
      - "Plumbing rough-in passes inspection"
      - "Framing approved by inspector"
    decision_maker: "General Contractor"
    if_no_go: "Correct violations, schedule re-inspection (adds 3-5 days)"

slack_buffer:
  total_duration: "12 weeks"
  critical_path_duration: "10 weeks"
  buffer_available: "2 weeks"
  buffer_allocation:
    - milestone: "M3: Materials Ordering"
      buffer: "1 week"
      reason: "Supply chain delays common, need buffer for material sourcing"
    - milestone: "M4: Demo and Framing"
      buffer: "1 week"
      reason: "High probability of discovering unexpected structural issues"

  recommendation: "Buffer adequate for typical renovation surprises"
```

## Example C: Surf Expedition WBP

```yaml
# Work Back Plan: Remote Surf Expedition

end_state:
  description: "Successful surf trip to remote location"
  success_criteria:
    - "Surf sessions completed at target breaks"
    - "All travelers return safely with equipment"
    - "Trip completed within budget"
    - "Memorable surf experiences captured"
  date: "2025-12-15"
  owner: "Trip Organizer"

critical_path:
  - milestone: "M6: Return Home Safely"
    description: "All travelers and equipment back home, no injuries or losses"
    target_date: "2025-12-15"
    duration: "Travel day"
    dependencies: ["M5"]
    owner: "Trip Organizer"

  - milestone: "M5: Surf Sessions Completed"
    description: "Multiple sessions at target breaks, captured on video/photo"
    target_date: "2025-12-14"
    duration: "7 days"
    dependencies: ["M4"]
    owner: "Trip Organizer"
    potential_issues:
      - issue: "Swell doesn't arrive as forecasted"
        probability: "medium"
        impact: "high"
        mitigation: "Book trip during peak swell season, have backup breaks identified"
      - issue: "Equipment damage (board ding, leash break)"
        probability: "high"
        impact: "medium"
        mitigation: "Bring repair kit, backup leash, travel insurance for boards"

  - milestone: "M4: Arrive at Destination, Equipment Checked"
    description: "All travelers arrived, boards intact, accommodations confirmed"
    target_date: "2025-12-07"
    duration: "Travel day"
    dependencies: ["M3"]
    owner: "Trip Organizer"
    potential_issues:
      - issue: "Lost luggage (surfboards)"
        probability: "low"
        impact: "high"
        mitigation: "Use board bags with GPS trackers, travel with carry-on essentials"
      - issue: "Flight cancellation"
        probability: "medium"
        impact: "high"
        mitigation: "Book refundable flights, arrive 1 day early before peak swell"

  - milestone: "M3: International Flights Booked"
    description: "Round-trip flights confirmed for all travelers"
    target_date: "2025-10-01"
    duration: "1 week"
    dependencies: ["M2"]
    owner: "Trip Organizer"
    decision_point:
      question: "Which airport/route to use?"
      options: ["Direct flight (expensive, fast)", "Connecting flight (cheaper, longer)", "Alternate airport (cheaper, more drive time)"]
      info_needed: "Flight prices, travel time comparison, group budget"
      deadline: "2025-10-01"

  - milestone: "M2: Accommodations Secured Near Surf Breaks"
    description: "Lodging booked within 15 minutes of target surf breaks"
    target_date: "2025-09-15"
    duration: "2 weeks"
    dependencies: ["M1"]
    owner: "Trip Organizer"
    potential_issues:
      - issue: "Accommodations fully booked for peak season"
        probability: "high"
        impact: "medium"
        mitigation: "Book 6+ months in advance, have 3 lodging options ready"

  - milestone: "M1: Destination Selected Based on Swell Forecast"
    description: "Target destination chosen based on historical swell data for December"
    target_date: "2025-09-01"
    duration: "2 weeks"
    owner: "Trip Organizer"
    decision_point:
      question: "Which destination to target?"
      options: ["Indonesia (consistent, crowded)", "Central America (easier travel, smaller waves)", "Pacific Islands (remote, expensive)"]
      info_needed: "Historical swell data, travel costs, group skill level"
      deadline: "2025-09-01"

most_likely_course:
  description: |
    Trip planning begins September 2025 with destination selection based on December swell
    forecasts. Indonesia chosen for consistent surf. Accommodations booked mid-September
    near target breaks (Uluwatu, Padang Padang). Flights booked October 1st with arrival
    Dec 7th. Equipment packed with board bags and repair kits. Surf sessions Dec 8-14 at
    various breaks depending on swell/wind. Return flights Dec 15th.
  assumptions:
    - "December swell arrives as forecasted"
    - "No flight cancellations or major delays"
    - "Accommodations match listing descriptions"
    - "No major equipment damage in transit"

alternate_paths:
  - trigger: "Swell forecast changes significantly"
    path: "Pivot to alternate destination OR adjust travel dates"
    impact: "May need to rebook flights and accommodations (loss of deposits)"

  - trigger: "Flight cancellation"
    path: "Book emergency alternate flight OR extend trip by 1 day"
    impact: "Additional $500-1000 per person, less surf time"

  - trigger: "Accommodations fall through"
    path: "Book backup lodging (may be farther from breaks)"
    impact: "More driving time, less convenient surf access"

resource_requirements:
  - resource: "Trip Organizer (Logistics Coordinator)"
    needed_from: "2025-09-01"
    needed_until: "2025-12-15"
    allocation: "5 hours/week planning, 100% during trip"

  - resource: "Surf Guide (Local Knowledge)"
    needed_from: "2025-12-07"
    needed_until: "2025-12-14"
    allocation: "As needed for break selection"

risks:
  - risk: "Swell doesn't materialize (flat conditions)"
    probability: "medium"
    impact: "critical"
    score: 6
    owner: "Trip Organizer"
    indicators:
      - "Long-range swell models not showing activity"
      - "Local surf reports indicating flat period"
    mitigation: "Book trip during peak swell season, have backup breaks for different swell directions"
    contingency: "Adjust expectations, explore different breaks, extend trip if possible"

  - risk: "Board damage in transit"
    probability: "high"
    impact: "medium"
    score: 6
    owner: "Each Traveler"
    indicators:
      - "Rough baggage handling observed"
      - "Board bag feels lighter than expected"
    mitigation: "Use padded board bags, travel insurance, bring repair kit"
    contingency: "Repair board at destination (surf shops common) OR rent backup board"

  - risk: "Injury during surf session"
    probability: "medium"
    impact: "high"
    score: 6
    owner: "Trip Organizer"
    indicators:
      - "Large swell, heavy waves"
      - "Shallow reef breaks"
    mitigation: "Surf within skill level, use reef booties, travel medical insurance"
    contingency: "Seek medical attention, may end trip early for injured traveler"

  - risk: "Lost luggage/surfboards"
    probability: "low"
    impact: "high"
    score: 3
    owner: "Each Traveler"
    indicators:
      - "Flight connections very tight (<2 hours)"
      - "International transfer points"
    mitigation: "Use GPS trackers in board bags, arrive 1 day early"
    contingency: "File claim immediately, rent boards while waiting for luggage"

go_no_go_gates:
  - gate: "Destination Selection"
    date: "2025-09-01"
    criteria:
      - "Swell forecast favorable for December"
      - "Accommodations available near breaks"
      - "Group budget supports destination choice"
    decision_maker: "Trip Organizer + Group Consensus"
    if_no_go: "Select alternate destination or adjust travel dates"

  - gate: "Flight Booking"
    date: "2025-10-01"
    criteria:
      - "Flights within budget"
      - "Arrival timing aligns with peak swell window"
      - "All travelers can commit to dates"
    decision_maker: "Trip Organizer"
    if_no_go: "Adjust dates or destination based on flight availability/cost"

slack_buffer:
  total_duration: "3.5 months"
  critical_path_duration: "3 months"
  buffer_available: "2 weeks"
  buffer_allocation:
    - milestone: "M2: Accommodations"
      buffer: "1 week"
      reason: "Peak season lodging may require extra search time"
    - milestone: "M3: Flights"
      buffer: "1 week"
      reason: "Flight prices fluctuate, may need to wait for deals"

  recommendation: "Buffer adequate for surf trip planning timeline"
```

## WBP Process Flow

```
┌─────────────────────────────────────────────────────────┐
│                    WBP PROCESS FLOW                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. DEFINE END STATE                                    │
│     ↓                                                   │
│     • What does success look like?                      │
│     • When must it be achieved?                         │
│     • Who owns the outcome?                             │
│                                                         │
│  2. IDENTIFY FINAL MILESTONE (M_n)                      │
│     ↓                                                   │
│     • Last action before end state                      │
│     • Duration to complete                              │
│     • Dependencies (what must be done before)           │
│                                                         │
│  3. WORK BACKWARD TO PREVIOUS MILESTONE (M_n-1)         │
│     ↓                                                   │
│     • What must happen before M_n?                      │
│     • How long does it take?                            │
│     • Who owns it?                                      │
│     • What could go wrong?                              │
│     • Any decisions needed?                             │
│                                                         │
│  4. REPEAT BACKWARD TO START (M_1)                      │
│     ↓                                                   │
│     • Continue until reaching present/start date        │
│     • Each milestone identifies dependencies            │
│                                                         │
│  5. CALCULATE CRITICAL PATH                             │
│     ↓                                                   │
│     • Sum durations of dependent milestones             │
│     • Identify longest path (critical path)             │
│     • Determines minimum timeline                       │
│                                                         │
│  6. IDENTIFY PARALLEL TRACKS                            │
│     ↓                                                   │
│     • What can happen concurrently?                     │
│     • Optimize timeline by parallelizing                │
│                                                         │
│  7. ADD DECISION POINTS                                 │
│     ↓                                                   │
│     • Where do we need to choose path?                  │
│     • What info needed to decide?                       │
│     • When must decision be made?                       │
│                                                         │
│  8. ASSESS RISKS AT EACH MILESTONE                      │
│     ↓                                                   │
│     • What could prevent this milestone?                │
│     • Probability × Impact = Risk Score                 │
│     • Mitigation plan                                   │
│     • Contingency plan                                  │
│                                                         │
│  9. ALLOCATE SLACK BUFFER                               │
│     ↓                                                   │
│     • Total time - critical path = available buffer     │
│     • Assign buffer to high-risk milestones             │
│     • Typical: 20-30% buffer for complex projects       │
│                                                         │
│  10. DEFINE GO/NO-GO GATES                              │
│      ↓                                                  │
│      • Where should we validate before proceeding?      │
│      • What are the criteria?                           │
│      • What happens if we don't meet them?              │
│                                                         │
│  11. DOCUMENT MOST LIKELY COURSE                        │
│      ↓                                                  │
│      • Narrative of expected execution                  │
│      • Assumptions made                                 │
│      • Alternate paths if assumptions wrong             │
│                                                         │
│  12. VALIDATE FEASIBILITY                               │
│      ↓                                                  │
│      • Can we start early enough?                       │
│      • Do we have resources?                            │
│      • Is timeline realistic?                           │
│      • Do we have enough buffer?                        │
│                                                         │
│  13. GET APPROVAL & EXECUTE                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Integration with Commander's Intent

WBP is the **tactical execution plan** for Commander's Intent:

| Commander's Intent | Work Back Plan |
|--------------------|----------------|
| Purpose (Why) | End State (What) |
| Key Tasks (What) | Critical Path (How & When) |
| End State (Done) | Success Criteria (Measurable) |
| Decision Authority | Decision Points & Go/No-Go Gates |
| Constraints | Risk Assessment & Mitigation |

**Workflow:**
1. User provides goal or intent
2. Commander's Intent agent defines purpose, key tasks, end state
3. WBP agent works backward from end state to create detailed plan
4. Execution agents follow WBP milestones with Commander's Intent as guidance

## Example D: Conference Organization WBP

```yaml
# Work Back Plan: Professional Conference with 500 Attendees

end_state:
  description: "Successful conference with 500 attendees"
  success_criteria:
    - "All sessions delivered as scheduled"
    - "Attendee satisfaction rating exceeds 4.5/5"
    - "Event concludes on time and within budget"
    - "No major incidents or safety issues"
  date: "2025-09-15 17:00"
  owner: "Conference Organizer"

critical_path:
  - milestone: "M7: Conference Concludes, Venue Restored"
    description: "All sessions complete, attendees departed, venue cleaned and returned"
    target_date: "2025-09-15 17:00"
    duration: "2 days (conference duration)"
    dependencies: ["M6"]
    owner: "Event Team"

  - milestone: "M6: Day 1 Completed Successfully"
    description: "Opening keynote delivered, all Day 1 sessions on schedule"
    target_date: "2025-09-14 17:00"
    duration: "1 day"
    dependencies: ["M5"]
    owner: "Event Team"
    potential_issues:
      - issue: "AV equipment failure during keynote"
        probability: "medium"
        impact: "high"
        mitigation: "Full AV tech rehearsal day before, backup equipment on site"

  - milestone: "M5: Registration and Setup Complete"
    description: "Registration desk operational, all rooms set up, signage in place"
    target_date: "2025-09-13 18:00"
    duration: "1 day"
    dependencies: ["M4"]
    owner: "Event Team"
    go_no_go_gate: true
    decision_point:
      question: "Is venue ready for conference opening?"
      criteria:
        - "All session rooms set up correctly"
        - "Registration system tested and working"
        - "Catering confirmed for all meals"
        - "Speaker AV needs confirmed"
      decision_maker: "Conference Organizer"
      if_no_go: "Delay opening by 4 hours, address critical setup gaps"

  - milestone: "M4: All Speakers Confirmed and Materials Ready"
    description: "All speakers confirmed attendance, presentations uploaded, A/V needs documented"
    target_date: "2025-09-01"
    duration: "2 weeks"
    dependencies: ["M3"]
    owner: "Program Committee"
    potential_issues:
      - issue: "Keynote speaker cancels within 2 weeks"
        probability: "low"
        impact: "critical"
        mitigation: "Have backup keynote speaker on standby, confirm 2 weeks before event"

  - milestone: "M3: Venue Contracted, Catering Arranged"
    description: "Conference venue secured, catering contract signed for all meals"
    target_date: "2025-06-01"
    duration: "4 weeks"
    dependencies: ["M2"]
    owner: "Conference Organizer"
    potential_issues:
      - issue: "Venue capacity insufficient after speaker room allocation"
        probability: "medium"
        impact: "high"
        mitigation: "Calculate room allocations before signing venue contract"

  - milestone: "M2: Speaker Lineup Finalized"
    description: "All speakers accepted invitations, session schedule published"
    target_date: "2025-05-01"
    duration: "6 weeks"
    dependencies: ["M1"]
    owner: "Program Committee"
    decision_point:
      question: "How many concurrent tracks?"
      options: ["Single track (simpler, all attendees see same content)", "Dual track (more variety, splits audience)", "Triple track (maximum variety, complex logistics)"]
      info_needed: "Expected attendee count, speaker availability, venue room capacity"
      deadline: "2025-05-01"

  - milestone: "M1: Conference Theme and Format Determined"
    description: "Theme selected, format decided (virtual/hybrid/in-person), budget set"
    target_date: "2025-03-15"
    duration: "4 weeks"
    owner: "Organizing Committee"

most_likely_course:
  description: |
    Planning begins mid-February 2025 with organizing committee forming and budget discussion.
    Conference theme and format finalized March 15th. Speaker outreach begins immediately,
    lineup finalized by May 1st with session schedule. Venue search in April, contract signed
    June 1st. Registration opens July 1st. Speaker confirmations and materials collected in
    August, all confirmed by Sept 1st. Setup day Sept 13th with full tech rehearsal. Conference
    runs Sept 14-15 with closing remarks at 5pm Sept 15th.
  assumptions:
    - "No speaker cancellations within 2 weeks of event"
    - "Venue availability aligns with conference dates"
    - "Registration reaches 500 attendees by August 1st"
    - "No major AV or technical failures during sessions"

alternate_paths:
  - trigger: "Registration significantly below target (< 300 by Aug 1)"
    path: "Reduce venue size OR increase marketing spend OR reduce ticket price"
    impact: "Budget adjustments, possible venue change if <4 weeks notice"

  - trigger: "Keynote speaker cancels within 2 weeks"
    path: "Activate backup speaker OR adjust schedule to promote other session"
    impact: "Marketing materials need update, attendee communication required"

  - trigger: "Venue cancels or becomes unavailable"
    path: "Emergency venue search, may need to adjust date"
    impact: "Could delay conference by 2-4 weeks, speaker re-confirmation needed"

resource_requirements:
  - resource: "Conference Organizer"
    needed_from: "2025-02-15"
    needed_until: "2025-09-15"
    allocation: "20 hours/week, 100% during event"

  - resource: "Program Committee (3 people)"
    needed_from: "2025-03-15"
    needed_until: "2025-09-01"
    allocation: "10 hours/week"

  - resource: "Event Team (5 people)"
    needed_from: "2025-09-13"
    needed_until: "2025-09-15"
    allocation: "100%"

  - resource: "AV Technician"
    needed_from: "2025-09-13"
    needed_until: "2025-09-15"
    allocation: "100%"

risks:
  - risk: "Low registration numbers (< 300 attendees)"
    probability: "medium"
    impact: "high"
    score: 6
    owner: "Conference Organizer"
    indicators:
      - "Registration pace slower than projected"
      - "Early bird tickets not selling"
    mitigation: "Start marketing 4 months before event, offer early bird pricing"
    contingency: "Reduce venue size, cut catering costs, or cancel if < 200 registrations"

  - risk: "Speaker cancellation within 2 weeks of event"
    probability: "low"
    impact: "high"
    score: 3
    owner: "Program Committee"
    indicators:
      - "Speaker stops responding to emails"
      - "Speaker mentions conflicting commitment"
    mitigation: "Confirm all speakers 2 weeks before, have backup speakers identified"
    contingency: "Promote backup speaker or adjust schedule to fill gap"

  - risk: "AV equipment failure during keynote"
    probability: "medium"
    impact: "high"
    score: 6
    owner: "AV Technician"
    indicators:
      - "Equipment showing glitches during rehearsal"
      - "Old or unreliable venue AV systems"
    mitigation: "Full tech rehearsal day before, backup projector and microphones on site"
    contingency: "Switch to backup equipment immediately, brief delay acceptable"

  - risk: "Catering service failure (late delivery, wrong food)"
    probability: "low"
    impact: "medium"
    score: 2
    owner: "Conference Organizer"
    indicators:
      - "Caterer has poor reviews"
      - "Caterer misses planning meetings"
    mitigation: "Use reputable caterer with references, confirm details 1 week before"
    contingency: "Have backup restaurant contacts for emergency food delivery"

go_no_go_gates:
  - gate: "Speaker Lineup Confirmation"
    date: "2025-05-01"
    criteria:
      - "Minimum 20 speakers confirmed"
      - "Keynote speaker committed"
      - "Session schedule balanced and interesting"
    decision_maker: "Program Committee"
    if_no_go: "Delay conference by 4 weeks OR pivot to smaller format"

  - gate: "Registration Threshold"
    date: "2025-08-01"
    criteria:
      - "Minimum 300 registrations received"
      - "Revenue covers 80% of fixed costs"
      - "Venue deposit paid and contract signed"
    decision_maker: "Conference Organizer"
    if_no_go: "Cancel conference (issue refunds) OR reduce scope to smaller venue"

  - gate: "Setup Day Completion"
    date: "2025-09-13"
    criteria:
      - "All session rooms set up and tested"
      - "Registration system operational"
      - "All AV equipment tested with speaker presentations"
    decision_maker: "Event Team Lead"
    if_no_go: "Delay opening by 4 hours to complete setup"

slack_buffer:
  total_duration: "7 months"
  critical_path_duration: "6 months"
  buffer_available: "4 weeks"
  buffer_allocation:
    - milestone: "M2: Speaker Lineup"
      buffer: "2 weeks"
      reason: "Speaker confirmations often take longer than expected"
    - milestone: "M3: Venue and Catering"
      buffer: "1 week"
      reason: "Venue negotiations and contract review may extend timeline"
    - milestone: "M4: Speaker Materials"
      buffer: "1 week"
      reason: "Speakers often late submitting presentations"

  recommendation: "Buffer adequate for conference planning timeline"
```

## WBP for Different Scenarios

### 1.0 Fixed Deadline (Restaurant Opening for Health Inspection)
**Focus:** Work backward from inspection date, ensure critical path fits, add buffer for corrections.

```yaml
end_state: "Health inspection passed, restaurant ready to open"
date: "2025-03-15 09:00 EST"

critical_path:
  - M5: Health inspection passed, certificate issued (target: Mar 15 09:00)
  - M4: Pre-inspection walkthrough completed, all issues corrected (target: Mar 14 17:00) [16h before]
  - M3: Kitchen equipment installed and operational (target: Mar 13 17:00) [2 days before]
  - M2: All permits obtained, final construction complete (target: Mar 10 17:00) [5 days before]
  - M1: Contractor work completed, ready for equipment (target: Mar 6 17:00) [9 days before]
```

### 2.0 Resource-Constrained (Multi-Stop Road Trip with Limited Budget)
**Focus:** Work backward considering budget and time constraints.

```yaml
end_state: "Road trip completed, all destinations visited within budget"
date: "2025-07-10"
budget: "$2,000 total"

critical_path:
  - M5: Return home (requires: $0 remaining, car in good condition)
    target_date: "2025-07-10"
    duration: "1 day drive"
    dependencies: ["M4"]

  - M4: Destination 3 visited (requires: $500 budget remaining for gas/food home)
    target_date: "2025-07-09"
    duration: "2 days"
    dependencies: ["M3"]
    note: "Must stay within daily budget of $150"

  - M3: Destination 2 visited (requires: $800 budget remaining)
    target_date: "2025-07-07"
    duration: "2 days"
    dependencies: ["M2"]
    note: "Camping instead of hotel to save money"

  - M2: Destination 1 visited (requires: $1,100 budget remaining)
    target_date: "2025-07-05"
    duration: "2 days"
    dependencies: ["M1"]

  - M1: Depart home (requires: Full budget of $2,000, car serviced)
    target_date: "2025-07-03"
    duration: "0d"
```

### 3.0 Dependency-Heavy (Home Addition with Multiple Trade Contractors)
**Focus:** Work backward identifying handoffs between contractors.

```yaml
end_state: "Home addition completed with final inspection passed"
date: "2025-08-01"

critical_path:
  - M6: Final inspection passed (Building Inspector)
  - M5: Interior finishes complete (Painter, Flooring) [depends on M4]
  - M4: Electrical and plumbing finals (Licensed Electrician, Licensed Plumber) [depends on M3]
  - M3: Drywall hung and taped (Drywall Contractor) [depends on M2]
  - M2: Framing inspection passed (Building Inspector) [depends on M1]
  - M1: Foundation poured and cured (Concrete Contractor)

handoff_points:
  - from: "Concrete Contractor"
    to: "Framing Contractor"
    at: "M1 complete (foundation cured 7 days)"
    sla: "Framing must start within 3 days of foundation cure"

  - from: "Framing Contractor"
    to: "Building Inspector"
    at: "M2 complete"
    sla: "Inspection within 2 business days, must pass before drywall"

  - from: "Drywall Contractor"
    to: "Electrician/Plumber"
    at: "M3 complete"
    sla: "24h for electrical/plumbing to complete finals"
```

## Anti-Patterns

### ❌ Forward Planning Disguised as WBP
```yaml
# WRONG: This is forward planning with milestones
- M1: Start planning wedding
- M2: Book venue
- M3: Book catering
- M4: Wedding day

# RIGHT: Start from wedding day, work backward
- M4: Wedding day (need: M3 done, all vendors confirmed)
- M3: Catering finalized (need: M2 done, menu approved)
- M2: Venue booked (need: M1 done, budget set)
- M1: Budget and guest count determined
```

### ❌ No Buffers
```yaml
# WRONG: Critical path exactly equals available time
total_time: 12 weeks (kitchen renovation)
critical_path: 12 weeks
buffer: 0 days  # 🚨 One delay = missed Thanksgiving deadline
```

### ❌ Ignoring Dependencies
```yaml
# WRONG: Parallel milestones that should be sequential
- M3: Final inspection (Nov 20)
- M2: Install countertops (Nov 20)  # Same day!
# M3 depends on M2 complete, can't be same day
```

### ❌ Vague Milestones
```yaml
# WRONG: Can't verify completion
- milestone: "Make progress on renovation"
- milestone: "Work on wedding planning"

# RIGHT: Concrete, verifiable
- milestone: "Rough-in inspection passed, permit posted on site"
- milestone: "All 200 wedding invitations addressed and mailed with RSVP deadline"
```

## Benefits

### For Planning:
1. **Realistic Timelines:** Know exactly when to start to hit deadline
2. **Dependency Clarity:** See what blocks what
3. **Risk Visibility:** Identify failure modes before they occur
4. **Resource Planning:** Know when you need specific people/services

### For Execution:
1. **Clear Milestones:** Everyone knows what's next
2. **Go/No-Go Decisions:** Built-in checkpoints
3. **Early Warning:** See when you're falling behind
4. **Adaptation:** Clear what to do if things go wrong

### For Communication:
1. **Stakeholder Updates:** "We're at M5 of 8, on track for March 1"
2. **Risk Communication:** "M4 has high risk, we've allocated 2-day buffer"
3. **Decision Clarity:** "Need to decide on identity provider by Feb 19"

## Storage Format

Work Back Plans can be stored in YAML, JSON, or spreadsheet formats:

### YAML Format (Recommended for Version Control)
```yaml
# wedding-wbp.yaml
version: 1.0
created: 2025-01-15T10:00:00Z
updated: 2025-04-03T14:30:00Z

plan_name: "Smith-Johnson Wedding Celebration"
owner: "Bride & Groom"
status: "in_progress"

# ... (full WBP structure as shown in template)

execution_log:
  - milestone: "M1"
    actual_completion: "2024-11-05"
    planned_completion: "2024-11-01"
    variance: "+4 days"
    notes: "Budget discussion took longer than expected, still within buffer"

  - milestone: "M2"
    actual_completion: "2024-12-08"
    planned_completion: "2024-12-01"
    variance: "+7 days"
    notes: "Preferred venue required later date, adjusted timeline"

  - milestone: "M3"
    actual_completion: "2025-04-03"
    planned_completion: "2025-04-01"
    variance: "+2 days"
    notes: "Invitation printing delayed, mailed 2 days late but within buffer"
```

### Spreadsheet Format (Excel/Google Sheets)
```
File: Kitchen-Renovation-WBP.xlsx

Tab 1: Overview
- Plan Name: Kitchen Renovation
- Owner: Homeowner
- End State: Final inspection passed
- Target Date: 2025-11-20
- Status: In Progress
- Buffer: 2 weeks (14% of critical path)

Tab 2: Critical Path
| ID | Milestone | Description | Target Date | Duration | Status | Dependencies |
|----|-----------|-------------|-------------|----------|--------|--------------|
| M7 | Final inspection | Inspector approval | Nov 20 | 1d | Pending | M6 |
| M6 | Finishes installed | Countertops, fixtures | Nov 13 | 1w | In Progress | M5 |
| M5 | Rough-in complete | Plumbing, electrical | Nov 6 | 1w | Complete | M4 |

Tab 3: Risks
| Risk | Probability | Impact | Score | Mitigation | Status |
|------|-------------|--------|-------|------------|--------|
| Material delivery delay | Medium | High | 6 | Order 6 weeks early | Monitoring |
| Structural issues | Medium | High | 6 | $3K contingency budget | Not occurred |

Tab 4: Execution Log
| Milestone | Planned Date | Actual Date | Variance | Notes |
|-----------|--------------|-------------|----------|-------|
| M1 | Aug 25 | Aug 25 | On time | Permits approved first try |
| M2 | Sep 15 | Sep 18 | +3 days | Contractor negotiation |
```

### Markdown Format (Simple Documentation)
```markdown
# Surf Expedition WBP - Indonesia Dec 2025

**Owner:** Trip Organizer
**Status:** Planning
**End State:** Safe return from 7-day surf trip
**Target Date:** 2025-12-15

## Critical Path

- **M6:** Return home safely (Dec 15)
  - *Status:* Not started
  - *Dependencies:* M5

- **M5:** Surf sessions completed (Dec 8-14)
  - *Status:* Not started
  - *Risks:* Swell forecast changes (Medium/High)
  - *Dependencies:* M4

- **M4:** Arrive at destination (Dec 7)
  - *Status:* Not started
  - *Dependencies:* M3

[... continue with all milestones ...]

## Execution Log

| Date | Event | Notes |
|------|-------|-------|
| 2025-09-02 | M1 Complete | Indonesia selected based on Dec swell forecast |
| 2025-09-20 | M2 Complete | Accommodations booked near Uluwatu (+5 days, within buffer) |
```

## Command-Line and Tool Integration

WBP can be managed using various tools and formats:

### Spreadsheet Tracking
```
Project: Kitchen Renovation
End State: Inspection passed by Nov 20, 2025

| Milestone | Target Date | Status | Actual Date | Variance | Notes |
|-----------|-------------|--------|-------------|----------|-------|
| M7: Final inspection | Nov 20 | Pending | - | - | - |
| M6: Finishes installed | Nov 13 | In Progress | - | - | Countertop delayed 3 days |
| M5: Rough-in complete | Nov 6 | Complete | Nov 7 | +1 day | Within buffer |
| M4: Demo complete | Oct 30 | Complete | Oct 30 | On time | - |
```

### Project Management Software
- **MS Project / Primavera:** Critical path visualization, Gantt charts
- **Trello / Asana:** Card-based milestone tracking with dependencies
- **Notion / Airtable:** Database views with formulas for buffer calculation

### Command-Line Tool Pattern (Generic)
```bash
# Create new WBP
wbp create --end-state "Wedding celebration complete" \
  --deadline "2025-06-15" \
  --owner "Bride and Groom"

# View current plan
wbp show

# Update milestone status
wbp complete M3 --actual-date "2025-04-02" --notes "Guest list took 1 extra week"

# Check if on track
wbp status
# Output:
# ✅ M1: Complete (on time) - Budget set
# ✅ M2: Complete (+1 week, within buffer) - Venue booked
# 🔄 M3: In progress (due in 2 weeks) - Guest list finalization
# ⏳ M4: Not started - Menu planning starts after M3
# ⚠️  ALERT: M3 at risk, only 2 weeks remaining for invitations

# Identify critical path
wbp critical-path
# Output: M1 → M2 → M3 → M5 → M7 → M8 (7 months total)

# Show risks
wbp risks --threshold medium
# Output:
# 🔴 HIGH (score 6): Guest count exceeds venue capacity
# 🟡 MEDIUM (score 4): Vendor cancellation within 2 weeks
```

## WBP Planning Agent Pattern

When requesting a Work Back Plan from an AI assistant or planning tool, provide:

### Input Template
```yaml
wbp_request:
  end_state:
    description: "[What does success look like?]"
    date: "[Target completion date/time]"
    success_criteria:
      - "[Observable condition 1]"
      - "[Observable condition 2]"
      - "[Observable condition 3]"

  constraints:
    budget: "[Total budget available]"
    team_size: "[Number of people/resources]"
    blackout_dates: ["[Date 1]", "[Date 2]"]  # Dates when work cannot happen
    must_include: ["[Required milestone 1]", "[Required milestone 2]"]
    preferences: ["[Nice to have 1]", "[Nice to have 2]"]
```

### Example: Wedding Planning Request
```yaml
wbp_request:
  end_state:
    description: "Wedding celebration with 150 guests"
    date: "2025-06-15 15:00"
    success_criteria:
      - "Ceremony and reception executed as planned"
      - "All guests accommodated within budget"
      - "Memorable experience captured by photographer"

  constraints:
    budget: "$25,000"
    team_size: "Bride, Groom, Wedding Coordinator, 4 family volunteers"
    blackout_dates: ["2025-05-20 to 2025-05-25"]  # Family unavailable
    must_include: ["Live band for reception", "Professional photographer", "Sit-down dinner"]
    preferences: ["Outdoor ceremony if weather permits", "Local venue within 30 min of city"]
```

### WBP Agent Prompt
When asking an AI assistant to create a WBP:

```
Create a Work Back Plan for the following end state:

[Describe end state with date and success criteria]

Constraints:
- Budget: [Amount]
- Resources: [People/equipment/facilities]
- Blackout dates: [Dates when work cannot happen]
- Must include: [Required elements]

Work backward from the deadline to identify:
1. Critical path milestones (longest dependent sequence)
2. Decision points (where choices must be made)
3. Potential risks and mitigations (what could go wrong)
4. Resource requirements (who/what needed when)
5. Go/no-go gates (checkpoints before proceeding)

Provide realistic timeline with appropriate slack buffer (20-30% of critical path duration).
Format as YAML following the WBP template structure.
```

### Example Request to AI
```
Create a Work Back Plan for a kitchen renovation:

End State: Kitchen renovation completed and final inspection passed
Date: November 20, 2025
Success Criteria:
- All appliances installed and operational
- Building inspection passed, occupancy permitted
- Kitchen fully functional for holiday cooking

Constraints:
- Budget: $35,000
- Resources: General contractor, licensed electrician, licensed plumber, homeowner oversight
- Blackout dates: None, but prefer to avoid Thanksgiving week
- Must include: Granite countertops, new cabinets, electrical upgrade to 200amp

Work backward from November 20th to identify the critical path, risks, and decision points.
Include 20% buffer for typical renovation surprises.
```

## Application Across Project Types

WBP can be applied at different granularities and across diverse project types:

### Wedding Planning Stages
| Scope | WBP Application |
|-------|-----------------|
| **Overall Wedding** | End state = wedding day, milestones = major vendor bookings |
| **Ceremony Planning** | End state = ceremony complete, milestones = venue/officiant/music |
| **Reception Planning** | End state = reception complete, milestones = catering/venue/entertainment |
| **Individual Vendor** | End state = vendor delivered, milestones = booking/confirmation/payment |

### Construction Project Phases
| Scope | WBP Application |
|-------|-----------------|
| **Entire Project** | End state = final inspection passed, milestones = major construction phases |
| **Phase Level** | End state = framing complete, milestones = foundation/walls/roof |
| **Trade Level** | End state = electrical rough-in done, milestones = permits/installation/inspection |
| **Daily Tasks** | End state = day's work complete, milestones = specific installations |

### Expedition Planning Sequence
| Scope | WBP Application |
|-------|-----------------|
| **Full Expedition** | End state = safe return, milestones = destination selection/travel/activities/return |
| **Travel Phase** | End state = arrival at destination, milestones = flights/connections/ground transport |
| **Activity Phase** | End state = activities completed, milestones = daily surf sessions/hikes/experiences |
| **Equipment Prep** | End state = all gear packed, milestones = purchase/test/pack items |

### Conference Organization Timeline
| Scope | WBP Application |
|-------|-----------------|
| **Overall Conference** | End state = event concluded successfully, milestones = venue/speakers/execution |
| **Speaker Management** | End state = all speakers confirmed, milestones = outreach/acceptance/materials |
| **Venue Logistics** | End state = venue setup complete, milestones = contract/layout/tech check |
| **Day-of Execution** | End state = sessions completed, milestones = registration/sessions/teardown |

### General Project Lifecycle
| Scope | WBP Application |
|-------|-----------------|
| **Strategic Level** | End state = organizational goal achieved, milestones = major initiatives |
| **Project Level** | End state = project delivered, milestones = planning/execution/delivery |
| **Task Level** | End state = deliverable complete, milestones = research/draft/review/finalize |
| **Daily Level** | End state = daily goals met, milestones = hourly or task-based checkpoints |

**Example: Restaurant Opening WBP (Multi-Level)**
```yaml
# STRATEGIC LEVEL
end_state: "Restaurant profitably operating 6 months post-launch"
critical_path:
  - M4: Six-month profitability milestone (Aug 1)
  - M3: Three-month operations review (May 1)
  - M2: First month financial analysis (Mar 1)
  - M1: Grand opening event (Feb 1)

# PROJECT LEVEL (contained within M1 above)
end_state: "Grand opening event with health permit"
critical_path:
  - M5: Grand opening event (Feb 1)
  - M4: Health inspection passed (Jan 30)
  - M3: Equipment installed and operational (Jan 25)
  - M2: Construction and permits complete (Jan 15)
  - M1: Contractor selected and started (Dec 1)

# TASK LEVEL (contained within M4 above)
end_state: "Health inspection passed"
critical_path:
  - M4: Inspector signs off, certificate issued (Jan 30 10:00am)
  - M3: Pre-inspection walkthrough, all corrections made (Jan 29 5:00pm)
  - M2: All equipment cleaned and sanitized (Jan 29 2:00pm)
  - M1: Staff trained on food safety procedures (Jan 29 9:00am)
```

## Further Reading

### Universal Project Management
- "Critical Chain" by Eliyahu M. Goldratt (Theory of Constraints, manufacturing and project buffers)
- "The Goal" by Eliyahu Goldratt (constraint-based planning and execution)
- "The Checklist Manifesto" by Atul Gawande (surgical and aviation planning methodologies)
- "Getting Things Done" by David Allen (outcome-based planning)

### Construction and Engineering
- "The Mythical Man-Month" by Fred Brooks (complex project planning principles)
- Critical Path Method (CPM) and Program Evaluation Review Technique (PERT)
- Lean Construction Institute methodologies
- Construction scheduling with MS Project or Primavera

### Military Planning
- U.S. Army Field Manual 5-0 (Planning Process)
- "Backwards Planning" in Marine Corps Planning Process (MCPP)
- "Planning Backward from the Objective" in Special Operations planning doctrine

### Event Planning
- Professional Convention Management Association (PCMA) resources
- "The Event Planning Toolkit" by Judy Allen
- Wedding planning timelines (working backward from event date)

### Expedition and Adventure Planning
- "Mountaineering: The Freedom of the Hills" (expedition planning chapters)
- Surf travel planning guides (working backward from swell windows)
- Backpacking trip planning (reverse itinerary from exit point)

### General Methodology
- Gantt charts (visual timeline planning)
- Work Breakdown Structure (WBS) in reverse
- Backward chaining in AI planning systems

---

**File UUID:** 8d4b5e9f-2c7a-4f1b-9e3d-6a8c7b9d0e2f
**Version:** 1.0
**Last Updated:** 2025-02-12
**Owner:** Claude Code / Hopper Labs
