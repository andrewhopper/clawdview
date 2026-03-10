# Narratize: Transform Abstract Ideas into Concrete Future Stories

Convert abstract concepts, visions, or ideas into tangible human narratives that make the future feel real.

## Purpose

Many people struggle to imagine abstract futures. This tool bridges the gap by:
1. Grounding ideas in **specific human experiences**
2. Using **named protagonists** in **concrete settings**
3. Showing **first principles through action**, not exposition
4. Making the invisible **visible and relatable**

## Usage

```
/narratize <idea or concept>
```

---

## Narrative Structure (7 Required Elements)

Every narrative MUST include these components:

### 1. THE HOOK (Opening)
Start with the **problem or struggle**. Make the reader feel the friction.

```
❌ "In 2030, AI helps with education."
✅ "Ben is five years old and struggling to learn to read."
```

- Name the protagonist immediately
- Show their pain point in concrete terms
- Make the reader empathize before introducing the solution

### 2. THE SOLUTION (Introduction)
Introduce the technology **naturally**, as part of the protagonist's world.

```
❌ "An AI-powered adaptive learning system was deployed."
✅ "Then Rox arrives. Rox is Ben's humanoid robot companion."
```

- Don't explain what it is—show what it does
- Name the technology/AI if it has a presence
- Position it as a tool/partner, not magic

### 3. HOW IT WORKS (The Mechanism)
Show the **first principles through action**. The reader should understand WHY it works by watching it work.

```
❌ "The AI uses machine learning to personalize content."
✅ "Rox is already scanning—facial micro-expressions, pulse rate via radar,
    respiratory rhythm. The readings are clear: tired, hungry, frustrated.
    'Let's get you a snack first,' Rox says."
```

Techniques:
- Physiological sensing (what the AI perceives)
- Decision logic made visible (why it chose this action)
- Feedback loops (how it adapts)

### 4. THE MOMENT (Concrete Scene)
A **specific interaction** that demonstrates the transformation. This is the heart of the narrative.

```
"Rox lies down and curves into the shape of a letter. 'This is the letter S.
Like a snake! Can you make your body into an S too?' Ben grins and twists
himself into the shape."
```

- Dialogue grounds it in reality
- Sensory details (visual, auditory, kinesthetic)
- Show the human's emotional response

### 5. THE WITNESS (Optional but powerful)
Someone observing the transformation—often provides the emotional payoff.

```
"Ben's mom watches from the doorway. Her son is laughing while learning to read.
Last month, homework meant tears."
```

### 6. WHAT THIS MEANS (Implications)
Three-part structure:
- **For the protagonist:** Direct, personal benefit
- **For society:** Broader implication
- **The tradeoff:** What changes (honest, not utopian)

### 7. THE SHIFT (Closing line)
One sentence that captures the transformation. This is the thesis.

```
"Education adapts to the learner. Not the other way around."
"Humans stop feeding machines. Machines start seeing humans."
"Ideas used to need execution to survive. Now they just need validation."
```

---

## Narrative Patterns (Choose One)

### Pattern A: Before/After Contrast
Show the same person or situation in "before" and "after" states.

**Best for:** Removing friction, eliminating pain points
**Example:** Andrew's CRM nightmare → AI-observed work logging
**Structure:**
1. Before: Vivid description of the pain (specific, emotional)
2. Transition: "Then everything changed" / time jump
3. After: Same situation, transformed
4. Mechanism: Explain how it works
5. Payoff: The moment it all clicks

### Pattern B: Dual Protagonist
Two different people using the same system in completely different ways.

**Best for:** Adaptive interfaces, personalization
**Example:** Barbara (78, simple needs) vs Andrew (day trader, power user)
**Structure:**
1. Protagonist A's experience (complete mini-story)
2. Protagonist B's experience (complete mini-story)
3. Reveal: Same system, different interfaces
4. Mechanism: How the system knows
5. Implications

### Pattern C: Progressive Interaction
A back-and-forth between human and AI, showing iterative refinement.

**Best for:** AI assistants, creative tools, approval workflows
**Example:** Elena reviewing pitch deck during her run
**Structure:**
1. AI initiates with proactive offer
2. Human responds (approve/modify/reject)
3. AI adapts
4. Human refines
5. Final approval
6. Payoff: Result delivered

### Pattern D: Async Validation Loop
Human provides input, goes away, AI works, returns for validation.

**Best for:** Visionary/execution split, background processing
**Example:** Sam's idea → 4 days → prototype ready
**Structure:**
1. Human captures idea (casual, in-motion)
2. AI acknowledges, begins work
3. Time passes (human does other things)
4. AI returns with progress, asks for validation
5. Human provides quick feedback
6. Repeat until done
7. Payoff: Idea is real

### Pattern E: AI-to-AI Coordination
Systems talking to each other, with human setting preferences.

**Best for:** Scheduling, logistics, negotiations
**Example:** Sarah's dentist appointment
**Structure:**
1. Human expresses need (casual, ambient)
2. AI understands preferences/constraints
3. AI-to-AI negotiation happens
4. Human receives notification of result
5. (Optional) Dynamic update when conditions change
6. Human never touches the process

---

## Transformation Types

Tag your narrative with the type of shift it illustrates:

| Type | Description | Example |
|------|-------------|---------|
| `operator_to_approver` | Human shifts from doing to approving | Marcus reviewing specs, not code |
| `interface_evolution` | From static UI to adaptive/ambient | Barbara vs Andrew interfaces |
| `ai_to_ai_coordination` | Systems handle logistics | Sarah's scheduling |
| `personalization` | One-size-fits-all → adapted to individual | Ben's learning, Elena's pitch |
| `cognitive_offload` | Mental burden shifts to AI | Andrew's CRM logging |
| `time_compression` | Hours/days → seconds/minutes | Sam's idea-to-prototype |
| `proactive_ai` | AI anticipates needs | Elena's deck prepared automatically |

---

## Quality Checklist

Before finalizing a narrative, verify:

- [ ] **Named protagonist** (never "a user" or "someone")
- [ ] **Specific year and location** (2030, Austin TX)
- [ ] **Problem shown before solution** (hook has friction)
- [ ] **Mechanism visible through action** (not explained in exposition)
- [ ] **At least one concrete scene with dialogue**
- [ ] **Sensory details** (at least 2 senses engaged)
- [ ] **Witness or emotional payoff moment**
- [ ] **Three-part implications** (protagonist, society, tradeoff)
- [ ] **One-sentence shift** (the thesis)
- [ ] **~300-600 words** (2-3 minute read/listen)

---

## Process

1. **Capture the concept:** What abstract idea needs to be made concrete?
2. **Identify the transformation type:** Which shift does this represent?
3. **Choose a pattern:** Which narrative structure fits best?
4. **Create protagonist:** Name, age, situation, pain point
5. **Design the mechanism:** How does it work? What does the AI perceive/do?
6. **Write the scene:** Concrete moment with dialogue and sensory details
7. **Add the witness:** Who observes the transformation?
8. **Articulate implications:** Protagonist, society, tradeoff
9. **Craft the shift:** One sentence thesis
10. **Generate audio:** Use ElevenLabs for narration
11. **Publish:** Upload to S3

---

## Audio Generation

After writing, generate audio narration:

```python
# Use generate_audio.py in examples directory
# Voice: Adam (pNInz6obpgDQGcFmaJgB) - deep narrator, good for storytelling
# Model: eleven_multilingual_v2
```

---

## Examples

See `hmode/hmode/shared/semantic/domains/future-narrative/examples/` for 8 complete narratives:

| # | Story | Pattern | Transformation |
|---|-------|---------|----------------|
| 1 | Ben's Learning Game | A + elements of C | personalization |
| 2 | Sarah's Last Hold Music | E | ai_to_ai_coordination |
| 3 | Marcus Approves | A | operator_to_approver |
| 4 | The Pitch That Wrote Itself | C | proactive_ai + personalization |
| 5 | The Notification That Set Her Free | A | interface_evolution |
| 6 | The Interface That Knows You | B | interface_evolution |
| 7 | The System That Sees Your Work | A | cognitive_offload |
| 8 | The Idea That Built Itself | D | time_compression |

---

## Integration

This tool works well with:
- `/explain` - Adapt the narrative for different audiences
- `/proposal-microsite` - Turn narrative into shareable presentation
- `/story-voiceover` - Multi-voice audio with character dialogue
- `/arch-diagram` - Visualize the technical mechanisms

---

Start by asking: **What abstract idea, concept, or future vision would you like to make concrete?**
