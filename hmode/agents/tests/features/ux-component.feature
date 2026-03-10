# File UUID: 2c3d4e5f-6a7b-8c9d-0e1f-2a3b4c5d6e7f
@design @ux-agent @gate-8
Feature: UX Component Agent
  As a product designer
  I want the UX agent to compose valid UI components from the design library
  So that all visual assets are consistent and design-system compliant

  Background:
    Given the UX agent is initialized
    And the design system is loaded from "shared/design-system"
    And design tokens are available from "globals.css"

  # ==========================================================================
  # Design Token Compliance Tests
  # ==========================================================================

  @tokens @critical
  Scenario: UX agent uses design tokens for colors
    When I request any visual component
    Then the output should not contain raw hex colors
    And colors should use "hsl(var(--token-name))" format
    And Tailwind color classes should reference design tokens

  @tokens @critical
  Scenario: UX agent uses typography scale
    When I request any component with text
    Then font sizes should use the typography scale (text-xs through text-7xl)
    And no magic pixel values should be used for fonts
    And line heights should use Tailwind defaults

  @tokens @critical
  Scenario: UX agent uses spacing scale
    When I request any component with padding or margins
    Then spacing should use the 4px base unit scale
    And valid values should be: 4, 8, 12, 16, 24, 32, 48, 64px
    And Tailwind spacing classes (p-4, m-6, gap-2) should be used

  @tokens
  Scenario Outline: UX agent applies correct design tokens
    When I request a component needing "<token_type>"
    Then the output should use "<expected_usage>"

    Examples:
      | token_type        | expected_usage                    |
      | background color  | bg-background or --background     |
      | text color        | text-foreground or --foreground   |
      | border color      | border-border or --border         |
      | primary action    | bg-primary or --primary           |
      | muted text        | text-muted-foreground             |
      | border radius     | rounded-md or --radius            |

  # ==========================================================================
  # Asset Metadata Tests
  # ==========================================================================

  @metadata @critical
  Scenario: UX agent includes required metadata header
    When I generate any visual asset
    Then the output should include a metadata comment header
    And the header should contain "Asset:" with a descriptive name
    And the header should contain "Asset ID:" with a unique identifier
    And the header should contain "Date:" in ISO format
    And the header should contain "Atomic Level:" classification

  @metadata
  Scenario: UX agent documents tokens used
    When I generate a visual asset
    Then the metadata should include a "Tokens Used" section
    And it should list colors used (e.g., --background, --primary)
    And it should list spacing used (e.g., space-4, space-6)
    And it should list typography used (e.g., text-base, text-lg)

  @metadata @atomic
  Scenario Outline: UX agent correctly classifies atomic level
    When I request a "<component_type>"
    Then the atomic level should be "<expected_level>"

    Examples:
      | component_type              | expected_level |
      | button                      | atom           |
      | input field                 | atom           |
      | badge                       | atom           |
      | card with title and content | molecule       |
      | form field with label       | molecule       |
      | alert with icon and text    | molecule       |
      | header with nav and logo    | organism       |
      | sidebar with navigation     | organism       |
      | data table with pagination  | organism       |
      | dashboard layout            | template       |
      | landing page structure      | template       |
      | actual login page           | page           |

  # ==========================================================================
  # Template Selection Tests
  # ==========================================================================

  @templates
  Scenario: UX agent starts from design system template
    When I request a mockup or page
    Then it should use a template from "shared/design-system/templates"
    And the template selection should be announced

  @templates
  Scenario Outline: UX agent selects appropriate template
    When I request a "<mockup_type>"
    Then the agent should use "<expected_template>"

    Examples:
      | mockup_type              | expected_template     |
      | landing page             | landing-dark.html     |
      | component mockup         | mockup.html           |
      | early wireframe          | lofi-wireframe.html   |
      | marketing pitch          | pitch.html            |
      | documentation site       | microsite.html        |
      | mobile flow              | mobile-sequence-diagram.html |

  # ==========================================================================
  # Atomic Design Composition Tests
  # ==========================================================================

  @composition @critical
  Scenario: UX agent composes molecules from atoms
    When I request a "form field with label and validation message"
    Then the output should combine multiple atoms
    And it should use Label atom
    And it should use Input atom
    And it should use text for validation message
    And they should be properly grouped

  @composition
  Scenario: UX agent composes organisms from molecules
    When I request a "card grid section"
    Then the output should combine multiple Card molecules
    And it should include a section header
    And layout should use grid or flex patterns
    And spacing should be consistent between items

  @composition
  Scenario: UX agent references existing components
    When I request a component that exists in the design library
    Then it should reference the existing component
    And not recreate it from scratch
    And note the component path in documentation

  # ==========================================================================
  # Visual Hierarchy Tests
  # ==========================================================================

  @hierarchy @critical
  Scenario: UX agent enforces visual hierarchy limits
    When I generate any page or template
    Then visual hierarchy should have maximum 3 levels
    And there should be clear H1 > H2 > Body relationship
    And heading levels should not be skipped (no H1 > H3)

  @hierarchy @focal-point
  Scenario: UX agent creates single focal point
    When I generate a section or card
    Then there should be a single primary call-to-action
    And secondary actions should be visually subordinate
    And the visual weight should guide the eye naturally

  @hierarchy
  Scenario: UX agent uses whitespace effectively
    When I generate any layout
    Then there should be adequate whitespace between sections
    And content groups should be visually distinct
    And the layout should not feel cramped

  # ==========================================================================
  # IA Integration Tests
  # ==========================================================================

  @ia-handoff @critical
  Scenario: UX agent implements IA specification
    Given an IA specification with sidebar navigation
    When I request the visual implementation
    Then the output should use Sidebar organism from design library
    And navigation items should match IA structure
    And hierarchy depth should match IA specification

  @ia-handoff
  Scenario: UX agent maps IA components to design library
    Given an IA handoff specifying "tabs, breadcrumbs, sidebar"
    When I implement the visual components
    Then I should use Tabs from design library
    And I should use Breadcrumbs component
    And I should use Sidebar organism
    And all should follow design token patterns

  @ia-handoff
  Scenario: UX agent handles IA without handoff
    When I receive a direct mockup request without IA specification
    Then I should ask if IA is needed first
    Or proceed with simple structure for standalone components
    And document the assumption in metadata

  # ==========================================================================
  # Theme Application Tests
  # ==========================================================================

  @themes
  Scenario: UX agent can apply available themes
    When I request "marine-sunset theme" for a component
    Then the output should use Marine Sunset color tokens
    And the theme variables should override defaults
    And the theme fonts should be referenced

  @themes
  Scenario Outline: UX agent applies theme correctly
    When I apply "<theme_name>" theme
    Then the primary color should be "<primary_color>"
    And the background should be "<background_color>"

    Examples:
      | theme_name       | primary_color | background_color |
      | default          | --primary     | --background     |
      | marine-sunset    | coral/teal    | deep blue        |
      | night-sky        | violet        | cosmic blue      |

  # ==========================================================================
  # Design System Compliance Tests
  # ==========================================================================

  @design-system @critical
  Scenario: UX agent uses shadcn/ui or explicit theme
    When I generate any visual asset
    Then it must use either shadcn/ui with Tailwind defaults
    Or an explicit theme from the design system (marine-sunset, night-sky)
    And raw hex colors in backgrounds are not allowed

  @design-system @critical
  Scenario: UX agent uses required shadcn tokens
    When I generate a shadcn/ui compliant component
    Then all required CSS variables should be defined
    And the token coverage should be at least 70%
    And tokens should include: --background, --foreground, --primary, --secondary
    And tokens should include: --muted, --accent, --destructive, --border, --ring

  @design-system @tailwind
  Scenario: UX agent includes Tailwind CDN for HTML mockups
    When I generate an HTML mockup
    Then it should include the Tailwind CDN script
    Or it should include a <style> block with token definitions
    And Tailwind utility classes should be used for styling

  @design-system @react
  Scenario: UX agent uses shadcn imports for React components
    When I generate a React/TypeScript component
    Then it should import components from "@/components/ui/"
    And it should not use raw HTML elements for common UI patterns
    And the component should follow shadcn/ui conventions

  @design-system @tokens
  Scenario: UX agent uses hsl(var(--token)) format
    When I generate any component with colors
    Then CSS colors should use "hsl(var(--token-name))" format
    And no hardcoded HSL values like "hsl(240, 10%, 4%)"
    And no hardcoded RGB values like "rgb(26, 26, 46)"

  @design-system @consistency
  Scenario: UX agent uses single theme consistently
    When I generate a multi-component mockup
    Then only one theme should be applied throughout
    And mixing default shadcn with named themes is not allowed
    And theme markers should be consistent across all sections

  @design-system @detection
  Scenario Outline: UX agent theme is correctly detected
    When I generate a component using "<theme_approach>"
    Then the detected theme should be "<expected_detection>"
    And the confidence should be at least <min_confidence>

    Examples:
      | theme_approach                    | expected_detection    | min_confidence |
      | full shadcn/ui tokens             | default (shadcn/ui)   | 0.7            |
      | marine-sunset markers             | marine-sunset         | 0.6            |
      | night-sky markers                 | night-sky             | 0.6            |
      | partial tokens (under 50%)        | incomplete            | 0.0            |
      | no design system                  | none                  | 0.0            |

  # ==========================================================================
  # Output Format Tests
  # ==========================================================================

  @output @html
  Scenario: UX agent generates valid HTML mockups
    When I request an HTML mockup
    Then the output should be valid HTML5
    And it should use Tailwind CDN (no build step required)
    And it should include all necessary CSS in the file
    And it should be viewable by opening directly in browser

  @output @react
  Scenario: UX agent generates valid React components
    When I request a React component
    Then the output should use TypeScript
    And it should import from shadcn/ui where applicable
    And it should use proper component composition
    And it should include necessary type definitions

  # ==========================================================================
  # Gate Integration Tests
  # ==========================================================================

  @gate-integration
  Scenario: UX agent receives full context from upstream gates
    Given Gate 6 has loaded design tokens
    And Gate 7 has provided IA specification
    When the UX agent processes a request
    Then it should use tokens from Gate 6
    And it should implement structure from Gate 7
    And the output should acknowledge both inputs

  @gate-integration @skip-conditions
  Scenario Outline: UX agent gate is triggered appropriately
    Given a request for "<request_type>"
    Then Gate 8 should be "<gate_status>"

    Examples:
      | request_type                  | gate_status |
      | sitemap only                  | skipped     |
      | research task                 | skipped     |
      | API endpoint                  | skipped     |
      | button component              | triggered   |
      | landing page mockup           | triggered   |
      | dashboard UI                  | triggered   |
      | component from design library | triggered   |

  # ==========================================================================
  # File Size Tests
  # ==========================================================================

  @file-size @critical
  Scenario Outline: UX agent output stays within size limits
    When I generate a "<atomic_level>" component
    Then the file size should be at most <max_kb> KB

    Examples:
      | atomic_level | max_kb |
      | atom         | 5      |
      | molecule     | 15     |
      | organism     | 50     |
      | template     | 100    |
      | page         | 150    |

  @file-size
  Scenario: UX agent warns when approaching size limits
    When I generate a component that is 80% of its size limit
    Then the validator should produce a warning
    And suggest optimization strategies

  @file-size
  Scenario: UX agent avoids bloated output
    When I generate any visual asset
    Then the output should not include unnecessary whitespace
    And unused CSS should not be included
    And comments should be concise (metadata only)

  # ==========================================================================
  # Paint Time / Performance Tests
  # ==========================================================================

  @paint-time @critical
  Scenario: UX agent output loads within FCP threshold
    When I render any generated HTML asset in a browser
    Then First Contentful Paint should be under 1800ms
    And DOM content loaded should be under 2000ms

  @paint-time @critical
  Scenario: UX agent output has acceptable LCP
    When I render any generated HTML asset in a browser
    Then Largest Contentful Paint should be under 2500ms

  @paint-time
  Scenario: UX agent output has minimal layout shift
    When I render any generated HTML asset in a browser
    Then Cumulative Layout Shift should be under 0.1

  @paint-time @dom
  Scenario: UX agent output has reasonable DOM complexity
    When I generate any visual asset
    Then DOM node count should be under 1500
    And DOM nesting depth should be under 15 levels
    And inline style attributes should be under 20

  @paint-time @optimization
  Scenario: UX agent minimizes external resource loading
    When I generate an HTML mockup
    Then external script tags should be minimized
    And CSS should prefer inline style blocks over external links
    And images should use lazy loading where appropriate

  @paint-time @heuristic
  Scenario: UX agent output passes static paint time estimation
    When I run the paint time estimator on a generated asset
    Then the estimated FCP should be graded "good" (under 1800ms)
    And the breakdown should show base render, resource, and style costs

  # ==========================================================================
  # Miller's Law Tests (UX perspective)
  # ==========================================================================

  @millers-law @critical
  Scenario: UX agent limits visible choices to 7
    When I compose a navigation organism
    Then visible menu items at any level should not exceed 7
    And overflow items should use a "More" pattern or sub-menu

  @millers-law
  Scenario: UX agent limits action buttons per section
    When I compose a card or section with multiple actions
    Then there should be at most 7 visible action choices
    And the primary action should be visually prominent
    And secondary actions may be collapsed into a menu

  # ==========================================================================
  # Typography Tests
  # ==========================================================================

  @typography @critical
  Scenario: UX agent uses typography scale
    When I generate any text-containing component
    Then font sizes should use Tailwind scale (text-xs through text-7xl)
    And no raw pixel values for font-size (e.g., 15px, 17px)
    And font sizes should be at least 12px for readability

  @typography @critical
  Scenario: UX agent uses design token text colors
    When I generate any component with text
    Then text colors should use design tokens (text-foreground, text-muted-foreground)
    And no raw hex colors in color or fill properties
    And color should use hsl(var(--token)) format in CSS

  @typography
  Scenario: UX agent maintains heading hierarchy
    When I generate a page or template
    Then heading levels should not be skipped (no h1 > h3)
    And there should be at most one h1 per page
    And heading sizes should decrease with level (h1 > h2 > h3)

  @typography @font-weight
  Scenario: UX agent uses appropriate font weights
    When I generate text content
    Then font weights should use Tailwind classes (font-normal, font-medium, font-bold)
    And headings should be visually distinct from body text
    And primary CTAs should have appropriate weight emphasis

  # ==========================================================================
  # Contrast & Accessibility Tests
  # ==========================================================================

  @contrast @critical @wcag
  Scenario: UX agent maintains WCAG contrast ratios
    When I generate any text-containing component
    Then normal text should have at least 4.5:1 contrast ratio
    And large text (18px+) should have at least 3:1 contrast ratio
    And interactive elements should have visible focus states

  @contrast @critical
  Scenario: UX agent avoids low contrast color combinations
    When I compose components with colored backgrounds
    Then foreground text should contrast sufficiently with background
    And muted-foreground on muted should meet contrast requirements
    And primary-foreground on primary should meet requirements

  @contrast
  Scenario: UX agent ensures color is not the only indicator
    When I generate status indicators or interactive states
    Then color should not be the sole means of conveying information
    And icons, text, or patterns should accompany color changes
    And error states should have text, not just red color

  # ==========================================================================
  # Responsive Design Tests
  # ==========================================================================

  @responsive @critical
  Scenario Outline: UX agent output works on all viewport sizes
    When I render a generated asset on "<viewport>"
    Then the content should be visible without horizontal scrolling
    And text should remain readable (minimum 12px)
    And touch targets should be at least 44x44px on touch devices

    Examples:
      | viewport          | width | height |
      | phone             | 375   | 667    |
      | tablet_vertical   | 768   | 1024   |
      | tablet_horizontal | 1024  | 768    |
      | desktop           | 1440  | 900    |

  @responsive @critical
  Scenario: UX agent includes viewport meta tag
    When I generate an HTML mockup or page
    Then it should include viewport meta tag
    And the content should be: width=device-width, initial-scale=1.0

  @responsive
  Scenario: UX agent uses responsive Tailwind classes
    When I generate any layout component
    Then it should include responsive prefixes (sm:, md:, lg:, xl:)
    And layouts should adapt to different screen sizes
    And navigation should have mobile variant if complex

  @responsive @mobile-first
  Scenario: UX agent follows mobile-first approach
    When I generate a responsive component
    Then base styles should target mobile
    And larger viewport styles should use responsive prefixes
    And content should stack vertically on small screens

  @responsive @touch
  Scenario: UX agent creates touch-friendly interfaces
    When I generate interactive components for mobile
    Then buttons and links should be at least 44x44px
    And there should be adequate spacing between touch targets
    And hover states should have touch equivalents (active states)

  # ==========================================================================
  # Quality Validation Tests
  # ==========================================================================

  @quality @validation @critical
  Scenario: UX output passes design system validation
    When I generate any visual asset
    Then all colors should use "hsl(var(--token))" format
    And typography should use the defined scale
    And spacing should use token scale
    And visual hierarchy should be limited to 3 levels
    And there should be a single primary focal point per section
    And asset metadata header should be included
    And atomic level should be correctly classified
    And tokens used should be documented

  @quality @accessibility
  Scenario: UX agent considers accessibility
    When I generate any interactive component
    Then contrast ratios should meet WCAG 4.5:1 for text
    And interactive states should be defined (hover, focus, active)
    And focus indicators should be visible
    And color should not be the only indicator of state
