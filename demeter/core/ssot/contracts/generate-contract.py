#!/usr/bin/env python3
"""
Contract Generation Tool

Generate formal contracts from UoW definitions, Gherkin scenarios, or code annotations.
"""

import yaml
import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import re
from datetime import datetime

class ContractGenerator:
    def __init__(self, ssot_dir: Path, contracts_dir: Path):
        self.ssot_dir = ssot_dir
        self.contracts_dir = contracts_dir
        self.contracts_dir.mkdir(parents=True, exist_ok=True)

        # Load contract schema
        self.schema = self._load_contract_schema()

        # Load SSOT data
        self.ssot_data = self._load_ssot_data()

    def _load_contract_schema(self) -> Dict[str, Any]:
        """Load contract schema definition."""
        schema_file = self.contracts_dir / "contract-schema.yaml"
        if schema_file.exists():
            with open(schema_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}

    def _load_ssot_data(self) -> Dict[str, Any]:
        """Load all SSOT data files."""
        ssot_data = {}

        # Load framework requirements
        framework_file = self.ssot_dir / "framework-requirements.yaml"
        if framework_file.exists():
            ssot_data['framework_requirements'] = self._load_yaml_file(framework_file)

        # Load base files
        base_dir = self.ssot_dir / "base"
        if base_dir.exists():
            for yaml_file in base_dir.glob("*.yaml"):
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

        return None

    def generate_contract_from_uow(self, uow_id: str) -> Dict[str, Any]:
        """Generate contract from UoW definition."""
        uow_data = self.get_uow_by_id(uow_id)
        if not uow_data:
            raise ValueError(f"UoW {uow_id} not found")

        # Generate contract structure
        contract = {
            'contract_id': f"CTR-{uow_id.replace('UoW-', '').replace('-', '')}",
            'title': f"{uow_data.get('name', uow_id)} Contract",
            'description': f"Formal contract for {uow_data.get('goal', 'UoW operation')}",
            'applies_to': {
                'entity_type': 'uow',
                'entity_name': uow_id,
                'layer': uow_data.get('layer', 'Application')
            },
            'preconditions': self._generate_preconditions_from_uow(uow_data),
            'postconditions': self._generate_postconditions_from_uow(uow_data),
            'invariants': self._generate_invariants_from_uow(uow_data),
            'side_effects': self._generate_side_effects_from_uow(uow_data),
            'dependencies': self._generate_dependencies_from_uow(uow_data),
            'performance_guarantees': self._generate_performance_guarantees(uow_data),
            'security_constraints': self._generate_security_constraints(uow_data),
            'testing_requirements': self._generate_testing_requirements(uow_data),
            'metadata': {
                'created_by': 'SSOT Contract Generator',
                'created_date': datetime.now().strftime('%Y-%m-%d'),
                'version': '1.0.0',
                'status': 'draft',
                'related_uows': [uow_id],
                'related_frs': uow_data.get('implements', []),
                'related_nfrs': [impl for impl in uow_data.get('implements', []) if impl.startswith('NFR')]
            }
        }

        return contract

    def _generate_preconditions_from_uow(self, uow_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate preconditions from UoW data."""
        preconditions = []

        # From dependencies
        dependencies = uow_data.get('dependencies', [])
        if dependencies:
            preconditions.append({
                'condition_id': 'PRE-001',
                'description': 'All dependent UoWs must be completed',
                'predicate': f"forall dep in {dependencies}: dep.status eq 'completed'",
                'validation_method': 'check',
                'error_handling': {
                    'error_code': 'DEPENDENCIES_NOT_MET',
                    'error_message': 'Required dependencies are not completed',
                    'error_type': 'PreconditionError'
                }
            })

        # From layer constraints
        layer = uow_data.get('layer', '')
        if layer:
            preconditions.append({
                'condition_id': 'PRE-002',
                'description': f'{layer} layer services must be available',
                'predicate': f"{layer.lower()}_services_available eq true",
                'validation_method': 'check'
            })

        # From Gherkin Given clauses
        ac_data = uow_data.get('acceptance_criteria', {})
        if isinstance(ac_data, dict):
            counter = 3
            for ac_id, ac_info in ac_data.items():
                if isinstance(ac_info, dict) and 'scenario' in ac_info:
                    scenario = ac_info['scenario']
                    given = scenario.get('given', '')
                    if given:
                        preconditions.append({
                            'condition_id': f'PRE-{counter:03d}',
                            'description': f'Precondition from {ac_id}: {given}',
                            'predicate': self._convert_gherkin_to_predicate(given),
                            'validation_method': 'assert'
                        })
                        counter += 1

        return preconditions

    def _generate_postconditions_from_uow(self, uow_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate postconditions from UoW data."""
        postconditions = []

        # From Gherkin Then clauses
        ac_data = uow_data.get('acceptance_criteria', {})
        if isinstance(ac_data, dict):
            counter = 1
            for ac_id, ac_info in ac_data.items():
                if isinstance(ac_info, dict) and 'scenario' in ac_info:
                    scenario = ac_info['scenario']
                    then = scenario.get('then', '')
                    if then:
                        postconditions.append({
                            'condition_id': f'POST-{counter:03d}',
                            'description': f'Result from {ac_id}: {then}',
                            'predicate': self._convert_gherkin_to_predicate(then),
                            'validation_method': 'ensure',
                            'success_criteria': [then]
                        })

                        # Add And clauses
                        and_clauses = scenario.get('and', [])
                        for i, and_clause in enumerate(and_clauses):
                            counter += 1
                            postconditions.append({
                                'condition_id': f'POST-{counter:03d}',
                                'description': f'Additional condition from {ac_id}: {and_clause}',
                                'predicate': self._convert_gherkin_to_predicate(and_clause),
                                'validation_method': 'verify'
                            })
                        counter += 1

        # Default success postcondition
        if not postconditions:
            postconditions.append({
                'condition_id': 'POST-001',
                'description': 'Operation completes successfully',
                'predicate': 'result.status eq "success"',
                'validation_method': 'ensure'
            })

        return postconditions

    def _generate_invariants_from_uow(self, uow_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate invariants from UoW data."""
        invariants = []

        layer = uow_data.get('layer', '')

        # Layer-specific invariants
        if layer == 'Foundation':
            invariants.append({
                'invariant_id': 'INV-001',
                'description': 'System configuration remains valid',
                'predicate': 'valid(system_config)',
                'scope': 'global',
                'monitoring': {
                    'check_frequency': 'always',
                    'alert_on_violation': True
                }
            })

        if layer == 'Infrastructure':
            invariants.append({
                'invariant_id': 'INV-001',
                'description': 'Resource connections remain stable',
                'predicate': 'all_connections_healthy eq true',
                'scope': 'global',
                'monitoring': {
                    'check_frequency': 'periodic',
                    'alert_on_violation': True
                }
            })

        # Security invariant for all layers
        invariants.append({
            'invariant_id': 'INV-999',
            'description': 'Security context is maintained',
            'predicate': 'security_context_valid eq true',
            'scope': 'transaction',
            'monitoring': {
                'check_frequency': 'always',
                'alert_on_violation': True
            }
        })

        return invariants

    def _generate_side_effects_from_uow(self, uow_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate side effects from UoW data."""
        side_effects = []

        uow_name = uow_data.get('name', '').lower()

        # Infer side effects from name and description
        if any(keyword in uow_name for keyword in ['create', 'add', 'insert']):
            side_effects.append({
                'effect_id': 'EFF-001',
                'description': 'Creates new entity in system',
                'effect_type': 'state_change',
                'scope': 'entity_store',
                'reversible': True
            })

        if any(keyword in uow_name for keyword in ['update', 'modify', 'change']):
            side_effects.append({
                'effect_id': 'EFF-001',
                'description': 'Modifies existing entity state',
                'effect_type': 'state_change',
                'scope': 'entity_store',
                'reversible': True
            })

        if any(keyword in uow_name for keyword in ['delete', 'remove']):
            side_effects.append({
                'effect_id': 'EFF-001',
                'description': 'Removes entity from system',
                'effect_type': 'state_change',
                'scope': 'entity_store',
                'reversible': False
            })

        if any(keyword in uow_name for keyword in ['log', 'audit', 'track']):
            side_effects.append({
                'effect_id': 'EFF-002',
                'description': 'Records operation in audit log',
                'effect_type': 'io_operation',
                'scope': 'audit_log',
                'reversible': False
            })

        # Default side effect if none detected
        if not side_effects:
            side_effects.append({
                'effect_id': 'EFF-001',
                'description': 'Updates system state as specified in acceptance criteria',
                'effect_type': 'state_change',
                'scope': 'system_state',
                'reversible': True
            })

        return side_effects

    def _generate_dependencies_from_uow(self, uow_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate contract dependencies from UoW data."""
        dependencies = []

        uow_dependencies = uow_data.get('dependencies', [])
        for dep_uow in uow_dependencies:
            dependencies.append({
                'dependency_type': 'requires',
                'contract_id': f'{dep_uow}-CONTRACT',
                'description': f'Requires completion of {dep_uow}'
            })

        return dependencies

    def _generate_performance_guarantees(self, uow_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate performance guarantees based on UoW data."""
        layer = uow_data.get('layer', '')
        priority = uow_data.get('priority', '')

        guarantees = {}

        # Layer-based performance expectations
        if layer == 'Foundation':
            guarantees['max_execution_time'] = '100ms'
            guarantees['availability'] = '99.99%'
        elif layer == 'Infrastructure':
            guarantees['max_execution_time'] = '200ms'
            guarantees['availability'] = '99.9%'
        elif layer == 'Application':
            guarantees['max_execution_time'] = '500ms'
            guarantees['availability'] = '99.5%'

        # Priority-based adjustments
        if priority == 'Critical':
            guarantees['availability'] = '99.99%'
        elif priority == 'High':
            guarantees['availability'] = '99.9%'

        # Default complexity estimates
        guarantees['time_complexity'] = 'O(n)'
        guarantees['space_complexity'] = 'O(1)'

        return guarantees

    def _generate_security_constraints(self, uow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate security constraints from UoW data."""
        constraints = {
            'authentication_required': True,
            'authorization_rules': ['user.authenticated'],
            'data_classification': 'internal',
            'encryption_required': False,
            'audit_required': True
        }

        # Check for security-related NFRs
        implements = uow_data.get('implements', [])
        if any('NFR-003' in impl or 'security' in impl.lower() for impl in implements):
            constraints.update({
                'encryption_required': True,
                'data_classification': 'confidential',
                'authorization_rules': ['user.authenticated', 'user.authorized_for_operation']
            })

        return constraints

    def _generate_testing_requirements(self, uow_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate testing requirements from UoW data."""
        requirements = {
            'unit_tests': [
                'Test all preconditions',
                'Test all postconditions',
                'Test error handling scenarios'
            ],
            'integration_tests': [
                'Test with dependent UoWs',
                'Test with external services'
            ],
            'property_tests': [
                'Test contract invariants',
                'Test performance guarantees'
            ],
            'performance_tests': [
                'Load testing within performance limits',
                'Stress testing for error conditions'
            ]
        }

        # Add specific tests based on acceptance criteria
        ac_data = uow_data.get('acceptance_criteria', {})
        if isinstance(ac_data, dict):
            for ac_id, ac_info in ac_data.items():
                if isinstance(ac_info, dict):
                    description = ac_info.get('description', '')
                    requirements['unit_tests'].append(f'Test {ac_id}: {description}')

        return requirements

    def _convert_gherkin_to_predicate(self, gherkin_text: str) -> str:
        """Convert Gherkin text to CDL predicate (simplified conversion)."""
        # This is a simplified conversion - in practice, this would be more sophisticated
        text = gherkin_text.lower()

        # Simple pattern matching
        if '성공적으로' in text or 'successfully' in text:
            return 'result.status eq "success"'
        elif '오류' in text or 'error' in text:
            return 'defined(error_info)'
        elif '검증' in text or 'valid' in text:
            return 'valid(input_data)'
        elif '설정' in text or 'config' in text:
            return 'defined(configuration) and valid(configuration)'
        else:
            # Default predicate
            return 'operation_completed eq true'

    def save_contract(self, contract: Dict[str, Any], output_file: Path):
        """Save contract to YAML file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(contract, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"Contract saved: {output_file}")

    def validate_contract(self, contract: Dict[str, Any]) -> List[str]:
        """Validate contract against schema."""
        errors = []

        # Basic required field validation
        required_fields = ['contract_id', 'title', 'description', 'applies_to']
        for field in required_fields:
            if field not in contract:
                errors.append(f"Missing required field: {field}")

        # Validate contract_id pattern
        if 'contract_id' in contract:
            contract_id = contract['contract_id']
            if not re.match(r'^[A-Z]{2,4}-[0-9]{3,4}(-[A-Z0-9]{1,10})?$', contract_id):
                errors.append(f"Invalid contract_id format: {contract_id}")

        # Validate preconditions
        preconditions = contract.get('preconditions', [])
        used_pre_ids = set()
        for pre in preconditions:
            if 'condition_id' in pre:
                if pre['condition_id'] in used_pre_ids:
                    errors.append(f"Duplicate precondition ID: {pre['condition_id']}")
                used_pre_ids.add(pre['condition_id'])

        # Validate postconditions
        postconditions = contract.get('postconditions', [])
        used_post_ids = set()
        for post in postconditions:
            if 'condition_id' in post:
                if post['condition_id'] in used_post_ids:
                    errors.append(f"Duplicate postcondition ID: {post['condition_id']}")
                used_post_ids.add(post['condition_id'])

        return errors

    def generate_contract_report(self, contract: Dict[str, Any]) -> str:
        """Generate a human-readable contract report."""
        report = f"""
# Contract Report: {contract.get('title', 'Unknown')}

**Contract ID**: {contract.get('contract_id', 'N/A')}
**Description**: {contract.get('description', 'N/A')}

## Applies To
- **Entity Type**: {contract.get('applies_to', {}).get('entity_type', 'N/A')}
- **Entity Name**: {contract.get('applies_to', {}).get('entity_name', 'N/A')}
- **Layer**: {contract.get('applies_to', {}).get('layer', 'N/A')}

## Preconditions
"""
        for pre in contract.get('preconditions', []):
            report += f"- **{pre.get('condition_id')}**: {pre.get('description', 'N/A')}\n"
            report += f"  - Predicate: `{pre.get('predicate', 'N/A')}`\n"

        report += "\n## Postconditions\n"
        for post in contract.get('postconditions', []):
            report += f"- **{post.get('condition_id')}**: {post.get('description', 'N/A')}\n"
            report += f"  - Predicate: `{post.get('predicate', 'N/A')}`\n"

        report += "\n## Invariants\n"
        for inv in contract.get('invariants', []):
            report += f"- **{inv.get('invariant_id')}**: {inv.get('description', 'N/A')}\n"
            report += f"  - Predicate: `{inv.get('predicate', 'N/A')}`\n"
            report += f"  - Scope: {inv.get('scope', 'N/A')}\n"

        report += f"\n## Performance Guarantees\n"
        perf = contract.get('performance_guarantees', {})
        for key, value in perf.items():
            report += f"- **{key}**: {value}\n"

        report += f"\n## Security Constraints\n"
        sec = contract.get('security_constraints', {})
        for key, value in sec.items():
            report += f"- **{key}**: {value}\n"

        return report


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate formal contracts from SSOT data')
    parser.add_argument('--ssot-dir', type=str, default='./demeter/core/ssot',
                       help='SSOT directory path')
    parser.add_argument('--contracts-dir', type=str, default='./demeter/core/ssot/contracts',
                       help='Contracts output directory')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Generate contract from UoW
    uow_parser = subparsers.add_parser('from-uow', help='Generate contract from UoW')
    uow_parser.add_argument('--uow-id', required=True, help='UoW ID to generate contract for')
    uow_parser.add_argument('--output', help='Output file name')

    # Validate contract
    validate_parser = subparsers.add_parser('validate', help='Validate contract file')
    validate_parser.add_argument('--contract-file', required=True, help='Contract file to validate')

    # Generate report
    report_parser = subparsers.add_parser('report', help='Generate contract report')
    report_parser.add_argument('--contract-file', required=True, help='Contract file to report on')

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()

    ssot_dir = Path(args.ssot_dir).resolve()
    contracts_dir = Path(args.contracts_dir).resolve()

    if not ssot_dir.exists():
        print(f"Error: SSOT directory not found: {ssot_dir}")
        sys.exit(1)

    generator = ContractGenerator(ssot_dir, contracts_dir)

    try:
        if args.command == 'from-uow':
            contract = generator.generate_contract_from_uow(args.uow_id)

            # Validate contract
            errors = generator.validate_contract(contract)
            if errors:
                print("Contract validation errors:")
                for error in errors:
                    print(f"  - {error}")
                print()

            # Save contract
            output_file = contracts_dir / (args.output or f"{args.uow_id.lower()}-contract.yaml")
            generator.save_contract(contract, output_file)

            # Generate report
            report = generator.generate_contract_report(contract)
            report_file = output_file.with_suffix('.md')
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Contract report saved: {report_file}")

        elif args.command == 'validate':
            contract_file = Path(args.contract_file)
            if not contract_file.exists():
                print(f"Error: Contract file not found: {contract_file}")
                sys.exit(1)

            with open(contract_file, 'r', encoding='utf-8') as f:
                contract = yaml.safe_load(f)

            errors = generator.validate_contract(contract)
            if errors:
                print("Validation errors:")
                for error in errors:
                    print(f"  - {error}")
                sys.exit(1)
            else:
                print("Contract validation passed!")

        elif args.command == 'report':
            contract_file = Path(args.contract_file)
            if not contract_file.exists():
                print(f"Error: Contract file not found: {contract_file}")
                sys.exit(1)

            with open(contract_file, 'r', encoding='utf-8') as f:
                contract = yaml.safe_load(f)

            report = generator.generate_contract_report(contract)
            print(report)

        else:
            print("Please specify a command. Use --help for available options.")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()