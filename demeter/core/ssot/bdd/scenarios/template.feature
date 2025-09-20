# BDD Feature Template
# This template is used to generate Feature files from UoW definitions

Feature: {{UOW_TITLE}}
  As a {{STAKEHOLDER_ROLE}}
  I want {{UOW_DESCRIPTION}}
  So that {{BUSINESS_VALUE}}

  Background:
    Given the system is properly initialized
    And all necessary configurations are loaded

{{SCENARIOS_CONTENT}}

  {{#ERROR_SCENARIOS}}
  Scenario: {{ERROR_SCENARIO_NAME}}
    # Error handling scenario for {{ERROR_CONTEXT}}
    Given {{ERROR_GIVEN}}
    When {{ERROR_WHEN}}
    Then {{ERROR_THEN}}
    And the error should be logged appropriately
    And the system should remain stable

  {{/ERROR_SCENARIOS}}

  {{#PERFORMANCE_SCENARIOS}}
  Scenario: {{PERFORMANCE_SCENARIO_NAME}}
    # Performance validation for {{PERFORMANCE_CONTEXT}}
    Given {{PERFORMANCE_GIVEN}}
    When {{PERFORMANCE_WHEN}}
    Then {{PERFORMANCE_THEN}}
    And the response time should be within acceptable limits
    And system resources should be efficiently utilized

  {{/PERFORMANCE_SCENARIOS}}

# Tags for test organization
@{{UOW_ID}}
@{{UOW_CATEGORY}}
@{{MVP_PHASE}}
{{#TAGS}}
@{{TAG}}
{{/TAGS}}

# Related Requirements
# Implements: {{RELATED_FRS}}
# Validates: {{RELATED_NFRS}}
# Dependencies: {{DEPENDENCIES}}