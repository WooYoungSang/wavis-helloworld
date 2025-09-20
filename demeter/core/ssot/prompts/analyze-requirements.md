# Requirements Analysis Prompt Template

## Purpose
Use this prompt to analyze natural language requirements and suggest appropriate SSOT extensions for Demeter projects.

## Usage
1. Copy the prompt below
2. Replace placeholders with actual project information
3. Provide the requirements text to Claude Code
4. Get domain/extension recommendations

---

# 📊 Analyze Project Requirements

## Task
Analyze the following requirements and recommend appropriate SSOT extensions for a Demeter project.

## Project Information
- **Project Name**: [PROJECT_NAME]
- **Requirements Source**: [REQUIREMENTS_FILE_PATH]

## Requirements Text
```
[PASTE_REQUIREMENTS_TEXT_HERE]
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

```yaml
# Requirements Analysis Results

project_name: [PROJECT_NAME]
analysis_date: [CURRENT_DATE]

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

suggested_command:
  basic: ./demeter-init.sh [PROJECT_NAME] "[PRIMARY_DOMAIN]"
  full: ./demeter-init.sh [PROJECT_NAME] "[ALL_EXTENSIONS_COMMA_SEPARATED]"

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

## Validation Checklist

After analysis, verify:
- [ ] Domain detection makes sense given the requirements
- [ ] All compliance requirements are identified
- [ ] Feature requirements are appropriate
- [ ] Extension combinations are valid
- [ ] Command syntax is correct

## Example Usage

For the provided requirements, output a complete analysis following the format above, focusing on:
1. Clear identification of domain patterns
2. Specific reasoning for recommendations
3. Practical next steps for project initialization

Analyze the requirements now and provide the structured output.