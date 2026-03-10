# File UUID: 1b2c3d4e-5f6a-7b8c-9d0e-1f2a3b4c5d6e
@design @ia-agent @gate-7
Feature: Information Architecture Agent
  As a product designer
  I want the IA agent to create valid navigation structures and user flows
  So that the UX agent can compose compliant visual components

  Background:
    Given the IA agent is initialized
    And the design system is loaded from "shared/design-system"

  # ==========================================================================
  # Navigation Hierarchy Tests
  # ==========================================================================

  @navigation @critical
  Scenario: IA agent creates navigation hierarchy within depth limit
    When I request navigation structure for "analytics dashboard"
    Then the output should contain a navigation hierarchy
    And the hierarchy depth should be at most 3 levels
    And each navigation item should have a non-empty label

  @navigation
  Scenario: IA agent respects maximum navigation depth
    When I request navigation for a complex app with "12 features across 5 categories"
    Then the hierarchy should be restructured to fit within 3 levels
    And the output should explain the flattening rationale

  @navigation @patterns
  Scenario Outline: IA agent suggests appropriate navigation patterns
    When I request navigation for a "<app_type>" application
    Then the output should recommend "<nav_pattern>" navigation
    And the recommendation should include rationale

    Examples:
      | app_type            | nav_pattern |
      | dashboard           | sidebar     |
      | marketing site      | tabs        |
      | mobile app          | bottom tabs |
      | documentation site  | sidebar     |
      | settings page       | tabs        |

  # ==========================================================================
  # User Flow Tests
  # ==========================================================================

  @user-flow @critical
  Scenario: IA agent creates valid user flow diagrams
    When I request a user flow for "user onboarding"
    Then the output should contain a flow diagram
    And the flow should have a clear start point
    And the flow should have at least one end point
    And all decision points should have multiple exit paths

  @user-flow
  Scenario: IA agent identifies error states in flows
    When I request a user flow for "checkout process"
    Then the flow should include error recovery paths
    And the flow should document validation states

  @user-flow @edge-cases
  Scenario: IA agent handles branching logic
    When I request a flow for "subscription selection with trial vs paid paths"
    Then the output should show branching decision points
    And each branch should lead to a valid end state
    And the branches should be clearly labeled

  # ==========================================================================
  # Miller's Law Tests (max 7 items per group)
  # ==========================================================================

  @millers-law @critical
  Scenario: IA agent limits navigation items to 7 per group
    When I request navigation structure for any application
    Then no navigation level should have more than 7 items
    And groups exceeding 7 should be split into sub-categories

  @millers-law
  Scenario: IA agent restructures oversized navigation groups
    When I request navigation for an app with "15 top-level features"
    Then the output should group items into no more than 7 categories
    And each category should contain no more than 7 children
    And the grouping rationale should be explained

  @millers-law
  Scenario Outline: IA agent enforces 7-item limit across contexts
    When I create a "<context>" with <item_count> options
    Then the output should have at most 7 items at any level
    And excess items should be grouped into logical sub-categories

    Examples:
      | context               | item_count |
      | primary navigation    | 12         |
      | dropdown menu         | 15         |
      | tab bar               | 9          |
      | sidebar sections      | 10         |
      | action menu           | 8          |
      | settings categories   | 14         |

  @millers-law @exception
  Scenario: Miller's Law does not apply to data lists
    When I create a search results page showing "50 results"
    Then the data list may exceed 7 items
    And pagination or infinite scroll should be recommended
    But navigation and action menus should still respect the 7-item limit

  # ==========================================================================
  # Content Hierarchy Tests
  # ==========================================================================

  @content-hierarchy
  Scenario: IA agent organizes content by user mental model
    When I request content hierarchy for "e-commerce product catalog"
    Then the hierarchy should prioritize user tasks over org structure
    And related content should be grouped together
    And the hierarchy should support progressive disclosure

  @content-hierarchy @labels
  Scenario: IA agent uses clear, consistent labels
    When I create navigation for any application
    Then all labels should be plain language (no jargon)
    And labels should be specific (not generic like "Settings")
    And labels should be consistent across the hierarchy

  # ==========================================================================
  # Sitemap Tests
  # ==========================================================================

  @sitemap @critical
  Scenario: IA agent generates valid sitemap structure
    When I request a sitemap for "corporate website"
    Then the output should contain a hierarchical tree structure
    And all pages should be reachable from the root
    And there should be no orphan pages
    And cross-links should be documented

  @sitemap @urls
  Scenario: IA agent suggests URL structure aligned with hierarchy
    When I request sitemap with URL recommendations
    Then URLs should reflect the navigation hierarchy
    And URLs should use lowercase kebab-case
    And dynamic segments should be clearly marked

  # ==========================================================================
  # Handoff Tests
  # ==========================================================================

  @handoff @critical
  Scenario: IA agent provides valid handoff for UX agent
    When I complete any IA task
    Then the output should include an "IA HANDOFF SUMMARY" section
    And the handoff should specify the navigation pattern
    And the handoff should list components needed
    And the handoff should indicate ready state for UX agent

  @handoff @components
  Scenario: IA agent maps structure to design system components
    When I create navigation requiring "sidebar with collapsible sections"
    Then the handoff should reference specific design system components
    And the components should exist in "shared/design-system/components"

  # ==========================================================================
  # Gate Integration Tests
  # ==========================================================================

  @gate-integration
  Scenario: IA agent receives context from upstream gates
    Given Gate 6 (Design System) has provided token context
    When the IA agent processes a request
    Then it should acknowledge available design patterns
    And it should reference appropriate navigation components

  @gate-integration @skip-conditions
  Scenario Outline: IA agent gate is skipped appropriately
    Given a request for "<request_type>"
    Then Gate 7 should be "<gate_status>"

    Examples:
      | request_type                           | gate_status |
      | simple button component                | skipped     |
      | stats card molecule                    | skipped     |
      | full dashboard with navigation         | triggered   |
      | sitemap for new application            | triggered   |
      | onboarding user flow                   | triggered   |
      | quick fix to existing page             | skipped     |

  # ==========================================================================
  # Quality Validation Tests
  # ==========================================================================

  @quality @validation
  Scenario: IA output passes quality checklist
    When I complete an IA task
    Then all primary user goals should have clear paths (less than 3 clicks)
    And navigation hierarchy should be 3 levels or fewer
    And labels should be consistent and user-centered
    And there should be no orphan pages
    And error/empty states should be considered
    And mobile navigation approach should be documented

  @quality @accessibility
  Scenario: IA agent considers accessibility in structure
    When I request navigation for any application
    Then the structure should support keyboard navigation
    And the hierarchy should work with screen readers
    And focus order should be logical and documented
