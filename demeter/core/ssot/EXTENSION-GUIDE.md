# SSOT Extension Guide

이 가이드는 Demeter 템플릿 시스템에서 SSOT(Single Source of Truth)를 확장하는 방법을 설명합니다.

## 🎯 확장 철학

**"SSOT defines WHAT to build, technology stack defines HOW to build"**

Demeter의 확장 시스템은 다음 원칙을 따릅니다:
- **모듈성**: 각 확장은 독립적으로 동작
- **조합성**: 여러 확장을 조합하여 복합 요구사항 충족
- **기술 중립성**: 확장은 구현 기술에 의존하지 않음

## 📁 확장 구조

```
demeter/core/ssot/extensions/
├── domain/                    # 도메인별 확장
│   ├── e-commerce.yaml       # 전자상거래
│   ├── fintech.yaml          # 금융기술
│   └── healthcare.yaml       # 헬스케어
├── features/                  # 기능별 확장
│   ├── ai-ml.yaml            # AI/ML 통합
│   ├── blockchain.yaml       # 블록체인
│   ├── iot.yaml              # IoT 디바이스
│   └── streaming.yaml        # 실시간 스트리밍
└── compliance/               # 규정 준수
    ├── gdpr.yaml             # EU 개인정보보호
    ├── hipaa.yaml            # 의료정보 보호
    └── pci-dss.yaml          # 결제카드 보안
```

## 🔧 확장 파일 구조

각 확장 파일은 다음 구조를 따릅니다:

```yaml
# Extension Metadata
extension:
  id: "domain-ecommerce"
  name: "E-Commerce Domain Extension"
  version: "1.0.0"
  description: "전자상거래 도메인을 위한 요구사항 확장"
  category: "domain"  # domain, features, compliance
  compatibility:
    mvp_phases: ["phase_2", "phase_3"]  # 적용 가능한 MVP 단계
    conflicts: []  # 충돌하는 확장
    requires: []   # 필수 의존 확장

# Functional Requirements
functional_requirements:
  FR-EC-001:
    id: "FR-EC-001"
    title: "Product Catalog Management"
    description: "상품 카탈로그 관리 기능"
    priority: "High"
    category: "E-Commerce"
    acceptance_criteria:
      AC-1: "상품 등록, 수정, 삭제 기능"
      AC-2: "카테고리별 상품 분류"
      AC-3: "재고 관리 및 알림"
      AC-4: "상품 검색 및 필터링"
    business_value: "효율적인 상품 관리"
    dependencies: ["FR-003"]  # Data Persistence
    estimated_effort: "high"

# Non-Functional Requirements
non_functional_requirements:
  NFR-EC-001:
    id: "NFR-EC-001"
    title: "E-Commerce Performance"
    description: "전자상거래 특화 성능 요구사항"
    category: "Performance"
    requirements:
      - "상품 검색 응답시간 < 100ms"
      - "동시 주문 처리: 1000건/초"
      - "결제 처리 시간 < 3초"
    measurement:
      - "부하 테스트를 통한 성능 검증"
      - "실시간 트랜잭션 모니터링"
    priority: "High"

# Units of Work
units_of_work:
  UoW-EC-001:
    id: "UoW-EC-001"
    title: "Product Catalog Implementation"
    description: "상품 카탈로그 시스템 구현"
    category: "E-Commerce"
    priority: "High"
    estimated_effort: "high"
    dependencies: ["UoW-101", "UoW-103"]  # Database + Interface
    related_frs: ["FR-EC-001"]
    related_nfrs: ["NFR-EC-001"]
    acceptance_criteria:
      AC-1: "상품 CRUD API 구현"
      AC-2: "카테고리 관리 시스템"
      AC-3: "재고 추적 로직"
      AC-4: "검색 인덱싱 구현"

# Integration Points
integration:
  framework_requirements:
    extends:
      - "FR-003"  # Data Persistence - 상품 데이터 저장
      - "FR-002"  # Interface Layer - 상품 API
      - "FR-008"  # Monitoring - 전자상거래 메트릭
    modifies:
      - "NFR-001": "전자상거래 특화 성능 요구사항 추가"
```

## 🔀 확장 병합 프로세스

### 1. 자동 병합

```bash
# 단일 확장 적용
python demeter/core/ssot/tools/merge-ssot.py \
  --base demeter/core/ssot/framework-requirements.yaml \
  --extensions demeter/core/ssot/extensions/domain/e-commerce.yaml \
  --output merged-ssot.yaml

# 다중 확장 적용
python demeter/core/ssot/tools/merge-ssot.py \
  --base demeter/core/ssot/framework-requirements.yaml \
  --extensions \
    demeter/core/ssot/extensions/domain/e-commerce.yaml \
    demeter/core/ssot/extensions/features/ai-ml.yaml \
    demeter/core/ssot/extensions/compliance/gdpr.yaml \
  --output merged-ssot.yaml
```

### 2. 병합 규칙

#### ID 충돌 해결
- **Namespace 추가**: `FR-001` → `FR-EC-001` (도메인별)
- **우선순위**: compliance > domain > features > framework
- **오류 발생**: 같은 ID가 다른 내용으로 정의된 경우

#### 의존성 검증
- **순환 의존성 검사**: UoW 간 순환 참조 방지
- **필수 의존성 확인**: requires 필드 검증
- **충돌 확장 확인**: conflicts 필드 검증

#### 내용 병합
- **List 필드**: 중복 제거 후 병합
- **Dict 필드**: 깊은 병합 (deep merge)
- **Scalar 필드**: 마지막 값 우선

## 📝 새로운 확장 작성

### 1. 확장 파일 생성

```yaml
# demeter/core/ssot/extensions/domain/my-domain.yaml
extension:
  id: "domain-mydomain"
  name: "My Domain Extension"
  version: "1.0.0"
  description: "사용자 정의 도메인 확장"
  category: "domain"
  compatibility:
    mvp_phases: ["phase_1", "phase_2", "phase_3"]
    conflicts: []
    requires: []

functional_requirements:
  # 도메인별 FR 정의...

non_functional_requirements:
  # 도메인별 NFR 정의...

units_of_work:
  # 도메인별 UoW 정의...
```

### 2. 확장 검증

```bash
# 확장 문법 검증
python demeter/core/ssot/tools/verify-extension.py \
  --extension demeter/core/ssot/extensions/domain/my-domain.yaml

# 확장 호환성 검사
python demeter/core/ssot/tools/merge-ssot.py \
  --base demeter/core/ssot/framework-requirements.yaml \
  --extensions demeter/core/ssot/extensions/domain/my-domain.yaml \
  --validate-only
```

### 3. 확장 테스트

```bash
# 확장 적용 테스트
python demeter/core/ssot/tools/test-extension.py \
  --extension demeter/core/ssot/extensions/domain/my-domain.yaml \
  --mvp-phase phase_2
```

## 🎨 확장 사용 예시

### E-Commerce + AI/ML 조합

```bash
./setup.sh
# 프로젝트 이름: my-ecommerce
# MVP 단계: phase_2
# 도메인 확장: e-commerce
# 기능 확장: ai-ml
```

결과:
- 기본 프레임워크 요구사항
- 전자상거래 도메인 요구사항 (상품관리, 주문처리, 결제)
- AI/ML 기능 요구사항 (추천시스템, 개인화)

### FinTech + GDPR 조합

```bash
./setup.sh
# 프로젝트 이름: my-fintech
# MVP 단계: phase_3
# 도메인 확장: fintech
# 규정 준수: gdpr
```

결과:
- 기본 프레임워크 요구사항
- 금융기술 도메인 요구사항 (거래처리, 위험관리)
- GDPR 규정 준수 요구사항 (개인정보보호, 데이터 권리)

## 🔍 확장 디버깅

### 병합 과정 추적

```bash
# 상세 로그와 함께 병합
python demeter/core/ssot/tools/merge-ssot.py \
  --base demeter/core/ssot/framework-requirements.yaml \
  --extensions demeter/core/ssot/extensions/domain/e-commerce.yaml \
  --output merged-ssot.yaml \
  --verbose \
  --debug
```

### 충돌 분석

```bash
# 충돌 원인 분석
python demeter/core/ssot/tools/analyze-conflicts.py \
  --extensions \
    demeter/core/ssot/extensions/domain/e-commerce.yaml \
    demeter/core/ssot/extensions/features/blockchain.yaml
```

## 📋 확장 개발 체크리스트

### 필수 요소
- [ ] 확장 메타데이터 정의
- [ ] 고유한 ID 네임스페이스 사용
- [ ] MVP 단계별 호환성 명시
- [ ] 의존성 및 충돌 정의
- [ ] AC 기반 검증 가능한 요구사항

### 품질 검증
- [ ] YAML 문법 검증
- [ ] 의존성 순환 참조 검사
- [ ] 기존 확장과의 호환성 확인
- [ ] 병합 테스트 통과
- [ ] 문서화 완료

### 테스트
- [ ] 단독 적용 테스트
- [ ] 다른 확장과 조합 테스트
- [ ] MVP 단계별 적용 테스트
- [ ] 계약 검증 테스트 통과

## 🎯 확장 활용 시나리오

### 1. 스타트업 MVP
- **Phase 1**: framework-requirements only
- **Phase 2**: + domain extension
- **Phase 3**: + features + compliance

### 2. 엔터프라이즈 프로젝트
- **Phase 1**: framework-requirements + compliance
- **Phase 2**: + domain + basic features
- **Phase 3**: + advanced features + full compliance

### 3. 특화 도메인 프로젝트
- **Phase 1**: framework-requirements + domain
- **Phase 2**: + domain-specific features
- **Phase 3**: + domain compliance requirements

이 가이드를 통해 Demeter 시스템의 확장성을 최대한 활용하여 프로젝트별 맞춤형 요구사항을 정의할 수 있습니다.