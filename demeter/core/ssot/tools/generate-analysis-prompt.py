#!/usr/bin/env python3
"""
⚠️  DEPRECATED: Generate Requirements Analysis Prompt
⚠️  This script is deprecated. Use ai-refinement.prompt.template in Claude Code instead.
⚠️
⚠️  Migration Path:
⚠️  1. Use demeter/core/prompts/templates/ai-refinement.prompt.template
⚠️  2. Benefits: Constitutional compliance, AI-enhanced analysis, GraphRAG integration
⚠️  3. See demeter/core/ssot/tools/README.md for migration guide

DEPRECATED: Creates a Claude Code prompt for analyzing requirements and suggesting extensions

Legacy Usage:
    python generate-analysis-prompt.py --input requirements.md --project-name "MyShop"

Recommended Usage:
    Use ai-refinement.prompt.template in Claude Code with constitutional AI analysis
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime


def generate_analysis_prompt(input_file, project_name, requirements_content):
    """Generate Claude Code prompt for requirements analysis"""

    prompt = f'''# 📊 Analyze Project Requirements

## Task
Analyze the following requirements and recommend appropriate SSOT extensions for a Demeter project.

## Project Information
- **Project Name**: {project_name}
- **Requirements Source**: {input_file}
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Requirements Text
```
{requirements_content}
```

## Analysis Instructions

### 1. Domain Detection
Analyze the requirements text for domain indicators:

**E-Commerce Patterns:**
- Keywords: product, cart, shopping, order, payment, inventory, customer, checkout, catalog, store, shop, buy, sell
- Korean: 제품, 장바구니, 주문, 결제, 재고, 고객, 쇼핑, 상점

**FinTech Patterns:**
- Keywords: transaction, account, transfer, banking, finance, money, payment, wallet, currency, exchange, trading, invest
- Korean: 거래, 계좌, 송금, 은행, 금융, 투자, 화폐, 지갑

**Healthcare Patterns:**
- Keywords: patient, medical, diagnosis, treatment, doctor, hospital, health, clinic, medicine, prescription, record
- Korean: 환자, 의료, 진료, 치료, 의사, 병원, 건강, 처방

**IoT Patterns:**
- Keywords: sensor, device, real-time, mqtt, telemetry, monitoring, hardware, embedded, data collection, automation
- Korean: 센서, 디바이스, 실시간, 모니터링, 하드웨어, 자동화

### 2. Compliance Detection
Look for compliance requirements:

**GDPR**: privacy, personal data, consent, data protection, 개인정보, 프라이버시
**HIPAA**: protected health information, medical records, 의료정보
**PCI-DSS**: payment card, credit card, card data, 신용카드, 카드결제

### 3. Feature Detection
Identify additional features:

**AI/ML**: machine learning, artificial intelligence, recommendation, 인공지능, 추천
**Blockchain**: blockchain, crypto, smart contract, distributed ledger, 블록체인
**Streaming**: real-time, websocket, stream, live, push notification, 실시간, 스트리밍

## Expected Output Format

Provide a structured analysis with:

```yaml
# Requirements Analysis Results

project_name: {project_name}
analysis_date: {datetime.now().strftime('%Y-%m-%d')}

domain_detection:
  primary_domain: [DETECTED_DOMAIN]  # e-commerce, fintech, healthcare, iot, or general
  confidence: [HIGH/MEDIUM/LOW]
  reasoning: [EXPLANATION_OF_DETECTION]

recommended_extensions:
  domain:
    - domain/[PRIMARY_DOMAIN].yaml
  compliance:
    - compliance/[COMPLIANCE_NAME].yaml  # if detected
  features:
    - features/[FEATURE_NAME].yaml  # if detected

suggested_commands:
  basic: ./demeter-init.sh {project_name} "[PRIMARY_DOMAIN]"
  full: ./demeter-init.sh {project_name} "[ALL_EXTENSIONS_COMMA_SEPARATED]"

analysis_summary:
  domain_indicators: [LIST_OF_FOUND_KEYWORDS]
  compliance_requirements: [LIST_OF_COMPLIANCE_NEEDS]
  feature_requirements: [LIST_OF_FEATURES]

confidence_notes: |
  - HIGH: Strong keyword matches and clear domain patterns
  - MEDIUM: Some indicators present, manual review recommended
  - LOW: Weak signals, consider base SSOT or manual selection

next_steps:
  - Review the analysis results
  - Confirm domain selection is appropriate
  - Consider any missing extensions
  - Initialize project with recommended command
```

## Analysis Request

Please analyze the requirements above and provide:
1. Clear identification of domain patterns
2. Specific reasoning for recommendations
3. Practical initialization commands
4. Confidence assessment

Focus on detecting the strongest domain signals and providing actionable recommendations for Demeter project initialization.'''

    return prompt


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Generate requirements analysis prompt for Claude Code')
    parser.add_argument('--input', type=str, required=True,
                       help='Input requirements file (markdown, text, etc.)')
    parser.add_argument('--project-name', type=str, required=True,
                       help='Project name')
    parser.add_argument('--output', type=str, default='analyze-requirements.prompt',
                       help='Output prompt file')

    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()

    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: Input file not found: {input_path}")
        sys.exit(1)

    # Read requirements file
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            requirements_content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

    if not requirements_content.strip():
        print(f"❌ Error: Requirements file is empty")
        sys.exit(1)

    print(f"📖 Processing requirements from: {input_path}")
    print(f"📄 Content length: {len(requirements_content)} characters")

    # Generate prompt
    prompt = generate_analysis_prompt(args.input, args.project_name, requirements_content)

    # Save prompt file
    prompt_file = Path(args.output)
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)

    print(f"✅ Analysis prompt generated!")
    print(f"📋 Prompt file: {prompt_file}")
    print(f"🚀 Next: Execute this prompt in Claude Code to get domain recommendations")


if __name__ == '__main__':
    main()