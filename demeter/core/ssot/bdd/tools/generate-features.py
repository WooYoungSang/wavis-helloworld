#!/usr/bin/env python3
"""
Generate BDD Feature Files from UoW Definitions

This tool converts UoW acceptance criteria into executable Gherkin scenarios.
"""

import yaml
import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

class BDDFeatureGenerator:
    def __init__(self, ssot_dir: Path, output_dir: Path):
        self.ssot_dir = ssot_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load step definitions
        self.common_steps = self._load_step_definitions("common-steps.yaml")
        self.domain_steps = self._load_step_definitions("domain-steps.yaml")

        # Load template
        self.template = self._load_template()

    def _load_step_definitions(self, filename: str) -> Dict[str, Any]:
        """Load step definition YAML file."""
        step_file = self.ssot_dir / "bdd" / "step-definitions" / filename
        if step_file.exists():
            with open(step_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}

    def _load_template(self) -> str:
        """Load the Feature file template."""
        template_file = self.ssot_dir / "bdd" / "scenarios" / "template.feature"
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        return self._get_default_template()

    def _get_default_template(self) -> str:
        """Default template if file doesn't exist."""
        return """Feature: {{UOW_TITLE}}
  As a {{STAKEHOLDER_ROLE}}
  I want {{UOW_DESCRIPTION}}
  So that {{BUSINESS_VALUE}}

  Background:
    Given the system is properly initialized
    And all necessary configurations are loaded

{{SCENARIOS_CONTENT}}
"""

    def load_uow_data(self, uow_file: Path) -> Dict[str, Any]:
        """Load UoW data from YAML file."""
        try:
            with open(uow_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading UoW file {uow_file}: {e}")
            return {}

    def extract_scenarios_from_uow(self, uow_id: str, uow_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract BDD scenarios from UoW data."""
        scenarios = []

        # Get acceptance criteria
        ac_list = uow_data.get('acceptance_criteria', {})

        if isinstance(ac_list, list):
            # Handle list format (legacy)
            for i, ac_value in enumerate(ac_list):
                ac_id = f"AC-{i+1:03d}"
                if isinstance(ac_value, str):
                    scenario = self._create_basic_scenario(ac_id, ac_value, uow_data)
                    scenarios.append(scenario)
        elif isinstance(ac_list, dict):
            # Handle dictionary format
            for ac_id, ac_data in ac_list.items():
                if isinstance(ac_data, dict) and 'scenario' in ac_data:
                    # Gherkin scenario is explicitly defined
                    scenario = self._extract_explicit_scenario(ac_id, ac_data)
                    scenarios.append(scenario)
                elif isinstance(ac_data, dict):
                    # Try to infer scenario from description
                    scenario = self._infer_scenario_from_ac(ac_id, ac_data)
                    scenarios.append(scenario)
                else:
                    # Simple string AC - create basic scenario
                    scenario = self._create_basic_scenario(ac_id, str(ac_data), uow_data)
                    scenarios.append(scenario)

        # Add error scenarios
        error_scenarios = self._generate_error_scenarios(uow_data)
        scenarios.extend(error_scenarios)

        # Add performance scenarios if NFRs exist
        performance_scenarios = self._generate_performance_scenarios(uow_data)
        scenarios.extend(performance_scenarios)

        return scenarios

    def _extract_explicit_scenario(self, ac_id: str, ac_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract explicitly defined Gherkin scenario."""
        scenario_data = ac_data.get('scenario', {})

        return {
            'name': f"Validate {ac_data.get('description', ac_id)}",
            'type': 'acceptance',
            'ac_id': ac_id,
            'given': scenario_data.get('given', 'the system is ready'),
            'when': scenario_data.get('when', 'the action is performed'),
            'then': scenario_data.get('then', 'the result should be correct'),
            'additional_given': scenario_data.get('additional_given', []),
            'additional_when': scenario_data.get('additional_when', []),
            'additional_then': scenario_data.get('and', [])
        }

    def _infer_scenario_from_ac(self, ac_id: str, ac_data: Dict[str, Any]) -> Dict[str, Any]:
        """Infer BDD scenario from AC description."""
        description = ac_data.get('description', ac_id)

        # Simple inference rules based on common patterns
        if 'create' in description.lower() or 'add' in description.lower():
            given = "the system is ready to accept new data"
            when = f"a {self._extract_entity(description)} creation is requested"
            then = f"the {self._extract_entity(description)} should be created successfully"
        elif 'update' in description.lower() or 'modify' in description.lower():
            given = f"a {self._extract_entity(description)} exists in the system"
            when = f"the {self._extract_entity(description)} is updated"
            then = f"the {self._extract_entity(description)} should reflect the changes"
        elif 'delete' in description.lower() or 'remove' in description.lower():
            given = f"a {self._extract_entity(description)} exists in the system"
            when = f"the {self._extract_entity(description)} deletion is requested"
            then = f"the {self._extract_entity(description)} should be removed"
        else:
            # Generic scenario
            given = "the preconditions are met"
            when = "the action is performed"
            then = description

        return {
            'name': f"Validate {description}",
            'type': 'acceptance',
            'ac_id': ac_id,
            'given': given,
            'when': when,
            'then': then,
            'additional_given': [],
            'additional_when': [],
            'additional_then': []
        }

    def _create_basic_scenario(self, ac_id: str, ac_description: str, uow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create basic scenario from simple AC string."""
        return {
            'name': f"Validate {ac_id}",
            'type': 'acceptance',
            'ac_id': ac_id,
            'given': "the system is properly configured",
            'when': "the functionality is executed",
            'then': ac_description,
            'additional_given': [],
            'additional_when': [],
            'additional_then': []
        }

    def _generate_error_scenarios(self, uow_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate error handling scenarios."""
        scenarios = []

        # Common error scenarios
        error_cases = [
            {
                'name': 'Handle invalid input',
                'given': 'invalid input data is provided',
                'when': 'the operation is attempted',
                'then': 'an appropriate error should be returned'
            },
            {
                'name': 'Handle system unavailability',
                'given': 'a required service is unavailable',
                'when': 'the operation is attempted',
                'then': 'a service unavailable error should be returned'
            }
        ]

        for error_case in error_cases:
            scenarios.append({
                'name': error_case['name'],
                'type': 'error',
                'given': error_case['given'],
                'when': error_case['when'],
                'then': error_case['then'],
                'additional_given': [],
                'additional_when': [],
                'additional_then': ['the error should be logged appropriately', 'the system should remain stable']
            })

        return scenarios

    def _generate_performance_scenarios(self, uow_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate performance validation scenarios."""
        scenarios = []

        # Check if there are related NFRs
        related_nfrs = uow_data.get('related_nfrs', [])
        if any('NFR-001' in nfr or 'performance' in str(nfr).lower() for nfr in related_nfrs):
            scenarios.append({
                'name': 'Validate performance requirements',
                'type': 'performance',
                'given': 'the system is under normal load',
                'when': 'the operation is performed',
                'then': 'the response time should be within acceptable limits',
                'additional_given': [],
                'additional_when': [],
                'additional_then': ['system resources should be efficiently utilized']
            })

        return scenarios

    def _extract_entity(self, description: str) -> str:
        """Extract entity name from description."""
        # Simple entity extraction - can be enhanced
        entities = ['user', 'product', 'order', 'payment', 'configuration', 'data', 'record', 'item']
        for entity in entities:
            if entity in description.lower():
                return entity
        return 'entity'

    def generate_feature_file(self, uow_id: str, uow_data: Dict[str, Any], output_file: Path):
        """Generate a complete Feature file for a UoW."""

        # Extract scenarios
        scenarios = self.extract_scenarios_from_uow(uow_id, uow_data)

        # Prepare template variables
        template_vars = {
            'UOW_TITLE': uow_data.get('title', uow_id),
            'UOW_DESCRIPTION': uow_data.get('description', ''),
            'BUSINESS_VALUE': uow_data.get('business_value', 'achieve the desired outcome'),
            'STAKEHOLDER_ROLE': self._determine_stakeholder_role(uow_data),
            'UOW_ID': uow_id,
            'UOW_CATEGORY': uow_data.get('category', 'General'),
            'MVP_PHASE': self._extract_mvp_phase(uow_data),
            'RELATED_FRS': ', '.join(uow_data.get('related_frs', [])),
            'RELATED_NFRS': ', '.join(uow_data.get('related_nfrs', [])),
            'DEPENDENCIES': ', '.join(uow_data.get('dependencies', []))
        }

        # Generate feature content
        feature_content = self._apply_template(template_vars, scenarios)

        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(feature_content)

        print(f"Generated feature file: {output_file}")

    def _determine_stakeholder_role(self, uow_data: Dict[str, Any]) -> str:
        """Determine the stakeholder role based on UoW category."""
        category = uow_data.get('category', '').lower()

        role_mapping = {
            'foundation': 'system administrator',
            'infrastructure': 'platform engineer',
            'application': 'end user',
            'deployment': 'devops engineer',
            'e-commerce': 'customer',
            'fintech': 'financial user',
            'healthcare': 'healthcare provider',
            'iot': 'device operator'
        }

        return role_mapping.get(category, 'system user')

    def _extract_mvp_phase(self, uow_data: Dict[str, Any]) -> str:
        """Extract MVP phase from UoW data."""
        # This would typically come from the UoW definition
        return uow_data.get('mvp_phase', 'phase_1')

    def _apply_template(self, template_vars: Dict[str, Any], scenarios: List[Dict[str, Any]]) -> str:
        """Apply template variables and scenarios to generate feature content."""

        # Start with basic template substitution
        content = self.template

        for key, value in template_vars.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))

        # Generate scenarios section
        scenarios_content = ""

        for scenario in scenarios:
            scenario_text = f"\n  Scenario: {scenario['name']}\n"
            scenario_text += f"    Given {scenario['given']}\n"

            # Add additional given clauses
            for additional_given in scenario['additional_given']:
                scenario_text += f"    And {additional_given}\n"

            scenario_text += f"    When {scenario['when']}\n"

            # Add additional when clauses
            for additional_when in scenario['additional_when']:
                scenario_text += f"    And {additional_when}\n"

            scenario_text += f"    Then {scenario['then']}\n"

            # Add additional then clauses
            for additional_then in scenario['additional_then']:
                scenario_text += f"    And {additional_then}\n"

            scenarios_content += scenario_text

        # Replace scenarios content placeholder
        content = content.replace("{{SCENARIOS_CONTENT}}", scenarios_content)

        return content

    def generate_all_features(self, uow_files: List[Path]):
        """Generate feature files for all UoWs."""
        print(f"Generating BDD feature files from {len(uow_files)} UoW files...")

        for uow_file in uow_files:
            print(f"Processing {uow_file}...")

            uow_data = self.load_uow_data(uow_file)
            if not uow_data:
                continue

            # Extract UoWs from the file
            units_of_work = uow_data.get('units_of_work', {})
            if not units_of_work:
                # Try alternative structure
                if 'universal_uows' in uow_data:
                    units_of_work = uow_data['universal_uows']

            for uow_id, uow_info in units_of_work.items():
                feature_filename = f"{uow_id.lower().replace('-', '_')}.feature"
                output_file = self.output_dir / feature_filename

                self.generate_feature_file(uow_id, uow_info, output_file)


def find_uow_files(ssot_dir: Path) -> List[Path]:
    """Find all UoW definition files."""
    uow_files = []

    # Base UoW files
    base_dir = ssot_dir / "base"
    if base_dir.exists():
        uow_files.extend(base_dir.glob("*uow*.yaml"))

    # Framework requirements
    framework_file = ssot_dir / "framework-requirements.yaml"
    if framework_file.exists():
        uow_files.append(framework_file)

    # Extension UoW files
    extensions_dir = ssot_dir / "extensions"
    if extensions_dir.exists():
        uow_files.extend(extensions_dir.rglob("*.yaml"))

    return uow_files


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate BDD Feature files from UoW definitions')
    parser.add_argument('--ssot-dir', type=str, default='./demeter/core/ssot',
                       help='SSOT directory path')
    parser.add_argument('--output-dir', type=str, default='./features',
                       help='Output directory for feature files')
    parser.add_argument('--uow-file', type=str,
                       help='Specific UoW file to process')
    parser.add_argument('--uow-id', type=str,
                       help='Specific UoW ID to generate')

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()

    ssot_dir = Path(args.ssot_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    if not ssot_dir.exists():
        print(f"Error: SSOT directory not found: {ssot_dir}")
        sys.exit(1)

    generator = BDDFeatureGenerator(ssot_dir, output_dir)

    if args.uow_file:
        # Process specific file
        uow_file = Path(args.uow_file)
        if not uow_file.exists():
            print(f"Error: UoW file not found: {uow_file}")
            sys.exit(1)

        generator.generate_all_features([uow_file])
    else:
        # Process all UoW files
        uow_files = find_uow_files(ssot_dir)
        if not uow_files:
            print("No UoW files found in SSOT directory")
            sys.exit(1)

        generator.generate_all_features(uow_files)

    print("BDD feature generation completed!")


if __name__ == '__main__':
    main()