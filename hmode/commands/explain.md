Transform content for a specific audience profile.

## Usage
/explain <source_file> [--profile <profile_name>] [--duration <duration>] [--interactive]

## Arguments
- `source_file`: Path to the markdown/text file to transform
- `--profile`: Preset profile name (see below) or "custom"
- `--duration`: Override duration (30s, 2min, 5min, 20min, 60min)
- `--interactive`: Enable refinement mode

## Preset Profiles

| Profile | Description |
|---------|-------------|
| `cold-vc` | First meeting with VC, 2min pitch |
| `warm-vc` | Follow-up VC meeting, 5min |
| `family-investor` | High-stakes personal investor, 5min |
| `phd-advisor-field` | Expert in your domain, 20min |
| `phd-advisor-adjacent` | Expert in related field, 20min |
| `tech-cofounder` | Technical partner, implementation focus, 5min |
| `executive-sponsor` | Business leader, strategic focus, 2min |
| `engineer-team` | Technical team members, 5min |
| `conference-attendee` | Quick intro at event, 30s |
| `grant-reviewer` | Academic/gov funding reviewer, 5min |

## Audience Axes (6 Dimensions)

When using `--profile custom`, you'll set:

1. **Relationship**: stranger → acquaintance → colleague → friend → trusted_ally
2. **Personal Stakes**: none → professional → personal → family
3. **Cognitive Style**: 1-5 (1=very different, 5=thinks like me)
4. **Technical Capacity**: none → basic → intermediate → advanced → expert
5. **Domain Expertise**: none → aware → familiar → proficient → expert
6. **Operator↔Visionary**: 1-5 (1=pure operator/how, 5=pure visionary/why)

## Instructions

1. Read the source file provided by the user
2. If no profile specified, ask user to select from preset profiles or create custom
3. If custom profile requested, walk through each axis interactively
4. Transform the content according to:
   - **Relationship**: High = direct, Low = build credibility first
   - **Stakes**: High = emphasize risk mitigation, downside protection
   - **Cognitive Style**: Low = translate mental models, use their frameworks
   - **Technical Capacity**: Low = analogies over equations
   - **Domain Expertise**: Low = build from first principles
   - **Operator↔Visionary**: Operator = how/implementation, Visionary = why/strategy
   - **Duration**: Target word count (30s=75w, 2min=300w, 5min=750w, 20min=3000w, 60min=9000w)
5. Present transformed output with:
   - Word count and estimated speaking time
   - Key adaptations made for this audience
6. If `--interactive`, offer refinement options:
   - More/less technical depth
   - More/less risk emphasis
   - Simpler language
   - Different duration
   - Custom feedback

## Example

```
User: /explain whitepaper.md --profile cold-vc

Claude:
╭─ AUDIENCE-ADAPTIVE EXPLAINER ─╮

Source: whitepaper.md (2,847 words)
Profile: cold-vc
  → stranger · professional · cog:2 · intermediate · none · vis:4 · 2min

╭─ OUTPUT (2min / 287 words) ─╮

[Transformed content optimized for cold VC meeting...]

╭─ ADAPTATIONS ─╮
• Removed technical implementation details
• Led with market size and opportunity
• Added team credibility section
• Framed as visionary opportunity, not operational details

[c]opy  [r]efine  [s]ave
```

## Output Format

Always structure output as:
1. Profile summary (axes values)
2. Transformed content in a code block
3. Adaptations made (bullet list)
4. Action options if interactive
