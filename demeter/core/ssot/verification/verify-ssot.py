#!/usr/bin/env python3
"""
SSOT Verification Tool

Comprehensive verification of Single Source of Truth consistency, completeness,
and correctness across requirements, UoWs, contracts, and BDD scenarios.
"""

import yaml
import json
import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime
import re

class SSOTVerifier:
    def __init__(self, ssot_dir: Path, project_root: Path):
        self.ssot_dir = ssot_dir
        self.project_root = project_root

        # Load all SSOT data
        self.ssot_data = self._load_ssot_data()

        # Verification results
        self.verification_results = {
            'metadata': {
                'verification_date': datetime.now().isoformat(),
                'verifier_version': '1.0.0',
                'project_root': str(project_root),
                'ssot_dir': str(ssot_dir)
            },
            'summary': {
                'total_errors': 0,
                'total_warnings': 0,
                'total_checks': 0,
                'passed_checks': 0
            },
            'categories': {
                'structural_integrity': {'errors': [], 'warnings': []},
                'reference_consistency': {'errors': [], 'warnings': []},
                'requirement_completeness': {'errors': [], 'warnings': []},
                'uow_validation': {'errors': [], 'warnings': []},
                'contract_validation': {'errors': [], 'warnings': []},
                'bdd_validation': {'errors': [], 'warnings': []},
                'extension_compatibility': {'errors': [], 'warnings': []},
                'naming_conventions': {'errors': [], 'warnings': []},
                'dependency_validation': {'errors': [], 'warnings': []}
            }
        }

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

        # Load extension files
        extensions_dir = self.ssot_dir / "extensions"
        if extensions_dir.exists():
            ssot_data['extensions'] = {}
            for category_dir in extensions_dir.iterdir():
                if category_dir.is_dir():
                    ssot_data['extensions'][category_dir.name] = {}
                    for yaml_file in category_dir.glob("*.yaml"):
                        ssot_data['extensions'][category_dir.name][yaml_file.stem] = self._load_yaml_file(yaml_file)

        # Load contracts
        contracts_dir = self.ssot_dir / "contracts"
        if contracts_dir.exists():
            ssot_data['contracts'] = {}
            for yaml_file in contracts_dir.glob("*.yaml"):
                ssot_data['contracts'][yaml_file.stem] = self._load_yaml_file(yaml_file)

        # Load other SSOT files
        for yaml_file in self.ssot_dir.glob("*.yaml"):
            if yaml_file.name not in ["framework-requirements.yaml"]:
                ssot_data[yaml_file.stem] = self._load_yaml_file(yaml_file)

        return ssot_data

    def _load_yaml_file(self, file_path: Path) -> Dict[str, Any]:
        """Load a single YAML file with error handling."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            self._add_error('structural_integrity', f"YAML syntax error in {file_path}: {e}")
            return {}
        except Exception as e:
            self._add_error('structural_integrity', f"Cannot load {file_path}: {e}")
            return {}

    def _add_error(self, category: str, message: str, details: Optional[Dict[str, Any]] = None):
        """Add an error to verification results."""
        error_entry = {
            'message': message,
            'severity': 'error',
            'timestamp': datetime.now().isoformat()
        }
        if details:
            error_entry['details'] = details

        self.verification_results['categories'][category]['errors'].append(error_entry)
        self.verification_results['summary']['total_errors'] += 1

    def _add_warning(self, category: str, message: str, details: Optional[Dict[str, Any]] = None):
        """Add a warning to verification results."""
        warning_entry = {
            'message': message,
            'severity': 'warning',
            'timestamp': datetime.now().isoformat()
        }
        if details:
            warning_entry['details'] = details

        self.verification_results['categories'][category]['warnings'].append(warning_entry)
        self.verification_results['summary']['total_warnings'] += 1

    def _increment_check(self, passed: bool = True):
        """Increment check counters."""
        self.verification_results['summary']['total_checks'] += 1
        if passed:
            self.verification_results['summary']['passed_checks'] += 1

    def verify_structural_integrity(self):
        """Verify structural integrity of SSOT files."""
        print("🏗️  Verifying structural integrity...")

        # Check required SSOT files exist
        required_files = [
            'framework-requirements.yaml',
            'base/fr-base.yaml',
            'base/nfr-base.yaml',
            'base/uow-base.yaml'
        ]

        for req_file in required_files:
            file_path = self.ssot_dir / req_file
            if not file_path.exists():
                self._add_error('structural_integrity', f"Required SSOT file missing: {req_file}")
            self._increment_check(file_path.exists())

        # Check required sections in framework requirements
        if 'framework_requirements' in self.ssot_data:
            fr_data = self.ssot_data['framework_requirements']
            required_sections = ['functional_requirements', 'non_functional_requirements', 'units_of_work']

            for section in required_sections:
                if section not in fr_data:
                    self._add_error('structural_integrity', f"Missing required section '{section}' in framework-requirements.yaml")
                self._increment_check(section in fr_data)
        else:
            self._add_error('structural_integrity', "Framework requirements file not loaded")
            self._increment_check(False)

        # Validate YAML structure consistency
        for file_name, data in self.ssot_data.items():
            if not isinstance(data, dict):
                self._add_error('structural_integrity', f"Invalid YAML structure in {file_name}: expected dictionary at root level")
                self._increment_check(False)
            else:
                self._increment_check(True)

    def verify_reference_consistency(self):
        """Verify consistency of cross-references between SSOT entities."""
        print("🔗 Verifying reference consistency...")

        # Collect all entity IDs
        all_fr_ids = set()
        all_nfr_ids = set()
        all_uow_ids = set()

        # From framework requirements
        if 'framework_requirements' in self.ssot_data:
            fr_data = self.ssot_data['framework_requirements']
            all_fr_ids.update(fr_data.get('functional_requirements', {}).keys())
            all_nfr_ids.update(fr_data.get('non_functional_requirements', {}).keys())
            all_uow_ids.update(fr_data.get('units_of_work', {}).keys())

        # From base files
        if 'fr-base' in self.ssot_data:
            all_fr_ids.update(self.ssot_data['fr-base'].get('functional_requirements', {}).keys())

        if 'nfr-base' in self.ssot_data:
            all_nfr_ids.update(self.ssot_data['nfr-base'].get('non_functional_requirements', {}).keys())

        if 'uow-base' in self.ssot_data:
            all_uow_ids.update(self.ssot_data['uow-base'].get('units_of_work', {}).keys())

        # From extensions
        if 'extensions' in self.ssot_data:
            for category, extensions in self.ssot_data['extensions'].items():
                for extension_name, extension_data in extensions.items():
                    all_fr_ids.update(extension_data.get('functional_requirements', {}).keys())
                    all_nfr_ids.update(extension_data.get('non_functional_requirements', {}).keys())
                    all_uow_ids.update(extension_data.get('units_of_work', {}).keys())

        # Check UoW dependencies
        for source, data in self.ssot_data.items():
            if isinstance(data, dict) and 'units_of_work' in data:
                for uow_id, uow_data in data['units_of_work'].items():
                    # Check dependency references
                    dependencies = uow_data.get('dependencies', [])
                    for dep_id in dependencies:
                        if dep_id not in all_uow_ids:
                            self._add_error('reference_consistency',
                                          f"UoW {uow_id} references non-existent dependency: {dep_id}",
                                          {'source_file': source, 'uow_id': uow_id, 'invalid_reference': dep_id})
                        self._increment_check(dep_id in all_uow_ids)

                    # Check implements references
                    implements = uow_data.get('implements', [])
                    for impl_id in implements:
                        valid_reference = (impl_id in all_fr_ids) or (impl_id in all_nfr_ids)
                        if not valid_reference:
                            self._add_error('reference_consistency',
                                          f"UoW {uow_id} implements non-existent requirement: {impl_id}",
                                          {'source_file': source, 'uow_id': uow_id, 'invalid_reference': impl_id})
                        self._increment_check(valid_reference)

    def verify_requirement_completeness(self):
        """Verify completeness of requirements definitions."""
        print("📋 Verifying requirement completeness...")

        # Check functional requirements completeness
        for source, data in self.ssot_data.items():
            if isinstance(data, dict) and 'functional_requirements' in data:
                for fr_id, fr_data in data['functional_requirements'].items():
                    self._check_requirement_completeness('functional', fr_id, fr_data, source)

        # Check non-functional requirements completeness
        for source, data in self.ssot_data.items():
            if isinstance(data, dict) and 'non_functional_requirements' in data:
                for nfr_id, nfr_data in data['non_functional_requirements'].items():
                    self._check_requirement_completeness('non_functional', nfr_id, nfr_data, source)

    def _check_requirement_completeness(self, req_type: str, req_id: str, req_data: Dict[str, Any], source: str):
        """Check completeness of a single requirement."""
        required_fields = ['title', 'description', 'priority']

        for field in required_fields:
            if field not in req_data or not req_data[field]:
                self._add_error('requirement_completeness',
                              f"{req_type.title()} requirement {req_id} missing required field: {field}",
                              {'source_file': source, 'requirement_id': req_id, 'missing_field': field})
            self._increment_check(field in req_data and req_data[field])

        # Check priority values
        valid_priorities = ['Critical', 'High', 'Medium', 'Low']
        priority = req_data.get('priority', '')
        if priority and priority not in valid_priorities:
            self._add_warning('requirement_completeness',
                            f"{req_type.title()} requirement {req_id} has invalid priority: {priority}",
                            {'source_file': source, 'requirement_id': req_id, 'invalid_priority': priority})

        # NFR-specific checks
        if req_type == 'non_functional':
            if 'requirements' not in req_data or not req_data['requirements']:
                self._add_warning('requirement_completeness',
                                f"NFR {req_id} should have specific requirements list",
                                {'source_file': source, 'requirement_id': req_id})

            if 'measurement' not in req_data or not req_data['measurement']:
                self._add_warning('requirement_completeness',
                                f"NFR {req_id} should have measurement criteria",
                                {'source_file': source, 'requirement_id': req_id})

    def verify_uow_validation(self):
        """Verify Units of Work definitions."""
        print("⚙️  Verifying UoW definitions...")

        for source, data in self.ssot_data.items():
            if isinstance(data, dict) and 'units_of_work' in data:
                for uow_id, uow_data in data['units_of_work'].items():
                    self._check_uow_completeness(uow_id, uow_data, source)
                    self._check_uow_gherkin_scenarios(uow_id, uow_data, source)

    def _check_uow_completeness(self, uow_id: str, uow_data: Dict[str, Any], source: str):
        """Check completeness of a UoW definition."""
        required_fields = ['name', 'goal', 'layer', 'priority', 'acceptance_criteria']

        for field in required_fields:
            if field not in uow_data or not uow_data[field]:
                self._add_error('uow_validation',
                              f"UoW {uow_id} missing required field: {field}",
                              {'source_file': source, 'uow_id': uow_id, 'missing_field': field})
            self._increment_check(field in uow_data and uow_data[field])

        # Check layer values
        valid_layers = ['Foundation', 'Infrastructure', 'Application', 'Deployment']
        layer = uow_data.get('layer', '')
        if layer and layer not in valid_layers:
            self._add_error('uow_validation',
                          f"UoW {uow_id} has invalid layer: {layer}",
                          {'source_file': source, 'uow_id': uow_id, 'invalid_layer': layer})

        # Check priority values
        valid_priorities = ['Critical', 'High', 'Medium', 'Low']
        priority = uow_data.get('priority', '')
        if priority and priority not in valid_priorities:
            self._add_error('uow_validation',
                          f"UoW {uow_id} has invalid priority: {priority}",
                          {'source_file': source, 'uow_id': uow_id, 'invalid_priority': priority})

    def _check_uow_gherkin_scenarios(self, uow_id: str, uow_data: Dict[str, Any], source: str):
        """Check Gherkin scenarios in UoW acceptance criteria."""
        ac_data = uow_data.get('acceptance_criteria', {})

        if isinstance(ac_data, dict):
            for ac_id, ac_info in ac_data.items():
                if isinstance(ac_info, dict) and 'scenario' in ac_info:
                    scenario = ac_info['scenario']
                    self._validate_gherkin_scenario(uow_id, ac_id, scenario, source)

    def _validate_gherkin_scenario(self, uow_id: str, ac_id: str, scenario: Dict[str, Any], source: str):
        """Validate a Gherkin scenario structure."""
        required_gherkin_fields = ['given', 'when', 'then']

        for field in required_gherkin_fields:
            if field not in scenario or not scenario[field]:
                self._add_error('bdd_validation',
                              f"UoW {uow_id}, AC {ac_id}: Missing Gherkin {field} clause",
                              {'source_file': source, 'uow_id': uow_id, 'ac_id': ac_id, 'missing_field': field})
            self._increment_check(field in scenario and scenario[field])

        # Check for common Gherkin anti-patterns
        given_text = scenario.get('given', '').lower()
        when_text = scenario.get('when', '').lower()
        then_text = scenario.get('then', '').lower()

        # Given should not contain "when" or "then"
        if 'when' in given_text or 'then' in given_text:
            self._add_warning('bdd_validation',
                            f"UoW {uow_id}, AC {ac_id}: Given clause should not contain 'when' or 'then'",
                            {'source_file': source, 'uow_id': uow_id, 'ac_id': ac_id})

        # When should be action-oriented
        if not any(verb in when_text for verb in ['실행', '수행', '처리', '요청', 'execute', 'perform', 'process', 'request']):
            self._add_warning('bdd_validation',
                            f"UoW {uow_id}, AC {ac_id}: When clause should describe an action",
                            {'source_file': source, 'uow_id': uow_id, 'ac_id': ac_id})

        # Then should be observable outcome
        if not any(word in then_text for word in ['되어야', 'should', 'must', '한다', '된다']):
            self._add_warning('bdd_validation',
                            f"UoW {uow_id}, AC {ac_id}: Then clause should describe observable outcome",
                            {'source_file': source, 'uow_id': uow_id, 'ac_id': ac_id})

    def verify_contract_validation(self):
        """Verify contract definitions."""
        print("📜 Verifying contract definitions...")

        if 'contracts' in self.ssot_data:
            for contract_file, contract_data in self.ssot_data['contracts'].items():
                self._validate_contract_structure(contract_file, contract_data)
                self._validate_contract_predicates(contract_file, contract_data)

    def _validate_contract_structure(self, contract_file: str, contract_data: Dict[str, Any]):
        """Validate contract structure."""
        required_fields = ['contract_id', 'title', 'description', 'applies_to']

        for field in required_fields:
            if field not in contract_data:
                self._add_error('contract_validation',
                              f"Contract {contract_file} missing required field: {field}",
                              {'contract_file': contract_file, 'missing_field': field})
            self._increment_check(field in contract_data)

        # Validate contract_id format
        contract_id = contract_data.get('contract_id', '')
        if contract_id and not re.match(r'^[A-Z]{2,4}-[0-9]{3,4}(-[A-Z0-9]{1,10})?$', contract_id):
            self._add_error('contract_validation',
                          f"Contract {contract_file} has invalid contract_id format: {contract_id}",
                          {'contract_file': contract_file, 'invalid_id': contract_id})

        # Check for duplicate condition IDs
        self._check_duplicate_condition_ids(contract_file, contract_data, 'preconditions', 'PRE-')
        self._check_duplicate_condition_ids(contract_file, contract_data, 'postconditions', 'POST-')
        self._check_duplicate_condition_ids(contract_file, contract_data, 'invariants', 'INV-')

    def _check_duplicate_condition_ids(self, contract_file: str, contract_data: Dict[str, Any],
                                     section: str, prefix: str):
        """Check for duplicate condition IDs in a contract section."""
        conditions = contract_data.get(section, [])
        seen_ids = set()

        for condition in conditions:
            if isinstance(condition, dict):
                condition_id = condition.get('condition_id') or condition.get('invariant_id')
                if condition_id:
                    if condition_id in seen_ids:
                        self._add_error('contract_validation',
                                      f"Contract {contract_file} has duplicate {section} ID: {condition_id}",
                                      {'contract_file': contract_file, 'duplicate_id': condition_id})
                    else:
                        seen_ids.add(condition_id)
                        self._increment_check(True)

    def _validate_contract_predicates(self, contract_file: str, contract_data: Dict[str, Any]):
        """Validate contract predicates syntax."""
        # This is a simplified validation - in practice, this would parse CDL syntax
        predicate_sections = ['preconditions', 'postconditions', 'invariants']

        for section in predicate_sections:
            conditions = contract_data.get(section, [])
            for condition in conditions:
                if isinstance(condition, dict) and 'predicate' in condition:
                    predicate = condition['predicate']
                    if not predicate or not isinstance(predicate, str):
                        self._add_error('contract_validation',
                                      f"Contract {contract_file} has empty or invalid predicate in {section}",
                                      {'contract_file': contract_file, 'section': section})
                    self._increment_check(predicate and isinstance(predicate, str))

    def verify_extension_compatibility(self):
        """Verify extension compatibility and conflicts."""
        print("🔧 Verifying extension compatibility...")

        # Load compatibility matrix
        compatibility_file = self.ssot_dir / "compatibility-matrix.yaml"
        if not compatibility_file.exists():
            self._add_warning('extension_compatibility', "Compatibility matrix file not found")
            return

        compatibility_data = self._load_yaml_file(compatibility_file)

        # Check domain extension conflicts
        domain_conflicts = compatibility_data.get('domain_extensions', {})
        active_extensions = self._get_active_extensions()

        for domain, rules in domain_conflicts.items():
            if domain in active_extensions['domain']:
                conflicts = rules.get('conflicts', [])
                for conflict in conflicts:
                    if conflict in active_extensions['features']:
                        self._add_error('extension_compatibility',
                                      f"Domain extension '{domain}' conflicts with feature extension '{conflict}'",
                                      {'domain': domain, 'conflicting_feature': conflict})

        # Check required dependencies
        for domain, rules in domain_conflicts.items():
            if domain in active_extensions['domain']:
                requires = rules.get('requires', [])
                for requirement in requires:
                    if requirement not in active_extensions['compliance']:
                        self._add_error('extension_compatibility',
                                      f"Domain extension '{domain}' requires compliance extension '{requirement}'",
                                      {'domain': domain, 'missing_requirement': requirement})

    def _get_active_extensions(self) -> Dict[str, List[str]]:
        """Get list of active extensions."""
        active_extensions = {
            'domain': [],
            'features': [],
            'compliance': []
        }

        if 'extensions' in self.ssot_data:
            for category, extensions in self.ssot_data['extensions'].items():
                for extension_name in extensions.keys():
                    if category in active_extensions:
                        active_extensions[category].append(extension_name)

        return active_extensions

    def verify_naming_conventions(self):
        """Verify naming conventions across SSOT."""
        print("📝 Verifying naming conventions...")

        # Check FR naming convention (FR-XXX)
        for source, data in self.ssot_data.items():
            if isinstance(data, dict) and 'functional_requirements' in data:
                for fr_id in data['functional_requirements'].keys():
                    if not re.match(r'^FR-[0-9]{3}$', fr_id):
                        self._add_error('naming_conventions',
                                      f"Functional requirement ID '{fr_id}' doesn't follow FR-XXX convention",
                                      {'source_file': source, 'invalid_id': fr_id})
                    self._increment_check(re.match(r'^FR-[0-9]{3}$', fr_id) is not None)

        # Check NFR naming convention (NFR-XXX)
        for source, data in self.ssot_data.items():
            if isinstance(data, dict) and 'non_functional_requirements' in data:
                for nfr_id in data['non_functional_requirements'].keys():
                    if not re.match(r'^NFR-[0-9]{3}$', nfr_id):
                        self._add_error('naming_conventions',
                                      f"Non-functional requirement ID '{nfr_id}' doesn't follow NFR-XXX convention",
                                      {'source_file': source, 'invalid_id': nfr_id})
                    self._increment_check(re.match(r'^NFR-[0-9]{3}$', nfr_id) is not None)

        # Check UoW naming convention (UoW-XXX or UoW-XXXX)
        for source, data in self.ssot_data.items():
            if isinstance(data, dict) and 'units_of_work' in data:
                for uow_id in data['units_of_work'].keys():
                    if not re.match(r'^UoW-[0-9A-Z]{3,4}[A-Z]?$', uow_id):
                        self._add_error('naming_conventions',
                                      f"UoW ID '{uow_id}' doesn't follow UoW-XXX convention",
                                      {'source_file': source, 'invalid_id': uow_id})
                    self._increment_check(re.match(r'^UoW-[0-9A-Z]{3,4}[A-Z]?$', uow_id) is not None)

    def verify_dependency_validation(self):
        """Verify dependency relationships and detect cycles."""
        print("🔄 Verifying dependency relationships...")

        # Build dependency graph
        dependency_graph = {}
        all_uow_ids = set()

        for source, data in self.ssot_data.items():
            if isinstance(data, dict) and 'units_of_work' in data:
                for uow_id, uow_data in data['units_of_work'].items():
                    all_uow_ids.add(uow_id)
                    dependencies = uow_data.get('dependencies', [])
                    dependency_graph[uow_id] = dependencies

        # Check for circular dependencies
        for uow_id in all_uow_ids:
            if self._has_circular_dependency(uow_id, dependency_graph, set()):
                self._add_error('dependency_validation',
                              f"Circular dependency detected involving UoW: {uow_id}",
                              {'uow_id': uow_id})
            else:
                self._increment_check(True)

        # Check for orphaned UoWs (no dependents)
        all_dependencies = set()
        for deps in dependency_graph.values():
            all_dependencies.update(deps)

        roots = all_uow_ids - all_dependencies
        if len(roots) > 5:  # Threshold for too many root UoWs
            self._add_warning('dependency_validation',
                            f"Many root UoWs detected ({len(roots)}). Consider if dependencies are missing.",
                            {'root_uows': list(roots)})

    def _has_circular_dependency(self, uow_id: str, graph: Dict[str, List[str]], visited: Set[str]) -> bool:
        """Check if a UoW has circular dependencies."""
        if uow_id in visited:
            return True

        visited.add(uow_id)
        dependencies = graph.get(uow_id, [])

        for dep in dependencies:
            if self._has_circular_dependency(dep, graph, visited):
                return True

        visited.remove(uow_id)
        return False

    def run_verification(self) -> Dict[str, Any]:
        """Run all verification checks."""
        print("🔍 Starting SSOT verification...")

        self.verify_structural_integrity()
        self.verify_reference_consistency()
        self.verify_requirement_completeness()
        self.verify_uow_validation()
        self.verify_contract_validation()
        self.verify_extension_compatibility()
        self.verify_naming_conventions()
        self.verify_dependency_validation()

        # Calculate success rate
        total_checks = self.verification_results['summary']['total_checks']
        passed_checks = self.verification_results['summary']['passed_checks']
        success_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        self.verification_results['summary']['success_rate'] = success_rate

        print(f"\n✅ Verification completed!")
        print(f"📊 Summary: {passed_checks}/{total_checks} checks passed ({success_rate:.1f}%)")
        print(f"❌ Errors: {self.verification_results['summary']['total_errors']}")
        print(f"⚠️  Warnings: {self.verification_results['summary']['total_warnings']}")

        return self.verification_results

    def save_results(self, output_file: Path):
        """Save verification results to JSON file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.verification_results, f, indent=2, ensure_ascii=False)
        print(f"📄 Verification results saved: {output_file}")

    def generate_html_report(self, output_file: Path):
        """Generate HTML verification report."""
        summary = self.verification_results['summary']
        categories = self.verification_results['categories']

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SSOT Verification Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .summary {{ display: flex; gap: 20px; margin-bottom: 20px; }}
        .metric-card {{ background-color: #e8f4fd; padding: 15px; border-radius: 5px; flex: 1; text-align: center; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #0066cc; }}
        .error {{ color: #dc3545; }}
        .warning {{ color: #ffc107; }}
        .success {{ color: #28a745; }}
        .category {{ margin-bottom: 30px; }}
        .category h3 {{ color: #333; border-bottom: 2px solid #0066cc; padding-bottom: 5px; }}
        .issue-item {{ margin-bottom: 10px; padding: 10px; border-left: 4px solid; }}
        .issue-error {{ border-left-color: #dc3545; background-color: #f8d7da; }}
        .issue-warning {{ border-left-color: #ffc107; background-color: #fff3cd; }}
        .details {{ font-size: 0.9em; color: #666; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 SSOT Verification Report</h1>
        <p><strong>Generated:</strong> {self.verification_results['metadata']['verification_date']}</p>
        <p><strong>Project:</strong> {self.verification_results['metadata']['project_root']}</p>
    </div>

    <div class="summary">
        <div class="metric-card">
            <h3>Success Rate</h3>
            <div class="metric-value {'success' if summary['success_rate'] >= 90 else 'warning' if summary['success_rate'] >= 70 else 'error'}">{summary['success_rate']:.1f}%</div>
            <p>{summary['passed_checks']}/{summary['total_checks']} checks passed</p>
        </div>
        <div class="metric-card">
            <h3>Errors</h3>
            <div class="metric-value error">{summary['total_errors']}</div>
            <p>Critical issues found</p>
        </div>
        <div class="metric-card">
            <h3>Warnings</h3>
            <div class="metric-value warning">{summary['total_warnings']}</div>
            <p>Potential issues found</p>
        </div>
    </div>
"""

        # Add category details
        for category_name, category_data in categories.items():
            errors = category_data['errors']
            warnings = category_data['warnings']

            if errors or warnings:
                html_content += f"""
    <div class="category">
        <h3>{category_name.replace('_', ' ').title()}</h3>
"""

                for error in errors:
                    html_content += f"""
        <div class="issue-item issue-error">
            <strong>❌ Error:</strong> {error['message']}
            {f'<div class="details">Details: {error.get("details", {})}</div>' if error.get('details') else ''}
        </div>
"""

                for warning in warnings:
                    html_content += f"""
        <div class="issue-item issue-warning">
            <strong>⚠️ Warning:</strong> {warning['message']}
            {f'<div class="details">Details: {warning.get("details", {})}</div>' if warning.get('details') else ''}
        </div>
"""

                html_content += """
    </div>
"""

        html_content += """
</body>
</html>
"""

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"📊 HTML report saved: {output_file}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Verify SSOT consistency and completeness')
    parser.add_argument('--ssot-dir', type=str, default='./demeter/core/ssot',
                       help='SSOT directory path')
    parser.add_argument('--project-root', type=str, default='.',
                       help='Project root directory')
    parser.add_argument('--output', type=str, default='./ssot-verification.json',
                       help='Output JSON file path')
    parser.add_argument('--html-report', type=str, default='./ssot-verification.html',
                       help='HTML report output path')
    parser.add_argument('--fail-on-error', action='store_true',
                       help='Exit with error code if verification fails')

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()

    ssot_dir = Path(args.ssot_dir).resolve()
    project_root = Path(args.project_root).resolve()

    if not ssot_dir.exists():
        print(f"Error: SSOT directory not found: {ssot_dir}")
        sys.exit(1)

    verifier = SSOTVerifier(ssot_dir, project_root)

    try:
        results = verifier.run_verification()

        # Save results
        output_file = Path(args.output)
        verifier.save_results(output_file)

        # Generate HTML report
        html_report_file = Path(args.html_report)
        verifier.generate_html_report(html_report_file)

        # Exit with error if requested and verification failed
        if args.fail_on_error and (results['summary']['total_errors'] > 0):
            print(f"\n💥 Verification failed with {results['summary']['total_errors']} errors!")
            sys.exit(1)

        print(f"\n🎉 Verification process completed successfully!")

    except Exception as e:
        print(f"Error during verification: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()