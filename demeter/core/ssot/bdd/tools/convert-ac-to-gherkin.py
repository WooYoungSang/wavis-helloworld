#!/usr/bin/env python3
"""
Convert Acceptance Criteria to Gherkin Scenarios

This tool helps convert existing AC strings to structured Gherkin scenarios.
"""

import yaml
import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

class ACToGherkinConverter:
    def __init__(self):
        # Common patterns for AC to Gherkin conversion
        self.conversion_patterns = {
            # Creation patterns
            r'(?:생성|만들|추가|작성|create|add|generate|setup)': {
                'given': '필요한 전제조건이 충족된 상태에서',
                'when': '생성 작업이 실행되면',
                'then': '대상이 성공적으로 생성되어야 한다'
            },

            # Update/modification patterns
            r'(?:수정|변경|업데이트|갱신|update|modify|change)': {
                'given': '수정할 대상이 존재하는 상태에서',
                'when': '수정 작업이 실행되면',
                'then': '대상이 성공적으로 수정되어야 한다'
            },

            # Deletion patterns
            r'(?:삭제|제거|delete|remove)': {
                'given': '삭제할 대상이 존재하는 상태에서',
                'when': '삭제 작업이 실행되면',
                'then': '대상이 성공적으로 삭제되어야 한다'
            },

            # Validation patterns
            r'(?:검증|확인|검사|validate|verify|check)': {
                'given': '검증할 데이터가 준비된 상태에서',
                'when': '검증 작업이 실행되면',
                'then': '검증 결과가 올바르게 반환되어야 한다'
            },

            # Configuration patterns
            r'(?:설정|구성|config|configure|setup)': {
                'given': '설정 가능한 환경이 준비된 상태에서',
                'when': '설정 작업이 실행되면',
                'then': '설정이 올바르게 적용되어야 한다'
            },

            # Processing patterns
            r'(?:처리|실행|수행|process|execute|perform)': {
                'given': '처리할 데이터가 준비된 상태에서',
                'when': '처리 작업이 실행되면',
                'then': '처리 결과가 올바르게 생성되어야 한다'
            }
        }

        # Domain-specific templates
        self.domain_templates = {
            'e-commerce': {
                'product': {
                    'given': '상품 카탈로그가 준비된 상태에서',
                    'when': '상품 관련 작업이 실행되면',
                    'then': '상품이 올바르게 처리되어야 한다'
                },
                'order': {
                    'given': '주문 가능한 상품이 있는 상태에서',
                    'when': '주문 관련 작업이 실행되면',
                    'then': '주문이 올바르게 처리되어야 한다'
                }
            },

            'fintech': {
                'transaction': {
                    'given': '유효한 계좌와 충분한 잔액이 있는 상태에서',
                    'when': '거래가 실행되면',
                    'then': '거래가 성공적으로 처리되어야 한다'
                },
                'payment': {
                    'given': '결제 수단이 유효한 상태에서',
                    'when': '결제가 요청되면',
                    'then': '결제가 성공적으로 완료되어야 한다'
                }
            },

            'healthcare': {
                'patient': {
                    'given': '환자 정보가 등록된 상태에서',
                    'when': '환자 관련 작업이 실행되면',
                    'then': '환자 데이터가 올바르게 처리되어야 한다'
                },
                'record': {
                    'given': '의료 기록 시스템이 준비된 상태에서',
                    'when': '의료 기록 작업이 실행되면',
                    'then': '기록이 안전하게 저장되어야 한다'
                }
            }
        }

    def convert_ac_to_gherkin(self, ac_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Convert an AC description to Gherkin scenario."""
        if not ac_description:
            return self._get_default_scenario()

        # Extract domain from context
        domain = self._extract_domain(context) if context else None
        entity = self._extract_entity(ac_description)

        # Try domain-specific templates first
        if domain and entity and domain in self.domain_templates:
            if entity in self.domain_templates[domain]:
                template = self.domain_templates[domain][entity]
                return self._create_scenario_from_template(template, ac_description)

        # Try pattern matching
        for pattern, template in self.conversion_patterns.items():
            if re.search(pattern, ac_description, re.IGNORECASE):
                return self._create_scenario_from_template(template, ac_description)

        # Fallback to generic scenario
        return self._create_generic_scenario(ac_description)

    def _extract_domain(self, context: Dict[str, Any]) -> Optional[str]:
        """Extract domain from context."""
        if not context:
            return None

        category = context.get('category', '').lower()

        domain_mapping = {
            'e-commerce': 'e-commerce',
            'ecommerce': 'e-commerce',
            'fintech': 'fintech',
            'finance': 'fintech',
            'healthcare': 'healthcare',
            'medical': 'healthcare'
        }

        return domain_mapping.get(category)

    def _extract_entity(self, description: str) -> Optional[str]:
        """Extract main entity from description."""
        entities = [
            'product', 'order', 'payment', 'user', 'customer',
            'transaction', 'account', 'patient', 'record',
            'configuration', 'setting', 'data', 'file',
            '상품', '주문', '결제', '사용자', '고객',
            '거래', '계좌', '환자', '기록', '설정', '데이터'
        ]

        for entity in entities:
            if entity in description.lower():
                return entity

        return None

    def _create_scenario_from_template(self, template: Dict[str, str], description: str) -> Dict[str, Any]:
        """Create scenario from template."""
        scenario = {
            'given': template['given'],
            'when': template['when'],
            'then': template['then'],
            'and': self._generate_and_clauses(description)
        }

        return scenario

    def _create_generic_scenario(self, description: str) -> Dict[str, Any]:
        """Create generic scenario."""
        return {
            'given': '시스템이 정상적으로 동작하는 상태에서',
            'when': '요구된 기능이 실행되면',
            'then': description,
            'and': [
                '결과가 예상된 형태로 반환되어야 한다',
                '시스템 상태가 일관성을 유지해야 한다'
            ]
        }

    def _get_default_scenario(self) -> Dict[str, Any]:
        """Get default scenario for empty AC."""
        return {
            'given': '시스템이 초기화된 상태에서',
            'when': '기능이 실행되면',
            'then': '예상된 결과가 반환되어야 한다',
            'and': []
        }

    def _generate_and_clauses(self, description: str) -> List[str]:
        """Generate And clauses based on description analysis."""
        and_clauses = []

        # Common validation clauses
        if any(word in description.lower() for word in ['validate', '검증', 'verify', '확인']):
            and_clauses.append('입력값이 유효성 검사를 통과해야 한다')

        if any(word in description.lower() for word in ['security', '보안', 'auth', '인증']):
            and_clauses.append('보안 요구사항이 충족되어야 한다')

        if any(word in description.lower() for word in ['log', '로그', 'audit', '감사']):
            and_clauses.append('관련 로그가 적절히 기록되어야 한다')

        if any(word in description.lower() for word in ['error', '오류', 'exception', '예외']):
            and_clauses.append('오류 상황이 적절히 처리되어야 한다')

        # If no specific clauses found, add generic ones
        if not and_clauses:
            and_clauses = [
                '성능 요구사항이 충족되어야 한다',
                '오류 처리가 적절해야 한다'
            ]

        return and_clauses

    def convert_uow_file(self, input_file: Path, output_file: Path = None):
        """Convert UoW file from string ACs to Gherkin scenarios."""
        if not input_file.exists():
            print(f"Error: Input file not found: {input_file}")
            return

        # Load YAML file
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading file {input_file}: {e}")
            return

        # Convert UoWs
        modified = False
        for section_name in ['units_of_work', 'universal_uows']:
            if section_name in data:
                for uow_id, uow_data in data[section_name].items():
                    if 'acceptance_criteria' in uow_data:
                        ac_data = uow_data['acceptance_criteria']

                        if isinstance(ac_data, list):
                            # Convert list format to structured format
                            converted_ac = {}
                            for i, ac_value in enumerate(ac_data):
                                if isinstance(ac_value, str):
                                    ac_id = f"AC-{i+1:03d}"
                                    converted_ac[ac_id] = {
                                        'description': ac_value,
                                        'scenario': self.convert_ac_to_gherkin(ac_value, uow_data)
                                    }
                                    modified = True
                                else:
                                    # Keep existing structured AC
                                    converted_ac[f"AC-{i+1:03d}"] = ac_value
                            uow_data['acceptance_criteria'] = converted_ac
                        elif isinstance(ac_data, dict):
                            # Handle dictionary format
                            converted_ac = {}
                            for ac_id, ac_value in ac_data.items():
                                if isinstance(ac_value, str):
                                    # Convert string AC to structured format
                                    converted_ac[ac_id] = {
                                        'description': ac_value,
                                        'scenario': self.convert_ac_to_gherkin(ac_value, uow_data)
                                    }
                                    modified = True
                                else:
                                    # Keep existing structured AC
                                    converted_ac[ac_id] = ac_value
                            uow_data['acceptance_criteria'] = converted_ac

        if not modified:
            print(f"No string ACs found in {input_file}. File already uses structured format.")
            return

        # Save converted file
        output_path = output_file or input_file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            print(f"Converted file saved: {output_path}")
        except Exception as e:
            print(f"Error saving file {output_path}: {e}")

    def convert_directory(self, input_dir: Path, output_dir: Path = None):
        """Convert all UoW files in a directory."""
        if not input_dir.exists():
            print(f"Error: Input directory not found: {input_dir}")
            return

        output_path = output_dir or input_dir
        output_path.mkdir(parents=True, exist_ok=True)

        # Find YAML files
        yaml_files = []
        yaml_files.extend(input_dir.glob("*.yaml"))
        yaml_files.extend(input_dir.glob("*.yml"))
        yaml_files.extend(input_dir.rglob("*.yaml"))
        yaml_files.extend(input_dir.rglob("*.yml"))

        if not yaml_files:
            print(f"No YAML files found in {input_dir}")
            return

        print(f"Found {len(yaml_files)} YAML files to process...")

        for yaml_file in yaml_files:
            print(f"Processing {yaml_file}...")

            # Calculate output file path
            rel_path = yaml_file.relative_to(input_dir)
            out_file = output_path / rel_path
            out_file.parent.mkdir(parents=True, exist_ok=True)

            self.convert_uow_file(yaml_file, out_file)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Convert AC strings to Gherkin scenarios')
    parser.add_argument('--input', type=str, required=True,
                       help='Input file or directory path')
    parser.add_argument('--output', type=str,
                       help='Output file or directory path (default: overwrite input)')
    parser.add_argument('--backup', action='store_true',
                       help='Create backup before conversion')

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve() if args.output else input_path

    if not input_path.exists():
        print(f"Error: Input path not found: {input_path}")
        sys.exit(1)

    # Create backup if requested
    if args.backup and input_path.is_file():
        backup_path = input_path.with_suffix(input_path.suffix + '.backup')
        import shutil
        shutil.copy2(input_path, backup_path)
        print(f"Backup created: {backup_path}")

    converter = ACToGherkinConverter()

    if input_path.is_file():
        converter.convert_uow_file(input_path, output_path if output_path != input_path else None)
    elif input_path.is_dir():
        converter.convert_directory(input_path, output_path if output_path != input_path else None)
    else:
        print(f"Error: Invalid input path: {input_path}")
        sys.exit(1)

    print("AC to Gherkin conversion completed!")


if __name__ == '__main__':
    main()