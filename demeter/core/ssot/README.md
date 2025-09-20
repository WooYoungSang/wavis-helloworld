# 🎯 SSOT 동적 주입 시스템

**Single Source of Truth**를 모듈화하여 프로젝트별 요구사항을 동적으로 조합할 수 있는 시스템입니다.

## 🏗️ 구조

```
demeter/core/ssot/
├── base/                         # 기본 SSOT (모든 프로젝트 공통)
│   ├── fr-base.yaml             # 기본 기능 요구사항 (FR-001~010)
│   ├── nfr-base.yaml            # 기본 비기능 요구사항 (NFR-001~007)
│   └── uow-base.yaml            # 기본 작업 단위 (UoW-000~210)
├── extensions/                   # 확장 SSOT (선택적)
│   ├── domain/                  # 도메인별 확장
│   │   ├── e-commerce.yaml     # 전자상거래
│   │   ├── fintech.yaml        # 금융기술
│   │   └── healthcare.yaml     # 헬스케어
│   ├── features/                # 기능별 확장
│   │   ├── ai-ml.yaml          # AI/ML 통합
│   │   ├── blockchain.yaml     # 블록체인
│   │   └── iot.yaml            # IoT 통합
│   └── compliance/              # 규정 준수
│       ├── gdpr.yaml           # GDPR 요구사항
│       ├── hipaa.yaml          # HIPAA 요구사항
│       └── pci-dss.yaml        # PCI-DSS 요구사항
├── custom/                      # 프로젝트별 커스텀
├── tools/                       # SSOT 처리 도구
│   ├── merge-ssot.py           # SSOT 병합 스크립트
│   └── generate-template.py    # 템플릿 생성기
└── templates/
    ├── SSOT.md.template        # 레거시 템플릿
    └── ...
```

## 🚀 사용법

### 1. 자동 사용 (setup.sh)

```bash
./setup.sh
```

대화형 인터페이스에서 다음을 선택:
- **도메인**: E-Commerce, FinTech, Healthcare 등
- **기능**: AI/ML, Blockchain, IoT 등
- **규정**: GDPR, HIPAA, PCI-DSS 등

### 2. 수동 사용 (직접 스크립트 실행)

```bash
# 기본 + E-Commerce + AI/ML + GDPR
python3 demeter/core/ssot/tools/merge-ssot.py \
  --base demeter/core/ssot/base \
  --extensions \
    demeter/core/ssot/extensions/domain/e-commerce.yaml \
    demeter/core/ssot/extensions/features/ai-ml.yaml \
    demeter/core/ssot/extensions/compliance/gdpr.yaml \
  --output merged-ssot.yaml \
  --project-name "MyShop" \
  --project-type "web-api" \
  --language "go"

# 최종 문서 생성
python3 demeter/core/ssot/tools/generate-template.py \
  --input merged-ssot.yaml \
  --output docs/SSOT.md \
  --project-name "MyShop" \
  --language "Go"
```

### 3. 커스텀 SSOT 추가

프로젝트별 특별한 요구사항이 있다면:

```yaml
# custom/my-project.yaml
extends: "base"
custom: "my-project"

functional_requirements:
  FR-CUSTOM-001:
    name: "특별한 비즈니스 로직"
    description: "프로젝트만의 특화 요구사항"
    priority: "High"
    business_value: "고유 비즈니스 가치"
    acceptance_criteria:
      - "특별한 기능 구현"
      - "성능 최적화"
```

## 🔧 확장 시스템

### 도메인 확장 예시

**E-Commerce (전자상거래)**
- 상품 카탈로그 관리
- 장바구니 시스템
- 주문 처리
- 결제 게이트웨이
- 고객 관리

**FinTech (금융기술)**
- KYC/AML 준수
- 거래 처리
- 위험 관리
- 보고 및 감사
- 보안 강화

### 기능 확장 예시

**AI/ML**
- 모델 관리
- 데이터 파이프라인
- 추론 엔진
- 훈련 자동화

**GDPR 규정 준수**
- 데이터 주체 권리
- 동의 관리
- 개인정보보호
- 침해 대응

## 📊 병합 과정

1. **기본 SSOT 로드**: `base/` 디렉토리의 FR/NFR/UoW
2. **확장 병합**: 선택된 확장들을 순차적으로 병합
3. **ID 충돌 해결**: 자동으로 고유 ID 생성
4. **의존성 업데이트**: 참조 관계 자동 수정
5. **검증**: 모든 의존성 존재 여부 확인
6. **문서 생성**: 최종 SSOT 마크다운 생성

## 🎯 장점

- **모듈화**: 기본/확장/커스텀 분리로 재사용성 향상
- **유연성**: 프로젝트별 맞춤 요구사항 조합
- **일관성**: 표준화된 구조와 검증 프로세스
- **확장성**: 새로운 도메인/기능 쉽게 추가
- **자동화**: 수동 작업 최소화

## 📝 YAML 스키마

### 기본 구조
```yaml
extends: "base"  # 기본 SSOT 확장
domain/feature/compliance: "name"  # 확장 타입

functional_requirements:
  FR-XXX-001:
    name: "요구사항 이름"
    description: "상세 설명"
    priority: "Critical|High|Medium|Low"
    dependencies: ["FR-001", "FR-002"]  # 선택사항
    business_value: "비즈니스 가치"
    acceptance_criteria:
      - "수락 조건 1"
      - "수락 조건 2"
    tags: ["태그1", "태그2"]

non_functional_requirements:
  NFR-XXX-001:
    name: "비기능 요구사항"
    category: "Performance|Security|Usability"
    measurement_criteria:
      - "측정 기준 1"
    testing_method: "테스트 방법"
    priority: "Critical|High|Medium|Low"

units_of_work:
  UoW-XXX-001:
    name: "작업 단위"
    goal: "목표"
    layer: "Foundation|Infrastructure|Application|Deployment"
    dependencies: ["UoW-001"]
    implements: ["FR-001", "NFR-001"]
    estimated_effort_hours: "24"
    acceptance_criteria:
      - "완료 조건"
```

## 🔍 고급 기능

### ID 충돌 자동 해결
```bash
# 충돌 발생 시 자동 리네이밍
FR-001 (base) + FR-001 (extension)
→ FR-001 (base) + FR-ECOMMERCE-001 (extension)
```

### 의존성 자동 업데이트
```yaml
# 병합 전
dependencies: ["FR-001"]

# 병합 후 (ID 변경 반영)
dependencies: ["FR-ECOMMERCE-001"]
```

### 통계 및 검증
- 총 요구사항 수
- 우선순위별 분포
- 레이어별 UoW 분포
- 의존성 검증 결과

이 시스템을 통해 프로젝트별로 최적화된 SSOT를 자동 생성하고, 일관된 품질을 유지할 수 있습니다.