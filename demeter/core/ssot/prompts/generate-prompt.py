#!/usr/bin/env python3
"""
Generate AI Prompts from SSOT Templates

This tool generates ready-to-use AI prompts based on SSOT data and prompt templates.
"""

import yaml
import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import re
import json

class PromptGenerator:
    def __init__(self, ssot_dir: Path, templates_file: Path):
        self.ssot_dir = ssot_dir
        self.templates_file = templates_file

        # Load templates
        self.templates = self._load_templates()

        # Load SSOT data
        self.ssot_data = self._load_ssot_data()

    def _load_templates(self) -> Dict[str, Any]:
        """Load prompt templates from YAML file."""
        try:
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading templates: {e}")
            return {}

    def _load_ssot_data(self) -> Dict[str, Any]:
        """Load all SSOT data files."""
        ssot_data = {}

        # Load main framework requirements
        framework_file = self.ssot_dir / "framework-requirements.yaml"
        if framework_file.exists():
            ssot_data['framework_requirements'] = self._load_yaml_file(framework_file)

        # Load base files
        base_dir = self.ssot_dir / "base"
        if base_dir.exists():
            for yaml_file in base_dir.glob("*.yaml"):
                ssot_data[yaml_file.stem] = self._load_yaml_file(yaml_file)

        # Load extension files
        extensions_dir = self.ssot_dir / "extensions"
        if extensions_dir.exists():
            ssot_data['extensions'] = {}
            for category_dir in extensions_dir.iterdir():
                if category_dir.is_dir():
                    ssot_data['extensions'][category_dir.name] = {}
                    for yaml_file in category_dir.glob("*.yaml"):
                        ssot_data['extensions'][category_dir.name][yaml_file.stem] = self._load_yaml_file(yaml_file)

        # Load other SSOT files
        for yaml_file in self.ssot_dir.glob("*.yaml"):
            if yaml_file.name not in ["framework-requirements.yaml"]:
                ssot_data[yaml_file.stem] = self._load_yaml_file(yaml_file)

        return ssot_data

    def _load_yaml_file(self, file_path: Path) -> Dict[str, Any]:
        """Load a single YAML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load {file_path}: {e}")
            return {}

    def get_uow_by_id(self, uow_id: str) -> Optional[Dict[str, Any]]:
        """Find UoW by ID across all SSOT files."""
        # Check framework requirements
        if 'framework_requirements' in self.ssot_data:
            fr_data = self.ssot_data['framework_requirements']
            if 'units_of_work' in fr_data and uow_id in fr_data['units_of_work']:
                return fr_data['units_of_work'][uow_id]

        # Check base UoW files
        if 'uow-base' in self.ssot_data:
            uow_data = self.ssot_data['uow-base']
            if 'units_of_work' in uow_data and uow_id in uow_data['units_of_work']:
                return uow_data['units_of_work'][uow_id]

        # Check extensions
        if 'extensions' in self.ssot_data:
            for category, extensions in self.ssot_data['extensions'].items():
                for extension_name, extension_data in extensions.items():
                    if 'units_of_work' in extension_data and uow_id in extension_data['units_of_work']:
                        return extension_data['units_of_work'][uow_id]

        return None

    def get_fr_by_id(self, fr_id: str) -> Optional[Dict[str, Any]]:
        """Find FR by ID across all SSOT files."""
        # Check framework requirements
        if 'framework_requirements' in self.ssot_data:
            fr_data = self.ssot_data['framework_requirements']
            if 'functional_requirements' in fr_data and fr_id in fr_data['functional_requirements']:
                return fr_data['functional_requirements'][fr_id]

        # Check base FR files
        if 'fr-base' in self.ssot_data:
            fr_data = self.ssot_data['fr-base']
            if 'functional_requirements' in fr_data and fr_id in fr_data['functional_requirements']:
                return fr_data['functional_requirements'][fr_id]

        return None

    def build_uow_context(self, uow_id: str) -> Dict[str, Any]:
        """Build complete context for UoW-based prompts."""
        uow_data = self.get_uow_by_id(uow_id)
        if not uow_data:
            raise ValueError(f"UoW {uow_id} not found")

        context = {
            'UOW_ID': uow_id,
            'UOW_TITLE': uow_data.get('name', uow_id),
            'UOW_GOAL': uow_data.get('goal', ''),
            'UOW_LAYER': uow_data.get('layer', ''),
            'UOW_PRIORITY': uow_data.get('priority', ''),
            'DEPENDENCIES': ', '.join(uow_data.get('dependencies', [])),
            'IMPLEMENTS_FRS': ', '.join(uow_data.get('implements', [])),
            'IMPLEMENTS_NFRS': ', '.join([impl for impl in uow_data.get('implements', []) if impl.startswith('NFR')]),
        }

        # Build acceptance criteria context
        ac_list = []
        ac_data = uow_data.get('acceptance_criteria', {})

        if isinstance(ac_data, dict):
            for ac_id, ac_info in ac_data.items():
                if isinstance(ac_info, dict):
                    ac_context = {
                        'AC_ID': ac_id,
                        'AC_DESCRIPTION': ac_info.get('description', ''),
                    }

                    # Add Gherkin scenario details if available
                    scenario = ac_info.get('scenario', {})
                    if scenario:
                        ac_context.update({
                            'AC_GIVEN': scenario.get('given', ''),
                            'AC_WHEN': scenario.get('when', ''),
                            'AC_THEN': scenario.get('then', ''),
                        })

                    ac_list.append(ac_context)

        context['ACCEPTANCE_CRITERIA'] = ac_list

        return context

    def build_project_context(self) -> Dict[str, Any]:
        """Build project-wide context."""
        context = {}

        # Add tech stack info (would normally come from meta-config.yaml)
        context.update({
            'TECH_STACK': 'Technology Agnostic (determined at setup)',
            'PROJECT_STRUCTURE': 'Layered Architecture (Foundation, Infrastructure, Application, Deployment)',
        })

        return context

    def generate_prompt(self, template_category: str, template_name: str, context: Dict[str, Any]) -> str:
        """Generate a prompt from template and context."""
        templates = self.templates.get('prompt_templates', {})
        category_templates = templates.get(template_category, {})
        template_info = category_templates.get(template_name)

        if not template_info:
            raise ValueError(f"Template {template_category}.{template_name} not found")

        template_text = template_info.get('template', '')

        # Simple template substitution (could be enhanced with proper templating engine)
        result = template_text

        # Replace simple variables
        for key, value in context.items():
            if isinstance(value, str):
                result = result.replace(f"{{{{{key}}}}}", value)

        # Handle list templates (simplified)
        result = self._process_list_templates(result, context)

        return result

    def _process_list_templates(self, template: str, context: Dict[str, Any]) -> str:
        """Process list-based template sections."""
        result = template

        # Handle ACCEPTANCE_CRITERIA list
        if 'ACCEPTANCE_CRITERIA' in context:
            ac_pattern = r'{{#ACCEPTANCE_CRITERIA}}(.*?){{/ACCEPTANCE_CRITERIA}}'
            matches = re.findall(ac_pattern, result, re.DOTALL)

            for match in matches:
                ac_section = ""
                for ac in context['ACCEPTANCE_CRITERIA']:
                    ac_text = match
                    for key, value in ac.items():
                        ac_text = ac_text.replace(f"{{{{{key}}}}}", str(value))
                    ac_section += ac_text

                result = re.sub(ac_pattern, ac_section, result, count=1, flags=re.DOTALL)

        return result

    def list_templates(self) -> List[Dict[str, str]]:
        """List all available templates."""
        templates = []
        prompt_templates = self.templates.get('prompt_templates', {})

        for category, category_templates in prompt_templates.items():
            for template_name, template_info in category_templates.items():
                templates.append({
                    'category': category,
                    'name': template_name,
                    'title': template_info.get('name', template_name),
                    'description': template_info.get('description', ''),
                })

        return templates

    def generate_uow_implementation_prompt(self, uow_id: str) -> str:
        """Generate implementation prompt for a specific UoW."""
        uow_context = self.build_uow_context(uow_id)
        project_context = self.build_project_context()

        # Merge contexts
        full_context = {**uow_context, **project_context}

        return self.generate_prompt('code_generation', 'implement_uow', full_context)

    def generate_bdd_test_prompt(self, uow_id: str) -> str:
        """Generate BDD test prompt for a specific UoW."""
        uow_data = self.get_uow_by_id(uow_id)
        if not uow_data:
            raise ValueError(f"UoW {uow_id} not found")

        # Build scenarios from acceptance criteria
        scenarios = []
        ac_data = uow_data.get('acceptance_criteria', {})

        if isinstance(ac_data, dict):
            for ac_id, ac_info in ac_data.items():
                if isinstance(ac_info, dict) and 'scenario' in ac_info:
                    scenario_data = ac_info['scenario']
                    scenario = {
                        'SCENARIO_NAME': f"Validate {ac_info.get('description', ac_id)}",
                        'GIVEN': scenario_data.get('given', ''),
                        'WHEN': scenario_data.get('when', ''),
                        'THEN': scenario_data.get('then', ''),
                        'AND_STEPS': scenario_data.get('and', [])
                    }
                    scenarios.append(scenario)

        context = {
            'FEATURE_NAME': uow_data.get('name', uow_id),
            'FEATURE_DESCRIPTION': uow_data.get('goal', ''),
            'SCENARIOS': scenarios,
            'TEST_FRAMEWORK': 'Framework-specific (determined at setup)',
            'TEST_ENV': 'Test environment',
            'DATABASE_TYPE': 'As configured',
            'EXTERNAL_SERVICES': 'As defined in requirements'
        }

        return self.generate_prompt('code_generation', 'generate_tests', context)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate AI prompts from SSOT templates')
    parser.add_argument('--ssot-dir', type=str, default='./demeter/core/ssot',
                       help='SSOT directory path')
    parser.add_argument('--templates', type=str, default='./demeter/core/ssot/prompts/templates.yaml',
                       help='Templates file path')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # List templates command
    list_parser = subparsers.add_parser('list', help='List available templates')

    # Generate UoW implementation prompt
    impl_parser = subparsers.add_parser('implement', help='Generate UoW implementation prompt')
    impl_parser.add_argument('--uow-id', required=True, help='UoW ID to generate prompt for')

    # Generate BDD test prompt
    test_parser = subparsers.add_parser('test', help='Generate BDD test prompt')
    test_parser.add_argument('--uow-id', required=True, help='UoW ID to generate test prompt for')

    # Custom prompt generation
    custom_parser = subparsers.add_parser('custom', help='Generate custom prompt')
    custom_parser.add_argument('--category', required=True, help='Template category')
    custom_parser.add_argument('--template', required=True, help='Template name')
    custom_parser.add_argument('--context', help='Context JSON file')

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()

    ssot_dir = Path(args.ssot_dir).resolve()
    templates_file = Path(args.templates).resolve()

    if not ssot_dir.exists():
        print(f"Error: SSOT directory not found: {ssot_dir}")
        sys.exit(1)

    if not templates_file.exists():
        print(f"Error: Templates file not found: {templates_file}")
        sys.exit(1)

    generator = PromptGenerator(ssot_dir, templates_file)

    try:
        if args.command == 'list':
            templates = generator.list_templates()
            print("Available Prompt Templates:")
            print("=" * 50)
            for template in templates:
                print(f"{template['category']}.{template['name']}")
                print(f"  Title: {template['title']}")
                print(f"  Description: {template['description']}")
                print()

        elif args.command == 'implement':
            prompt = generator.generate_uow_implementation_prompt(args.uow_id)
            print("=" * 80)
            print(f"IMPLEMENTATION PROMPT FOR UoW: {args.uow_id}")
            print("=" * 80)
            print(prompt)

        elif args.command == 'test':
            prompt = generator.generate_bdd_test_prompt(args.uow_id)
            print("=" * 80)
            print(f"BDD TEST PROMPT FOR UoW: {args.uow_id}")
            print("=" * 80)
            print(prompt)

        elif args.command == 'custom':
            context = {}
            if args.context and Path(args.context).exists():
                with open(args.context, 'r') as f:
                    context = json.load(f)

            prompt = generator.generate_prompt(args.category, args.template, context)
            print("=" * 80)
            print(f"CUSTOM PROMPT: {args.category}.{args.template}")
            print("=" * 80)
            print(prompt)

        else:
            print("Please specify a command. Use --help for available options.")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()