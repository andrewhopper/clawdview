# Generate Project Card

Generate a card.html file for the current project's docs/ folder.

## Instructions

1. Find the `.project` file in the current working directory or nearest parent
2. Read the `.project` file to extract:
   - name
   - uuid
   - phase (number 1-9)
   - phase_name
   - category (work/shared/oss/personal/unspecified)
   - status (active/archived/completed)
   - description
   - tech_stack
   - domain (if deployed)

3. Count files in the project (exclude node_modules, .git, __pycache__, .venv)

4. Generate a densified summary (1 sentence: what it does + target user)

5. Extract 3 key features/details as bullet points

6. Create docs/ folder if it doesn't exist

7. Generate docs/card.html using this structure:

```html
<div class="project-card" data-category="{category}" data-status="{status}" data-phase="{phase}">
  <div class="card-left">
    <div class="card-header">
      <h2>{name}</h2>
      <span class="category-badge category-{category}">{CATEGORY}</span>
      <span class="file-count">{file_count} files</span>
      <span class="uuid">{uuid}</span>
    </div>
    <div class="stage-indicator">
      <div class="stage-dots">
        <!-- For each phase 1-9: class="stage-dot completed" if < current, "active" if == current, empty if > current -->
        <div class="stage-dot {phase_1_class}"></div>
        <div class="stage-dot {phase_2_class}"></div>
        <div class="stage-dot {phase_3_class}"></div>
        <div class="stage-dot {phase_4_class}"></div>
        <div class="stage-dot {phase_5_class}"></div>
        <div class="stage-dot {phase_6_class}"></div>
        <div class="stage-dot {phase_7_class}"></div>
        <div class="stage-dot {phase_8_class}"></div>
        <div class="stage-dot {phase_9_class}"></div>
      </div>
      <span class="stage-label">Phase {phase}</span>
      <span class="stage-name">{phase_name}</span>
    </div>
    <div class="card-summary">
      {summary}
    </div>
    <div class="card-details">
      <ul>
        <li>{detail_1}</li>
        <li>{detail_2}</li>
        <li>{detail_3}</li>
      </ul>
      <div class="tech-stack">{tech_stack}</div>
      {domain_html if domain else ""}
    </div>
  </div>
  <div class="card-right">
    <h3>Next Steps</h3>
    <div class="notes-lines">
      <div class="notes-line"></div>
      <div class="notes-line"></div>
      <div class="notes-line"></div>
      <div class="notes-line"></div>
      <div class="notes-line"></div>
    </div>
  </div>
</div>
```

8. If domain URL exists, add: `<div class="domain-url">{domain}</div>` after tech-stack

9. Report success with path to generated card

## Phase Classes

- Phases before current: `completed`
- Current phase: `active`
- Phases after current: (empty string)

## Summary Rules

- 1 sentence max
- Format: "{What it does}. Target: {who it's for}."
- No flowery language
- Be specific

## Example Output

```
Generated: projects/work/active/strands-narrative-7k9m2/docs/card.html
- Name: Strands Narrative Agent
- Phase: 6 (Design)
- Category: work
- Files: 45
```
