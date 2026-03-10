---
name: "design_agent_tests_readme"
---

<!-- File UUID: 4e5f6a7b-8c9d-0e1f-2a3b-4c5d6e7f8a9b -->

# Design Agent Tests

Automated tests for validating the Information Architecture (IA) and UX Component agents.

## Test Structure

```
tests/
├── README.md                  # This file
├── validate_design_output.py  # Output validation functions
├── test_validators.py         # Pytest unit tests
├── features/
│   ├── information-architecture.feature  # BDD scenarios for IA agent
│   └── ux-component.feature              # BDD scenarios for UX agent
└── fixtures/
    ├── valid_html_asset.html    # Valid HTML (should pass)
    ├── invalid_html_asset.html  # Invalid HTML (should fail)
    ├── valid_ia_output.md       # Valid IA output (should pass)
    └── invalid_ia_output.md     # Invalid IA output (should fail)
```

## Running Tests

### Unit Tests (pytest)

```bash
# Run all validator tests
cd hmode/agents/tests
pytest test_validators.py -v

# Run with coverage
pytest test_validators.py --cov=validate_design_output --cov-report=html

# Run specific test class
pytest test_validators.py::TestHtmlAssetValidation -v

# Run specific test
pytest test_validators.py::TestHtmlAssetValidation::test_valid_html_passes -v
```

### Output Validation CLI

```bash
# Validate an HTML asset
python validate_design_output.py path/to/asset.html

# Validate with explicit type
python validate_design_output.py path/to/output.md --type ia

# Validate YAML navigation
python validate_design_output.py navigation.yaml --type yaml
```

### BDD Tests (Cucumber)

The feature files in `features/` define behavior specifications. To run them:

```bash
# Install cucumber dependencies (if not already)
npm install --save-dev @cucumber/cucumber ts-node typescript

# Run with cucumber-js
npx cucumber-js features/*.feature --require step-definitions/*.ts
```

**Note:** Step definitions need to be implemented to connect Gherkin scenarios to actual agent invocations.

## What's Tested

### HTML Asset Validation

| Check | Severity | Description |
|-------|----------|-------------|
| Metadata header | Error | Must have Asset, Asset ID, Date |
| Design tokens | Error | No raw hex colors (#ffffff) |
| Atomic level | Error | Must be valid (atom/molecule/organism/template/page) |
| Inline styles | Warning | Should use Tailwind classes |
| Spacing scale | Warning | Should use 4px-based tokens |

### IA Output Validation

| Check | Severity | Description |
|-------|----------|-------------|
| Hierarchy depth | Error | Max 3 levels deep |
| Empty labels | Error | All nav items need labels |
| Handoff section | Warning | Should have "IA HANDOFF SUMMARY" |
| User flow | Warning | Should include flow diagram |

### Gate Handoff Validation

| Check | Severity | Description |
|-------|----------|-------------|
| Handoff section | Error | IA must have handoff summary |
| Component mapping | Warning | UX should reference IA components |

## Adding New Tests

### Adding Fixtures

1. Create a new file in `fixtures/`
2. For valid fixtures: Follow all design system rules
3. For invalid fixtures: Add comment explaining violations

### Adding Unit Tests

1. Add test methods to appropriate class in `test_validators.py`
2. Use `@pytest.mark.parametrize` for data-driven tests
3. Follow naming: `test_<what>_<expected_result>`

### Adding BDD Scenarios

1. Add scenarios to appropriate `.feature` file
2. Use existing step patterns where possible
3. Tag scenarios: `@critical`, `@smoke`, `@gate-integration`

## Integration with CI/CD

Add to your project's Makefile:

```makefile
test-design-agents:
	cd hmode/agents/tests && pytest test_validators.py -v

validate-design-output:
	python hmode/agents/tests/validate_design_output.py $(FILE)
```

## Validation in Agent Workflow

To automatically validate agent outputs, integrate the validators:

```python
from validate_design_output import validate_html_asset, validate_ia_output

# After IA agent generates output
ia_result = validate_ia_output(ia_agent_output)
if not ia_result.valid:
    raise ValueError(f"IA output invalid: {ia_result.errors}")

# After UX agent generates output
ux_result = validate_html_asset(ux_agent_output)
if not ux_result.valid:
    raise ValueError(f"UX output invalid: {ux_result.errors}")
```

## Related Documentation

- Agent definitions: `hmode/agents/`
- Design system: `hmode/shared/design-system/`
- Gate definitions: `CLAUDE.md` Section 5.0
- Testing standards: `hmode/shared/standards/testing/`
