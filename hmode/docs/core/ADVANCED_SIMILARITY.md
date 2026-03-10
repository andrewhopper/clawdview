# Advanced Similarity Metrics for Response Validation

## Overview

Beyond simple Levenshtein distance, use multiple similarity metrics to understand user intent with high accuracy.

---

## 1. Phonetic Similarity (Soundex/Metaphone)

**Purpose:** Catch typos that "sound right" but are spelled wrong.

**Use Cases:**
- Voice-to-text typos
- Common pronunciation-based misspellings
- Technical term variations

### Implementation Strategy

**Lightweight Option: Soundex**
```python
import jellyfish

def phonetic_match(word1: str, word2: str) -> bool:
    """Check if two words sound similar"""
    return jellyfish.soundex(word1) == jellyfish.soundex(word2)
```

**Examples:**
```
"gith" → soundex("gith") == soundex("git") → Match! (gh/t sound similar)
"nop" → soundex("nop") == soundex("nope") → Match!
"yex" → soundex("yex") == soundex("yes") → Match!
"postgre" → soundex("postgre") ≈ soundex("postgres") → Partial match
```

### Confidence Boost

**Phonetic match found:**
- Base confidence: 70%
- Phonetic boost: +15%
- Final: 85% → CONFIRM (or PROCEED if non-destructive)

**Example:**
```
AI: "Which version control?"
User: "gith"

Analysis:
  ✓ Phonetically similar to "git"
  ✓ Context: version control
  ✓ Technical term match: "GitHub"
  → Confidence: 85% (70% base + 15% phonetic)
  → Auto-correct to "GitHub"
  → CONFIRM (just below 90% threshold)

AI: "Using GitHub? y/n"
```

---

## 2. Semantic Similarity (BERT/Embeddings)

**Purpose:** Understand intent beyond exact word matching.

**Use Cases:**
- Command synonyms (test ≈ check ≈ verify ≈ validate)
- Action equivalents (open ≈ start ≈ launch ≈ run)
- Technical paraphrases

### Implementation Strategy

**Option A: Lightweight (sentence-transformers)**
```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast, small model

def semantic_similarity(text1: str, text2: str) -> float:
    """Calculate semantic similarity (0-1)"""
    embeddings = model.encode([text1, text2])
    cosine_sim = np.dot(embeddings[0], embeddings[1]) / (
        np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
    )
    return cosine_sim
```

**Option B: Pre-computed Command Clusters**
```python
COMMAND_CLUSTERS = {
    'testing': {'test', 'check', 'verify', 'validate', 'inspect'},
    'viewing': {'open', 'start', 'launch', 'run', 'show', 'display'},
    'fixing': {'fix', 'repair', 'correct', 'resolve', 'debug'},
    'creating': {'create', 'make', 'build', 'generate', 'add'},
}

def find_command_cluster(word: str) -> Optional[str]:
    """Find which cluster a word belongs to"""
    for cluster_name, words in COMMAND_CLUSTERS.items():
        if word in words:
            return cluster_name
    return None
```

### Examples

**Semantic Command Recognition:**
```
User: "check this"
→ "check" ∈ testing cluster
→ Semantic similarity to "test" = 0.85
→ Treat as "test this" command
→ Confidence: 95% → PROCEED

User: "verify the api"
→ "verify" ∈ testing cluster
→ Semantic similarity to "test" = 0.82
→ Treat as "test the api" command
→ Confidence: 95% → PROCEED

User: "launch it"
→ "launch" ∈ viewing cluster
→ Semantic similarity to "start" = 0.88
→ Treat as "start it" command
→ Confidence: 95% → PROCEED
```

### Confidence Boost

**Semantic match found (similarity > 0.75):**
- Base confidence: 70%
- Semantic boost: +20-25% (based on similarity score)
- Final: 90-95% → PROCEED

---

## 3. ROUGE Score (for longer responses)

**Purpose:** Measure n-gram overlap for paraphrased responses.

**Use Cases:**
- User provides detailed explanation instead of yes/no
- Alternative phrasing of requirements
- Confirmation with context

### Implementation Strategy

```python
from rouge_score import rouge_scorer

def calculate_rouge(response: str, expected: str) -> dict:
    """Calculate ROUGE scores"""
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'])
    scores = scorer.score(expected, response)
    return {
        'rouge1': scores['rouge1'].fmeasure,
        'rouge2': scores['rouge2'].fmeasure,
        'rougeL': scores['rougeL'].fmeasure,
    }
```

### Examples

**Long-form confirmation:**
```
AI: "Should we deploy to production with these changes?"
User: "yes let's push this to prod with the updates"

ROUGE Analysis:
  rouge1: 0.72 (word overlap)
  rouge2: 0.45 (bigram overlap)
  rougeL: 0.65 (longest common subsequence)

Keywords detected: "yes", "prod"
Semantic intent: Affirmative + production deployment
→ Confidence: 96% → PROCEED
```

**Paraphrased requirement:**
```
AI: "Create API endpoint for user authentication?"
User: "build auth route for login system"

ROUGE Analysis:
  rouge1: 0.58 (some word overlap)
  Semantic similarity: 0.82 (high)

Intent: Same (create authentication endpoint)
→ Confidence: 92% → PROCEED with interpretation
AI: "Creating authentication API endpoint"
```

### Confidence Boost

**ROUGE score > 0.6:**
- Base confidence: 70%
- ROUGE boost: +15-20%
- Final: 85-90% → PROCEED

---

## 4. Combined Scoring Strategy

**Multi-metric approach for maximum accuracy:**

### Scoring Formula

```
Final Confidence = Base + Σ(Boosts)

Base Confidence: 70%

Boosts:
- Standard shorthand: +26% → 96%
- Common command: +25% → 95%
- Phonetic match: +15% → 85%
- Semantic match (>0.75): +20% → 90%
- Contextual validation: +5-10% → 75-80%
- Edit distance ≤1: +10% → 80%
- Edit distance =2: +5% → 75%
- ROUGE score >0.6: +15% → 85%
- Non-destructive action: +20% (applied to typos)

Max confidence: 96% (capped)
Threshold: 90% = auto-proceed
```

### Example: Multi-Metric Analysis

```
AI: "Which testing framework?"
User: "jst"

Analysis:
  1. Edit distance: "jst" → "jest" (distance=1) → +10%
  2. Phonetic: soundex("jst") ≈ soundex("jest") → +15%
  3. Semantic: "jest" in testing frameworks → Context match
  4. Base: 70%

  Total: 70% + 10% + 15% = 95%
  → PROCEED with "Jest"

AI: "Using Jest for testing"
```

---

## 5. Implementation Priorities

### Phase 1: Lightweight (Current)
- ✅ Levenshtein distance
- ✅ Standard shorthand recognition
- ✅ Common command patterns
- ✅ Contextual validation

### Phase 2: Phonetic (Next)
- Add Soundex/Metaphone matching
- Pre-compute phonetic codes for common terms
- ~5-10% accuracy improvement
- Minimal performance impact

### Phase 3: Semantic (Medium-term)
- Pre-computed command clusters (lightweight)
- OR sentence-transformers (if acceptable latency)
- ~10-15% accuracy improvement
- Moderate performance impact

### Phase 4: Advanced (Future)
- ROUGE scoring for long responses
- Full BERT semantic matching
- Custom fine-tuned models
- ~5-10% additional accuracy improvement
- Higher performance cost

---

## 6. Trade-offs

### Performance vs. Accuracy

| Metric | Latency | Accuracy Gain | Complexity | Priority |
|--------|---------|---------------|------------|----------|
| **Levenshtein** | <1ms | Baseline | Low | ✅ DONE |
| **Soundex** | <1ms | +5-10% | Low | ⭐ HIGH |
| **Command Clusters** | <1ms | +10-15% | Low | ⭐ HIGH |
| **Sentence-BERT** | ~10ms | +10-15% | Medium | 🔵 MEDIUM |
| **ROUGE** | ~5ms | +5-10% | Medium | 🟡 LOW |
| **Full BERT** | ~50ms | +5-10% | High | ⚪ LATER |

### Recommendation

**Start with Phase 2 (Phonetic + Command Clusters):**
- Minimal latency impact (<1ms)
- Significant accuracy improvement (+15-25%)
- Easy to implement and maintain
- Covers most real-world cases

---

## 7. Real-World Examples

### Before Advanced Similarity

```
User: "chek this"
→ No match found
→ Edit distance to "check" = 1
→ Confidence: 80% → CONFIRM

AI: "Did you mean 'check this'? y/n"
```

### After Advanced Similarity

```
User: "chek this"
→ Edit distance to "check" = 1 → +10%
→ Phonetic match: soundex("chek") == soundex("check") → +15%
→ Semantic: "check" ∈ testing cluster → Recognized as command
→ Base: 70% + 10% + 15% = 95%
→ PROCEED

AI: [Proceeds with checking/testing]
```

---

## 8. Example: Multi-Layered Validation

```python
def validate_with_similarity(user_response: str, context: str) -> ValidationResult:
    """Multi-metric validation"""

    # Layer 1: Exact match (shorthand, commands)
    if is_standard_shorthand(user_response):
        return ValidationResult(96, "PROCEED", "Standard shorthand")

    # Layer 2: Edit distance
    closest_match, distance = find_closest_match(user_response)
    if distance <= 1:
        confidence = 80 + (10 if distance == 1 else 0)

    # Layer 3: Phonetic similarity
    if phonetic_match(user_response, closest_match):
        confidence += 15

    # Layer 4: Semantic similarity
    semantic_score = get_semantic_similarity(user_response, closest_match)
    if semantic_score > 0.75:
        confidence += 20

    # Layer 5: Contextual boost
    if is_non_destructive_action(context):
        confidence += 20

    # Layer 6: ROUGE (for long responses)
    if len(user_response.split()) > 5:
        rouge_score = calculate_rouge(user_response, expected_pattern)
        if rouge_score > 0.6:
            confidence += 15

    return ValidationResult(
        confidence=min(96, confidence),
        action="PROCEED" if confidence >= 90 else "CONFIRM",
        reasoning=f"Multi-metric: edit={distance}, phonetic={phonetic_match}, semantic={semantic_score:.2f}"
    )
```

---

## Summary

**Key Improvements:**
1. **Phonetic matching** catches "sounds like" typos (gith→git)
2. **Semantic similarity** recognizes command synonyms (test≈check)
3. **ROUGE scoring** handles paraphrased responses
4. **Combined approach** maximizes accuracy with minimal latency

**Expected Impact:**
- 15-25% reduction in false confirmations
- Better handling of voice-to-text errors
- More natural synonym recognition
- Smoother user experience overall

**Next Steps:**
1. Implement Phase 2 (phonetic + clusters)
2. Test with real conversation data
3. Measure improvement in confidence accuracy
4. Consider Phase 3 (semantic) if needed
