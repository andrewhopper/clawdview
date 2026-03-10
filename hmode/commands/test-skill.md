---
uuid: cmd-test-skill-3a4b5c6d
version: 1.0.0
last_updated: 2025-11-11
description: Test Claude skills with input/output verification
---

# Test Skill

Unit testing framework for Claude skills. Validates skill behavior against expected inputs/outputs stored in JSON test cases.

## Usage

```bash
# Test a specific skill
/test-skill densify

# Test all skills
/test-skill --all

# Create new test case template
/test-skill densify --create-test

# Run tests and update snapshots
/test-skill densify --update-snapshots
```

**Arguments:**
- `{skill_name}`: Name of skill to test (e.g., densify, cite, kill-m-dash)
- `--all`: Run tests for all skills with test files
- `--create-test`: Generate test template for skill
- `--update-snapshots`: Update expected outputs with actual outputs
- `--verbose`: Show detailed test execution logs

## Test File Structure

**Location:** `tests/skills/{skill_name}.test.jsonl`

**Format:** JSONL (one JSON test case per line)

```jsonl
{"id": "test-001", "description": "Basic compression", "input": "This is a very long sentence...", "expected_output": "Long sentence...", "match_type": "exact"}
{"id": "test-002", "description": "Preserve brand names", "input": "Use PostgreSQL and GitHub...", "expected_output": "Use postgres and GitHub...", "match_type": "contains", "contains": ["postgres", "GitHub"]}
```

## Test Case Schema

```json
{
  "id": "test-001",
  "description": "Brief description of what this test validates",
  "input": "Input text or parameters for the skill",
  "expected_output": "Expected output from skill execution",
  "match_type": "exact|contains|regex|semantic",
  "contains": ["keyword1", "keyword2"],
  "regex_pattern": "pattern.*to.*match",
  "semantic_threshold": 0.85,
  "tags": ["compression", "brand-names"],
  "skip": false,
  "skip_reason": "Flaky test - needs investigation"
}
```

**Match Types:**

| Type | Description | Use Case |
|------|-------------|----------|
| `exact` | Output must match exactly | Deterministic transformations |
| `contains` | Output must contain all keywords | Check presence of key elements |
| `regex` | Output must match regex pattern | Flexible structure validation |
| `semantic` | Semantic similarity > threshold | LLM-generated outputs |

**Optional Fields:**
- `contains`: Array of strings for `match_type: "contains"`
- `regex_pattern`: Regex string for `match_type: "regex"`
- `semantic_threshold`: Float 0.0-1.0 for `match_type: "semantic"` (default: 0.85)
- `tags`: Array of strings for categorizing tests
- `skip`: Boolean to skip test temporarily
- `skip_reason`: Explanation for skipped test

## Workflow

### Step 1: Load Test Cases

1. **Determine skill to test**:
   - If `--all` flag: Find all `tests/skills/*.test.jsonl` files
   - Otherwise: Use provided `{skill_name}`

2. **Read test file**:
   - Path: `tests/skills/{skill_name}.test.jsonl`
   - Parse each line as JSON object
   - Validate schema (required fields: id, description, input, expected_output, match_type)

3. **Filter tests**:
   - Skip tests where `skip: true`
   - Log skipped tests with reason

### Step 2: Execute Tests

4. **For each test case**:
   ```python
   test_case = load_test_case(line)

   # Execute skill with input
   actual_output = execute_skill(skill_name, test_case.input)

   # Validate output
   result = validate_output(actual_output, test_case)

   # Record result
   record_result(result)
   ```

5. **Execute skill**:
   - Simulate invoking `/densify "input text"` or equivalent
   - Capture output from skill execution
   - Handle errors gracefully

6. **Validate output** based on `match_type`:

**Exact:**
```python
result = actual_output.strip() == expected_output.strip()
```

**Contains:**
```python
result = all(keyword in actual_output for keyword in test_case.contains)
```

**Regex:**
```python
import re
result = re.search(test_case.regex_pattern, actual_output) is not None
```

**Semantic:**
```python
# Use simple word overlap or embedding similarity
similarity = compute_semantic_similarity(actual_output, expected_output)
result = similarity >= test_case.semantic_threshold
```

### Step 3: Report Results

7. **Generate test report**:

```markdown
# Test Results: {skill_name}

**Skill**: {skill_name}
**Tested**: {timestamp}
**Total**: {total_tests}
**Passed**: {passed_count} ✅
**Failed**: {failed_count} ❌
**Skipped**: {skipped_count} ⏭️

---

## Passed Tests ✅

- [test-001] Basic compression
- [test-003] Preserve brand names

---

## Failed Tests ❌

### [test-002] Arrow replacement

**Input:**
```
This leads to the following result
```

**Expected:**
```
This → following result
```

**Actual:**
```
This leads to result
```

**Match Type**: exact
**Diff**:
- Expected: "This → following result"
+ Actual: "This leads to result"

---

## Skipped Tests ⏭️

- [test-004] Complex nested structure (Reason: Flaky test - needs investigation)

---

## Summary

✅ {passed_count}/{total_tests} tests passed ({pass_rate}%)
❌ {failed_count} tests failed
⏭️ {skipped_count} tests skipped

{pass/fail status emoji}
```

8. **Display summary**:
   - Show pass/fail counts
   - List failed tests with diffs
   - Exit with appropriate status

### Step 4: Update Snapshots (Optional)

9. **If `--update-snapshots` flag**:
   - For each test, replace `expected_output` with `actual_output`
   - Write updated test cases back to JSONL file
   - Report updated tests

```markdown
# Snapshots Updated

Updated {count} snapshots in tests/skills/{skill_name}.test.jsonl

- [test-001] Basic compression
- [test-003] Preserve brand names

⚠️ Review changes before committing
```

### Step 5: Create Test Template (Optional)

10. **If `--create-test` flag**:
    - Read skill command file: `commands/{skill_name}.md`
    - Extract examples from documentation
    - Generate template test cases
    - Write to `tests/skills/{skill_name}.test.jsonl`

```jsonl
{"id": "test-001", "description": "TODO: Describe test", "input": "TODO: Add input", "expected_output": "TODO: Add expected output", "match_type": "exact"}
{"id": "test-002", "description": "TODO: Describe test", "input": "TODO: Add input", "expected_output": "TODO: Add expected output", "match_type": "contains", "contains": ["keyword1", "keyword2"]}
```

## Implementation Notes

### Executing Skills

**Challenge:** Skills are markdown files, not executable code

**Solution 1 - Parse and execute instructions:**
```python
# Read skill markdown file
skill_content = read_file(f"commands/{skill_name}.md")

# Extract instructions section
instructions = extract_instructions(skill_content)

# Execute using Claude with skill instructions + test input
output = execute_with_claude(instructions, test_input)
```

**Solution 2 - Integration test approach:**
```python
# Create temporary conversation context
# Simulate user invoking skill with test input
# Capture Claude's response
# Extract output from response
```

**Recommended:** Solution 1 - Parse skill file, execute instructions directly

### Semantic Similarity

For `match_type: "semantic"`, implement simple similarity:

```python
def compute_semantic_similarity(actual, expected):
    # Simple word overlap approach
    actual_words = set(actual.lower().split())
    expected_words = set(expected.lower().split())

    intersection = actual_words & expected_words
    union = actual_words | expected_words

    return len(intersection) / len(union) if union else 0.0
```

**Future enhancement:** Use embedding models for better semantic comparison

### Test Isolation

Each test should be independent:
- No shared state between tests
- Clean execution context per test
- Deterministic ordering

## Directory Structure

```
tests/
└── skills/
    ├── densify.test.jsonl
    ├── cite.test.jsonl
    ├── kill-m-dash.test.jsonl
    ├── amazon-style-checker.test.jsonl
    └── generate-delivery-email.test.jsonl
```

## Example Test Cases

**densify.test.jsonl:**
```jsonl
{"id": "test-001", "description": "Basic compression with arrow", "input": "This leads to the following result", "expected_output": "This → following result", "match_type": "exact"}
{"id": "test-002", "description": "Preserve PostgreSQL as postgres", "input": "Use PostgreSQL database", "expected_output": "Use postgres database", "match_type": "exact"}
{"id": "test-003", "description": "Preserve brand names", "input": "Deploy to GitHub and AWS", "expected_output": "Deploy to GitHub and AWS", "match_type": "contains", "contains": ["GitHub", "AWS"]}
{"id": "test-004", "description": "Remove filler words", "input": "This is very really basically good", "expected_output": "This is good", "match_type": "exact"}
```

**cite.test.jsonl:**
```jsonl
{"id": "test-001", "description": "Add citation to fact", "input": "AWS launched in 2006", "expected_output": "AWS launched in 2006[1]", "match_type": "contains", "contains": ["2006[1]", "## References", "[1]"]}
{"id": "test-002", "description": "Multiple citations", "input": "Python released 1991. JavaScript released 1995.", "expected_output": "Python released 1991[1]. JavaScript released 1995[2].", "match_type": "regex", "regex_pattern": "1991\\[\\d+\\].*1995\\[\\d+\\]"}
```

**kill-m-dash.test.jsonl:**
```jsonl
{"id": "test-001", "description": "Remove em dashes", "input": "This is good—really good—for testing", "expected_output": "This is good, really good, for testing", "match_type": "exact"}
{"id": "test-002", "description": "Remove AI fluff words", "input": "It's important to note that we should carefully consider", "expected_output": "We should consider", "match_type": "semantic", "semantic_threshold": 0.8}
```

## Error Handling

**Missing test file:**
```
❌ Error: No test file found for skill 'densify'
Expected: tests/skills/densify.test.jsonl

Run: /test-skill densify --create-test
```

**Invalid test JSON:**
```
❌ Error: Invalid JSON in test file line 3
Line: {"id": "test-003", "description": "Test", "input": "...

Error: Unexpected end of JSON input
```

**Skill execution error:**
```
❌ Test failed: test-001
Reason: Skill execution error
Error: Command 'densify' not found
```

## Best Practices

1. **Test coverage**: Create tests for each example in skill documentation
2. **Edge cases**: Test empty input, very long input, special characters
3. **Regression tests**: Add test for each bug fix
4. **Clear descriptions**: Make test descriptions self-explanatory
5. **Semantic matching**: Use for LLM outputs, not deterministic transformations
6. **Update snapshots carefully**: Review changes before committing

## Integration with Development Workflow

**Add skill:**
1. Create skill markdown file: `commands/{name}.md`
2. Run: `/test-skill {name} --create-test`
3. Fill in test cases in `tests/skills/{name}.test.jsonl`
4. Run: `/test-skill {name}` to validate

**Modify skill:**
1. Edit skill markdown file
2. Run: `/test-skill {name}` to check for regressions
3. Update test cases or fix skill as needed
4. Optionally: `/test-skill {name} --update-snapshots` if changes are intentional

**Pre-commit:**
```bash
# Run all skill tests before committing changes
/test-skill --all
```

## Future Enhancements

- [ ] Parallel test execution for faster runs
- [ ] Watch mode: re-run tests on file changes
- [ ] Coverage report: which skill features are tested
- [ ] Benchmark mode: measure skill execution time
- [ ] Fuzzing: generate random inputs to find edge cases
- [ ] CI integration: GitHub Actions workflow

---

Build confidence in skill behavior through systematic testing.
