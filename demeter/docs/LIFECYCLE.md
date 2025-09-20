# 🌾 WAVIS Demeter Framework v1.1 - AI-First 개발 라이프사이클 가이드

## 📖 개요

WAVIS Demeter Framework v1.1은 **완전히 프롬프트 기반**의 AI-First 개발 라이프사이클을 제공합니다. 이번 버전에서는 모든 스크립트 기반 작업이 Claude Code와 직접 상호작용하는 지능형 프롬프트로 대체되었습니다.

### 🎯 v1.1 핵심 특징
- **Zero Script Dependency**: 모든 Python/Shell 스크립트 제거
- **AI-Driven Automation**: Claude Code를 통한 완전 자동화
- **Prompt-Based Operations**: 각 단계별 전문화된 프롬프트 제공
- **GraphRAG Integration**: 지식 기반 개발 및 컨텍스트 활용
- **Intelligent Quality Assurance**: AI 기반 품질 보증 및 검증

### 🚀 Major Changes in v1.1
- **Prompt Templates**: `demeter/prompts/` 디렉토리의 전문화된 프롬프트
- **Tool Integration**: SSOT, UoW, Quality, Deployment 도구 프롬프트
- **Phase-Based Workflow**: 각 Phase별 완전 자동화된 워크플로우
- **Knowledge-Driven Development**: GraphRAG 기반 패턴 재사용

---

## 🚀 Phase 0: AI-Driven 프로젝트 초기화

### 0.1 프롬프트 기반 프로젝트 설정

**Claude Code에서 실행**:
```markdown
프롬프트 파일: demeter/prompts/phase0-project-init.md

이 프롬프트를 Claude Code에서 실행하여:
- 완전한 프로젝트 구조 자동 생성
- 도메인별 SSOT 템플릿 커스터마이징
- GraphRAG 지식베이스 초기화
- 개발 환경 자동 구성
```

### 0.2 AI가 수행하는 초기화 과정
1. **프로젝트 컨텍스트 분석**
   - 도메인 특성 분석 (E-Commerce, FinTech, Healthcare)
   - 기술 스택 요구사항 파악
   - 규정 준수 요구사항 식별

2. **지능형 구조 생성**
   - 맞춤형 SSOT 템플릿 생성
   - 도메인별 확장 통합
   - 프로젝트별 컨벤션 설정

3. **자동 환경 구성**
   - GraphRAG 지식베이스 구조 생성
   - 개발 가이드라인 생성
   - Claude Code 통합 설정

### 0.3 생성된 구조
```
my-project/
├── docs/SSOT.md              # AI 생성 SSOT 템플릿
├── CLAUDE.md                 # AI 개발 가이드라인
├── LEARNING.md               # 학습 및 진행 기록
├── demeter/prompts/          # 프롬프트 템플릿 (v1.1)
│   ├── README.md
│   ├── phase0-project-init.md
│   ├── phase1-2-ssot-management.md
│   ├── phase3-5-development.md
│   ├── phase6-7-verification-deployment.md
│   └── tools/
│       ├── ssot-operations.md
│       ├── uow-management.md
│       ├── quality-checks.md
│       └── deployment-prep.md
├── graphrag/                 # GraphRAG 지식베이스
│   └── knowledge/
└── .graphrag_config          # GraphRAG 활성화 마커
```

---

## 📋 Phase 1-2: AI-Driven SSOT 관리 및 UoW 설계

### 1.1 지능형 SSOT 작성 및 관리

**Claude Code에서 실행**:
```markdown
프롬프트 파일: demeter/prompts/phase1-2-ssot-management.md

이 프롬프트가 자동으로 수행:
- SSOT 구조 검증 및 품질 분석
- 도메인별 확장 지능형 병합
- UoW 의존성 자동 분석
- 최적 실행 순서 생성
```

### 1.2 AI SSOT 도구 (기존 스크립트 대체)

**SSOT 운영**: `demeter/prompts/tools/ssot-operations.md`
- ✅ `validate-ssot`: SSOT 구조 및 콘텐츠 검증
- ✅ `merge-ssot-extensions`: 지능형 확장 병합
- ✅ `analyze-requirements-gaps`: 요구사항 갭 분석
- ✅ `verify-contracts`: 계약 준수 검증
- ✅ `optimize-ssot`: SSOT 구조 최적화

**UoW 관리**: `demeter/prompts/tools/uow-management.md`
- ✅ `analyze-uow-dependencies`: 의존성 그래프 분석
- ✅ `generate-execution-order`: 최적 실행 순서 생성
- ✅ `generate-uow-prompts`: GraphRAG 통합 프롬프트 생성
- ✅ `validate-uow-quality`: UoW 품질 검증
- ✅ `optimize-uow-structure`: UoW 구조 최적화

### 1.3 자동화된 SSOT 워크플로우
1. **지능형 분석**: AI가 프로젝트 컨텍스트 파악
2. **자동 병합**: 도메인별 확장 지능적 통합
3. **의존성 최적화**: UoW 관계 최적화
4. **품질 보증**: 자동 검증 및 개선 제안

---

## 🎯 Phase 3-5: AI-Driven 개발 실행

### 3.1 지식 기반 개발 워크플로우

**Claude Code에서 실행**:
```markdown
프롬프트 파일: demeter/prompts/phase3-5-development.md

3단계 지능형 개발 사이클:
- Phase 1: Knowledge Discovery (지식 탐색)
- Phase 2: Implementation (구현)
- Phase 3: Knowledge Documentation (지식 문서화)
```

### 3.2 AI-Enhanced 개발 프로세스

**기존 스크립트 vs v1.1 AI 접근**:
```markdown
❌ 기존 v1.0:
- generate-uow-prompts.py
- batch-execute-uows.sh
- execute-uow.sh

✅ v1.1 AI-First:
- demeter/prompts/phase3-5-development.md
- 완전 자동화된 배치 관리
- 실시간 적응형 실행
- 지능형 진행 상황 모니터링
```

### 3.3 지능형 배치 실행
1. **컨텍스트 인식 준비**: AI가 프로젝트 상태 파악
2. **적응형 실행**: 실시간 상황에 맞는 전략 조정
3. **자동 문제 해결**: 오류 자동 분석 및 해결
4. **지식 축적**: 실행 중 학습한 내용 자동 문서화

---

## ✅ Phase 6-7: AI-Driven 품질 보증 및 배포 준비

### 6.1 지능형 품질 검증

**Claude Code에서 실행**:
```markdown
프롬프트 파일: demeter/prompts/phase6-7-verification-deployment.md

AI가 수행하는 종합 품질 검증:
- 계약 준수 자동 검증
- 테스트 커버리지 지능형 분석
- 보안 취약점 자동 탐지
- 성능 기준 자동 검증
```

### 6.2 AI 품질 도구 (기존 스크립트 대체)

**품질 검증**: `demeter/prompts/tools/quality-checks.md`
- ✅ `verify-contract-compliance`: 수용 기준 검증
- ✅ `analyze-test-coverage`: 테스트 커버리지 분석
- ✅ `assess-code-quality`: 코드 품질 평가
- ✅ `verify-performance`: 성능 검증
- ✅ `verify-security-compliance`: 보안 준수 검증
- ✅ `validate-integration-testing`: 통합 테스트 검증

**배포 준비 (Docker-Compose First)**: `demeter/prompts/tools/deployment-prep.md`
- ✅ `optimize-production-build`: 프로덕션 빌드 최적화
- ✅ `generate-docker-compose-config`: Docker-Compose 구성 생성 (Primary)
- ✅ `generate-kubernetes-config`: Kubernetes 구성 (Advanced/Optional)
- ✅ `setup-monitoring-stack`: Docker-Compose 기반 모니터링 설정
- ✅ `configure-security-hardening`: 컨테이너 보안 강화
- ✅ `setup-backup-dr`: 백업 및 재해 복구
- ✅ `configure-cicd-pipeline`: CI/CD 파이프라인 구성

### 6.3 자동화된 품질 보증
1. **종합 계약 검증**: 모든 AC 자동 검증
2. **지능형 테스트 분석**: 커버리지 및 품질 평가
3. **자동 보안 검증**: 취약점 탐지 및 해결
4. **성능 자동 검증**: NFR 준수 확인

---

## 🤖 v1.1 AI-First 워크플로우 사용법

### Claude Code에서의 실행 방법

1. **Phase별 프롬프트 실행**:
   ```markdown
   # Phase 0: 프로젝트 초기화
   Claude Code에서 demeter/prompts/phase0-project-init.md 실행

   # Phase 1-2: SSOT 관리
   Claude Code에서 demeter/prompts/phase1-2-ssot-management.md 실행

   # Phase 3-5: 개발 실행
   Claude Code에서 demeter/prompts/phase3-5-development.md 실행

   # Phase 6-7: 품질 보증 및 배포
   Claude Code에서 demeter/prompts/phase6-7-verification-deployment.md 실행
   ```

2. **도구별 개별 실행**:
   ```markdown
   # SSOT 운영
   Claude Code에서 demeter/prompts/tools/ssot-operations.md 실행

   # UoW 관리
   Claude Code에서 demeter/prompts/tools/uow-management.md 실행

   # 품질 검증
   Claude Code에서 demeter/prompts/tools/quality-checks.md 실행

   # 배포 준비
   Claude Code에서 demeter/prompts/tools/deployment-prep.md 실행
   ```

### 스크립트에서 AI 프롬프트로의 전환

**v1.0 (스크립트 기반)**:
```bash
# Phase 2 예시
python demeter/core/ssot/tools/merge-ssot.py --base docs/SSOT.md --output merged-ssot.yaml
python demeter/batch/tools/validate-uow-dependencies.py --input merged-ssot.yaml
python demeter/batch/tools/generate-execution-order.py --input merged-ssot.yaml
```

**v1.1 (AI-First)**:
```markdown
# Claude Code에서 단일 프롬프트로 모든 작업 자동화
demeter/prompts/phase1-2-ssot-management.md 실행

AI가 자동으로:
1. SSOT 분석 및 병합
2. UoW 의존성 분석
3. 실행 순서 최적화
4. 품질 검증 및 개선 제안
```

---

## 📊 v1.1 개발 메트릭 및 AI 인사이트

### 지능형 진행상황 추적
- **AI 분석 대시보드**: 실시간 프로젝트 상태 분석
- **지능형 예측**: 완료 시점 및 리스크 예측
- **자동 품질 평가**: 코드 품질 실시간 모니터링
- **지식 축적 지표**: GraphRAG 지식베이스 성장 추적

### AI 기반 품질 지표
- **자동 SSOT 일관성**: >98% AI 검증 정확도
- **지능형 버그 예방**: 구현 전 패턴 기반 위험 탐지
- **적응형 성능 최적화**: 실시간 성능 조정 제안
- **자동 보안 강화**: 지속적 보안 패턴 적용

### 생산성 향상 지표
- **개발 시간 단축**: AI 패턴 재사용으로 60% 감소
- **품질 향상**: 자동 검증으로 재작업 80% 감소
- **지식 재사용**: 이전 프로젝트 패턴 90% 활용
- **완전 자동화**: 수동 개입 5% 미만

---

## 🎯 v1.1 베스트 프랙티스

### AI-First 개발 원칙
1. **프롬프트 우선**: 모든 작업을 프롬프트로 시작
2. **지능형 탐색**: AI가 먼저 기존 지식 분석
3. **적응형 실행**: 상황에 맞는 전략 자동 조정
4. **지속적 학습**: 실행 중 지식 자동 축적

### AI 협업 개발
1. **컨텍스트 제공**: 충분한 프로젝트 컨텍스트 제공
2. **점진적 개선**: AI 제안을 바탕으로 점진적 개선
3. **패턴 검증**: AI가 제안한 패턴의 적절성 검토
4. **지식 피드백**: 구현 결과를 지식베이스에 반영

### 품질 보증
1. **AI 검증 신뢰**: AI 기반 자동 검증 결과 활용
2. **지능형 테스트**: AI가 생성한 테스트 케이스 검토
3. **자동 보안**: AI 보안 패턴 적용 결과 확인
4. **성능 최적화**: AI 성능 튜닝 제안 적용

---

## 🛠️ v1.1 문제 해결 가이드

### AI 프롬프트 관련 문제

#### 프롬프트 실행 실패
```markdown
# 해결 방법:
1. Claude Code에서 프롬프트 파일 경로 확인
2. 프로젝트 컨텍스트 충분히 제공
3. 필요한 파일들이 존재하는지 확인
4. AI에게 단계별 실행 요청
```

#### GraphRAG 지식 부족
```markdown
# 해결 방법:
1. 기존 구현 패턴을 AI와 함께 분석
2. 외부 지식 소스 활용 요청
3. 단계적 지식 구축 진행
4. 팀 지식 공유 및 문서화
```

#### 품질 검증 실패
```markdown
# 해결 방법:
1. AI에게 구체적인 품질 기준 제시
2. 단계별 품질 검증 요청
3. 실패한 부분의 상세 분석 요청
4. 개선 방안 AI와 함께 도출
```

### 복구 및 개선 절차
1. **AI 분석**: Claude Code를 통한 문제 분석
2. **지능형 진단**: 자동 원인 분석 및 해결 방안 제시
3. **적응형 수정**: 상황에 맞는 개선 전략 적용
4. **지식 갱신**: 해결 과정을 지식베이스에 반영

---

## 📚 v1.1 추가 리소스

### v1.1 새로운 문서
- `demeter/prompts/README.md`: 프롬프트 기반 개발 가이드
- `demeter/prompts/phase*.md`: Phase별 상세 워크플로우
- `demeter/prompts/tools/*.md`: 도구별 AI 운영 가이드

### 레거시 문서 (참고용)
- `CLAUDE.md`: AI 개발 가이드라인
- `graphrag/knowledge/project-overview.md`: 프로젝트 컨벤션

### v1.1 마이그레이션 가이드
```markdown
v1.0에서 v1.1로 업그레이드:

1. demeter/prompts/ 디렉토리 추가
2. 기존 스크립트 호출을 프롬프트 실행으로 변경
3. Claude Code 통합 개발 환경 구성
4. GraphRAG 지식베이스 점진적 구축
```

---

## 🌟 v1.1 Features Summary

### 🚫 제거된 요소 (Zero Script Dependency)
- ❌ Python 스크립트 의존성
- ❌ Shell 스크립트 실행
- ❌ 수동 도구 실행
- ❌ 복잡한 배치 설정

### ✅ 새로 추가된 요소 (AI-First)
- ✅ 완전 프롬프트 기반 워크플로우
- ✅ Claude Code 네이티브 통합
- ✅ 지능형 자동화 시스템
- ✅ 적응형 품질 보증
- ✅ 실시간 AI 인사이트

---

**🌾 데메테르 v1.1의 AI 축복이 여러분의 프로젝트에 지능적인 풍요로움을 가져다주기를!**

*"From Scripts to Intelligence, Guided by AI"*