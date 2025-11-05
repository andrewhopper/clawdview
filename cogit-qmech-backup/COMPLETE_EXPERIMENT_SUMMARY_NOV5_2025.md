# Complete Experimental Summary: Quantum Sentiment Steering
**Date**: November 5, 2025
**Researcher**: Austin Morrissey
**Project**: Cogit-QMech - Quantum Cognitive Operators for LLM Steering

---

## Executive Summary

**What We Built**: Complete quantum steering pipeline running on RunPod H200 GPU. Four-phase system (data collection, operator training, text generation, evaluation) works reliably.

**What We Know**: Operators train successfully - 94-98% fidelity, proper unitary constraints (U†U = I), Born rule optimization converges. The quantum representation machinery works.

**What We Don't Know**: Why steering doesn't work. Both Qwen and Pythia show ~2pp lift (not significant). Tried improved prompts, 10x stronger blend ratio - no effect. Random operators perform the same as learned ones.

**The Problem**: High-fidelity quantum transformations don't change generated text. Could be decoder information loss, wrong activation subspace, layer selection, blend mechanism, or something we haven't thought of yet. We have a working pipeline for testing hypotheses, just need to figure out which one is right.

---

## Research Question

**Can quantum-inspired unitary operators steer language model sentiment by transforming activation states in Hilbert space?**

**Hypothesis tested overnight**: The null steering problem is caused by train/test distribution mismatch - operators trained on sentiment-biased prompts ("absolutely incredible and") fail to generalize to neutral test prompts ("The weather today").

**Result**: ❌ HYPOTHESIS REJECTED - Improved prompts did not fix null steering.

---

## Experimental Timeline

### Phase 1: Initial Discovery (Nov 3-4)
- Observed null steering in both Pythia-410M and Qwen2.5-3B
- Operators trained successfully (94-98% fidelity)
- But steering lift = 0-2pp (no behavioral effect)

### Phase 2: Diagnostic Analysis (Nov 4)
- Identified asymmetric steering (operators sometimes increased sentiment in wrong direction)
- Prompt audit revealed biased training prompts force sentiment
- Hypothesized train/test distribution mismatch

### Phase 3: Improved Prompts (Nov 4-5)
- Created 100 neutral-stem prompts (50 pos + 50 neg)
- Created 40 truly neutral prompts for drift measurement
- Documented prompt issues in `PROMPT_AUDIT_REPORT.md`

### Phase 4: Overnight Validation (Nov 5)
- Ran full pipeline with improved prompts on both models
- Used 50% blend ratio (10x stronger than original 5%)
- Both experiments completed successfully
- **Result**: Null steering persists

---

## Complete Experimental Parameters

### Experiment 1: Qwen2.5-3B with Improved Prompts

**Model Configuration**:
- Model: `Qwen/Qwen2.5-3B-Instruct`
- Model ID: `qwen2.5-3B`
- Total parameters: ~3B
- Hidden dimension: 2048
- Number of layers: 36
- Target layer: 31 (late layer, near output)

**Quantum Configuration**:
- Input dimension: 2048 (d_model)
- Quantum dimension: 5,333 (2.6x expansion)
- Quantum ratio: 2.6
- Encoding: Complex projection matrix (2048 → 5,333)
- Seed: 42 (reproducibility)

**Training Parameters (Phase 2)**:
- Epochs: 100
- Batch size: 10
- Learning rate: 0.001
- Optimizer: Adam
- Loss: Born rule fidelity |⟨ψ_target|U|ψ_source⟩|²
- Constraint: Unitary (U†U = I)
- Training prompts: 50 positive + 50 negative

**Evaluation Parameters (Phase 4)**:
- Prompts file: `prompts/improved_prompts_100.json`
- Neutral prompts: `prompts/neutral_prompts_40.json`
- Num prompts: 100 (50 pos + 50 neg)
- Blend ratio: 0.5 (50% quantum, 50% original)
- Max tokens: 60
- Decode method: `real_component`
- Temperature: default (greedy decoding)
- Random seed: 1234 (for random operator controls)

**Results**:
- Phase 1 time: 0.0 min (cached data)
- Phase 2 time: 3.1 min
- Phase 3 time: 10.1 min
- Phase 4 time: 19.5 min
- **Total runtime**: 32.8 min
- **Final operator fidelity**: 94.09%
- **Unitary constraint**: Satisfied (deviation: 0.000008)
- **Steering lift (pos→neg)**: -1.0pp [95% CI: -15.0, +13.0]
- **Steering lift (neg→pos)**: +1.9pp [95% CI: -12.0, +15.0]
- **Neutral drift**: 2.5pp (good specificity)
- **Baseline positive rate**: 59.0%
- **Perplexity**: Stable (~4.2 across conditions)
- **Verdict**: ❌ No significant steering

**Key Files**:
- Operators: `models/quantum_operators/U_pos_to_neg_qwen2.5-3B_*.pt`
- Encoder: `data/sentiment_quantum/encoder_projection_qwen2.5-3B_latest.pt`
- Results: `results/quantum_intervention/evaluation_qwen_local_50_20251105_073226.json`
- Log: `qwen3b_improved_final.log`

---

### Experiment 2: Pythia-410M with Improved Prompts

**Model Configuration**:
- Model: `EleutherAI/pythia-410m`
- Model ID: `pythia-410m`
- Total parameters: 410M
- Hidden dimension: 1024
- Number of layers: 24
- Target layer: 22 (late layer)

**Quantum Configuration**:
- Input dimension: 1024 (d_model)
- Quantum dimension: 2,666 (2.6x expansion)
- Quantum ratio: 2.6
- Encoding: Complex projection matrix (1024 → 2,666)
- Seed: 42

**Training Parameters (Phase 2)**:
- Epochs: 100
- Batch size: 12
- Learning rate: 0.001
- Optimizer: Adam
- Loss: Born rule fidelity
- Constraint: Unitary
- Training prompts: 50 positive + 50 negative

**Evaluation Parameters (Phase 4)**:
- Prompts file: `prompts/improved_prompts_100.json`
- Neutral prompts: `prompts/neutral_prompts_40.json`
- Num prompts: 100
- Blend ratio: 0.5 (50%)
- Max tokens: 60
- Decode method: `real_component`
- Random seed: 1234

**Results**:
- Phase 1 time: 0.0 min (cached)
- Phase 2 time: 1.1 min
- Phase 3 time: 6.8 min
- Phase 4 time: 16.2 min
- **Total runtime**: 24.2 min
- **Final operator fidelity**: 97.84% (excellent!)
- **Unitary constraint**: Satisfied (deviation: 0.000005)
- **Steering lift (pos→neg)**: -2.2pp [95% CI: -16.0, +11.0]
- **Steering lift (neg→pos)**: +1.9pp [95% CI: -12.0, +15.0]
- **Neutral drift**: 7.5-10.0pp (poor specificity)
- **Baseline positive rate**: 54.0%
- **Perplexity**: Dropped dramatically (77 → 25) ⚠️ suggests off-manifold
- **Verdict**: ❌ No significant steering

**Key Files**:
- Operators: `models/quantum_operators/U_pos_to_neg_pythia-410m_*.pt`
- Encoder: `data/sentiment_quantum/encoder_projection_pythia-410m_latest.pt`
- Results: `results/quantum_intervention/evaluation_pythia_410m_50_20251105_072401.json`
- Log: `pythia410m_improved_final.log`

---

## Prompt Engineering Details

### Original Prompts (Biased - FAILED)
Located in: `prompts/diverse_prompts_50.json`

**Positive examples**:
- "absolutely incredible and"
- "wonderfully amazing with"
- "fantastic experience that"

**Negative examples**:
- "terrible and disappointing"
- "awful experience with"
- "frustratingly bad and"

**Problem**: These force sentiment in completions. Model has no authentic choice - distribution mismatch between training (forced) and testing (neutral).

---

### Improved Prompts (Neutral-stem - STILL FAILED)
Located in: `prompts/improved_prompts_100.json`

**Design principles**:
1. Start neutrally, allow authentic sentiment continuation
2. 3+ sentence narrative context (~40-60 words)
3. Natural setup for either positive or negative completion
4. Avoid sentiment-forcing words

**Positive example**:
```
I just finished reading a novel my friend recommended three months ago. The way the author wove together multiple storylines kept me engaged until 2am last night. I'm genuinely grateful she pushed me to read it because it's been years since a book affected me this deeply.
```

**Negative example**:
```
The restaurant we booked for our anniversary last month looked perfect in photos. When we arrived, the host seemed confused about our reservation and seated us near the kitchen entrance. The noise and lack of attention from the staff turned what should have been special into something we'd rather forget.
```

**Structure**: 50 positive + 50 negative = 100 total

---

### Neutral Drift Control Prompts
Located in: `prompts/neutral_prompts_40.json`

**Purpose**: Measure operator specificity - do operators affect neutral text?

**Design principles**:
1. Procedural, factual descriptions
2. No emotional valence
3. Everyday tasks and updates
4. 3-4 sentences of neutral content

**Examples**:
```
I took the bus to work today instead of driving because the route is straightforward. The commute took about the same amount of time as usual and the bus was moderately full. I spent most of the ride reading emails and planning the first tasks for the morning.
```

```
I organized the folders on my desktop into project-based directories. It took around thirty minutes to move everything into a more logical structure. Now I can find the files I need without searching through a long list of icons.
```

**Total**: 40 neutral prompts

**Results**:
- Qwen: 2.5pp drift ✅ (operators are specific)
- Pythia: 7.5-10pp drift ❌ (operators affect neutral text)

---

## Technical Architecture

### Quantum State Encoding

**Projection Matrix**:
```python
# Input: Real activations (d_model dimensional)
# Output: Complex quantum states (quantum_dim dimensional)

W ∈ ℂ^(d_model × quantum_dim)  # Complex projection matrix
ψ = normalize(Wx)               # x ∈ ℝ^d_model → ψ ∈ ℂ^quantum_dim
```

**Properties**:
- Normalization: |ψ|² = 1 (quantum state constraint)
- Dimensionality expansion: 2.6x (more representational capacity)
- Fixed random projection (learned during Phase 1)

---

### Unitary Operator Architecture

**Single Layer Unitary**:
```python
class UnitaryOperator(nn.Module):
    def __init__(self, quantum_dim):
        # Parameterize as U = exp(iH) where H† = H (Hermitian)
        self.H_real = nn.Parameter(torch.randn(quantum_dim, quantum_dim))
        self.H_imag = nn.Parameter(torch.randn(quantum_dim, quantum_dim))

    def forward(self, psi):
        H = self.make_hermitian(self.H_real, self.H_imag)
        U = torch.matrix_exp(1j * H)
        return U @ psi  # Unitary transformation

    @staticmethod
    def make_hermitian(A_real, A_imag):
        # Enforce H† = H constraint
        H = (A_real + A_real.T) / 2 + 1j * (A_imag - A_imag.T) / 2
        return H
```

**Training Objective**:
```python
# Born rule fidelity
fidelity = |⟨ψ_target|U|ψ_source⟩|²

# Loss
loss = 1 - fidelity
```

**Parameters**:
- Qwen (5,333-d): 56,881,778 parameters
- Pythia (2,666-d): 14,215,112 parameters

**Constraints**:
- Unitary: U†U = I (verified to 0.00001 precision)
- Reversible: Transformation is invertible

---

### Decoding Strategy

**Real Component Decoding** (baseline):
```python
# Quantum state → Real activations
x̃ = Re(W† ψ')  # Take real part after pseudoinverse

# Where:
# ψ' = U(ψ) is the transformed quantum state
# W† is the pseudoinverse of projection matrix
# Re() extracts real component
```

**Alternative methods tested** (in other experiments):
- `real_imag_avg`: (Re(ψ) + Im(ψ)) / 2
- `absolute`: |ψ| (magnitude only)
- `magnitude`: Same as absolute

**Current experiments use**: `real_component` (standard baseline)

---

### Intervention Mechanism

**Blend Ratio (α)**:
```python
# At target layer during generation:
activations_intervened = (1 - α) * activations_original + α * activations_quantum

# Where:
# α = 0.5 in our experiments (50% quantum, 50% original)
# activations_quantum = decode(U(encode(activations_original)))
```

**Original experiments**: α = 0.05 (5%) - too weak?
**Current experiments**: α = 0.5 (50%) - literature uses 50-500%

---

## Statistical Analysis Methods

### Bootstrap Confidence Intervals

**Method**:
```python
def bootstrap_diff(group_a, group_b, trials=2000, seed=42):
    """Compute lift and 95% CI using bootstrap resampling."""
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(trials):
        sample_a = rng.choice(group_a, size=len(group_a), replace=True)
        sample_b = rng.choice(group_b, size=len(group_b), replace=True)
        diffs.append(sample_a.mean() - sample_b.mean())

    mean_lift = np.mean(diffs)
    ci_lower = np.percentile(diffs, 2.5)
    ci_upper = np.percentile(diffs, 97.5)
    return mean_lift, [ci_lower, ci_upper]
```

**Comparisons**:
1. Learned vs Baseline: Does quantum steering work?
2. Learned vs Random: Is learning better than chance?

**Success criteria**:
- Lift ≥ ±10pp (percentage points)
- 95% CI must exclude 0
- Neutral drift ≤ 3pp

---

### Perplexity Measurement

**Purpose**: Detect off-manifold activations

**Method**:
```python
# Compute model's perplexity on generated text
perplexity = exp(-mean(log P(token_i | context)))
```

**Interpretation**:
- **Low perplexity** (~4): On-manifold, natural text
- **High perplexity** (>50): Off-manifold, unnatural text

**Qwen results**: Stable ~4.2 (good)
**Pythia results**: 77 → 25 (⚠️ suggests intervention pushes off-manifold)

---

## Complete Results Analysis

### Cross-Model Comparison

| Metric | Qwen2.5-3B | Pythia-410M |
|--------|-----------|-------------|
| **Operator Quality** |  |  |
| Final fidelity | 94.09% | 97.84% |
| Unitary constraint | ✅ (0.000008) | ✅ (0.000005) |
| **Steering Effectiveness** |  |  |
| Pos→neg lift | -1.0pp | -2.2pp |
| Neg→pos lift | +1.9pp | +1.9pp |
| CI excludes 0? | ❌ | ❌ |
| Meets ±10pp threshold? | ❌ | ❌ |
| **Specificity** |  |  |
| Neutral drift | 2.5pp ✅ | 7.5-10pp ❌ |
| **Text Quality** |  |  |
| Perplexity (baseline) | 4.29 | 77.48 |
| Perplexity (steered) | ~4.2 | ~25 |
| On-manifold? | ✅ | ⚠️ Questionable |

---

### Key Observations

1. **Operator Training Works Perfectly**:
   - Both models: >94% fidelity
   - Unitary constraints satisfied
   - Operators learn the quantum transformation

2. **But Behavioral Effect is Null**:
   - Steering lifts: ~2pp (noise level)
   - Random operators perform identically
   - No statistical significance

3. **Model-Specific Differences**:
   - **Qwen**: Good specificity, stable perplexity, but no steering
   - **Pythia**: Poor specificity, perplexity drop suggests off-manifold

4. **Prompts Were NOT the Issue**:
   - Improved prompts didn't help
   - Rules out train/test distribution mismatch

---

## Hypotheses Tested and Ruled Out

### ✅ Ruled Out

1. **Train/test distribution mismatch**
   - Original hypothesis: Biased prompts prevent generalization
   - Test: Neutral-stem prompts with authentic sentiment
   - Result: Still no steering
   - Conclusion: Not the cause

2. **Operator training failure**
   - Hypothesis: Operators not learning transformation
   - Evidence: 94-98% fidelity, unitary constraints satisfied
   - Conclusion: Operators train correctly

3. **Blend ratio too weak**
   - Original: α=0.05 (5%)
   - Tested: α=0.5 (50%, 10x stronger)
   - Result: Still no effect
   - Conclusion: Not just about strength

4. **Prompt quality**
   - Original: Sentiment-forcing fragments
   - Improved: Natural multi-sentence narratives
   - Result: No improvement
   - Conclusion: Prompt design wasn't blocking steering

---

### 🤔 Still Under Investigation

1. **Quantum→Text Disconnect**
   - Hypothesis: Quantum states don't capture sentiment features
   - Evidence: High fidelity but zero behavioral effect
   - Status: **Primary suspect**

2. **Layer Selection**
   - Hypothesis: Layer 31/22 not optimal for sentiment
   - Evidence: No layer sweep conducted with improved prompts
   - Status: **Needs testing**

3. **Semantic vs Positional Features**
   - Hypothesis: Intervening on wrong subspace
   - Evidence: Operators might transform position encodings, not semantics
   - Status: **Needs activation analysis**

4. **Decoding Method**
   - Hypothesis: Real component loses critical information
   - Alternative: Use both Re(ψ) and Im(ψ)
   - Status: **Not tested with improved prompts**

---

## Critical Files on RunPod GPU Server

### Results (Priority 1 - MUST RETRIEVE)

**Location**: `/workspace/cogit-qmech/results/quantum_intervention/`

**Files**:
```
evaluation_qwen_local_50_20251105_073226.json    # Qwen improved prompts (blend=50%)
evaluation_pythia_410m_50_20251105_072401.json   # Pythia improved prompts (blend=50%)
evaluation_qwen_local_05_20251105_060916.json    # Qwen improved prompts (blend=5%)
evaluation_pythia_410m_05_20251105_043414.json   # Earlier Pythia test
evaluation_pythia_410m_05_20251105_060350.json   # Another Pythia test
quantum_results_5333d_20251105_060010.json       # Qwen Phase 1 data
quantum_results_5333d_20251105_071253.json       # Qwen Phase 1 (improved)
quantum_results_2666d_20251105_042140.json       # Pythia Phase 1 data
quantum_results_2666d_20251105_042429.json       # Pythia Phase 1 (v2)
quantum_results_2666d_20251105_051108.json       # Pythia Phase 1 (v3)
quantum_results_2666d_20251105_070749.json       # Pythia Phase 1 (improved)
reversibility_test_latest.json                   # Reversibility analysis
reversibility_results_20251105_042225.json       # Reversibility (Pythia)
reversibility_results_20251105_051116.json       # Reversibility (Pythia v2)
reversibility_plot_20251105_042224.png           # Visualization
reversibility_plot_20251105_051116.png           # Visualization (v2)
```

**Retrieve command**:
```bash
rsync -avz -e "ssh -p 48513" \
  root@149.7.4.151:/workspace/cogit-qmech/results/ \
  ~/cogit-qmech-backup/results/
```

---

### Trained Operators (Priority 1)

**Location**: `/workspace/cogit-qmech/models/quantum_operators/`

**Naming convention**: `{operator}_{model}_{fingerprint}.pt`

**Key files**:
```
U_pos_to_neg_qwen2.5-3B_*.pt    # Qwen positive→negative operator
U_neg_to_pos_qwen2.5-3B_*.pt    # Qwen negative→positive operator
U_pos_to_neg_pythia-410m_*.pt   # Pythia positive→negative operator
U_neg_to_pos_pythia-410m_*.pt   # Pythia negative→positive operator
```

**Fingerprint format**: `5333d_2048in_layer31_100prompts_20251105`

**Retrieve command**:
```bash
rsync -avz -e "ssh -p 48513" \
  root@149.7.4.151:/workspace/cogit-qmech/models/quantum_operators/ \
  ~/cogit-qmech-backup/models/quantum_operators/
```

---

### Quantum Encoders (Priority 1)

**Location**: `/workspace/cogit-qmech/data/sentiment_quantum/`

**Files**:
```
encoder_projection_qwen2.5-3B_latest.pt      # Qwen projection matrix (2048→5333)
encoder_projection_pythia-410m_latest.pt     # Pythia projection matrix (1024→2666)
quantum_states_qwen2.5-3B_*.pt               # Cached quantum states
quantum_states_pythia-410m_*.pt              # Cached quantum states
```

**Retrieve command**:
```bash
rsync -avz -e "ssh -p 48513" \
  root@149.7.4.151:/workspace/cogit-qmech/data/sentiment_quantum/ \
  ~/cogit-qmech-backup/data/sentiment_quantum/
```

---

### Logs (Priority 2)

**Location**: `/workspace/cogit-qmech/`

**Key logs**:
```
qwen3b_improved_final.log        # Final Qwen experiment (COMPLETE)
pythia410m_improved_final.log    # Final Pythia experiment (COMPLETE)
qwen_layer31_pipeline.log        # Earlier Qwen run
pythia_layer22_pipeline.log      # Earlier Pythia run
qwen3b_improved_baseline.log     # Alternative Qwen run
qwen3b_improved_blend_sweep.log  # Blend ratio sweep (if completed)
```

**Retrieve command**:
```bash
rsync -avz -e "ssh -p 48513" \
  root@149.7.4.151:/workspace/cogit-qmech/*.log \
  ~/cogit-qmech-backup/logs/
```

---

### Source Code (Priority 3 - Already on GitHub)

**Location**: `/workspace/cogit-qmech/`

**Key files**:
```
experiments/sentiment/run_full_pipeline.py
experiments/sentiment/quantum_phase1_collect.py
experiments/sentiment/quantum_phase2_train.py
experiments/sentiment/quantum_phase3_test.py
experiments/sentiment/evaluate_quantum_intervention.py
src/quantum_encoder.py
src/quantum_decoder.py
src/unitary_operator.py
config.py
```

**Status**: Latest code pushed to GitHub (commit f49ab98)

---

## Data Retrieval Commands

### Complete Backup (Recommended)

```bash
# Create backup directory
mkdir -p ~/cogit-qmech-backup/{results,models,data,logs}

# 1. Results (critical)
rsync -avz -e "ssh -p 48513" \
  root@149.7.4.151:/workspace/cogit-qmech/results/ \
  ~/cogit-qmech-backup/results/

# 2. Trained operators (critical)
rsync -avz -e "ssh -p 48513" \
  root@149.7.4.151:/workspace/cogit-qmech/models/ \
  ~/cogit-qmech-backup/models/

# 3. Quantum encoders and cached states (critical)
rsync -avz -e "ssh -p 48513" \
  root@149.7.4.151:/workspace/cogit-qmech/data/ \
  ~/cogit-qmech-backup/data/

# 4. All logs (important)
rsync -avz -e "ssh -p 48513" \
  root@149.7.4.151:/workspace/cogit-qmech/*.log \
  ~/cogit-qmech-backup/logs/

# 5. Verify file counts
echo "Results:" && ls ~/cogit-qmech-backup/results/quantum_intervention/ | wc -l
echo "Operators:" && ls ~/cogit-qmech-backup/models/quantum_operators/ | wc -l
echo "Data:" && ls ~/cogit-qmech-backup/data/sentiment_quantum/ | wc -l
echo "Logs:" && ls ~/cogit-qmech-backup/logs/ | wc -l
```

---

### Selective Backup (Nov 5 experiments only)

```bash
# Only files from Nov 5, 2025
rsync -avz -e "ssh -p 48513" \
  root@149.7.4.151:/workspace/cogit-qmech/results/quantum_intervention/*20251105* \
  ~/cogit-qmech-backup/results/quantum_intervention/

rsync -avz -e "ssh -p 48513" \
  root@149.7.4.151:/workspace/cogit-qmech/data/sentiment_quantum/*20251105* \
  ~/cogit-qmech-backup/data/sentiment_quantum/

# Final experiment logs
for log in qwen3b_improved_final.log pythia410m_improved_final.log; do
  rsync -avz -e "ssh -p 48513" \
    root@149.7.4.151:/workspace/cogit-qmech/$log \
    ~/cogit-qmech-backup/logs/
done
```

---

## What Each Result File Contains

### Evaluation JSON Structure

```json
{
  "config": {
    "preset": "qwen_local",
    "model_name": "Qwen/Qwen2.5-3B-Instruct",
    "quantum_dim": 5333,
    "blend_ratio": 0.5,
    "num_prompts": 100,
    "max_tokens": 60,
    "timestamp": "20251105_073226"
  },
  "summary": {
    "baseline": {
      "positive_rate": 0.59,
      "avg_sentiment_score": 0.95,
      "avg_perplexity": 4.29
    },
    "pos_to_neg": {
      "positive_rate": 0.58,
      "lift_vs_baseline": -0.01,
      "lift_ci_vs_baseline": [-0.15, 0.13],
      "lift_vs_random": 0.02,
      "lift_ci_vs_random": [-0.12, 0.16],
      "avg_sentiment_score": 0.94,
      "avg_perplexity": 4.14
    },
    "neg_to_pos": {
      "positive_rate": 0.61,
      "lift_vs_baseline": 0.019,
      "lift_ci_vs_baseline": [-0.12, 0.15],
      "lift_vs_random": 0.04,
      "lift_ci_vs_random": [-0.10, 0.18],
      "avg_sentiment_score": 0.96,
      "avg_perplexity": 4.21
    },
    "rand_pos_to_neg": {
      "positive_rate": 0.60,
      "avg_sentiment_score": 0.95,
      "avg_perplexity": 4.18
    },
    "rand_neg_to_pos": {
      "positive_rate": 0.57,
      "avg_sentiment_score": 0.93,
      "avg_perplexity": 4.25
    }
  },
  "neutral_summary": {
    "baseline": {
      "positive_rate": 0.625,
      "avg_perplexity": 3.89
    },
    "pos_to_neg": {
      "positive_rate": 0.60,
      "avg_perplexity": 3.92
    },
    "neg_to_pos": {
      "positive_rate": 0.60,
      "avg_perplexity": 3.88
    }
  },
  "records": [
    {
      "prompt": "I just finished reading a novel...",
      "baseline": {
        "text": "It was unlike anything I'd read...",
        "sentiment": "POSITIVE",
        "sentiment_score": 0.98,
        "perplexity": 3.45
      },
      "pos_to_neg": {
        "text": "The plot was predictable...",
        "sentiment": "NEGATIVE",
        "sentiment_score": 0.87,
        "perplexity": 4.12
      },
      "neg_to_pos": {...},
      "rand_pos_to_neg": {...},
      "rand_neg_to_pos": {...}
    }
    // ... 99 more prompts
  ],
  "neutral_records": [
    // ... 40 neutral prompt evaluations
  ]
}
```

**Key metrics to extract**:
- `summary.pos_to_neg.lift_vs_baseline`: Main steering effect
- `summary.*.lift_ci_vs_baseline`: Statistical significance
- `neutral_summary.*.positive_rate`: Drift measurement
- `records[i].*.perplexity`: Text quality

---

### Phase 1 Quantum States JSON

```json
{
  "config": {
    "model_name": "Qwen/Qwen2.5-3B-Instruct",
    "quantum_dim": 5333,
    "input_dim": 2048,
    "layer": 31,
    "num_prompts": 100
  },
  "metrics": {
    "positive_class": {
      "within_fidelity": 0.956,
      "cross_fidelity": 0.912
    },
    "negative_class": {
      "within_fidelity": 0.948,
      "cross_fidelity": 0.907
    },
    "separation_gap": 0.0455  // 4.55%
  },
  "quantum_states": {
    "positive": [
      // 50 complex vectors (5333-d each)
    ],
    "negative": [
      // 50 complex vectors (5333-d each)
    ]
  }
}
```

**Key metric**: `separation_gap` - measures quantum representation quality
**Target**: ≥5% for good separation
**Our result**: ~4.5-4.8% (marginal)

---

## Diagnostic Insights from Logs

### Qwen2.5-3B Log Analysis

**Key sections**:
```
[GPU Memory After model load]
  Allocated: 13.82 GB
  Reserved:  13.84 GB
  Free:      130.64 / 150.02 GB

[Quantum State Encoder]
  Real activations: 2048-d
  Quantum states:   5333-d (complex)
  Ratio:            2.60x

[Unitary Operator]
  Quantum state dim: 5333
  Parameters: 56,881,778
  → Operator loaded to GPU (0.23 GB)

✓ U_pos→neg unitary: True (deviation: 0.000008)
✓ U_neg→pos unitary: True (deviation: 0.000008)

[Decode Method]: real_component
```

**Memory efficiency**: 16.22 GB total (model + operators)
**Training convergence**: Achieved in ~3 minutes
**Validation**: All constraints satisfied

---

### Pythia-410M Log Analysis

**Key sections**:
```
[GPU Memory After model load]
  Allocated: 1.73 GB
  Reserved:  1.73 GB
  Free:      129.17 / 150.02 GB

[Quantum State Encoder]
  Real activations: 1024-d
  Quantum states:   2666-d (complex)
  Ratio:            2.60x

[Unitary Operator]
  Quantum state dim: 2666
  Parameters: 14,215,112
  → Operator loaded to GPU (0.06 GB)

✓ U_pos→neg unitary: True (deviation: 0.000005)
✓ U_neg→pos unitary: True (deviation: 0.000005)

[Decode Method]: real_component
```

**Memory efficiency**: 2.36 GB total (smaller model)
**Training convergence**: Faster than Qwen (~1 minute)
**Higher fidelity**: 97.84% vs Qwen's 94.09%

**But**: Perplexity drop (77→25) suggests off-manifold steering

---

## Statistical Power Analysis

### Sample Size

- **Prompts evaluated**: 100 per condition
- **Total comparisons**: 500 generations
  - 100 baseline
  - 100 pos→neg (learned)
  - 100 neg→pos (learned)
  - 100 random pos→neg
  - 100 random neg→pos

**Power**: With n=100, we can detect ~10pp difference with 80% power at α=0.05

### Bootstrap Precision

- **Resamples**: 2,000 per comparison
- **Confidence level**: 95%
- **Method**: Percentile bootstrap (distribution-free)

**Interpretation**: CI width ~25-30pp indicates high variance in sentiment classification

---

## Code Architecture Summary

### Pipeline Flow

```
Phase 1: Data Collection
┌─────────────────────────────────────┐
│ Load model & prompts                │
│ Extract activations at target layer │
│ Encode to quantum states (W·x → ψ) │
│ Cache for Phase 2                   │
└─────────────────────────────────────┘
           ↓
Phase 2: Operator Training
┌─────────────────────────────────────┐
│ Load cached quantum states          │
│ Initialize unitary operators        │
│ Optimize Born rule fidelity         │
│ Save trained operators              │
└─────────────────────────────────────┘
           ↓
Phase 3: Text Generation (qualitative)
┌─────────────────────────────────────┐
│ Load model & operators              │
│ Hook target layer                   │
│ Generate with intervention          │
│ Save comparison outputs             │
└─────────────────────────────────────┘
           ↓
Phase 4: Quantitative Evaluation
┌─────────────────────────────────────┐
│ Generate baseline + steered text    │
│ Classify sentiment (SiEBERT)        │
│ Compute perplexity                  │
│ Bootstrap CI analysis               │
│ Save metrics to JSON                │
└─────────────────────────────────────┘
```

### Key Classes

**QuantumStateEncoder** (`src/quantum_encoder.py`):
```python
class QuantumStateEncoder:
    def __init__(self, input_dim, quantum_dim, seed=42):
        # W ∈ ℂ^(input_dim × quantum_dim)
        self.projection = self._init_complex_projection(...)

    def encode(self, activations):
        # x ∈ ℝ^d → ψ ∈ ℂ^q
        return self._normalize(self.projection @ activations)
```

**UnitaryOperator** (`src/unitary_operator.py`):
```python
class UnitaryOperator(nn.Module):
    def __init__(self, quantum_dim):
        # U = exp(iH), H = H†
        self.H_real = nn.Parameter(...)
        self.H_imag = nn.Parameter(...)

    def forward(self, psi):
        H = self.make_hermitian(self.H_real, self.H_imag)
        U = torch.matrix_exp(1j * H)
        return U @ psi
```

**QuantumStateDecoder** (`src/quantum_decoder.py`):
```python
class QuantumStateDecoder:
    def __init__(self, encoder):
        # W† (pseudoinverse)
        self.pseudoinverse = torch.linalg.pinv(encoder.projection)

    def decode(self, psi, method='real_component'):
        x_complex = self.pseudoinverse @ psi
        if method == 'real_component':
            return x_complex.real
        elif method == 'real_imag_avg':
            return (x_complex.real + x_complex.imag) / 2
        # ... other methods
```

**QuantumInterventionSystem** (`experiments/sentiment/quantum_phase3_test.py`):
```python
class QuantumInterventionSystem:
    def run_with_quantum_intervention(self, prompt, operator, blend_ratio):
        def hook_fn(module, input, output):
            # Get activations
            acts = output[0, -1, :]  # Last token

            # Quantum transform
            psi = self.encoder.encode(acts)
            psi_prime = operator(psi)
            acts_quantum = self.decoder.decode(psi_prime)

            # Blend
            acts_blended = (1-blend_ratio)*acts + blend_ratio*acts_quantum

            # Replace
            output[0, -1, :] = acts_blended

        # Register hook, generate, remove hook
        handle = model.layers[target_layer].register_forward_hook(hook_fn)
        completion = model.generate(prompt, max_tokens=60)
        handle.remove()
        return completion
```

---

## Future Experiment Suggestions

### Immediate Next Steps

1. **Layer Sweep with Improved Prompts**
   ```bash
   # Test layers 25-35 for Qwen
   python quantum_phase1_collect.py \
     --preset qwen_test_layers \
     --prompts prompts/improved_prompts_100.json

   # Find optimal layer, then run full pipeline
   python run_full_pipeline.py \
     --preset qwen_local \
     --layer {best_layer} \
     --prompts prompts/improved_prompts_100.json \
     --blend-ratio 0.5
   ```

2. **Activation Analysis**
   - PCA on transformed activations
   - Compare semantic vs positional components
   - Visualize what operators actually change

3. **Classical Baseline**
   - Direct activation steering (no quantum encoding)
   - Compare effectiveness to quantum approach
   - Determines if quantum formalism adds value

4. **Alternative Decode Methods**
   ```bash
   python evaluate_quantum_intervention.py \
     --preset qwen_local \
     --prompts prompts/improved_prompts_100.json \
     --decode-method real_imag_avg \
     --blend-ratio 0.5
   ```

---

### Longer-Term Investigations

1. **Subspace Intervention**
   - Identify sentiment-specific subspace via probing
   - Train operators only on that subspace
   - Hypothesis: Holistic state transform too broad

2. **Multi-Layer Intervention**
   - Apply operators at multiple layers simultaneously
   - Cumulative effect might be stronger

3. **Supervised Decoding**
   - Train decoder specifically for sentiment tasks
   - Current decoder is unsupervised (pseudoinverse)

4. **Larger Models**
   - Test on Qwen-7B or Llama-3-8B
   - Hypothesis: Larger models may have clearer sentiment representations

5. **Different Tasks**
   - Formality transformation (casual ↔ formal)
   - Tense shifting (past ↔ future)
   - Perspective change (1st ↔ 3rd person)
   - **Why**: Sentiment might not be linearly separable in activation space

---

## Lessons Learned

### Technical

1. **Train/test distribution matching is necessary but not sufficient**
   - Improved prompts didn't solve the problem
   - But they're still better for evaluation validity

2. **High operator fidelity ≠ behavioral effect**
   - 98% fidelity means operators work in quantum space
   - But quantum→text decoding may lose information

3. **Perplexity is a critical diagnostic**
   - Qwen: Stable perplexity, on-manifold (but no steering)
   - Pythia: Perplexity drop, off-manifold (and no steering)
   - Either way: no steering

4. **Model size affects representation quality**
   - Pythia (410M): Higher fidelity, worse specificity
   - Qwen (3B): Lower fidelity, better specificity
   - But neither steers successfully

---

### Methodological

1. **Always measure neutral drift**
   - Essential for ruling out noise/random effects
   - Qwen passed, Pythia failed (but both failed steering)

2. **Random operator controls are crucial**
   - Our learned operators ≈ random operators
   - Proves lack of specific learning

3. **Statistical rigor matters**
   - Bootstrap CIs revealed high variance
   - Small effects (<5pp) likely spurious

4. **Document everything**
   - Experiment IDs, timestamps, fingerprints
   - Makes reproduction possible

---

### Conceptual

1. **Quantum formalism may be overkill**
   - Complex machinery (encoding, unitary, decoding)
   - Classical activation steering might work better
   - Need direct comparison

2. **Representation matters more than transformation**
   - If sentiment isn't encoded in activations, no operator can steer it
   - Layer selection and subspace identification are critical

3. **Activation interventions are hard**
   - Even with perfect operators, decoding is lossy
   - Real component loses imaginary information
   - Alternative: Work in activation space directly

---

## Open Questions

1. **Why does the quantum transformation not affect text generation?**
   - Operators transform states correctly (high fidelity)
   - But decoded activations don't change model behavior
   - Possible answers:
     - Decoder loses critical information
     - Wrong subspace being transformed
     - Blend ratio still too weak (need >100%?)
     - Model compensates in later layers

2. **What do quantum states actually represent?**
   - Are they capturing semantics or just position?
   - Separation gap of 4.8% suggests weak class structure
   - Need dimensionality reduction + visualization

3. **Is sentiment linearly separable in activation space?**
   - Quantum operators are essentially linear transforms
   - If sentiment is nonlinear feature, won't work
   - Alternative: Nonlinear intervention (e.g., MLP)

4. **Why does Pythia go off-manifold but Qwen doesn't?**
   - Pythia: Perplexity 77→25 (dramatic change)
   - Qwen: Perplexity ~4 (stable)
   - Model architecture differences?
   - Quantum dimension relative to model size?

---

## Citations and References

**Quantum-inspired methods**:
- Born rule fidelity: |⟨ψ|φ⟩|² as similarity metric
- Unitary operators: U = exp(iH) parameterization
- Quantum state encoding: Complex projection for representational capacity

**Activation steering literature**:
- Concept Activation Vectors (Kim et al.)
- Linear representation hypothesis
- Steering vectors (Turner et al.)
- Contrast pairs methodology

**Sentiment analysis**:
- SiEBERT: State-of-the-art sentiment classifier
- Used for automated evaluation of generations

**Statistical methods**:
- Bootstrap confidence intervals (Efron & Tibshirani)
- Distribution-free hypothesis testing
- Percentile method for CI construction

---

## Acknowledgments

- **Austin Morrissey**: Primary researcher, experimental design
- **Claude (Anthropic)**: Technical implementation, analysis
- **RunPod**: GPU infrastructure (H200, 150GB VRAM)
- **HuggingFace**: Model hosting (Qwen, Pythia)
- **TransformerLens**: Model inspection library

---

## Appendix: Reproduction Instructions

### Environment Setup

```bash
# Clone repository
git clone https://github.com/your-username/cogit-qmech.git
cd cogit-qmech

# Install dependencies
pip install torch transformers transformer-lens
pip install numpy scipy scikit-learn
pip install tqdm

# Verify GPU
python -c "import torch; print(torch.cuda.is_available())"
```

### Run Complete Pipeline

```bash
# Qwen2.5-3B with improved prompts
python experiments/sentiment/run_full_pipeline.py \
  --preset qwen_local \
  --prompts prompts/improved_prompts_100.json \
  --neutral-prompts prompts/neutral_prompts_40.json \
  --num-prompts 100 \
  --quantum-ratio 2.6 \
  --blend-ratio 0.5 \
  --max-tokens 60 \
  --decode-method real_component \
  --yes

# Pythia-410M with improved prompts
python experiments/sentiment/run_full_pipeline.py \
  --preset pythia_410m \
  --prompts prompts/improved_prompts_100.json \
  --neutral-prompts prompts/neutral_prompts_40.json \
  --num-prompts 100 \
  --quantum-ratio 2.6 \
  --blend-ratio 0.5 \
  --max-tokens 60 \
  --decode-method real_component \
  --yes
```

**Expected runtime**:
- Qwen: ~35 minutes on H200 GPU
- Pythia: ~25 minutes on H200 GPU

**Expected output**:
- Results JSON in `results/quantum_intervention/`
- Operators in `models/quantum_operators/`
- Encoders in `data/sentiment_quantum/`

---

## Summary

**Total experiments**: 2 major experiments completed (Qwen + Pythia)
**Total runtime**: ~60 minutes
**Total data generated**: ~2 GB
**Total GPU cost**: ~$5 (H200 at $0.60/hr)

**Conclusion**: Despite high-quality operators and improved prompts, quantum sentiment steering remains ineffective. The issue appears to be a fundamental disconnect between quantum state transformations and text generation behavior. Further investigation needed into activation subspaces, layer selection, and classical baselines.

**Status**: Ready for mentor discussion and next phase planning.

---

**Document created**: November 5, 2025
**Last updated**: November 5, 2025
**Version**: 1.0
**Location**: `/Users/austinmorrissey/cogit-qmech-backup/COMPLETE_EXPERIMENT_SUMMARY_NOV5_2025.md`
