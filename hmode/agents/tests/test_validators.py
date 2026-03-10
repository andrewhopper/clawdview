#!/usr/bin/env python3
"""
Unit tests for design agent output validators.

Run with: pytest test_validators.py -v
"""
# File UUID: 3d4e5f6a-7b8c-9d0e-1f2a-3b4c5d6e7f8a

import pytest
from pathlib import Path

from validate_design_output import (
    validate_html_asset,
    validate_ia_output,
    validate_navigation_yaml,
    validate_gate_handoff,
    validate_file_size,
    estimate_paint_time,
    validate_typography,
    validate_contrast,
    validate_responsive_classes,
    validate_design_system,
    ValidationResult,
    MILLERS_LAW_MAX_ITEMS,
    AVAILABLE_THEMES,
    REQUIRED_SHADCN_TOKENS,
)

# =============================================================================
# Fixtures
# =============================================================================

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def valid_html():
    """Load valid HTML asset fixture."""
    return (FIXTURES_DIR / "valid_html_asset.html").read_text()


@pytest.fixture
def invalid_html():
    """Load invalid HTML asset fixture."""
    return (FIXTURES_DIR / "invalid_html_asset.html").read_text()


@pytest.fixture
def valid_ia():
    """Load valid IA output fixture."""
    return (FIXTURES_DIR / "valid_ia_output.md").read_text()


@pytest.fixture
def invalid_ia():
    """Load invalid IA output fixture."""
    return (FIXTURES_DIR / "invalid_ia_output.md").read_text()


# =============================================================================
# HTML Asset Validation Tests
# =============================================================================

class TestHtmlAssetValidation:
    """Tests for HTML/visual asset validation."""

    def test_valid_html_passes(self, valid_html):
        """Valid HTML with proper metadata and tokens should pass."""
        result = validate_html_asset(valid_html)
        assert result.valid, f"Expected valid, got errors: {result.errors}"
        assert len(result.errors) == 0

    def test_valid_html_extracts_metadata(self, valid_html):
        """Validator should extract metadata from valid HTML."""
        result = validate_html_asset(valid_html)
        assert result.metadata.get("name") is not None
        assert result.metadata.get("id") is not None
        assert result.metadata.get("date") is not None
        assert result.metadata.get("atomic_level") == "molecule"

    def test_invalid_html_fails(self, invalid_html):
        """Invalid HTML with violations should fail."""
        result = validate_html_asset(invalid_html)
        assert not result.valid, "Expected invalid result"
        assert len(result.errors) > 0

    def test_detects_missing_metadata(self, invalid_html):
        """Should detect missing asset metadata header."""
        result = validate_html_asset(invalid_html)
        assert any("metadata" in err.lower() for err in result.errors)

    def test_detects_raw_hex_colors(self, invalid_html):
        """Should detect raw hex colors that should be tokens."""
        result = validate_html_asset(invalid_html)
        assert any("hex" in err.lower() for err in result.errors)

    def test_detects_inline_styles(self, invalid_html):
        """Should warn about inline styles."""
        result = validate_html_asset(invalid_html)
        assert any("inline" in warn.lower() for warn in result.warnings)

    def test_allows_hex_in_comments(self):
        """Should not flag hex colors that are in example comments."""
        content = """
        <!--
        Asset: Example
        Asset ID: ex-12345678.v1
        Date: 2025-01-24
        Atomic Level: atom

        NEVER use raw hex like #1a1a2e
        ❌ BAD: #ffffff
        ✅ GOOD: hsl(var(--background))
        -->
        <div class="bg-background text-foreground"></div>
        """
        result = validate_html_asset(content)
        # Should not flag the hex colors in the comment examples
        assert result.valid or not any("hex" in err.lower() for err in result.errors)

    def test_validates_atomic_level(self):
        """Should validate atomic level is valid."""
        content = """
        <!--
        Asset: Test
        Asset ID: ts-12345678.v1
        Date: 2025-01-24
        Atomic Level: invalid_level
        -->
        <div></div>
        """
        result = validate_html_asset(content)
        assert any("atomic level" in err.lower() for err in result.errors)

    @pytest.mark.parametrize("atomic_level", [
        "atom", "molecule", "organism", "template", "page"
    ])
    def test_accepts_valid_atomic_levels(self, atomic_level):
        """Should accept all valid atomic levels."""
        content = f"""
        <!--
        Asset: Test
        Asset ID: ts-12345678.v1
        Date: 2025-01-24
        Atomic Level: {atomic_level}
        -->
        <div class="bg-background"></div>
        """
        result = validate_html_asset(content)
        assert not any("atomic level" in err.lower() for err in result.errors)


# =============================================================================
# IA Output Validation Tests
# =============================================================================

class TestIaOutputValidation:
    """Tests for Information Architecture output validation."""

    def test_valid_ia_passes(self, valid_ia):
        """Valid IA with proper structure should pass."""
        result = validate_ia_output(valid_ia)
        assert result.valid, f"Expected valid, got errors: {result.errors}"

    def test_valid_ia_has_handoff(self, valid_ia):
        """Valid IA should have handoff section detected."""
        result = validate_ia_output(valid_ia)
        assert result.metadata.get("has_handoff") is True

    def test_valid_ia_has_user_flow(self, valid_ia):
        """Valid IA should have user flow detected."""
        result = validate_ia_output(valid_ia)
        assert result.metadata.get("has_user_flow") is True

    def test_valid_ia_respects_depth(self, valid_ia):
        """Valid IA should have hierarchy depth <= 3."""
        result = validate_ia_output(valid_ia)
        assert result.metadata.get("hierarchy_depth", 0) <= 3

    def test_invalid_ia_fails_on_depth(self, invalid_ia):
        """Invalid IA with deep hierarchy should fail."""
        result = validate_ia_output(invalid_ia)
        assert not result.valid
        assert any("deep" in err.lower() or "level" in err.lower() for err in result.errors)

    def test_detects_missing_handoff(self, invalid_ia):
        """Should warn about missing handoff section."""
        result = validate_ia_output(invalid_ia)
        assert any("handoff" in warn.lower() for warn in result.warnings)

    def test_detects_empty_labels(self, invalid_ia):
        """Should detect items with missing/empty labels."""
        result = validate_ia_output(invalid_ia)
        assert any("label" in err.lower() for err in result.errors)


# =============================================================================
# YAML Navigation Validation Tests
# =============================================================================

class TestMillersLaw:
    """Tests for Miller's Law (max 7 items per group)."""

    def test_valid_ia_respects_millers_law(self, valid_ia):
        """Valid IA should have no more than 7 items per group."""
        result = validate_ia_output(valid_ia)
        max_siblings = result.metadata.get("max_siblings", 0)
        assert max_siblings <= MILLERS_LAW_MAX_ITEMS, (
            f"Max siblings {max_siblings} exceeds Miller's Law limit of {MILLERS_LAW_MAX_ITEMS}"
        )

    def test_detects_millers_law_violation_in_tree(self):
        """Should detect groups with more than 7 items."""
        content = """
## Navigation

```
├── Dashboard
├── Projects
├── Reports
├── Analytics
├── Settings
├── Users
├── Billing
├── Integrations
├── Support
├── Documentation
└── Admin
```

Flow → Something
IA HANDOFF SUMMARY:
- Navigation pattern: sidebar
"""
        result = validate_ia_output(content)
        assert any("miller" in err.lower() for err in result.errors)

    def test_accepts_7_items(self):
        """Should accept exactly 7 items (the limit)."""
        content = """
## Navigation

```
├── Dashboard
├── Projects
├── Reports
├── Analytics
├── Settings
├── Users
└── Help
```

Flow → Dashboard
IA HANDOFF SUMMARY:
- Done
"""
        result = validate_ia_output(content)
        assert not any("miller" in err.lower() for err in result.errors)

    def test_yaml_millers_law_violation(self):
        """YAML nav with >7 items at one level should fail."""
        yaml_content = """
        navigation:
          primary:
            - name: Home
            - name: Products
            - name: Services
            - name: About
            - name: Blog
            - name: Contact
            - name: Careers
            - name: Investors
            - name: Partners
            - name: Legal
        """
        result = validate_navigation_yaml(yaml_content)
        assert any("miller" in err.lower() for err in result.errors)

    def test_yaml_millers_law_children_violation(self):
        """YAML nav children exceeding 7 should fail."""
        yaml_content = """
        navigation:
          primary:
            - name: Products
              children:
                - name: P1
                - name: P2
                - name: P3
                - name: P4
                - name: P5
                - name: P6
                - name: P7
                - name: P8
                - name: P9
        """
        result = validate_navigation_yaml(yaml_content)
        assert any("miller" in err.lower() for err in result.errors)

    def test_yaml_millers_law_passes(self):
        """YAML nav with 7 or fewer items should pass."""
        yaml_content = """
        navigation:
          primary:
            - name: Home
            - name: Products
            - name: About
            - name: Blog
            - name: Contact
        """
        result = validate_navigation_yaml(yaml_content)
        assert not any("miller" in err.lower() for err in result.errors)


class TestYamlNavigationValidation:
    """Tests for YAML navigation structure validation."""

    def test_valid_yaml_passes(self):
        """Valid YAML navigation should pass."""
        yaml_content = """
        navigation:
          primary:
            - name: Dashboard
              path: /dashboard
            - name: Settings
              path: /settings
              children:
                - name: Account
                  path: /settings/account
        """
        result = validate_navigation_yaml(yaml_content)
        assert result.valid

    def test_detects_deep_hierarchy(self):
        """Should detect navigation exceeding 3 levels."""
        yaml_content = """
        navigation:
          primary:
            - name: Level 1
              children:
                - name: Level 2
                  children:
                    - name: Level 3
                      children:
                        - name: Level 4
                          children:
                            - name: Level 5
        """
        result = validate_navigation_yaml(yaml_content)
        assert not result.valid
        assert any("deep" in err.lower() for err in result.errors)

    def test_detects_missing_name(self):
        """Should detect nav items missing name field."""
        yaml_content = """
        navigation:
          primary:
            - path: /dashboard
        """
        result = validate_navigation_yaml(yaml_content)
        assert any("name" in err.lower() for err in result.errors)

    def test_invalid_yaml_fails(self):
        """Should fail on invalid YAML syntax."""
        result = validate_navigation_yaml("{ invalid yaml [[")
        assert not result.valid
        assert any("yaml" in err.lower() for err in result.errors)


# =============================================================================
# Gate Handoff Validation Tests
# =============================================================================

class TestGateHandoffValidation:
    """Tests for IA → UX gate handoff validation."""

    def test_valid_handoff_passes(self, valid_ia):
        """Valid handoff should pass when UX references components."""
        ux_input = """
        Implementing the dashboard with:
        - Sidebar navigation (as specified in IA)
        - Breadcrumbs for deep pages
        - Tab components for settings
        - Card components for metrics
        """
        result = validate_gate_handoff(valid_ia, ux_input)
        assert result.valid

    def test_detects_missing_handoff_section(self):
        """Should fail if IA output has no handoff summary."""
        ia_without_handoff = """
        # Some IA Output
        Navigation structure here but no handoff section.
        """
        ux_input = "Some UX implementation"
        result = validate_gate_handoff(ia_without_handoff, ux_input)
        assert not result.valid
        assert any("handoff" in err.lower() for err in result.errors)

    def test_warns_on_missing_components(self, valid_ia):
        """Should warn if UX doesn't reference IA components."""
        ux_input = """
        Just implementing a simple button.
        No navigation or charts mentioned.
        """
        result = validate_gate_handoff(valid_ia, ux_input)
        # Should have warnings about missing components
        assert len(result.warnings) > 0 or not result.valid


# =============================================================================
# Integration Tests
# =============================================================================

class TestValidatorIntegration:
    """Integration tests combining multiple validators."""

    def test_full_workflow_validation(self, valid_ia, valid_html):
        """Test validating a complete IA → UX workflow."""
        # Step 1: Validate IA output
        ia_result = validate_ia_output(valid_ia)
        assert ia_result.valid, "IA output should be valid"

        # Step 2: Validate UX output
        ux_result = validate_html_asset(valid_html)
        assert ux_result.valid, "UX output should be valid"

        # Step 3: Validate handoff (if both outputs exist)
        handoff_result = validate_gate_handoff(valid_ia, valid_html)
        # Handoff might have warnings but shouldn't have errors
        assert len(handoff_result.errors) == 0

    def test_result_serialization(self, valid_html):
        """Test that ValidationResult can be serialized to dict."""
        result = validate_html_asset(valid_html)
        result_dict = result.to_dict()

        assert "valid" in result_dict
        assert "errors" in result_dict
        assert "warnings" in result_dict
        assert "metadata" in result_dict
        assert isinstance(result_dict["errors"], list)


# =============================================================================
# Edge Cases
# =============================================================================

class TestEdgeCases:
    """Edge case tests for validators."""

    def test_empty_content(self):
        """Should handle empty content gracefully."""
        html_result = validate_html_asset("")
        ia_result = validate_ia_output("")

        # Should fail validation but not crash
        assert not html_result.valid
        assert not ia_result.valid

    def test_minimal_valid_html(self):
        """Test minimum valid HTML asset."""
        minimal = """
        <!--
        Asset: Minimal
        Asset ID: mn-12345678.v1
        Date: 2025-01-24
        Atomic Level: atom
        -->
        <div class="bg-background text-foreground p-4">Hello</div>
        """
        result = validate_html_asset(minimal)
        assert result.valid

    def test_unicode_content(self):
        """Should handle unicode content."""
        unicode_html = """
        <!--
        Asset: Unicode Test 日本語
        Asset ID: un-12345678.v1
        Date: 2025-01-24
        Atomic Level: molecule
        -->
        <div class="bg-background">こんにちは 🎉 Émoji</div>
        """
        result = validate_html_asset(unicode_html)
        assert result.valid



# =============================================================================
# Typography Validation Tests
# =============================================================================

class TestTypographyValidation:
    """Tests for typography validation."""

    def test_detects_magic_font_sizes(self):
        """Should detect non-standard font sizes."""
        content = """
        <style>
          .bad { font-size: 15px; }
          .also-bad { font-size: 17px; }
        </style>
        """
        result = validate_typography(content)
        assert len(result.metadata.get("font_size_violations", [])) == 2

    def test_accepts_standard_font_sizes(self):
        """Should accept font sizes in Tailwind scale."""
        content = """
        <style>
          .ok { font-size: 12px; }  /* text-xs */
          .also-ok { font-size: 16px; }  /* text-base */
          .large { font-size: 24px; }  /* text-2xl */
        </style>
        """
        result = validate_typography(content)
        assert len(result.metadata.get("font_size_violations", [])) == 0

    def test_detects_raw_font_colors(self):
        """Should detect raw hex colors in font properties."""
        content = """
        <style>
          .bad { color: #333333; }
          .also-bad { fill: #ff0000; }
        </style>
        """
        result = validate_typography(content)
        assert len(result.metadata.get("font_color_violations", [])) == 2

    def test_finds_tailwind_text_classes(self):
        """Should identify Tailwind text classes used."""
        content = """
        <div class="text-sm text-base text-lg text-xl">
          Content
        </div>
        """
        result = validate_typography(content)
        classes = result.metadata.get("tailwind_text_classes_found", [])
        assert "text-sm" in classes
        assert "text-base" in classes
        assert "text-lg" in classes
        assert "text-xl" in classes

    def test_valid_html_typography(self, valid_html):
        """Valid HTML fixture should pass typography checks."""
        result = validate_typography(valid_html)
        assert result.valid or len(result.errors) == 0


# =============================================================================
# Contrast Validation Tests
# =============================================================================

class TestContrastValidation:
    """Tests for color contrast validation."""

    def test_extracts_color_variables(self):
        """Should extract HSL color variables from CSS."""
        content = """
        <style>
          :root {
            --background: 0 0% 100%;
            --foreground: 240 10% 3.9%;
          }
        </style>
        """
        result = validate_contrast(content)
        assert "background" in result.metadata.get("color_variables_found", [])
        assert "foreground" in result.metadata.get("color_variables_found", [])

    def test_warns_on_low_contrast_patterns(self):
        """Should warn about obviously low contrast patterns."""
        content = """
        <div class="text-white bg-white">Invisible</div>
        """
        result = validate_contrast(content)
        assert len(result.warnings) > 0

    def test_accepts_high_contrast(self):
        """Should accept proper contrast ratios."""
        content = """
        <style>
          :root {
            --background: 0 0% 100%;
            --foreground: 0 0% 0%;
          }
        </style>
        <div class="text-foreground bg-background">Visible</div>
        """
        result = validate_contrast(content)
        assert result.valid


# =============================================================================
# Responsive Validation Tests
# =============================================================================

class TestResponsiveValidation:
    """Tests for responsive design validation."""

    def test_detects_responsive_prefixes(self):
        """Should detect Tailwind responsive prefixes."""
        content = """
        <div class="flex sm:flex-row md:grid lg:hidden xl:block">
          Content
        </div>
        """
        result = validate_responsive_classes(content)
        prefixes = result.metadata.get("responsive_prefixes_found", [])
        assert "sm" in prefixes
        assert "md" in prefixes
        assert "lg" in prefixes
        assert "xl" in prefixes

    def test_warns_on_no_responsive_classes(self):
        """Should warn when no responsive classes found."""
        content = """
        <div class="flex p-4 m-2">
          Non-responsive content
        </div>
        """
        result = validate_responsive_classes(content)
        assert len(result.warnings) > 0

    def test_detects_flex_and_grid(self):
        """Should detect flexible layout usage."""
        content = """
        <div class="flex">Flex</div>
        <div class="grid">Grid</div>
        """
        result = validate_responsive_classes(content)
        assert result.metadata.get("has_flex_layout") is True
        assert result.metadata.get("has_grid_layout") is True

    def test_requires_viewport_meta(self):
        """Should error when viewport meta is missing."""
        content = """
        <html>
        <head><title>Test</title></head>
        <body>No viewport meta</body>
        </html>
        """
        result = validate_responsive_classes(content)
        assert any("viewport" in err.lower() for err in result.errors)

    def test_accepts_viewport_meta(self):
        """Should accept pages with viewport meta."""
        content = """
        <html>
        <head>
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body class="flex">Has viewport meta</body>
        </html>
        """
        result = validate_responsive_classes(content)
        assert not any("viewport" in err.lower() for err in result.errors)

    def test_warns_on_small_touch_targets(self):
        """Should warn about potentially small touch targets."""
        content = """
        <button class="w-4 h-4">Tiny</button>
        <button class="w-6 h-6">Small</button>
        """
        result = validate_responsive_classes(content)
        assert len(result.warnings) > 0

    def test_valid_html_responsive(self, valid_html):
        """Valid HTML fixture should have some responsive features."""
        result = validate_responsive_classes(valid_html)
        # Valid fixture should at least have viewport meta
        assert result.metadata.get("has_flex_layout") or result.metadata.get("has_grid_layout")


# =============================================================================
# File Size Validation Tests
# =============================================================================

class TestFileSizeValidation:
    """Tests for file size limits."""

    def test_small_atom_passes(self):
        """Atom-level content under 5KB should pass."""
        content = '<button class="bg-primary text-primary-foreground p-2">Click</button>'
        result = validate_file_size(content, "atom")
        assert result.valid
        assert result.metadata["file_size_kb"] < 5

    def test_oversized_atom_fails(self):
        """Atom content over 5KB should fail."""
        content = "x" * 6000  # 6KB
        result = validate_file_size(content, "atom")
        assert not result.valid
        assert any("exceeds" in err.lower() for err in result.errors)

    def test_valid_html_file_size(self, valid_html):
        """Valid HTML fixture should be within molecule limits."""
        result = validate_file_size(valid_html, "molecule")
        assert result.valid

    def test_invalid_html_file_size_as_atom(self, invalid_html):
        """Invalid HTML fixture may exceed atom limits."""
        result = validate_file_size(invalid_html, "atom")
        # This fixture is larger than atom size
        assert result.metadata["file_size_bytes"] > 0

    @pytest.mark.parametrize("level,max_kb", [
        ("atom", 5),
        ("molecule", 15),
        ("organism", 50),
        ("template", 100),
        ("page", 150),
    ])
    def test_size_limits_by_level(self, level, max_kb):
        """Each atomic level should have correct size limit."""
        content = "x" * 100  # small content
        result = validate_file_size(content, level)
        assert result.metadata["size_limit_kb"] == max_kb

    def test_warns_near_limit(self):
        """Should warn when file is 80-100% of limit."""
        # molecule limit is 15KB, 80% = 12KB
        content = "x" * 13000  # ~12.7KB
        result = validate_file_size(content, "molecule")
        assert result.valid  # still valid
        assert any("approaching" in warn.lower() for warn in result.warnings)


# =============================================================================
# Paint Time Estimation Tests
# =============================================================================

class TestPaintTimeEstimation:
    """Tests for paint time heuristic estimation."""

    def test_small_html_is_fast(self):
        """Small HTML with no externals should estimate fast FCP."""
        content = """
        <html>
        <body>
          <div class="p-4">
            <h1>Hello</h1>
            <p>Small content</p>
          </div>
        </body>
        </html>
        """
        result = estimate_paint_time(content)
        assert result.valid
        assert result.metadata["fcp_grade"] == "good"

    def test_valid_fixture_performance(self, valid_html):
        """Valid HTML fixture should have good paint time estimate."""
        result = estimate_paint_time(valid_html)
        assert result.metadata["estimated_fcp_ms"] > 0
        assert result.metadata["fcp_grade"] in ["good", "needs_work"]

    def test_counts_external_resources(self):
        """Should count external scripts, stylesheets, and images."""
        content = """
        <html>
        <head>
          <script src="https://cdn.tailwindcss.com"></script>
          <link href="https://fonts.googleapis.com/css" rel="stylesheet">
        </head>
        <body>
          <img src="photo.jpg">
          <img src="logo.png">
        </body>
        </html>
        """
        result = estimate_paint_time(content)
        assert result.metadata["external_resource_count"] == 4
        assert result.metadata["external_resource_ms"] > 0

    def test_counts_inline_styles(self):
        """Should count inline style attributes."""
        content = """
        <div style="color: red;">
          <p style="padding: 10px;">Text</p>
          <span style="font-size: 12px;">More</span>
        </div>
        """
        result = estimate_paint_time(content)
        assert result.metadata["inline_style_count"] == 3
        assert result.metadata["inline_style_ms"] > 0

    def test_penalizes_deep_dom(self):
        """Should add penalty for deep DOM nesting."""
        # Build deeply nested HTML
        content = "<html><body>"
        for i in range(20):
            content += f"<div class='level-{i}'>"
        content += "Deep content"
        for _ in range(20):
            content += "</div>"
        content += "</body></html>"

        result = estimate_paint_time(content)
        assert result.metadata["dom_depth"] > 10
        assert result.metadata["dom_depth_penalty_ms"] > 0

    def test_bloated_html_fails(self):
        """Very large HTML with many resources should fail."""
        # Build large content with many external resources
        content = "<html><head>"
        for i in range(50):
            content += f'<script src="script{i}.js"></script>\n'
        content += "</head><body>"
        content += "<div>" * 50
        content += "x" * 100000  # 100KB of content
        content += "</div>" * 50
        content += "</body></html>"

        result = estimate_paint_time(content)
        assert result.metadata["fcp_grade"] == "poor"
        assert not result.valid

    def test_metadata_completeness(self, valid_html):
        """Should include all expected metadata fields."""
        result = estimate_paint_time(valid_html)
        expected_keys = [
            "estimated_fcp_ms", "base_render_ms", "external_resource_count",
            "external_resource_ms", "inline_style_count", "inline_style_ms",
            "dom_depth", "dom_depth_penalty_ms", "fcp_grade"
        ]
        for key in expected_keys:
            assert key in result.metadata, f"Missing metadata key: {key}"


# =============================================================================
# Design System / Theme Validation Tests
# =============================================================================

class TestDesignSystemValidation:
    """Tests for design system and theme compliance validation."""

    def test_detects_shadcn_tokens(self):
        """Should detect shadcn/ui CSS variable usage."""
        content = """
        <style>
          :root {
            --background: 0 0% 100%;
            --foreground: 240 10% 3.9%;
            --primary: 240 5.9% 10%;
            --secondary: 240 4.8% 95.9%;
            --muted: 240 4.8% 95.9%;
            --accent: 240 4.8% 95.9%;
            --destructive: 0 84.2% 60.2%;
            --border: 240 5.9% 90%;
            --ring: 240 5.9% 10%;
          }
        </style>
        <div class="bg-background text-foreground">Content</div>
        """
        result = validate_design_system(content)
        assert result.metadata["shadcn_token_coverage"] >= 0.7
        assert result.metadata.get("detected_theme") == "default (shadcn/ui)"

    def test_detects_marine_sunset_theme(self):
        """Should detect marine-sunset theme markers."""
        content = """
        <!--
        Theme: Marine Sunset
        Using coral and teal color scheme
        -->
        <div class="marine-bg coral-accent teal-highlight">
          Content
        </div>
        """
        result = validate_design_system(content)
        assert "marine-sunset" in result.metadata.get("theme_markers_found", {})

    def test_detects_night_sky_theme(self):
        """Should detect night-sky theme markers."""
        content = """
        <!--
        Theme: Night Sky
        Cosmic violet color scheme
        -->
        <div class="cosmic-bg violet-accent midnight-text">
          Content
        </div>
        """
        result = validate_design_system(content)
        assert "night-sky" in result.metadata.get("theme_markers_found", {})

    def test_fails_on_no_design_system(self):
        """Should fail when no design system is detected."""
        content = """
        <html>
        <body>
          <div style="background: #f0f0f0; color: #333;">
            No design tokens or theme
          </div>
        </body>
        </html>
        """
        result = validate_design_system(content)
        assert not result.valid
        assert any("design system" in err.lower() for err in result.errors)

    def test_fails_on_partial_shadcn(self):
        """Should fail when only partial shadcn tokens are used."""
        content = """
        <style>
          :root {
            --background: 0 0% 100%;
            --foreground: 240 10% 3.9%;
          }
        </style>
        <div class="bg-background">Partial tokens</div>
        """
        result = validate_design_system(content)
        assert result.metadata["shadcn_token_coverage"] < 0.5
        assert any("incomplete" in err.lower() for err in result.errors)

    def test_detects_tailwind_cdn(self):
        """Should detect Tailwind CDN usage."""
        content = """
        <html>
        <head>
          <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-background">Content</body>
        </html>
        """
        result = validate_design_system(content)
        assert result.metadata["has_tailwind_cdn"] is True

    def test_warns_html_without_tailwind(self):
        """Should warn when HTML lacks Tailwind or style block."""
        content = """
        <html>
        <head><title>Test</title></head>
        <body>No Tailwind CDN</body>
        </html>
        """
        result = validate_design_system(content)
        assert len(result.warnings) > 0

    def test_detects_shadcn_imports_react(self):
        """Should detect shadcn/ui imports in React components."""
        content = """
        import React from 'react';
        import { Button } from '@/components/ui/button';
        import { Card } from '@/components/ui/card';

        export function MyComponent() {
          return <Button>Click</Button>;
        }
        """
        result = validate_design_system(content)
        assert result.metadata["has_shadcn_imports"] is True

    def test_warns_react_without_shadcn(self):
        """Should warn when React component doesn't use shadcn."""
        content = """
        import React from 'react';

        export function MyComponent() {
          return <button style={{background: 'blue'}}>Click</button>;
        }
        """
        result = validate_design_system(content)
        assert len(result.warnings) > 0
        assert result.metadata["has_shadcn_imports"] is False

    def test_detects_raw_background_colors(self):
        """Should error on raw hex background colors."""
        content = """
        <style>
          .bad { background-color: #1a1a2e; }
        </style>
        """
        result = validate_design_system(content)
        assert any("hex background" in err.lower() for err in result.errors)

    def test_warns_on_multiple_themes(self):
        """Should warn when multiple themes are detected."""
        content = """
        <!--
        Using both themes somehow
        -->
        <div class="coral-bg teal-accent">Marine sunset</div>
        <div class="cosmic-bg violet-accent">Night sky</div>
        """
        result = validate_design_system(content)
        assert len(result.warnings) > 0

    def test_counts_hsl_var_usage(self):
        """Should count hsl(var(--token)) pattern usage."""
        content = """
        <style>
          .a { background: hsl(var(--background)); }
          .b { color: hsl(var(--foreground)); }
          .c { border-color: hsl(var(--border)); }
        </style>
        """
        result = validate_design_system(content)
        assert result.metadata["hsl_var_usage_count"] == 3

    def test_valid_html_design_system(self, valid_html):
        """Valid HTML fixture should pass design system validation."""
        result = validate_design_system(valid_html)
        # Valid fixture should use design tokens
        assert result.metadata.get("shadcn_token_coverage", 0) > 0 or len(result.metadata.get("theme_markers_found", {})) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
