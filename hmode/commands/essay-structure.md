---
uuid: cmd-essay-4n5o6p7q
---

# Essay Structure Validator

Validates markdown documents against the structured essay format (intro + body + conclusion).

## Usage

```
/essay-structure <file_path> [--fix]
```

**Arguments:**
- `<file_path>` - Path to markdown file to validate
- `--fix` - Optional: Automatically restructure document to meet essay format

**Examples:**
```bash
# Audit essay structure
/essay-structure docs/article.md

# Audit and fix structure issues
/essay-structure docs/article.md --fix
```

## Command

You are validating a document against the structured essay writing format.

### Validation Rules

**1. Introductory Paragraph Structure:**
- [ ] Contains topic statement (1 sentence)
- [ ] Contains 3-5 distinct main ideas (each in separate sentence)
- [ ] Contains transition/conclusion sentence
- [ ] Total sentences: 5-7

**2. Body Paragraph Requirements:**
- [ ] Number of body paragraphs matches number of intro ideas (3-5 paragraphs)
- [ ] Each body paragraph corresponds to one intro idea
- [ ] Each body paragraph contains 5-7 sentences
- [ ] Each body paragraph structure: intro + 3-5 supporting points + conclusion

**3. Body Paragraph Content:**
- [ ] First sentence restates/introduces the idea from intro
- [ ] Middle sentences provide evidence, examples, or reasoning
- [ ] Last sentence concludes or transitions
- [ ] Content expands on corresponding intro sentence

**4. Conclusion Paragraph:**
- [ ] Restates main topic from intro
- [ ] Recaps each main idea (matches number of body paragraphs)
- [ ] Provides synthesis or final statement
- [ ] Introduces NO new information
- [ ] Total sentences: 5-7

**5. Overall Structure:**
- [ ] Logical flow: intro → body → conclusion
- [ ] Transitions between paragraphs
- [ ] Consistent tone throughout
- [ ] No structural gaps or mismatches

### Execution Steps

1. **Read the target document**
   ```
   Read <file_path>
   ```

2. **Analyze structure**
   - Count paragraphs (should be 5-7 total: 1 intro + 3-5 body + 1 conclusion)
   - Parse intro paragraph into sentences
   - Identify main ideas (should be 3-5)
   - Verify each body paragraph corresponds to an intro idea
   - Check conclusion recaps all ideas

3. **Generate validation report**

   **Format:**
   ```markdown
   # Essay Structure Validation Report

   **File:** <file_path>
   **Grade:** [A/B/C/D/F]
   **Overall Assessment:** [PASS/FAIL with explanation]

   ---

   ## Structure Summary

   | Element | Expected | Found | Status |
   |---------|----------|-------|--------|
   | Intro paragraph | 1 | X | ✅/❌ |
   | Main ideas in intro | 3-5 | X | ✅/❌ |
   | Body paragraphs | 3-5 | X | ✅/❌ |
   | Conclusion paragraph | 1 | X | ✅/❌ |
   | Total paragraphs | 5-7 | X | ✅/❌ |

   ---

   ## Detailed Analysis

   ### 1. Introductory Paragraph

   **Status:** [PASS/FAIL]

   **Found structure:**
   - Sentence 1: [Topic statement or issue found]
   - Sentence 2: [Main idea A or issue]
   - Sentence 3: [Main idea B or issue]
   - Sentence 4: [Main idea C or issue]
   - Sentence 5: [Transition or issue]

   **Issues:**
   - [ ] Missing topic statement
   - [ ] Too few main ideas (found X, need 3-5)
   - [ ] Too many main ideas (found X, max 5)
   - [ ] Missing transition sentence
   - [ ] Sentences not distinct ideas

   ---

   ### 2. Body Paragraphs

   **Status:** [PASS/FAIL]

   #### Body Paragraph 1 (should develop: [Intro Idea A])
   - **Develops correct idea:** ✅/❌
   - **Sentence count:** X (need 5-7)
   - **Structure:** [Intro + X supporting + conclusion]
   - **Issues:** [List any structural problems]

   #### Body Paragraph 2 (should develop: [Intro Idea B])
   - **Develops correct idea:** ✅/❌
   - **Sentence count:** X (need 5-7)
   - **Structure:** [Intro + X supporting + conclusion]
   - **Issues:** [List any structural problems]

   [Continue for each body paragraph...]

   ---

   ### 3. Conclusion Paragraph

   **Status:** [PASS/FAIL]

   **Found structure:**
   - Restates main topic: ✅/❌
   - Recaps idea A: ✅/❌
   - Recaps idea B: ✅/❌
   - Recaps idea C: ✅/❌
   - Provides synthesis: ✅/❌
   - Introduces new info: ✅ (BAD) / ❌ (GOOD)

   **Issues:**
   - [ ] Missing topic restatement
   - [ ] Doesn't recap all ideas
   - [ ] Introduces new information
   - [ ] Missing synthesis

   ---

   ## Grading Criteria

   **Grade A (90-100%):**
   - All structural requirements met
   - Intro has 3-5 distinct ideas
   - Each body paragraph develops one idea
   - Conclusion recaps all points
   - Minor issues only

   **Grade B (80-89%):**
   - Core structure present
   - 1-2 body paragraphs need work
   - Conclusion mostly complete
   - Fixable issues

   **Grade C (70-79%):**
   - Basic structure exists
   - Missing or weak body paragraphs
   - Intro ideas unclear
   - Significant restructuring needed

   **Grade D (60-69%):**
   - Structure barely recognizable
   - Multiple missing elements
   - Major restructuring required

   **Grade F (0-59%):**
   - No discernible essay structure
   - Complete rewrite needed

   ---

   ## Recommendations

   ### Critical Issues (Fix First)
   1. [Highest priority structural problems]
   2. [...]

   ### Moderate Issues
   1. [Medium priority improvements]
   2. [...]

   ### Minor Improvements
   1. [Nice-to-have enhancements]
   2. [...]

   ---

   ## Quick Fixes

   [If --fix flag provided, show proposed restructuring]

   ### Proposed Intro Structure
   ```
   [Rewritten intro paragraph with clear topic + 3-5 ideas + transition]
   ```

   ### Body Paragraph Mapping
   - Body 1: Develop idea "[Idea A]"
   - Body 2: Develop idea "[Idea B]"
   - Body 3: Develop idea "[Idea C]"

   ### Proposed Conclusion
   ```
   [Rewritten conclusion recapping all ideas]
   ```
   ```

4. **If --fix flag provided:**
   - Generate restructured version of document
   - Preserve original content but reorganize
   - Add missing elements (intro ideas, transitions, conclusion recaps)
   - Show before/after comparison
   - Ask user approval before writing changes

### Output Format

**Validation Only (no --fix):**
- Display validation report
- Show grade and pass/fail status
- List specific issues with line numbers
- Provide recommendations

**Validation + Fix (--fix flag):**
- Display validation report
- Show proposed restructuring
- Explain changes
- Request approval: "Apply these changes? (yes/no)"
- If yes: Write restructured content to file
- If no: Exit without changes

### Example Output

```markdown
# Essay Structure Validation Report

**File:** docs/ai-healthcare.md
**Grade:** C (72%)
**Overall Assessment:** NEEDS WORK - Basic structure exists but requires significant improvements

---

## Structure Summary

| Element | Expected | Found | Status |
|---------|----------|-------|--------|
| Intro paragraph | 1 | 1 | ✅ |
| Main ideas in intro | 3-5 | 2 | ❌ |
| Body paragraphs | 3-5 | 2 | ❌ |
| Conclusion paragraph | 1 | 1 | ✅ |
| Total paragraphs | 5-7 | 4 | ❌ |

---

## Detailed Analysis

### 1. Introductory Paragraph

**Status:** FAIL - Too few main ideas

**Found structure:**
- Sentence 1: ✅ Topic statement: "AI is transforming healthcare"
- Sentence 2: ✅ Main idea A: "AI improves diagnostics"
- Sentence 3: ✅ Main idea B: "AI reduces administrative burden"
- Sentence 4: ❌ Missing main idea C
- Sentence 5: ⚠️ Weak transition

**Issues:**
- Only 2 main ideas (need minimum 3)
- Missing third idea about NLP/communication
- Transition sentence is vague

---

### 2. Body Paragraphs

**Status:** FAIL - Missing body paragraph

#### Body Paragraph 1 (develops: "AI improves diagnostics")
- **Develops correct idea:** ✅
- **Sentence count:** 6 (meets 5-7 requirement)
- **Structure:** ✅ Intro + 4 supporting + conclusion
- **Issues:** None - well structured

#### Body Paragraph 2 (develops: "AI reduces administrative burden")
- **Develops correct idea:** ✅
- **Sentence count:** 5 (meets 5-7 requirement)
- **Structure:** ✅ Intro + 3 supporting + conclusion
- **Issues:** None - well structured

**MISSING:** Body Paragraph 3 (need 3-5 body paragraphs total)

---

### 3. Conclusion Paragraph

**Status:** FAIL - Incomplete recaps

**Found structure:**
- Restates main topic: ✅
- Recaps idea A: ✅
- Recaps idea B: ✅
- Recaps idea C: ❌ (no idea C in intro)
- Provides synthesis: ✅
- Introduces new info: ❌ (good)

**Issues:**
- Only recaps 2 ideas (should match intro)
- Missing discussion of third aspect

---

## Recommendations

### Critical Issues (Fix First)
1. **Add third main idea to intro** - Include NLP/patient communication as third idea
2. **Add corresponding body paragraph** - Develop third idea with 5-7 sentences
3. **Update conclusion** - Add recap of third idea

### Moderate Issues
4. **Strengthen intro transition** - Make connection to body paragraphs clearer

---

## Quick Fixes

### Proposed Intro Addition
Add after sentence 3:
"Natural language processing improves patient communication through intelligent interfaces."

### New Body Paragraph 3
```
Natural language processing dramatically improves patient communication in healthcare settings.
AI-powered chatbots provide 24/7 access to basic medical information and appointment scheduling.
Symptom checkers guide patients to appropriate care levels, reducing emergency room overcrowding.
Translation services enable non-English speakers to access care without language barriers.
These communication tools increase patient engagement and satisfaction scores.
As NLP technology advances, patient-provider communication will become more accessible and effective.
```

### Updated Conclusion Addition
Add after recap of idea B:
"Natural language processing creates more accessible patient communication channels."
```

**Apply these changes? (yes/no)**
```

### Edge Cases

**Document has no clear paragraphs:**
- Provide structure guidance
- Suggest breaking into paragraphs first

**Document is not essay format:**
- Note: "This document doesn't follow essay structure"
- Provide brief explanation of essay format
- Ask if user wants to convert

**File doesn't exist:**
- Error: "File not found: <file_path>"
- Suggest checking path

### Success Criteria

- Identifies all structural deviations from essay format
- Provides specific, actionable feedback
- Grades accurately based on rubric
- Generates valid restructuring proposals (if --fix)
- Preserves original content meaning
