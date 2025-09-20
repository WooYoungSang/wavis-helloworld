#!/usr/bin/env python3
"""
Traceability Matrix Generator

Generate comprehensive traceability matrix linking requirements, UoWs, contracts,
BDD scenarios, and implementation artifacts.
"""

import yaml
import json
import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
import re

class TraceabilityMatrixGenerator:
    def __init__(self, ssot_dir: Path, project_root: Path):
        self.ssot_dir = ssot_dir
        self.project_root = project_root

        # Load all SSOT data
        self.ssot_data = self._load_ssot_data()

        # Initialize traceability data structures
        self.traceability_matrix = {
            'metadata': {
                'generated_date': datetime.now().isoformat(),
                'generator_version': '1.0.0',
                'project_root': str(project_root),
                'ssot_dir': str(ssot_dir)
            },
            'requirements': {},
            'units_of_work': {},
            'contracts': {},
            'bdd_scenarios': {},
            'implementation_artifacts': {},
            'relationships': {
                'fr_to_uow': {},
                'nfr_to_uow': {},
                'uow_to_contract': {},
                'uow_to_bdd': {},
                'uow_to_implementation': {},
                'contract_to_bdd': {},
                'bdd_to_implementation': {}
            },
            'coverage_metrics': {},
            'gaps': []
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

        # Load BDD features
        features_dir = self.project_root / "features"
        if features_dir.exists():
            ssot_data['bdd_features'] = {}
            for feature_file in features_dir.glob("*.feature"):
                ssot_data['bdd_features'][feature_file.stem] = self._parse_feature_file(feature_file)

        return ssot_data

    def _load_yaml_file(self, file_path: Path) -> Dict[str, Any]:
        """Load a single YAML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load {file_path}: {e}")
            return {}

    def _parse_feature_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse Gherkin feature file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            feature_info = {
                'file_path': str(file_path),
                'scenarios': [],
                'tags': []
            }

            # Extract feature title
            feature_match = re.search(r'^Feature:\s*(.+)$', content, re.MULTILINE)
            if feature_match:
                feature_info['title'] = feature_match.group(1).strip()

            # Extract scenarios
            scenario_pattern = r'Scenario:\s*(.+?)(?=\n\s*Scenario:|\n\s*@|\n\s*#|$)'
            scenarios = re.findall(scenario_pattern, content, re.DOTALL | re.MULTILINE)

            for i, scenario_content in enumerate(scenarios):
                scenario_info = {
                    'name': scenario_content.split('\n')[0].strip(),
                    'steps': [],
                    'tags': []
                }

                # Extract steps
                steps = re.findall(r'^\s*(Given|When|Then|And)\s+(.+)$', scenario_content, re.MULTILINE)
                for step_type, step_text in steps:
                    scenario_info['steps'].append({
                        'type': step_type,
                        'text': step_text.strip()
                    })

                feature_info['scenarios'].append(scenario_info)

            # Extract tags
            tags = re.findall(r'@(\w+)', content)
            feature_info['tags'] = list(set(tags))

            return feature_info

        except Exception as e:
            print(f"Warning: Could not parse feature file {file_path}: {e}")
            return {'file_path': str(file_path), 'scenarios': [], 'tags': []}

    def extract_requirements(self):
        """Extract and catalog all requirements."""
        # Extract Functional Requirements
        if 'framework_requirements' in self.ssot_data:
            fr_data = self.ssot_data['framework_requirements'].get('functional_requirements', {})
            for fr_id, fr_info in fr_data.items():
                self.traceability_matrix['requirements'][fr_id] = {
                    'type': 'functional',
                    'title': fr_info.get('title', fr_id),
                    'description': fr_info.get('description', ''),
                    'category': fr_info.get('category', 'General'),
                    'priority': fr_info.get('priority', 'Medium'),
                    'source_file': 'framework-requirements.yaml'
                }

        # Extract Non-Functional Requirements
        if 'framework_requirements' in self.ssot_data:
            nfr_data = self.ssot_data['framework_requirements'].get('non_functional_requirements', {})
            for nfr_id, nfr_info in nfr_data.items():
                self.traceability_matrix['requirements'][nfr_id] = {
                    'type': 'non_functional',
                    'title': nfr_info.get('title', nfr_id),
                    'description': nfr_info.get('description', ''),
                    'category': nfr_info.get('category', 'Quality'),
                    'priority': nfr_info.get('priority', 'Medium'),
                    'requirements': nfr_info.get('requirements', []),
                    'source_file': 'framework-requirements.yaml'
                }

        # Extract requirements from base files
        if 'fr-base' in self.ssot_data:
            fr_base_data = self.ssot_data['fr-base'].get('functional_requirements', {})
            for fr_id, fr_info in fr_base_data.items():
                if fr_id not in self.traceability_matrix['requirements']:
                    self.traceability_matrix['requirements'][fr_id] = {
                        'type': 'functional',
                        'title': fr_info.get('title', fr_id),
                        'description': fr_info.get('description', ''),
                        'category': fr_info.get('category', 'General'),
                        'priority': fr_info.get('priority', 'Medium'),
                        'source_file': 'base/fr-base.yaml'
                    }

        if 'nfr-base' in self.ssot_data:
            nfr_base_data = self.ssot_data['nfr-base'].get('non_functional_requirements', {})
            for nfr_id, nfr_info in nfr_base_data.items():
                if nfr_id not in self.traceability_matrix['requirements']:
                    self.traceability_matrix['requirements'][nfr_id] = {
                        'type': 'non_functional',
                        'title': nfr_info.get('title', nfr_id),
                        'description': nfr_info.get('description', ''),
                        'category': nfr_info.get('category', 'Quality'),
                        'priority': nfr_info.get('priority', 'Medium'),
                        'requirements': nfr_info.get('requirements', []),
                        'source_file': 'base/nfr-base.yaml'
                    }

    def extract_units_of_work(self):
        """Extract and catalog all Units of Work."""
        # From framework requirements
        if 'framework_requirements' in self.ssot_data:
            uow_data = self.ssot_data['framework_requirements'].get('units_of_work', {})
            for uow_id, uow_info in uow_data.items():
                self.traceability_matrix['units_of_work'][uow_id] = {
                    'name': uow_info.get('name', uow_id),
                    'goal': uow_info.get('goal', ''),
                    'layer': uow_info.get('layer', ''),
                    'priority': uow_info.get('priority', ''),
                    'dependencies': uow_info.get('dependencies', []),
                    'implements': uow_info.get('implements', []),
                    'estimated_effort_hours': uow_info.get('estimated_effort_hours', ''),
                    'acceptance_criteria': uow_info.get('acceptance_criteria', {}),
                    'tags': uow_info.get('tags', []),
                    'source_file': 'framework-requirements.yaml'
                }

        # From base UoW file
        if 'uow-base' in self.ssot_data:
            uow_base_data = self.ssot_data['uow-base'].get('units_of_work', {})
            for uow_id, uow_info in uow_base_data.items():
                if uow_id not in self.traceability_matrix['units_of_work']:
                    self.traceability_matrix['units_of_work'][uow_id] = {
                        'name': uow_info.get('name', uow_id),
                        'goal': uow_info.get('goal', ''),
                        'layer': uow_info.get('layer', ''),
                        'priority': uow_info.get('priority', ''),
                        'dependencies': uow_info.get('dependencies', []),
                        'implements': uow_info.get('implements', []),
                        'estimated_effort_hours': uow_info.get('estimated_effort_hours', ''),
                        'acceptance_criteria': uow_info.get('acceptance_criteria', {}),
                        'tags': uow_info.get('tags', []),
                        'source_file': 'base/uow-base.yaml'
                    }

        # From extensions
        if 'extensions' in self.ssot_data:
            for category, extensions in self.ssot_data['extensions'].items():
                for extension_name, extension_data in extensions.items():
                    if 'units_of_work' in extension_data:
                        for uow_id, uow_info in extension_data['units_of_work'].items():
                            if uow_id not in self.traceability_matrix['units_of_work']:
                                self.traceability_matrix['units_of_work'][uow_id] = {
                                    'name': uow_info.get('name', uow_id),
                                    'goal': uow_info.get('goal', ''),
                                    'layer': uow_info.get('layer', ''),
                                    'priority': uow_info.get('priority', ''),
                                    'dependencies': uow_info.get('dependencies', []),
                                    'implements': uow_info.get('implements', []),
                                    'estimated_effort_hours': uow_info.get('estimated_effort_hours', ''),
                                    'acceptance_criteria': uow_info.get('acceptance_criteria', {}),
                                    'tags': uow_info.get('tags', []),
                                    'extension_category': category,
                                    'extension_name': extension_name,
                                    'source_file': f'extensions/{category}/{extension_name}.yaml'
                                }

    def extract_contracts(self):
        """Extract and catalog all contracts."""
        if 'contracts' in self.ssot_data:
            for contract_file, contract_data in self.ssot_data['contracts'].items():
                if 'contract_id' in contract_data:
                    contract_id = contract_data['contract_id']
                    self.traceability_matrix['contracts'][contract_id] = {
                        'title': contract_data.get('title', contract_id),
                        'description': contract_data.get('description', ''),
                        'applies_to': contract_data.get('applies_to', {}),
                        'preconditions': contract_data.get('preconditions', []),
                        'postconditions': contract_data.get('postconditions', []),
                        'invariants': contract_data.get('invariants', []),
                        'side_effects': contract_data.get('side_effects', []),
                        'performance_guarantees': contract_data.get('performance_guarantees', {}),
                        'security_constraints': contract_data.get('security_constraints', {}),
                        'source_file': f'contracts/{contract_file}.yaml'
                    }

    def extract_bdd_scenarios(self):
        """Extract and catalog all BDD scenarios."""
        if 'bdd_features' in self.ssot_data:
            for feature_file, feature_data in self.ssot_data['bdd_features'].items():
                feature_id = f"FEATURE-{feature_file.upper().replace('_', '-')}"

                self.traceability_matrix['bdd_scenarios'][feature_id] = {
                    'title': feature_data.get('title', feature_file),
                    'file_path': feature_data.get('file_path', ''),
                    'tags': feature_data.get('tags', []),
                    'scenarios': []
                }

                for i, scenario in enumerate(feature_data.get('scenarios', [])):
                    scenario_id = f"{feature_id}-SCENARIO-{i+1:02d}"
                    scenario_info = {
                        'id': scenario_id,
                        'name': scenario.get('name', f'Scenario {i+1}'),
                        'steps': scenario.get('steps', []),
                        'tags': scenario.get('tags', [])
                    }
                    self.traceability_matrix['bdd_scenarios'][feature_id]['scenarios'].append(scenario_info)

    def extract_implementation_artifacts(self):
        """Extract implementation artifacts (placeholder - would scan actual code in real implementation)."""
        # This is a placeholder - in a real implementation, this would scan source code
        # and identify functions, classes, modules that implement UoWs

        # For now, we'll create placeholder entries based on UoWs
        for uow_id, uow_info in self.traceability_matrix['units_of_work'].items():
            layer = uow_info.get('layer', '').lower()
            artifact_id = f"IMPL-{uow_id}"

            # Infer likely implementation locations based on layer
            if layer == 'foundation':
                module_path = f"src/foundation/{uow_id.lower().replace('-', '_')}.py"
            elif layer == 'infrastructure':
                module_path = f"src/infrastructure/{uow_id.lower().replace('-', '_')}.py"
            elif layer == 'application':
                module_path = f"src/application/{uow_id.lower().replace('-', '_')}.py"
            else:
                module_path = f"src/{uow_id.lower().replace('-', '_')}.py"

            self.traceability_matrix['implementation_artifacts'][artifact_id] = {
                'type': 'module',
                'module_path': module_path,
                'estimated_loc': 100,  # Placeholder
                'functions': [f"{uow_info.get('name', uow_id).lower().replace(' ', '_')}"],
                'classes': [],
                'tests': [f"test_{uow_id.lower().replace('-', '_')}.py"],
                'implements_uow': uow_id,
                'layer': layer
            }

    def build_relationships(self):
        """Build relationship mappings between different artifact types."""
        # FR to UoW relationships
        for uow_id, uow_info in self.traceability_matrix['units_of_work'].items():
            implements = uow_info.get('implements', [])
            for requirement_id in implements:
                if requirement_id.startswith('FR-'):
                    if requirement_id not in self.traceability_matrix['relationships']['fr_to_uow']:
                        self.traceability_matrix['relationships']['fr_to_uow'][requirement_id] = []
                    self.traceability_matrix['relationships']['fr_to_uow'][requirement_id].append(uow_id)

        # NFR to UoW relationships
        for uow_id, uow_info in self.traceability_matrix['units_of_work'].items():
            implements = uow_info.get('implements', [])
            for requirement_id in implements:
                if requirement_id.startswith('NFR-'):
                    if requirement_id not in self.traceability_matrix['relationships']['nfr_to_uow']:
                        self.traceability_matrix['relationships']['nfr_to_uow'][requirement_id] = []
                    self.traceability_matrix['relationships']['nfr_to_uow'][requirement_id].append(uow_id)

        # UoW to Contract relationships
        for contract_id, contract_info in self.traceability_matrix['contracts'].items():
            applies_to = contract_info.get('applies_to', {})
            if applies_to.get('entity_type') == 'uow':
                uow_id = applies_to.get('entity_name')
                if uow_id:
                    self.traceability_matrix['relationships']['uow_to_contract'][uow_id] = contract_id

        # UoW to BDD relationships (based on file naming convention)
        for feature_id, feature_info in self.traceability_matrix['bdd_scenarios'].items():
            # Extract UoW ID from feature file name (assuming naming convention like uow_001.feature)
            feature_file = Path(feature_info['file_path']).stem
            if feature_file.startswith('uow_'):
                uow_part = feature_file.replace('uow_', '').upper()
                # Convert numbers to UoW format (e.g., 001 -> UoW-001)
                if uow_part.isdigit():
                    uow_id = f"UoW-{uow_part}"
                else:
                    uow_id = f"UoW-{uow_part.replace('_', '')}"

                if uow_id in self.traceability_matrix['units_of_work']:
                    self.traceability_matrix['relationships']['uow_to_bdd'][uow_id] = feature_id

        # UoW to Implementation relationships
        for impl_id, impl_info in self.traceability_matrix['implementation_artifacts'].items():
            uow_id = impl_info.get('implements_uow')
            if uow_id:
                self.traceability_matrix['relationships']['uow_to_implementation'][uow_id] = impl_id

    def calculate_coverage_metrics(self):
        """Calculate coverage metrics and identify gaps."""
        metrics = {}

        # Requirements coverage
        total_frs = len([r for r in self.traceability_matrix['requirements'].values() if r['type'] == 'functional'])
        covered_frs = len(self.traceability_matrix['relationships']['fr_to_uow'])
        metrics['fr_coverage'] = {
            'total': total_frs,
            'covered': covered_frs,
            'percentage': (covered_frs / total_frs * 100) if total_frs > 0 else 0
        }

        total_nfrs = len([r for r in self.traceability_matrix['requirements'].values() if r['type'] == 'non_functional'])
        covered_nfrs = len(self.traceability_matrix['relationships']['nfr_to_uow'])
        metrics['nfr_coverage'] = {
            'total': total_nfrs,
            'covered': covered_nfrs,
            'percentage': (covered_nfrs / total_nfrs * 100) if total_nfrs > 0 else 0
        }

        # UoW coverage
        total_uows = len(self.traceability_matrix['units_of_work'])
        uows_with_contracts = len(self.traceability_matrix['relationships']['uow_to_contract'])
        uows_with_bdd = len(self.traceability_matrix['relationships']['uow_to_bdd'])
        uows_with_impl = len(self.traceability_matrix['relationships']['uow_to_implementation'])

        metrics['uow_coverage'] = {
            'total': total_uows,
            'with_contracts': uows_with_contracts,
            'with_bdd': uows_with_bdd,
            'with_implementation': uows_with_impl,
            'contracts_percentage': (uows_with_contracts / total_uows * 100) if total_uows > 0 else 0,
            'bdd_percentage': (uows_with_bdd / total_uows * 100) if total_uows > 0 else 0,
            'implementation_percentage': (uows_with_impl / total_uows * 100) if total_uows > 0 else 0
        }

        self.traceability_matrix['coverage_metrics'] = metrics

    def identify_gaps(self):
        """Identify gaps in traceability coverage."""
        gaps = []

        # Requirements not covered by UoWs
        covered_frs = set(self.traceability_matrix['relationships']['fr_to_uow'].keys())
        all_frs = set(r_id for r_id, r in self.traceability_matrix['requirements'].items() if r['type'] == 'functional')
        uncovered_frs = all_frs - covered_frs
        for fr_id in uncovered_frs:
            gaps.append({
                'type': 'uncovered_requirement',
                'requirement_id': fr_id,
                'requirement_type': 'functional',
                'description': f'Functional requirement {fr_id} is not implemented by any UoW'
            })

        covered_nfrs = set(self.traceability_matrix['relationships']['nfr_to_uow'].keys())
        all_nfrs = set(r_id for r_id, r in self.traceability_matrix['requirements'].items() if r['type'] == 'non_functional')
        uncovered_nfrs = all_nfrs - covered_nfrs
        for nfr_id in uncovered_nfrs:
            gaps.append({
                'type': 'uncovered_requirement',
                'requirement_id': nfr_id,
                'requirement_type': 'non_functional',
                'description': f'Non-functional requirement {nfr_id} is not implemented by any UoW'
            })

        # UoWs without contracts
        uows_with_contracts = set(self.traceability_matrix['relationships']['uow_to_contract'].keys())
        all_uows = set(self.traceability_matrix['units_of_work'].keys())
        uows_without_contracts = all_uows - uows_with_contracts
        for uow_id in uows_without_contracts:
            gaps.append({
                'type': 'missing_contract',
                'uow_id': uow_id,
                'description': f'UoW {uow_id} does not have a formal contract'
            })

        # UoWs without BDD scenarios
        uows_with_bdd = set(self.traceability_matrix['relationships']['uow_to_bdd'].keys())
        uows_without_bdd = all_uows - uows_with_bdd
        for uow_id in uows_without_bdd:
            gaps.append({
                'type': 'missing_bdd',
                'uow_id': uow_id,
                'description': f'UoW {uow_id} does not have BDD scenarios'
            })

        # UoWs without implementation
        uows_with_impl = set(self.traceability_matrix['relationships']['uow_to_implementation'].keys())
        uows_without_impl = all_uows - uows_with_impl
        for uow_id in uows_without_impl:
            gaps.append({
                'type': 'missing_implementation',
                'uow_id': uow_id,
                'description': f'UoW {uow_id} does not have implementation artifacts'
            })

        self.traceability_matrix['gaps'] = gaps

    def generate_matrix(self) -> Dict[str, Any]:
        """Generate complete traceability matrix."""
        print("Extracting requirements...")
        self.extract_requirements()

        print("Extracting units of work...")
        self.extract_units_of_work()

        print("Extracting contracts...")
        self.extract_contracts()

        print("Extracting BDD scenarios...")
        self.extract_bdd_scenarios()

        print("Extracting implementation artifacts...")
        self.extract_implementation_artifacts()

        print("Building relationships...")
        self.build_relationships()

        print("Calculating coverage metrics...")
        self.calculate_coverage_metrics()

        print("Identifying gaps...")
        self.identify_gaps()

        return self.traceability_matrix

    def save_matrix(self, output_file: Path):
        """Save traceability matrix to JSON file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.traceability_matrix, f, indent=2, ensure_ascii=False)
        print(f"Traceability matrix saved: {output_file}")

    def generate_html_report(self, output_file: Path):
        """Generate HTML report of traceability matrix."""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Traceability Matrix Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .metrics {{ display: flex; gap: 20px; margin-bottom: 20px; }}
        .metric-card {{ background-color: #e8f4fd; padding: 15px; border-radius: 5px; flex: 1; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #0066cc; }}
        .gaps {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .gap-item {{ margin-bottom: 10px; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ color: #333; border-bottom: 2px solid #0066cc; padding-bottom: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Traceability Matrix Report</h1>
        <p><strong>Generated:</strong> {self.traceability_matrix['metadata']['generated_date']}</p>
        <p><strong>Project:</strong> {self.traceability_matrix['metadata']['project_root']}</p>
    </div>

    <div class="section">
        <h2>📈 Coverage Metrics</h2>
        <div class="metrics">
            <div class="metric-card">
                <h3>FR Coverage</h3>
                <div class="metric-value">{self.traceability_matrix['coverage_metrics']['fr_coverage']['percentage']:.1f}%</div>
                <p>{self.traceability_matrix['coverage_metrics']['fr_coverage']['covered']} of {self.traceability_matrix['coverage_metrics']['fr_coverage']['total']} FRs</p>
            </div>
            <div class="metric-card">
                <h3>NFR Coverage</h3>
                <div class="metric-value">{self.traceability_matrix['coverage_metrics']['nfr_coverage']['percentage']:.1f}%</div>
                <p>{self.traceability_matrix['coverage_metrics']['nfr_coverage']['covered']} of {self.traceability_matrix['coverage_metrics']['nfr_coverage']['total']} NFRs</p>
            </div>
            <div class="metric-card">
                <h3>UoW with BDD</h3>
                <div class="metric-value">{self.traceability_matrix['coverage_metrics']['uow_coverage']['bdd_percentage']:.1f}%</div>
                <p>{self.traceability_matrix['coverage_metrics']['uow_coverage']['with_bdd']} of {self.traceability_matrix['coverage_metrics']['uow_coverage']['total']} UoWs</p>
            </div>
            <div class="metric-card">
                <h3>UoW with Contracts</h3>
                <div class="metric-value">{self.traceability_matrix['coverage_metrics']['uow_coverage']['contracts_percentage']:.1f}%</div>
                <p>{self.traceability_matrix['coverage_metrics']['uow_coverage']['with_contracts']} of {self.traceability_matrix['coverage_metrics']['uow_coverage']['total']} UoWs</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>⚠️ Coverage Gaps</h2>
        <div class="gaps">
"""

        if self.traceability_matrix['gaps']:
            for gap in self.traceability_matrix['gaps']:
                html_content += f"""
            <div class="gap-item">
                <strong>{gap['type'].replace('_', ' ').title()}:</strong> {gap['description']}
            </div>
"""
        else:
            html_content += "<p>✅ No coverage gaps detected!</p>"

        html_content += """
        </div>
    </div>

    <div class="section">
        <h2>🔗 Traceability Relationships</h2>

        <h3>Requirements to UoWs</h3>
        <table>
            <tr><th>Requirement ID</th><th>Type</th><th>Title</th><th>Implementing UoWs</th></tr>
"""

        # Requirements to UoWs table
        for req_id, req_info in self.traceability_matrix['requirements'].items():
            implementing_uows = []
            if req_info['type'] == 'functional':
                implementing_uows = self.traceability_matrix['relationships']['fr_to_uow'].get(req_id, [])
            else:
                implementing_uows = self.traceability_matrix['relationships']['nfr_to_uow'].get(req_id, [])

            html_content += f"""
            <tr>
                <td>{req_id}</td>
                <td>{req_info['type']}</td>
                <td>{req_info['title']}</td>
                <td>{', '.join(implementing_uows) if implementing_uows else '❌ Not implemented'}</td>
            </tr>
"""

        html_content += """
        </table>

        <h3>UoWs to Artifacts</h3>
        <table>
            <tr><th>UoW ID</th><th>Name</th><th>Layer</th><th>Contract</th><th>BDD</th><th>Implementation</th></tr>
"""

        # UoWs to artifacts table
        for uow_id, uow_info in self.traceability_matrix['units_of_work'].items():
            contract = self.traceability_matrix['relationships']['uow_to_contract'].get(uow_id, '❌')
            bdd = self.traceability_matrix['relationships']['uow_to_bdd'].get(uow_id, '❌')
            impl = self.traceability_matrix['relationships']['uow_to_implementation'].get(uow_id, '❌')

            html_content += f"""
            <tr>
                <td>{uow_id}</td>
                <td>{uow_info['name']}</td>
                <td>{uow_info['layer']}</td>
                <td>{contract if contract != '❌' else contract}</td>
                <td>{bdd if bdd != '❌' else bdd}</td>
                <td>{'✅' if impl != '❌' else impl}</td>
            </tr>
"""

        html_content += """
        </table>
    </div>
</body>
</html>
"""

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML report saved: {output_file}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate traceability matrix from SSOT data')
    parser.add_argument('--ssot-dir', type=str, default='./demeter/core/ssot',
                       help='SSOT directory path')
    parser.add_argument('--project-root', type=str, default='.',
                       help='Project root directory')
    parser.add_argument('--output', type=str, default='./traceability-matrix.json',
                       help='Output JSON file path')
    parser.add_argument('--html-report', type=str, default='./traceability-report.html',
                       help='HTML report output path')

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()

    ssot_dir = Path(args.ssot_dir).resolve()
    project_root = Path(args.project_root).resolve()

    if not ssot_dir.exists():
        print(f"Error: SSOT directory not found: {ssot_dir}")
        sys.exit(1)

    generator = TraceabilityMatrixGenerator(ssot_dir, project_root)

    try:
        print("🔍 Generating traceability matrix...")
        matrix = generator.generate_matrix()

        # Save JSON matrix
        output_file = Path(args.output)
        generator.save_matrix(output_file)

        # Generate HTML report
        html_report_file = Path(args.html_report)
        generator.generate_html_report(html_report_file)

        print(f"\n✅ Traceability matrix generation completed!")
        print(f"📊 Coverage Summary:")
        print(f"  - FR Coverage: {matrix['coverage_metrics']['fr_coverage']['percentage']:.1f}%")
        print(f"  - NFR Coverage: {matrix['coverage_metrics']['nfr_coverage']['percentage']:.1f}%")
        print(f"  - UoW with BDD: {matrix['coverage_metrics']['uow_coverage']['bdd_percentage']:.1f}%")
        print(f"  - UoW with Contracts: {matrix['coverage_metrics']['uow_coverage']['contracts_percentage']:.1f}%")
        print(f"📁 Files generated:")
        print(f"  - Matrix: {output_file}")
        print(f"  - Report: {html_report_file}")

        if matrix['gaps']:
            print(f"\n⚠️  Found {len(matrix['gaps'])} coverage gaps - check the HTML report for details.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()