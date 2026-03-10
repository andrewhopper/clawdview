#!/usr/bin/env python3
# File UUID: 6fdddfb3-4fd4-4d19-af1e-e64f4e8ca33c
"""
Validation functions for design agent outputs.

Tests that generated assets comply with:
- Design token usage (no raw hex colors)
- Metadata requirements (UUID, date, atomic level)
- Typography and spacing token scales
- Visual hierarchy constraints
- Miller's Law (max 7 choices per group)
- File size limits
- Paint time estimation

Usage:
    python validate_design_output.py <file_path>

    # Or import as module
    from validate_design_output import validate_html_asset, validate_ia_output
"""
# File UUID: 8a3f2c1d-4e5b-6c7d-9e0f-1a2b3c4d5e6f

import re
import sys
import json
import yaml
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class ValidationResult:
    """Result of validating an agent output."""
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def add_error(self, message: str) -> None:
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    def to_dict(self) -> dict:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "metadata": self.metadata,
        }


# =============================================================================
# Design Token Patterns
# =============================================================================

# Raw hex colors that should be replaced with design tokens
RAW_HEX_PATTERN = re.compile(r'#[0-9a-fA-F]{3,8}(?![0-9a-fA-F])')

# Valid design token patterns
VALID_COLOR_PATTERNS = [
    r'hsl\(var\(--[\w-]+\)\)',           # hsl(var(--primary))
    r'var\(--[\w-]+\)',                   # var(--background)
    r'bg-[\w-]+',                         # Tailwind: bg-background
    r'text-[\w-]+',                       # Tailwind: text-foreground
    r'border-[\w-]+',                     # Tailwind: border-border
]

# Magic number patterns (spacing that doesn't use token scale)
MAGIC_SPACING_PATTERN = re.compile(r'(?:padding|margin|gap|space):\s*(\d+)px')
VALID_SPACING_VALUES = {4, 8, 12, 16, 24, 32, 48, 64, 96, 128}  # 4px base unit

# Typography patterns
MAGIC_FONT_SIZE_PATTERN = re.compile(r'font-size:\s*(\d+)px')
VALID_FONT_SIZES = {12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72}  # Tailwind scale

# Valid Tailwind text size classes
TAILWIND_TEXT_SIZES = {
    'text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl',
    'text-2xl', 'text-3xl', 'text-4xl', 'text-5xl', 'text-6xl', 'text-7xl'
}

# Font color patterns (detect raw colors in font/text contexts)
FONT_COLOR_PATTERN = re.compile(r'(?:color|fill):\s*#([0-9a-fA-F]{3,8})')

# WCAG Contrast Requirements
# Normal text (< 18pt or < 14pt bold): 4.5:1
# Large text (>= 18pt or >= 14pt bold): 3:1
CONTRAST_RATIO_NORMAL = 4.5
CONTRAST_RATIO_LARGE = 3.0

# Common color pairs to check (foreground, background) in HSL
# These are the design system defaults - actual values may vary
DEFAULT_COLOR_PAIRS = [
    ("foreground", "background"),      # Main text
    ("muted-foreground", "background"), # Secondary text
    ("primary-foreground", "primary"),  # Button text
    ("destructive-foreground", "destructive"),  # Error text
]

# =============================================================================
# Design System & Theme Detection
# =============================================================================

# Available themes in the design system
AVAILABLE_THEMES = {
    'default': {
        'name': 'Default (shadcn/ui)',
        'markers': ['--background', '--foreground', '--primary'],
        'description': 'Standard shadcn/ui theme with Tailwind defaults'
    },
    'marine-sunset': {
        'name': 'Marine Sunset',
        'markers': ['coral', 'teal', 'marine', 'sunset'],
        'description': 'Warm coral/orange with deep teal'
    },
    'night-sky': {
        'name': 'Night Sky',
        'markers': ['cosmic', 'violet', 'space', 'midnight', 'dawn'],
        'description': 'Cosmic blues with violet accents'
    },
}

# Required CSS variables for shadcn/ui compliance
REQUIRED_SHADCN_TOKENS = [
    '--background',
    '--foreground',
    '--primary',
    '--secondary',
    '--muted',
    '--accent',
    '--destructive',
    '--border',
    '--ring',
]

# Tailwind CDN pattern
TAILWIND_CDN_PATTERN = re.compile(r'cdn\.tailwindcss\.com|tailwindcss.*cdn', re.IGNORECASE)

# shadcn/ui import patterns (for React components)
SHADCN_IMPORT_PATTERN = re.compile(r'from\s+["\']@/components/ui/', re.IGNORECASE)

# Asset metadata pattern
METADATA_PATTERN = re.compile(
    r'<!--\s*'
    r'Asset:\s*(?P<name>[^\n]+)\s*'
    r'(?:Project:\s*(?P<project>[^\n]+)\s*)?'
    r'Asset ID:\s*(?P<id>[^\n]+)\s*'
    r'Date:\s*(?P<date>[^\n]+)\s*'
    r'(?:Design System:\s*(?P<design_system>[^\n]+)\s*)?'
    r'(?:Atomic Level:\s*(?P<atomic_level>[^\n]+)\s*)?',
    re.MULTILINE | re.DOTALL
)

# Atomic levels
VALID_ATOMIC_LEVELS = {'atom', 'molecule', 'organism', 'template', 'page'}

# Miller's Law: max items per navigation/choice group
MILLERS_LAW_MAX_ITEMS = 7

# File size limits (bytes)
FILE_SIZE_LIMITS = {
    'atom': 5_000,          # 5 KB - single element
    'molecule': 15_000,     # 15 KB - small component group
    'organism': 50_000,     # 50 KB - complex section
    'template': 100_000,    # 100 KB - full page layout
    'page': 150_000,        # 150 KB - complete page
    'default': 100_000,     # 100 KB - fallback
}

# Paint time thresholds (milliseconds)
# Based on Core Web Vitals: FCP < 1.8s, LCP < 2.5s
PAINT_TIME_THRESHOLDS = {
    'fcp_good': 1800,       # First Contentful Paint: good
    'fcp_needs_work': 3000, # FCP: needs improvement
    'lcp_good': 2500,       # Largest Contentful Paint: good
    'lcp_needs_work': 4000, # LCP: needs improvement
    'cls_good': 0.1,        # Cumulative Layout Shift: good
}

# Paint time heuristic weights (bytes per ms of render time)
# Rough estimate: each KB of HTML/CSS adds ~2ms of parse/render
BYTES_PER_MS_RENDER = 500
# External resources add latency
EXTERNAL_RESOURCE_PENALTY_MS = 50  # per <script src>, <link href>, <img src>
# Inline styles are slower than classes
INLINE_STYLE_PENALTY_MS = 5  # per inline style attribute
# Deep DOM nesting adds reflow cost
DOM_DEPTH_PENALTY_MS = 10  # per level beyond 10


# =============================================================================
# HTML/Visual Asset Validation
# =============================================================================

def validate_html_asset(content: str) -> ValidationResult:
    """
    Validate an HTML asset generated by the UX agent.

    Checks:
    - Has required metadata header
    - Uses design tokens (not raw hex)
    - Uses spacing token scale
    - Follows typography scale
    - Has valid atomic level
    """
    result = ValidationResult(valid=True)

    # Check for metadata header
    metadata_match = METADATA_PATTERN.search(content)
    if not metadata_match:
        result.add_error("Missing asset metadata header (Asset, Asset ID, Date required)")
    else:
        result.metadata = {
            "name": metadata_match.group("name").strip() if metadata_match.group("name") else None,
            "id": metadata_match.group("id").strip() if metadata_match.group("id") else None,
            "date": metadata_match.group("date").strip() if metadata_match.group("date") else None,
            "atomic_level": metadata_match.group("atomic_level").strip() if metadata_match.group("atomic_level") else None,
        }

        # Validate atomic level
        if result.metadata["atomic_level"]:
            level = result.metadata["atomic_level"].lower()
            if level not in VALID_ATOMIC_LEVELS:
                result.add_error(f"Invalid atomic level '{level}'. Must be one of: {VALID_ATOMIC_LEVELS}")

    # Check for raw hex colors
    hex_matches = RAW_HEX_PATTERN.findall(content)
    if hex_matches:
        # Filter out false positives in comments explaining what NOT to do
        actual_violations = [h for h in hex_matches if not _is_in_comment_example(content, h)]
        if actual_violations:
            result.add_error(f"Found raw hex colors (use design tokens): {actual_violations[:5]}")

    # Check for magic spacing numbers
    spacing_matches = MAGIC_SPACING_PATTERN.findall(content)
    invalid_spacing = [int(s) for s in spacing_matches if int(s) not in VALID_SPACING_VALUES]
    if invalid_spacing:
        result.add_warning(f"Non-standard spacing values (use token scale): {invalid_spacing[:5]}px")

    # Check for magic font sizes
    font_size_matches = MAGIC_FONT_SIZE_PATTERN.findall(content)
    invalid_font_sizes = [int(s) for s in font_size_matches if int(s) not in VALID_FONT_SIZES]
    if invalid_font_sizes:
        result.add_warning(f"Non-standard font sizes (use text-* classes): {invalid_font_sizes[:5]}px")

    # Check for raw hex colors in font/text color properties
    font_color_matches = FONT_COLOR_PATTERN.findall(content)
    if font_color_matches:
        # Filter out comment examples
        actual_violations = [f"#{c}" for c in font_color_matches if not _is_in_comment_example(content, f"#{c}")]
        if actual_violations:
            result.add_error(f"Found raw hex font colors (use text-* tokens): {actual_violations[:5]}")

    # Check for inline styles
    if 'style="' in content or "style='" in content:
        # Allow style in <style> blocks, flag inline element styles
        inline_style_count = content.count('style="') + content.count("style='")
        style_block_count = content.count('<style')
        if inline_style_count > style_block_count:
            result.add_warning("Found inline styles. Prefer Tailwind classes or CSS variables")

    # Check for raw HTML elements that should use components
    raw_elements = []
    if re.search(r'<button\s', content, re.IGNORECASE):
        raw_elements.append('<button>')
    if re.search(r'<input\s', content, re.IGNORECASE):
        raw_elements.append('<input>')
    if re.search(r'<select\s', content, re.IGNORECASE):
        raw_elements.append('<select>')

    # Only warn for React contexts (not plain HTML mockups)
    if raw_elements and ('.tsx' in content or '.jsx' in content or 'import React' in content):
        result.add_warning(f"Consider using shadcn/ui components instead of: {raw_elements}")

    return result


def _is_in_comment_example(content: str, hex_value: str) -> bool:
    """Check if a hex value appears in a comment showing what NOT to do."""
    # Find the hex value and check surrounding context
    idx = content.find(hex_value)
    if idx == -1:
        return False

    # Check if it's in a "NEVER" example or comment
    context_start = max(0, idx - 100)
    context = content[context_start:idx + len(hex_value)]
    return 'NEVER' in context or '❌' in context or 'bad' in context.lower()


# =============================================================================
# Typography Validation
# =============================================================================

def validate_typography(content: str) -> ValidationResult:
    """
    Validate typography usage in generated HTML.

    Checks:
    - Font sizes use Tailwind text-* scale (not raw px)
    - Font colors use design tokens (not raw hex)
    - Font weights use Tailwind classes
    - Line heights are appropriate
    """
    result = ValidationResult(valid=True)

    # Check for magic font size pixels
    font_size_matches = MAGIC_FONT_SIZE_PATTERN.findall(content)
    invalid_sizes = [int(s) for s in font_size_matches if int(s) not in VALID_FONT_SIZES]
    result.metadata["font_size_violations"] = invalid_sizes
    if invalid_sizes:
        result.add_error(
            f"Font sizes must use Tailwind scale. Found: {invalid_sizes}px. "
            "Use text-xs (12px), text-sm (14px), text-base (16px), etc."
        )

    # Check for raw hex font colors
    font_colors = FONT_COLOR_PATTERN.findall(content)
    raw_font_colors = [f"#{c}" for c in font_colors if not _is_in_comment_example(content, f"#{c}")]
    result.metadata["font_color_violations"] = raw_font_colors
    if raw_font_colors:
        result.add_error(
            f"Font colors must use design tokens. Found raw: {raw_font_colors[:5]}. "
            "Use text-foreground, text-muted-foreground, text-primary, etc."
        )

    # Check for Tailwind text classes (positive check)
    text_classes_found = set()
    for tc in TAILWIND_TEXT_SIZES:
        if tc in content:
            text_classes_found.add(tc)
    result.metadata["tailwind_text_classes_found"] = list(text_classes_found)

    # Check font-family declarations (should use CSS variables or system fonts)
    font_family_pattern = re.compile(r'font-family:\s*([^;]+);')
    font_families = font_family_pattern.findall(content)
    suspicious_fonts = [f for f in font_families if 'var(' not in f and 'system-ui' not in f.lower() and 'sans-serif' not in f.lower()]
    if suspicious_fonts:
        result.add_warning(f"Consider using CSS variable for fonts: {suspicious_fonts[:3]}")

    return result


# =============================================================================
# Contrast Validation
# =============================================================================

def validate_contrast(content: str) -> ValidationResult:
    """
    Validate color contrast for accessibility (WCAG).

    Static analysis to detect potential contrast issues.
    For actual measurement, use Playwright accessibility tests.

    Checks:
    - Foreground/background color pairs
    - Text on colored backgrounds
    - Button/link text contrast
    """
    result = ValidationResult(valid=True)

    # Extract color definitions from CSS variables or inline styles
    css_var_pattern = re.compile(r'--(\w[\w-]*):\s*(\d+)\s+(\d+)%?\s+(\d+)%?')
    color_vars = {}

    for match in css_var_pattern.finditer(content):
        name = match.group(1)
        h, s, l = int(match.group(2)), int(match.group(3)), int(match.group(4))
        color_vars[name] = (h, s, l)

    result.metadata["color_variables_found"] = list(color_vars.keys())

    # Check known contrast pairs
    contrast_issues = []
    for fg_name, bg_name in DEFAULT_COLOR_PAIRS:
        if fg_name in color_vars and bg_name in color_vars:
            fg_hsl = color_vars[fg_name]
            bg_hsl = color_vars[bg_name]

            # Convert HSL to relative luminance and calculate contrast
            fg_lum = _hsl_to_luminance(fg_hsl)
            bg_lum = _hsl_to_luminance(bg_hsl)

            contrast_ratio = _calculate_contrast_ratio(fg_lum, bg_lum)
            result.metadata[f"contrast_{fg_name}_on_{bg_name}"] = round(contrast_ratio, 2)

            if contrast_ratio < CONTRAST_RATIO_NORMAL:
                contrast_issues.append(
                    f"{fg_name} on {bg_name}: {contrast_ratio:.2f}:1 "
                    f"(needs {CONTRAST_RATIO_NORMAL}:1 for normal text)"
                )

    if contrast_issues:
        result.add_error(f"Contrast issues detected: {'; '.join(contrast_issues[:3])}")

    # Check for low-contrast patterns in Tailwind classes
    low_contrast_patterns = [
        (r'text-gray-\d00\s+bg-gray-\d00', "gray text on gray background"),
        (r'text-white\s+bg-white', "white text on white"),
        (r'text-black\s+bg-black', "black text on black"),
    ]

    for pattern, description in low_contrast_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            result.add_warning(f"Potential low contrast: {description}")

    return result


def _hsl_to_luminance(hsl: tuple[int, int, int]) -> float:
    """Convert HSL to relative luminance for contrast calculation."""
    h, s, l = hsl
    # Simplified: use lightness as proxy for luminance
    # For accurate contrast, would need full RGB conversion
    return l / 100.0


def _calculate_contrast_ratio(lum1: float, lum2: float) -> float:
    """Calculate WCAG contrast ratio between two luminance values."""
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)

    # WCAG formula: (L1 + 0.05) / (L2 + 0.05)
    return (lighter + 0.05) / (darker + 0.05)


# =============================================================================
# Responsive Design Validation
# =============================================================================

# Standard viewport breakpoints
VIEWPORTS = {
    'phone': {'width': 375, 'height': 667, 'name': 'iPhone SE'},
    'tablet_vertical': {'width': 768, 'height': 1024, 'name': 'iPad Portrait'},
    'tablet_horizontal': {'width': 1024, 'height': 768, 'name': 'iPad Landscape'},
    'desktop': {'width': 1440, 'height': 900, 'name': 'Desktop'},
}

def validate_responsive_classes(content: str) -> ValidationResult:
    """
    Validate that HTML uses responsive Tailwind classes.

    Checks for:
    - Mobile-first responsive prefixes (sm:, md:, lg:, xl:)
    - Flexible layouts (flex, grid)
    - Responsive images
    - Touch-friendly sizing
    """
    result = ValidationResult(valid=True)

    # Check for responsive prefixes
    responsive_prefixes = ['sm:', 'md:', 'lg:', 'xl:', '2xl:']
    found_prefixes = set()
    for prefix in responsive_prefixes:
        if prefix in content:
            found_prefixes.add(prefix.rstrip(':'))

    result.metadata["responsive_prefixes_found"] = list(found_prefixes)

    if not found_prefixes:
        result.add_warning(
            "No responsive prefixes found (sm:, md:, lg:, xl:). "
            "Consider adding responsive styles for different viewports"
        )

    # Check for flexible layouts
    has_flex = 'flex' in content
    has_grid = 'grid' in content
    result.metadata["has_flex_layout"] = has_flex
    result.metadata["has_grid_layout"] = has_grid

    if not has_flex and not has_grid:
        result.add_warning("No flex or grid layouts found. Consider using flexible layouts for responsiveness")

    # Check for responsive images
    has_responsive_images = (
        'max-w-full' in content or
        'w-full' in content or
        'object-fit' in content or
        'object-cover' in content
    )
    result.metadata["has_responsive_images"] = has_responsive_images

    # Check for touch-friendly sizing (min 44px tap targets)
    small_touch_targets = re.findall(r'(?:w-|h-)([1-9]|10)\s', content)
    if small_touch_targets:
        result.add_warning(
            f"Found potentially small touch targets: {small_touch_targets[:5]}. "
            "Interactive elements should be at least w-11 (44px) for touch"
        )

    # Check for viewport meta tag (critical for mobile)
    if '<meta name="viewport"' not in content.lower() and '<html' in content.lower():
        result.add_error("Missing viewport meta tag. Add: <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">")

    # Check for hidden/visible responsive classes
    visibility_classes = ['hidden', 'block', 'inline', 'flex', 'grid', 'invisible', 'visible']
    responsive_visibility = []
    for prefix in responsive_prefixes:
        for vis in visibility_classes:
            pattern = f"{prefix}{vis}"
            if pattern in content:
                responsive_visibility.append(pattern)

    result.metadata["responsive_visibility_classes"] = responsive_visibility

    return result


# =============================================================================
# Design System / Theme Validation
# =============================================================================

def validate_design_system(content: str) -> ValidationResult:
    """
    Validate that a generated asset uses either:
    1. Plain shadcn/ui with Tailwind defaults (valid)
    2. An explicit theme from the design system (valid)
    3. Neither (invalid - must use one or the other)

    Checks:
    - CSS variables for shadcn/ui tokens
    - Theme markers for named themes
    - Tailwind CDN or build configuration
    - Import patterns for React components
    """
    result = ValidationResult(valid=True)

    is_html = '<html' in content.lower() or '<!doctype html' in content.lower()
    is_react = 'import React' in content or '.tsx' in content or '.jsx' in content

    result.metadata["is_html_asset"] = is_html
    result.metadata["is_react_component"] = is_react

    # Detect which theme/system is being used
    detected_theme = None
    theme_confidence = 0

    # Check for shadcn/ui token usage (CSS variables)
    shadcn_tokens_found = []
    for token in REQUIRED_SHADCN_TOKENS:
        if token in content:
            shadcn_tokens_found.append(token)

    result.metadata["shadcn_tokens_found"] = shadcn_tokens_found
    shadcn_coverage = len(shadcn_tokens_found) / len(REQUIRED_SHADCN_TOKENS)
    result.metadata["shadcn_token_coverage"] = round(shadcn_coverage, 2)

    # Check for theme markers
    theme_matches = {}
    for theme_name, theme_info in AVAILABLE_THEMES.items():
        markers_found = [m for m in theme_info['markers'] if m.lower() in content.lower()]
        if markers_found:
            theme_matches[theme_name] = markers_found

    result.metadata["theme_markers_found"] = theme_matches

    # Determine which system is being used
    if shadcn_coverage >= 0.7:
        detected_theme = 'default'
        theme_confidence = shadcn_coverage
        result.metadata["detected_theme"] = 'default (shadcn/ui)'
        result.metadata["theme_confidence"] = round(theme_confidence, 2)

    for theme_name, markers in theme_matches.items():
        if theme_name != 'default' and len(markers) >= 2:
            detected_theme = theme_name
            theme_confidence = min(1.0, len(markers) / 3)
            result.metadata["detected_theme"] = theme_name
            result.metadata["theme_confidence"] = round(theme_confidence, 2)
            break

    # Check for Tailwind CDN (for HTML mockups)
    has_tailwind_cdn = bool(TAILWIND_CDN_PATTERN.search(content))
    result.metadata["has_tailwind_cdn"] = has_tailwind_cdn

    # Check for shadcn imports (for React components)
    has_shadcn_imports = bool(SHADCN_IMPORT_PATTERN.search(content))
    result.metadata["has_shadcn_imports"] = has_shadcn_imports

    # Validation logic
    if is_html and not has_tailwind_cdn:
        # HTML without Tailwind CDN - check for inline styles
        has_style_block = '<style' in content
        if not has_style_block:
            result.add_warning(
                "HTML mockup doesn't include Tailwind CDN or <style> block. "
                "Add: <script src=\"https://cdn.tailwindcss.com\"></script>"
            )

    if is_react and not has_shadcn_imports and shadcn_coverage < 0.3:
        result.add_warning(
            "React component doesn't import from shadcn/ui. "
            "Consider using components from @/components/ui/"
        )

    # Check for consistent theming
    if not detected_theme:
        # No clear design system detected
        if shadcn_coverage > 0 and shadcn_coverage < 0.5:
            result.add_error(
                f"Incomplete design system usage. Found only {len(shadcn_tokens_found)}/{len(REQUIRED_SHADCN_TOKENS)} "
                f"shadcn tokens. Either use full shadcn/ui or apply a complete theme"
            )
        elif shadcn_coverage == 0 and not theme_matches:
            result.add_error(
                "No design system detected. Must use either shadcn/ui (with Tailwind) "
                "or an explicit theme from the design system (marine-sunset, night-sky)"
            )

    # Check for conflicting themes
    named_themes = [k for k in theme_matches.keys() if k != 'default']
    if len(named_themes) > 1:
        result.add_warning(
            f"Multiple themes detected: {named_themes}. "
            "Use only one theme for consistency"
        )

    # Check for mixing custom and standard themes
    if detected_theme == 'default' and named_themes:
        result.add_warning(
            f"Mixing default shadcn/ui with named theme markers ({named_themes}). "
            "Choose one theming approach"
        )

    # Verify CSS variable usage format
    hsl_var_pattern = re.compile(r'hsl\(var\(--[\w-]+\)\)')
    hsl_var_count = len(hsl_var_pattern.findall(content))
    result.metadata["hsl_var_usage_count"] = hsl_var_count

    # Check for raw color values that should use tokens
    raw_bg_colors = re.findall(r'background(?:-color)?:\s*#[0-9a-fA-F]{3,8}', content)
    if raw_bg_colors:
        result.add_error(
            f"Found raw hex background colors. Use hsl(var(--background)) or bg-background: "
            f"{raw_bg_colors[:3]}"
        )

    return result


# =============================================================================
# Information Architecture Output Validation
# =============================================================================

def validate_ia_output(content: str) -> ValidationResult:
    """
    Validate an IA specification generated by the IA agent.

    Checks:
    - Has navigation hierarchy (max 3 levels)
    - Has user flow or sitemap
    - Labels are present and non-empty
    - Handoff section exists for UX agent
    """
    result = ValidationResult(valid=True)

    # Check for navigation hierarchy
    if not any(marker in content for marker in ['├──', '└──', '│', 'Navigation', 'navigation']):
        result.add_warning("No navigation hierarchy structure detected")

    # Check hierarchy depth
    depth = _calculate_hierarchy_depth(content)
    result.metadata["hierarchy_depth"] = depth
    if depth > 3:
        result.add_error(f"Navigation hierarchy too deep ({depth} levels). Maximum is 3 levels")

    # Check for user flows
    has_flow = any(marker in content for marker in ['───▶', '→', 'Step', 'Flow', 'flow'])
    result.metadata["has_user_flow"] = has_flow
    if not has_flow:
        result.add_warning("No user flow diagram detected")

    # Check for handoff section
    has_handoff = 'HANDOFF' in content.upper() or 'handoff' in content.lower()
    result.metadata["has_handoff"] = has_handoff
    if not has_handoff:
        result.add_warning("No handoff section for UX agent")

    # Check for empty labels
    tree_items = re.findall(r'[├└│]──\s*(\S.*?)(?:\n|$)', content)
    empty_labels = [item for item in tree_items if not item.strip() or item.strip() == '─']
    if empty_labels:
        result.add_error(f"Found {len(empty_labels)} items with missing labels")

    # Check Miller's Law: max 7 items per navigation group
    sibling_counts = _count_sibling_items(content)
    result.metadata["max_siblings"] = max(sibling_counts) if sibling_counts else 0
    violations = [count for count in sibling_counts if count > MILLERS_LAW_MAX_ITEMS]
    if violations:
        result.add_error(
            f"Miller's Law violation: found groups with {violations} items. "
            f"Maximum is {MILLERS_LAW_MAX_ITEMS} items per group"
        )

    return result


def _count_sibling_items(content: str) -> list[int]:
    """Count the number of sibling items at each level of a tree hierarchy.

    Returns a list of counts, one per group of siblings found.
    Used to enforce Miller's Law (max 7 items per group).
    """
    # Parse tree lines and group by indent level
    levels: dict[int, int] = {}  # indent_level -> count of items at that level in current group
    sibling_counts: list[int] = []
    prev_level = -1

    for line in content.split('\n'):
        # Detect tree items
        match = re.match(r'^(\s*[│ ]*)[├└]──\s*\S', line)
        if not match:
            continue

        # Calculate indent level
        prefix = match.group(1)
        level = len(prefix.replace('│', ' ').rstrip()) // 4

        if level < prev_level:
            # We've moved up - flush counts for deeper levels
            for deeper_level in list(levels.keys()):
                if deeper_level > level:
                    sibling_counts.append(levels.pop(deeper_level))

        if level == prev_level:
            levels[level] = levels.get(level, 0) + 1
        else:
            # New level or reset
            if level in levels:
                sibling_counts.append(levels[level])
            levels[level] = 1

        prev_level = level

    # Flush remaining
    for count in levels.values():
        sibling_counts.append(count)

    return sibling_counts


def _calculate_hierarchy_depth(content: str) -> int:
    """Calculate the depth of a tree hierarchy in the content."""
    max_depth = 0
    for line in content.split('\n'):
        # Count leading spaces/indent markers
        depth = 0
        for char in line:
            if char in ' │├└':
                depth += 1
            else:
                break
        # Normalize to levels (typically 4 chars per level)
        level = depth // 4 + 1 if '├' in line or '└' in line else 0
        max_depth = max(max_depth, level)
    return max_depth


# =============================================================================
# YAML/Structured Output Validation
# =============================================================================

def validate_navigation_yaml(content: str) -> ValidationResult:
    """
    Validate a YAML navigation structure.

    Expected format:
    navigation:
      primary:
        - name: Dashboard
          path: /dashboard
          children:
            - name: Overview
              path: /dashboard/overview
    """
    result = ValidationResult(valid=True)

    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        result.add_error(f"Invalid YAML: {e}")
        return result

    if not isinstance(data, dict):
        result.add_error("Expected YAML dict at root level")
        return result

    # Check for navigation key
    if 'navigation' not in data:
        result.add_warning("No 'navigation' key found at root")

    # Validate structure recursively
    def validate_nav_item(item: dict, depth: int, path: str) -> None:
        if depth > 3:
            result.add_error(f"Navigation too deep at {path} ({depth} levels)")
            return

        if not isinstance(item, dict):
            result.add_error(f"Invalid nav item at {path}: expected dict")
            return

        if 'name' not in item:
            result.add_error(f"Missing 'name' at {path}")

        if 'children' in item and isinstance(item['children'], list):
            child_count = len(item['children'])
            if child_count > MILLERS_LAW_MAX_ITEMS:
                result.add_error(
                    f"Miller's Law violation at {path}: {child_count} children "
                    f"(max {MILLERS_LAW_MAX_ITEMS})"
                )
            for i, child in enumerate(item['children']):
                validate_nav_item(child, depth + 1, f"{path}.children[{i}]")

    nav = data.get('navigation', data)
    if isinstance(nav, dict):
        for section_name, items in nav.items():
            if isinstance(items, list):
                # Check top-level item count per section
                if len(items) > MILLERS_LAW_MAX_ITEMS:
                    result.add_error(
                        f"Miller's Law violation: navigation.{section_name} has "
                        f"{len(items)} items (max {MILLERS_LAW_MAX_ITEMS})"
                    )
                for i, item in enumerate(items):
                    validate_nav_item(item, 1, f"navigation.{section_name}[{i}]")

    return result


# =============================================================================
# Gate Handoff Validation
# =============================================================================

def validate_gate_handoff(ia_output: str, ux_input: str) -> ValidationResult:
    """
    Validate that IA agent output properly hands off to UX agent.

    Checks:
    - IA output has handoff summary
    - UX input references IA components
    - Component mapping is consistent
    """
    result = ValidationResult(valid=True)

    # Extract handoff summary from IA
    handoff_match = re.search(
        r'IA HANDOFF SUMMARY:.*?(?=\n\n|\Z)',
        ia_output,
        re.DOTALL | re.IGNORECASE
    )

    if not handoff_match:
        result.add_error("IA output missing HANDOFF SUMMARY section")
        return result

    handoff_text = handoff_match.group()
    result.metadata["handoff_summary"] = handoff_text

    # Extract mentioned components
    components = re.findall(r'Components needed:\s*\[([^\]]+)\]', handoff_text)
    if components:
        mentioned_components = [c.strip() for c in components[0].split(',')]
        result.metadata["ia_components"] = mentioned_components

        # Check if UX output references these components
        missing_components = []
        for comp in mentioned_components:
            if comp.lower() not in ux_input.lower():
                missing_components.append(comp)

        if missing_components:
            result.add_warning(f"UX output doesn't reference IA components: {missing_components}")

    return result


# =============================================================================
# File Size Validation
# =============================================================================

def validate_file_size(content: str, atomic_level: Optional[str] = None) -> ValidationResult:
    """
    Validate that a generated asset stays within size limits.

    Limits vary by atomic level:
    - atom: 5 KB (single element)
    - molecule: 15 KB (small component group)
    - organism: 50 KB (complex section)
    - template: 100 KB (full page layout)
    - page: 150 KB (complete page)
    """
    result = ValidationResult(valid=True)

    size_bytes = len(content.encode('utf-8'))
    result.metadata["file_size_bytes"] = size_bytes
    result.metadata["file_size_kb"] = round(size_bytes / 1024, 1)

    # Determine limit
    level = (atomic_level or 'default').lower()
    limit = FILE_SIZE_LIMITS.get(level, FILE_SIZE_LIMITS['default'])
    result.metadata["size_limit_bytes"] = limit
    result.metadata["size_limit_kb"] = round(limit / 1024, 1)

    if size_bytes > limit:
        result.add_error(
            f"File size {result.metadata['file_size_kb']} KB exceeds "
            f"{result.metadata['size_limit_kb']} KB limit for '{level}' level"
        )

    # Warn at 80% of limit
    if size_bytes > limit * 0.8 and size_bytes <= limit:
        result.add_warning(
            f"File size {result.metadata['file_size_kb']} KB is approaching "
            f"{result.metadata['size_limit_kb']} KB limit"
        )

    return result


# =============================================================================
# Paint Time Estimation
# =============================================================================

def estimate_paint_time(content: str) -> ValidationResult:
    """
    Estimate browser paint time for an HTML asset using heuristics.

    This is a static analysis estimate, not a real browser measurement.
    For actual paint time, use the Playwright performance test.

    Heuristics:
    - Base cost: content size / BYTES_PER_MS_RENDER
    - External resources: EXTERNAL_RESOURCE_PENALTY_MS per resource
    - Inline styles: INLINE_STYLE_PENALTY_MS per style attribute
    - DOM depth: DOM_DEPTH_PENALTY_MS per level beyond 10
    """
    result = ValidationResult(valid=True)

    # Base render cost from content size
    size_bytes = len(content.encode('utf-8'))
    base_ms = size_bytes / BYTES_PER_MS_RENDER

    # Count external resources
    external_scripts = len(re.findall(r'<script\s+[^>]*src=', content, re.IGNORECASE))
    external_styles = len(re.findall(r'<link\s+[^>]*href=', content, re.IGNORECASE))
    external_images = len(re.findall(r'<img\s+[^>]*src=', content, re.IGNORECASE))
    total_external = external_scripts + external_styles + external_images
    external_ms = total_external * EXTERNAL_RESOURCE_PENALTY_MS

    # Count inline styles
    inline_count = content.count('style="') + content.count("style='")
    inline_ms = inline_count * INLINE_STYLE_PENALTY_MS

    # Estimate DOM depth
    dom_depth = _estimate_dom_depth(content)
    depth_penalty = max(0, dom_depth - 10) * DOM_DEPTH_PENALTY_MS

    # Total estimated FCP
    estimated_fcp = base_ms + external_ms + inline_ms + depth_penalty

    result.metadata["estimated_fcp_ms"] = round(estimated_fcp)
    result.metadata["base_render_ms"] = round(base_ms)
    result.metadata["external_resource_count"] = total_external
    result.metadata["external_resource_ms"] = round(external_ms)
    result.metadata["inline_style_count"] = inline_count
    result.metadata["inline_style_ms"] = round(inline_ms)
    result.metadata["dom_depth"] = dom_depth
    result.metadata["dom_depth_penalty_ms"] = round(depth_penalty)

    # Evaluate against thresholds
    if estimated_fcp > PAINT_TIME_THRESHOLDS['fcp_needs_work']:
        result.add_error(
            f"Estimated FCP {round(estimated_fcp)}ms exceeds 'needs work' threshold "
            f"({PAINT_TIME_THRESHOLDS['fcp_needs_work']}ms). Reduce file size, "
            f"external resources ({total_external}), or inline styles ({inline_count})"
        )
    elif estimated_fcp > PAINT_TIME_THRESHOLDS['fcp_good']:
        result.add_warning(
            f"Estimated FCP {round(estimated_fcp)}ms exceeds 'good' threshold "
            f"({PAINT_TIME_THRESHOLDS['fcp_good']}ms). Consider optimization"
        )

    # Grade
    if estimated_fcp <= PAINT_TIME_THRESHOLDS['fcp_good']:
        result.metadata["fcp_grade"] = "good"
    elif estimated_fcp <= PAINT_TIME_THRESHOLDS['fcp_needs_work']:
        result.metadata["fcp_grade"] = "needs_work"
    else:
        result.metadata["fcp_grade"] = "poor"

    return result


def _estimate_dom_depth(content: str) -> int:
    """Estimate maximum DOM nesting depth from HTML content."""
    max_depth = 0
    current_depth = 0

    # Simple tag counting (not a full parser, but good enough for estimation)
    # Self-closing tags that don't increase depth
    self_closing = {'br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'source'}

    for match in re.finditer(r'<(/?)(\w+)[^>]*(/?)>', content):
        is_closing = match.group(1) == '/'
        tag_name = match.group(2).lower()
        is_self_closing = match.group(3) == '/'

        if tag_name in self_closing or is_self_closing:
            continue

        if is_closing:
            current_depth = max(0, current_depth - 1)
        else:
            current_depth += 1
            max_depth = max(max_depth, current_depth)

    return max_depth


# =============================================================================
# CLI Entry Point
# =============================================================================

def main() -> int:
    """CLI entry point for validating design agent outputs."""
    if len(sys.argv) < 2:
        print("Usage: python validate_design_output.py <file_path> [--type html|ia|yaml] [--perf]")
        return 1

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return 1

    content = file_path.read_text()

    # Check for performance flag
    run_perf = "--perf" in sys.argv

    # Auto-detect type or use argument
    output_type = "html"
    if "--type" in sys.argv:
        type_idx = sys.argv.index("--type")
        if type_idx + 1 < len(sys.argv):
            output_type = sys.argv[type_idx + 1]
    elif file_path.suffix in ['.yaml', '.yml']:
        output_type = "yaml"
    elif 'HANDOFF' in content.upper() or 'Navigation' in content:
        output_type = "ia"

    # Run appropriate validator
    if output_type == "html":
        result = validate_html_asset(content)
    elif output_type == "ia":
        result = validate_ia_output(content)
    elif output_type == "yaml":
        result = validate_navigation_yaml(content)
    else:
        print(f"Unknown type: {output_type}")
        return 1

    # Run file size validation
    atomic_level = result.metadata.get("atomic_level")
    size_result = validate_file_size(content, atomic_level)
    result.metadata["file_size"] = size_result.metadata
    result.errors.extend(size_result.errors)
    result.warnings.extend(size_result.warnings)
    if not size_result.valid:
        result.valid = False

    # Run paint time estimation for HTML
    if run_perf or output_type == "html":
        paint_result = estimate_paint_time(content)
        result.metadata["paint_time"] = paint_result.metadata
        result.errors.extend(paint_result.errors)
        result.warnings.extend(paint_result.warnings)
        if not paint_result.valid:
            result.valid = False

    # Run design system validation for HTML/React
    if output_type == "html" or ".tsx" in str(file_path) or ".jsx" in str(file_path):
        ds_result = validate_design_system(content)
        result.metadata["design_system"] = ds_result.metadata
        result.errors.extend(ds_result.errors)
        result.warnings.extend(ds_result.warnings)
        if not ds_result.valid:
            result.valid = False

    # Output results
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.valid else 1


if __name__ == "__main__":
    sys.exit(main())
