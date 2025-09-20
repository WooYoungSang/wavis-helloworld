#!/usr/bin/env python3
"""
⚠️  DEPRECATED: Requirements Analysis Tool
⚠️  This script is deprecated. Use requirements-analysis.prompt.template in Claude Code instead.
⚠️
⚠️  Migration Path:
⚠️  1. Use demeter/core/prompts/templates/requirements-analysis.prompt.template
⚠️  2. Benefits: Constitutional compliance, AI-enhanced analysis, GraphRAG integration
⚠️  3. See demeter/core/ssot/tools/README.md for migration guide

DEPRECATED: Analyzes natural language requirements to detect domain and suggest extensions

Legacy Usage:
    python analyze-requirements.py --input requirements.md --project-name "MyShop"

Recommended Usage:
    Use requirements-analysis.prompt.template in Claude Code with constitutional AI analysis
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime


def analyze_requirements_text(text):
    """Analyze requirements text and detect patterns"""
    text_lower = text.lower()

    # Domain detection patterns
    domain_patterns = {
        'e-commerce': [
            'product', 'cart', 'shopping', 'order', 'payment', 'inventory',
            'customer', 'checkout', 'catalog', 'store', 'shop', 'buy', 'sell',
            '제품', '장바구니', '주문', '결제', '재고', '고객', '쇼핑', '상점'
        ],
        'fintech': [
            'transaction', 'account', 'transfer', 'banking', 'finance', 'money',
            'payment', 'wallet', 'currency', 'exchange', 'trading', 'invest',
            '거래', '계좌', '송금', '은행', '금융', '투자', '화폐', '지갑'
        ],
        'healthcare': [
            'patient', 'medical', 'diagnosis', 'treatment', 'doctor', 'hospital',
            'health', 'clinic', 'medicine', 'prescription', 'record',
            '환자', '의료', '진료', '치료', '의사', '병원', '건강', '처방'
        ],
        'iot': [
            'sensor', 'device', 'real-time', 'mqtt', 'telemetry', 'monitoring',
            'hardware', 'embedded', 'data collection', 'automation',
            '센서', '디바이스', '실시간', '모니터링', '하드웨어', '자동화'
        ]
    }

    # Calculate scores for each domain
    domain_scores = {}
    for domain, keywords in domain_patterns.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            domain_scores[domain] = score / len(keywords)  # Normalize by keyword count

    # Detect compliance requirements
    compliance_patterns = {
        'gdpr': ['gdpr', 'privacy', 'personal data', 'consent', 'data protection', '개인정보', '프라이버시'],
        'hipaa': ['hipaa', 'phi', 'protected health', 'medical record', '의료정보'],
        'pci-dss': ['pci', 'payment card', 'credit card', 'card data', '신용카드', '카드결제']
    }

    compliance_needed = []
    for compliance, keywords in compliance_patterns.items():
        if any(keyword in text_lower for keyword in keywords):
            compliance_needed.append(compliance)

    # Detect features
    feature_patterns = {
        'ai-ml': ['ai', 'ml', 'machine learning', 'artificial intelligence', 'recommendation', '인공지능', '추천'],
        'blockchain': ['blockchain', 'crypto', 'smart contract', 'distributed ledger', '블록체인'],
        'streaming': ['real-time', 'websocket', 'stream', 'live', 'push notification', '실시간', '스트리밍']
    }

    features_detected = []
    for feature, keywords in feature_patterns.items():
        if any(keyword in text_lower for keyword in keywords):
            features_detected.append(feature)

    return {
        'domain_scores': domain_scores,
        'compliance_needed': compliance_needed,
        'features_detected': features_detected
    }


def generate_analysis_prompt(input_file, project_name, analysis_results):
    """Generate Claude Code prompt for requirements analysis"""

    # Determine primary domain
    primary_domain = "general"
    max_score = 0
    if analysis_results['domain_scores']:
        primary_domain = max(analysis_results['domain_scores'], key=analysis_results['domain_scores'].get)
        max_score = analysis_results['domain_scores'][primary_domain]

    # Suggest extensions
    suggested_extensions = []
    if max_score > 0.1:  # Confidence threshold
        suggested_extensions.append(f"domain/{primary_domain}.yaml")

    # Add compliance extensions
    for compliance in analysis_results['compliance_needed']:
        suggested_extensions.append(f"compliance/{compliance}.yaml")

    # Add feature extensions
    for feature in analysis_results['features_detected']:
        suggested_extensions.append(f"features/{feature}.yaml")

    confidence = "high" if max_score > 0.3 else "medium" if max_score > 0.1 else "low"

    prompt = f'''# 📊 Requirements Analysis Report

## Project: {project_name}
**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Input**: {input_file}

## 🎯 Domain Detection Results

### Primary Domain: {primary_domain}
**Confidence**: {confidence} ({max_score:.2f})

### Domain Scores:
'''

    for domain, score in sorted(analysis_results['domain_scores'].items(), key=lambda x: x[1], reverse=True):
        prompt += f"- **{domain}**: {score:.2f}\n"

    prompt += f'''

## 🔧 Recommended Extensions

Based on the analysis, these extensions are recommended:

'''

    if suggested_extensions:
        for ext in suggested_extensions:
            prompt += f"- `{ext}`\n"
    else:
        prompt += "- Base SSOT only (no specific domain detected)\n"

    prompt += f'''

## 📋 Compliance Requirements Detected
'''

    if analysis_results['compliance_needed']:
        for compliance in analysis_results['compliance_needed']:
            prompt += f"- {compliance.upper()}\n"
    else:
        prompt += "- None detected\n"

    prompt += f'''

## ⚡ Features Detected
'''

    if analysis_results['features_detected']:
        for feature in analysis_results['features_detected']:
            prompt += f"- {feature}\n"
    else:
        prompt += "- None detected\n"

    prompt += f'''

## 🚀 Next Steps

To initialize the project with these recommendations:

```bash
./demeter-init.sh {project_name} "{','.join(suggested_extensions)}"
```

Or for manual selection:
```bash
./demeter-init.sh {project_name} "{primary_domain}"
```

## 📝 Manual Review Needed

Please review the analysis and:
1. Confirm the detected domain is correct
2. Add any missing extensions
3. Verify compliance requirements
4. Consider additional features

## 💡 Analysis Confidence Notes

- **High** (>0.3): Strong keyword match, recommended to use
- **Medium** (0.1-0.3): Some indicators, manual review suggested
- **Low** (<0.1): Weak signals, consider manual domain selection

Generated by Demeter Requirements Analyzer v1.0
'''

    return prompt


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Analyze requirements and suggest extensions')
    parser.add_argument('--input', type=str, required=True,
                       help='Input requirements file (markdown, text, etc.)')
    parser.add_argument('--project-name', type=str, required=True,
                       help='Project name')
    parser.add_argument('--output', type=str, default='requirements-analysis.prompt',
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
            requirements_text = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

    if not requirements_text.strip():
        print(f"❌ Error: Requirements file is empty")
        sys.exit(1)

    print(f"📖 Analyzing requirements from: {input_path}")
    print(f"📄 Content length: {len(requirements_text)} characters")

    # Analyze requirements
    analysis_results = analyze_requirements_text(requirements_text)

    # Generate prompt
    prompt = generate_analysis_prompt(args.input, args.project_name, analysis_results)

    # Save prompt file
    prompt_file = Path(args.output)
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)

    print(f"✅ Analysis complete!")
    print(f"📋 Report generated: {prompt_file}")

    # Show quick summary
    if analysis_results['domain_scores']:
        primary_domain = max(analysis_results['domain_scores'], key=analysis_results['domain_scores'].get)
        confidence = analysis_results['domain_scores'][primary_domain]
        print(f"🎯 Primary domain: {primary_domain} (confidence: {confidence:.2f})")
    else:
        print(f"🎯 No specific domain detected - will use base SSOT")

    if analysis_results['compliance_needed']:
        print(f"⚖️  Compliance: {', '.join(analysis_results['compliance_needed'])}")

    if analysis_results['features_detected']:
        print(f"⚡ Features: {', '.join(analysis_results['features_detected'])}")


if __name__ == '__main__':
    main()