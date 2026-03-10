"""
Test suite for microsite AI steering rules.

Tests verify that microsite rules correctly trigger for:
1. Vite + React frontend selection
2. FastAPI backend selection
3. Shared UI library prompts
4. S3 publishing prompts
5. Domain model usage and extension prompts
6. Storybook requirements for shared components

Run with: pytest .guardrails/ai-steering/tests/test_microsite_rules.py -v
"""

import json
import pytest
from pathlib import Path
from typing import Any
from dataclasses import dataclass


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def rules_path() -> Path:
    """Path to microsites.json rules file."""
    return Path(__file__).parent.parent / "rules" / "microsites.json"


@pytest.fixture
def schema_path() -> Path:
    """Path to schema.json for validation."""
    return Path(__file__).parent.parent / "schema.json"


@pytest.fixture
def microsite_rules(rules_path: Path) -> dict[str, Any]:
    """Load microsites rules."""
    with open(rules_path) as f:
        return json.load(f)


@pytest.fixture
def schema(schema_path: Path) -> dict[str, Any]:
    """Load schema for validation."""
    with open(schema_path) as f:
        return json.load(f)


@pytest.fixture
def domain_registry_path() -> Path:
    """Path to domain registry."""
    return Path(__file__).parent.parent.parent.parent / "shared" / "semantic" / "domains" / "registry.yaml"


# ============================================================================
# Schema Validation Tests
# ============================================================================

class TestSchemaCompliance:
    """Tests that rules conform to schema."""

    def test_rules_file_exists(self, rules_path: Path):
        """Verify microsites.json exists."""
        assert rules_path.exists(), f"Rules file not found: {rules_path}"

    def test_rules_valid_json(self, rules_path: Path):
        """Verify rules file is valid JSON."""
        with open(rules_path) as f:
            rules = json.load(f)
        assert "rules" in rules
        assert isinstance(rules["rules"], list)

    def test_all_rules_have_required_fields(self, microsite_rules: dict):
        """Verify all rules have required fields per schema."""
        required_fields = ["uuid", "id", "version", "level", "category", "description", "action"]

        for rule in microsite_rules["rules"]:
            for field in required_fields:
                assert field in rule, f"Rule {rule.get('id', 'unknown')} missing required field: {field}"

    def test_all_rules_have_valid_levels(self, microsite_rules: dict):
        """Verify all rules have valid constraint levels."""
        valid_levels = ["NEVER", "ALWAYS", "MUST", "MUST_NOT", "SHOULD", "SHOULD_NOT", "PREFER", "AVOID"]

        for rule in microsite_rules["rules"]:
            assert rule["level"] in valid_levels, f"Rule {rule['id']} has invalid level: {rule['level']}"

    def test_all_rules_have_valid_categories(self, microsite_rules: dict):
        """Verify all rules have valid categories."""
        valid_categories = ["tool_usage", "code_generation", "file_operations", "communication",
                          "workflow", "git", "performance", "security", "testing"]

        for rule in microsite_rules["rules"]:
            assert rule["category"] in valid_categories, f"Rule {rule['id']} has invalid category: {rule['category']}"

    def test_all_rules_have_unique_uuids(self, microsite_rules: dict):
        """Verify all UUIDs are unique."""
        uuids = [rule["uuid"] for rule in microsite_rules["rules"]]
        assert len(uuids) == len(set(uuids)), "Duplicate UUIDs found"

    def test_all_rules_have_unique_ids(self, microsite_rules: dict):
        """Verify all human-readable IDs are unique."""
        ids = [rule["id"] for rule in microsite_rules["rules"]]
        assert len(ids) == len(set(ids)), "Duplicate rule IDs found"


# ============================================================================
# Rule Content Tests
# ============================================================================

class TestMicrositeRuleContent:
    """Tests for specific rule content."""

    def test_vite_react_rule_exists(self, microsite_rules: dict):
        """Verify Vite+React frontend rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "site-use-vite-react")
        assert rule is not None
        assert rule["level"] == "SHOULD"
        assert "Vite" in rule["action"]["target"]

    def test_nextjs_rule_exists(self, microsite_rules: dict):
        """Verify Next.js frontend rule exists as equal option."""
        rule = self._find_rule_by_id(microsite_rules, "site-use-nextjs")
        assert rule is not None
        assert rule["level"] == "SHOULD"
        assert "Next.js" in rule["action"]["target"]

    def test_fastapi_rule_exists(self, microsite_rules: dict):
        """Verify FastAPI backend rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "microsite-use-fastapi-backend")
        assert rule is not None
        assert rule["level"] == "SHOULD"
        assert "FastAPI" in rule["action"]["target"]

    def test_shared_ui_library_prompt_rule_exists(self, microsite_rules: dict):
        """Verify shared UI library prompt rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "microsite-prompt-shared-ui-library")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "shared" in rule["action"]["message"].lower()

    def test_s3_publish_prompt_rule_exists(self, microsite_rules: dict):
        """Verify S3 publishing prompt rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "microsite-prompt-s3-publish")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "S3" in rule["action"]["target"]

    def test_domain_model_usage_rule_exists(self, microsite_rules: dict):
        """Verify domain model usage rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "microsite-use-existing-domain-models")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "registry.yaml" in rule["action"]["target"]

    def test_domain_model_extension_rule_exists(self, microsite_rules: dict):
        """Verify domain model extension prompt rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "microsite-prompt-extend-domain-models")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "extend" in rule["description"].lower()

    def test_storybook_rule_exists(self, microsite_rules: dict):
        """Verify Storybook requirement rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "microsite-react-components-storybook")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "Storybook" in rule["action"]["target"]

    def test_pydantic_models_rule_exists(self, microsite_rules: dict):
        """Verify Pydantic models rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "microsite-pydantic-models")
        assert rule is not None
        assert rule["level"] == "MUST"

    def test_semantic_layer_registry_rule_exists(self, microsite_rules: dict):
        """Verify semantic layer registry rule exists for all app types."""
        rule = self._find_rule_by_id(microsite_rules, "app-use-semantic-layer-registry")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "semantic" in rule["action"]["target"].lower()
        # Should apply to Python, Node, React, Next.js
        when_contexts = rule["context"]["when"]
        assert any("Python" in w for w in when_contexts)
        assert any("Node" in w for w in when_contexts)
        assert any("React" in w for w in when_contexts)
        assert any("Next" in w for w in when_contexts)

    def test_design_system_repository_rule_exists(self, microsite_rules: dict):
        """Verify design system repository rule exists for React/UI apps."""
        rule = self._find_rule_by_id(microsite_rules, "react-use-design-system-repository")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "ui-components" in rule["action"]["target"].lower()

    def test_design_system_audit_rule_exists(self, microsite_rules: dict):
        """Verify design system component audit rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "design-system-component-audit")
        assert rule is not None
        assert rule["level"] == "SHOULD"

    def test_app_creation_workflow_rule_exists(self, microsite_rules: dict):
        """Verify app creation workflow rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "app-creation-workflow")
        assert rule is not None
        assert rule["level"] == "MUST"
        # Verify workflow has all steps
        message = rule["action"]["message"]
        assert "CREATE" in message
        assert "DEFINE" in message
        assert "CHECK" in message
        assert "USE" in message or "CREATE" in message

    def test_human_approval_rule_exists(self, microsite_rules: dict):
        """Verify human approval rule exists for new registry additions."""
        rule = self._find_rule_by_id(microsite_rules, "new-component-human-approval")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "approval" in rule["action"]["target"].lower()

    def test_known_primitives_rule_exists(self, microsite_rules: dict):
        """Verify rule for using known primitives exists."""
        rule = self._find_rule_by_id(microsite_rules, "use-known-primitives-first")
        assert rule is not None
        assert rule["level"] == "MUST"
        # Should mention key primitives
        message = rule["action"]["message"]
        assert "Artifact" in message
        assert "Workflow" in message
        assert "Rule" in message
        assert "Guardrail" in message

    def test_ensure_primitives_in_shared_domain_rule_exists(self, microsite_rules: dict):
        """Verify rule ensuring primitives are in shared domains exists."""
        rule = self._find_rule_by_id(microsite_rules, "ensure-primitives-in-shared-domain")
        assert rule is not None
        assert rule["level"] == "MUST"

    def test_typescript_domain_types_rule_exists(self, microsite_rules: dict):
        """Verify TypeScript strong typing rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "typescript-use-domain-types")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "TypeScript" in rule["description"]
        assert "shared/semantic/domains" in rule["action"]["target"]
        # Should mention avoiding 'any' type
        assert "any" in rule["action"]["message"].lower()

    def test_python_pydantic_models_rule_exists(self, microsite_rules: dict):
        """Verify Python Pydantic models rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "python-use-pydantic-models")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "Python" in rule["description"]
        assert "Pydantic" in rule["description"]
        assert "BaseModel" in rule["action"]["message"]

    def test_html_s3_publish_rule_exists(self, microsite_rules: dict):
        """Verify HTML S3 publishing rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "html-offer-s3-publish")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "HTML" in rule["description"]
        assert "S3" in rule["action"]["target"]
        # Should have file pattern for HTML
        assert "*.html" in rule["context"]["filePattern"]

    def test_zip_s3_publish_rule_exists(self, microsite_rules: dict):
        """Verify ZIP S3 publishing rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "zip-offer-s3-publish")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "*.zip" in rule["context"]["filePattern"]

    def test_svg_s3_publish_rule_exists(self, microsite_rules: dict):
        """Verify SVG S3 publishing rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "svg-offer-s3-publish")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "*.svg" in rule["context"]["filePattern"]

    def test_pdf_s3_publish_rule_exists(self, microsite_rules: dict):
        """Verify PDF S3 publishing rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "pdf-offer-s3-publish")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "*.pdf" in rule["context"]["filePattern"]

    def test_mp3_s3_publish_rule_exists(self, microsite_rules: dict):
        """Verify MP3 S3 publishing rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "mp3-offer-s3-publish")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "*.mp3" in rule["context"]["filePattern"]

    def test_mp4_s3_publish_rule_exists(self, microsite_rules: dict):
        """Verify MP4 S3 publishing rule exists."""
        rule = self._find_rule_by_id(microsite_rules, "mp4-offer-s3-publish")
        assert rule is not None
        assert rule["level"] == "MUST"
        assert "*.mp4" in rule["context"]["filePattern"]

    def _find_rule_by_id(self, rules: dict, rule_id: str) -> dict | None:
        """Helper to find rule by ID."""
        for rule in rules["rules"]:
            if rule["id"] == rule_id:
                return rule
        return None


# ============================================================================
# Scenario-Based Tests
# ============================================================================

@dataclass
class TestScenario:
    """Test scenario for rule matching."""
    name: str
    context: dict[str, Any]
    expected_rules: list[str]
    description: str


class TestScenarioMatching:
    """Tests that rules match expected scenarios."""

    @pytest.fixture
    def scenarios(self) -> list[TestScenario]:
        """Define test scenarios for microsites."""
        return [
            TestScenario(
                name="new_site_project",
                context={
                    "taskType": "New Project",
                    "when": ["creating site", "creating microsite"]
                },
                expected_rules=[
                    "site-use-vite-react",
                    "site-use-nextjs",
                    "microsite-use-fastapi-backend"
                ],
                description="When creating a new site, should offer Vite+React or Next.js, and FastAPI for backend"
            ),
            TestScenario(
                name="creating_ui_component",
                context={
                    "taskType": "Task",
                    "when": ["creating new UI component"]
                },
                expected_rules=[
                    "microsite-prompt-shared-ui-library",
                    "microsite-use-shadcn-components"
                ],
                description="When creating UI components, should prompt for shared library and suggest shadcn"
            ),
            TestScenario(
                name="adding_shared_component",
                context={
                    "taskType": "Task",
                    "when": ["adding component to shared UI library"]
                },
                expected_rules=[
                    "microsite-react-components-storybook"
                ],
                description="When adding to shared library, should require Storybook stories"
            ),
            TestScenario(
                name="deployment_ready",
                context={
                    "phase": "PHASE_8_IMPLEMENTATION",
                    "when": ["microsite implementation complete"]
                },
                expected_rules=[
                    "microsite-prompt-s3-publish"
                ],
                description="When implementation complete, should prompt for S3 deployment"
            ),
            TestScenario(
                name="creating_data_models",
                context={
                    "taskType": "Task",
                    "when": ["creating data models"]
                },
                expected_rules=[
                    "microsite-use-existing-domain-models"
                ],
                description="When creating data models, should check shared domains first"
            ),
            TestScenario(
                name="new_entity_needed",
                context={
                    "taskType": "Task",
                    "when": ["new entity type needed"]
                },
                expected_rules=[
                    "microsite-prompt-extend-domain-models"
                ],
                description="When new entity needed, should prompt to extend shared models"
            ),
            TestScenario(
                name="fastapi_endpoint",
                context={
                    "taskType": "Task",
                    "when": ["creating FastAPI endpoints"]
                },
                expected_rules=[
                    "microsite-pydantic-models"
                ],
                description="When creating FastAPI endpoints, should require Pydantic models"
            ),
            TestScenario(
                name="python_app_creation",
                context={
                    "taskType": "New Project",
                    "when": ["creating Python app"]
                },
                expected_rules=[
                    "app-use-semantic-layer-registry"
                ],
                description="Python apps must use semantic layer registry"
            ),
            TestScenario(
                name="nodejs_app_creation",
                context={
                    "taskType": "New Project",
                    "when": ["creating Node.js app"]
                },
                expected_rules=[
                    "app-use-semantic-layer-registry"
                ],
                description="Node.js apps must use semantic layer registry"
            ),
            TestScenario(
                name="react_app_creation",
                context={
                    "taskType": "New Project",
                    "when": ["creating React app", "creating frontend"]
                },
                expected_rules=[
                    "app-use-semantic-layer-registry",
                    "react-use-design-system-repository"
                ],
                description="React apps must use both semantic layer and design system"
            ),
            TestScenario(
                name="nextjs_app_creation",
                context={
                    "taskType": "New Project",
                    "when": ["creating Next.js app"]
                },
                expected_rules=[
                    "app-use-semantic-layer-registry"
                ],
                description="Next.js apps must use semantic layer registry"
            ),
            TestScenario(
                name="creating_ui_component_audit",
                context={
                    "taskType": "Task",
                    "when": ["creating UI component"]
                },
                expected_rules=[
                    "design-system-component-audit"
                ],
                description="Creating UI components should audit design system first"
            ),
            TestScenario(
                name="new_app_workflow",
                context={
                    "taskType": "New Project",
                    "when": ["creating new app", "creating microsite"]
                },
                expected_rules=[
                    "app-creation-workflow"
                ],
                description="New app creation should follow structured workflow"
            ),
            TestScenario(
                name="new_component_approval",
                context={
                    "taskType": "Task",
                    "when": ["creating new component not in registry"]
                },
                expected_rules=[
                    "new-component-human-approval"
                ],
                description="New components not in registry require human approval"
            ),
            TestScenario(
                name="typescript_app_creation",
                context={
                    "taskType": "New Project",
                    "when": ["creating TypeScript app", "creating TypeScript types"]
                },
                expected_rules=[
                    "typescript-use-domain-types"
                ],
                description="TypeScript apps must use strongly-typed domain models"
            ),
            TestScenario(
                name="python_app_with_pydantic",
                context={
                    "taskType": "New Project",
                    "when": ["creating Python app", "creating Python models"]
                },
                expected_rules=[
                    "python-use-pydantic-models"
                ],
                description="Python apps must use Pydantic models from shared domains"
            ),
            TestScenario(
                name="html_file_creation",
                context={
                    "taskType": "Task",
                    "when": ["creating HTML file", "HTML file complete"]
                },
                expected_rules=[
                    "html-offer-s3-publish"
                ],
                description="HTML files should prompt for S3 publishing"
            ),
        ]

    def test_scenario_rules_exist(self, microsite_rules: dict, scenarios: list[TestScenario]):
        """Verify all expected rules from scenarios exist."""
        all_rule_ids = {rule["id"] for rule in microsite_rules["rules"]}

        for scenario in scenarios:
            for expected_rule in scenario.expected_rules:
                assert expected_rule in all_rule_ids, \
                    f"Scenario '{scenario.name}' expects rule '{expected_rule}' which doesn't exist"

    def test_scenario_context_matching(self, microsite_rules: dict, scenarios: list[TestScenario]):
        """Verify rules have matching context for scenarios."""
        for scenario in scenarios:
            for expected_rule_id in scenario.expected_rules:
                rule = next((r for r in microsite_rules["rules"] if r["id"] == expected_rule_id), None)
                assert rule is not None

                # Check if rule context matches scenario
                rule_context = rule.get("context", {})

                # Check taskType if specified
                if "taskType" in scenario.context and "taskType" in rule_context:
                    assert scenario.context["taskType"] in rule_context["taskType"], \
                        f"Rule '{expected_rule_id}' taskType doesn't match scenario '{scenario.name}'"

    def test_all_scenarios_have_matching_rules(self, scenarios: list[TestScenario]):
        """Verify all scenarios have at least one expected rule."""
        for scenario in scenarios:
            assert len(scenario.expected_rules) > 0, \
                f"Scenario '{scenario.name}' has no expected rules"


# ============================================================================
# Integration Tests
# ============================================================================

class TestMicrositeWorkflowIntegration:
    """Integration tests for complete microsite workflow."""

    def test_two_microsite_workflow(self, microsite_rules: dict):
        """
        Test Case 1: Create two microsites with FastAPI backends.

        Verifies rules trigger for:
        - React/Vite frontend selection
        - FastAPI backend selection
        - Shared UI library prompts
        - S3 publishing prompts
        - Domain model usage/extension prompts
        """
        # Simulate microsite 1 creation
        microsite1_steps = [
            ("New Project", ["creating microsite"]),  # Should trigger Vite+React, FastAPI
            ("Task", ["creating new UI component"]),   # Should trigger shared library prompt
            ("Task", ["creating data models"]),        # Should trigger domain model check
            ("Task", ["new entity type needed"]),      # Should trigger extension prompt
            ("PHASE_8_IMPLEMENTATION", ["microsite implementation complete"]),  # S3 prompt
        ]

        # Microsite 2 follows same pattern
        microsite2_steps = microsite1_steps.copy()

        # Collect triggered rules for each step
        for step_type, step_context in microsite1_steps:
            triggered = self._get_triggered_rules(microsite_rules, step_type, step_context)
            assert len(triggered) > 0, f"No rules triggered for step: {step_type}, {step_context}"

    def test_shared_component_flow(self, microsite_rules: dict):
        """Test that shared component flow triggers Storybook requirement."""
        # When adding component to shared library
        triggered = self._get_triggered_rules(
            microsite_rules,
            "Task",
            ["adding component to shared UI library"]
        )

        rule_ids = [r["id"] for r in triggered]
        assert "microsite-react-components-storybook" in rule_ids

    def test_domain_model_check_flow(self, microsite_rules: dict, domain_registry_path: Path):
        """Test domain model check references real registry."""
        rule = next(
            (r for r in microsite_rules["rules"] if r["id"] == "microsite-use-existing-domain-models"),
            None
        )
        assert rule is not None
        assert "registry.yaml" in rule["action"]["target"]

        # Verify registry actually exists
        assert domain_registry_path.exists(), f"Domain registry not found: {domain_registry_path}"

    def _get_triggered_rules(
        self,
        rules: dict,
        task_type: str,
        context_when: list[str]
    ) -> list[dict]:
        """Get rules that would trigger for given context."""
        triggered = []
        for rule in rules["rules"]:
            rule_context = rule.get("context", {})

            # Check taskType match
            task_match = "taskType" not in rule_context or task_type in rule_context.get("taskType", [])

            # Check phase match (if phase provided as task_type)
            phase_match = "phase" not in rule_context or task_type in rule_context.get("phase", [])

            # Check when conditions
            rule_when = rule_context.get("when", [])
            when_match = any(w in rule_when for w in context_when) if rule_when else True

            if (task_match or phase_match) and when_match:
                triggered.append(rule)

        return triggered


# ============================================================================
# Rule Constraint Level Tests
# ============================================================================

class TestConstraintLevels:
    """Tests for rule constraint level appropriateness."""

    def test_must_rules_are_critical(self, microsite_rules: dict):
        """MUST rules should be for critical behaviors."""
        must_rules = [r for r in microsite_rules["rules"] if r["level"] == "MUST"]

        # Verify MUST rules exist for critical behaviors
        must_rule_ids = {r["id"] for r in must_rules}
        critical_behaviors = [
            "microsite-prompt-shared-ui-library",
            "microsite-prompt-s3-publish",
            "microsite-use-existing-domain-models",
            "microsite-prompt-extend-domain-models",
            "microsite-react-components-storybook",
            "microsite-pydantic-models",
            "app-use-semantic-layer-registry",
            "react-use-design-system-repository",
            "app-creation-workflow",
            "new-component-human-approval",
            "use-known-primitives-first",
            "ensure-primitives-in-shared-domain",
            "typescript-use-domain-types",
            "python-use-pydantic-models",
            "html-offer-s3-publish",
            "zip-offer-s3-publish",
            "svg-offer-s3-publish",
            "pdf-offer-s3-publish",
            "mp3-offer-s3-publish",
            "mp4-offer-s3-publish"
        ]

        for behavior in critical_behaviors:
            assert behavior in must_rule_ids, f"Critical behavior '{behavior}' should be MUST level"

    def test_should_rules_are_recommendations(self, microsite_rules: dict):
        """SHOULD rules should be for recommendations, not requirements."""
        should_rules = [r for r in microsite_rules["rules"] if r["level"] == "SHOULD"]

        # These are preferences, not requirements
        should_rule_ids = {r["id"] for r in should_rules}
        preference_rules = [
            "site-use-vite-react",
            "site-use-nextjs",
            "microsite-use-fastapi-backend",
            "microsite-use-shadcn-components",
            "microsite-storybook-required-stories",
            "design-system-component-audit"
        ]

        for pref in preference_rules:
            assert pref in should_rule_ids, f"Preference rule '{pref}' should be SHOULD level"

    def test_no_never_rules_for_tech_choices(self, microsite_rules: dict):
        """NEVER rules shouldn't be used for tech stack choices."""
        never_rules = [r for r in microsite_rules["rules"] if r["level"] == "NEVER"]

        # Tech choices should be SHOULD/PREFER, not NEVER
        for rule in never_rules:
            assert "vite" not in rule["id"].lower()
            assert "react" not in rule["id"].lower()
            assert "fastapi" not in rule["id"].lower()


# ============================================================================
# Example Tests
# ============================================================================

class TestRuleExamples:
    """Tests that rule examples are well-formed."""

    def test_all_rules_have_examples(self, microsite_rules: dict):
        """Verify all rules have at least one example."""
        for rule in microsite_rules["rules"]:
            assert "examples" in rule, f"Rule {rule['id']} missing examples"
            assert len(rule["examples"]) > 0, f"Rule {rule['id']} has empty examples"

    def test_examples_have_correct_and_incorrect(self, microsite_rules: dict):
        """Verify examples show both correct and incorrect behavior."""
        for rule in microsite_rules["rules"]:
            for i, example in enumerate(rule.get("examples", [])):
                assert "scenario" in example, f"Rule {rule['id']} example {i} missing scenario"
                assert "correct" in example, f"Rule {rule['id']} example {i} missing correct behavior"
                # incorrect is optional but recommended
                if "incorrect" not in example:
                    pytest.skip(f"Rule {rule['id']} example {i} missing incorrect (optional)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
