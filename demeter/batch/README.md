# 🤖 WAVIS Demeter Batch Execution System

## 📖 개요

Demeter Batch Execution System은 SSOT에서 정의된 UoW(Unit of Work)를 순차적으로 자동 실행하는 시스템입니다. GraphRAG 지식 관리가 완전히 통합되어, AI가 이전 구현 지식을 활용하여 새로운 UoW를 구현합니다.

### 🎯 핵심 특징
- **자동화된 UoW 실행**: 의존성 기반 순차 실행
- **GraphRAG 통합**: 프롬프트 레벨에서 지식 관리 워크플로우 통합
- **AI 협업**: Claude Code와 완전 통합된 개발 워크플로우
- **품질 보증**: 자동 테스트 및 빌드 검증
- **지식 축적**: 각 UoW 구현 시 자동 지식 문서화

---

## 🏗️ 시스템 아키텍처

### 디렉토리 구조
```
demeter/batch/
├── configs/
│   └── uow-execution-order.yaml    # UoW 실행 순서 정의
├── prompts/
│   ├── UoW-001.md                  # UoW별 통합 프롬프트
│   └── UoW-002.md
├── scripts/
│   ├── batch-execute-uows.sh       # 배치 실행 마스터 스크립트
│   └── execute-uow.sh              # 개별 UoW 실행 스크립트
├── templates/
│   └── uow-prompt-template.md      # GraphRAG 통합 프롬프트 템플릿
├── tools/
│   ├── generate-execution-order.py # 실행 순서 생성
│   ├── generate-uow-prompts.py     # 프롬프트 생성
│   └── validate-uow-dependencies.py # 의존성 검증
├── logs/                           # 실행 로그
└── reports/                        # 실행 보고서
```

### GraphRAG 지식베이스 구조
```
graphrag/knowledge/
├── implementations/                # UoW 구현 지식
│   ├── UoW-001.md                 # 자동 생성된 구현 문서
│   └── UoW-002.md
├── patterns/                      # 아키텍처 패턴
│   ├── common-patterns.md         # 공통 패턴
│   └── layer-specific-patterns.md # 레이어별 패턴
├── lessons/                       # 교훈 및 베스트 프랙티스
├── decisions/                     # 기술적 결정 사항
└── project-overview.md            # 프로젝트 전체 컨벤션
```

---

## ⚡ 시작하기

### 1. 전제 조건
```bash
# SSOT가 병합되고 UoW가 정의되어 있어야 함
ls merged-ssot.yaml

# Claude Code CLI 설치 및 설정
claude --version

# GraphRAG 초기화 완료
ls .graphrag_config
```

### 2. 배치 시스템 설정
```bash
# UoW 실행 순서 생성
python demeter/batch/tools/generate-execution-order.py \
    --input merged-ssot.yaml \
    --output demeter/batch/configs/uow-execution-order.yaml

# GraphRAG 통합 프롬프트 생성
python demeter/batch/tools/generate-uow-prompts.py \
    --input merged-ssot.yaml \
    --output-dir demeter/batch/prompts/ \
    --project-name "My Project"
```

### 3. 배치 실행
```bash
# 전체 UoW 배치 실행
./demeter/batch/scripts/batch-execute-uows.sh

# 드라이런으로 실행 계획 확인
./demeter/batch/scripts/batch-execute-uows.sh --dry-run
```

---

## 🎯 GraphRAG 통합 워크플로우

### 프롬프트 기반 지식 관리

각 UoW 프롬프트는 3단계 워크플로우를 포함합니다:

#### Phase 1: Knowledge Discovery and Context Analysis
```markdown
### 1.1 Dependency Analysis
- Read `graphrag/knowledge/implementations/UoW-XXX.md` for dependency implementations
- Identify interfaces and integration points
- Extract reusable patterns

### 1.2 Pattern Discovery
- Check `graphrag/knowledge/patterns/` for applicable patterns
- Review layer-specific patterns
- Identify common solutions

### 1.3 Convention Review
- Read `graphrag/knowledge/project-overview.md` for conventions
- Follow established coding standards
- Apply architectural principles
```

#### Phase 2: Implementation
```markdown
### Implementation Guidelines
1. **Follow Discovered Patterns**: Apply patterns from Phase 1
2. **Reuse Components**: Utilize interfaces from dependency UoWs
3. **Maintain Consistency**: Follow project conventions
4. **Layer Compliance**: Ensure proper layer responsibilities
```

#### Phase 3: Knowledge Documentation
```markdown
### 3.1 Implementation Knowledge Document
Create `graphrag/knowledge/implementations/UoW-XXX.md` with:
- Implementation overview
- Key components and interfaces
- Patterns applied
- Integration points
- Technical decisions
- Lessons learned

### 3.2 Pattern Updates
- Update pattern documents with new discoveries
- Document reusable components
- Record architectural decisions
```

### 자동 지식 축적
- **구현 중**: Claude가 관련 지식 탐색 및 적용
- **구현 후**: 자동으로 지식 문서 생성
- **패턴 발견**: 새로운 패턴 자동 식별 및 문서화
- **교훈 기록**: 구현 과정에서 얻은 인사이트 저장

---

## 🛠️ 사용법

### 배치 실행 옵션

#### 전체 배치 실행
```bash
# 기본 실행
./demeter/batch/scripts/batch-execute-uows.sh

# 상세 로그와 함께 실행
./demeter/batch/scripts/batch-execute-uows.sh --verbose

# 실패 시에도 계속 진행
./demeter/batch/scripts/batch-execute-uows.sh --continue-on-failure
```

#### 부분 실행
```bash
# 특정 UoW부터 시작
./demeter/batch/scripts/batch-execute-uows.sh --start-from=UoW-005

# 특정 UoW에서 중단
./demeter/batch/scripts/batch-execute-uows.sh --stop-at=UoW-010

# 특정 단계만 실행
./demeter/batch/scripts/batch-execute-uows.sh --phase=2
```

#### 테스트 및 빌드 옵션
```bash
# 테스트 스킵
./demeter/batch/scripts/batch-execute-uows.sh --skip-tests

# 빌드 스킵
./demeter/batch/scripts/batch-execute-uows.sh --skip-build

# 병렬 실행 비활성화
./demeter/batch/scripts/batch-execute-uows.sh --no-parallel
```

### 개별 UoW 실행

#### 기본 실행
```bash
# 개별 UoW 실행
./demeter/batch/scripts/execute-uow.sh UoW-001

# 드라이런
./demeter/batch/scripts/execute-uow.sh UoW-001 --dry-run

# 상세 로그
./demeter/batch/scripts/execute-uow.sh UoW-001 --verbose
```

#### 고급 옵션
```bash
# 타임아웃 설정 (초)
./demeter/batch/scripts/execute-uow.sh UoW-001 --timeout=7200

# 재시도 횟수
./demeter/batch/scripts/execute-uow.sh UoW-001 --retry=3

# 실패 시에도 계속
./demeter/batch/scripts/execute-uow.sh UoW-001 --continue
```

---

## 📊 모니터링 및 로깅

### 로그 구조
```bash
# 배치 실행 마스터 로그
demeter/batch/logs/batch_execution_YYYYMMDD_HHMMSS.log

# 개별 UoW 로그
demeter/batch/logs/UoW-XXX_YYYYMMDD_HHMMSS.log

# Claude Code 실행 로그
demeter/batch/logs/UoW-XXX_claude_YYYYMMDD_HHMMSS.log

# 테스트 실행 로그
demeter/batch/logs/UoW-XXX_test_YYYYMMDD_HHMMSS.log
```

### 실시간 모니터링
```bash
# 배치 실행 상태 모니터링
tail -f demeter/batch/logs/batch_execution_*.log

# 개별 UoW 진행상황
tail -f demeter/batch/logs/UoW-001_*.log

# 에러 로그만 확인
grep "ERROR\|FAILED" demeter/batch/logs/*.log
```

### 보고서 생성
```bash
# 실행 완료 후 자동 생성되는 보고서
cat demeter/batch/reports/batch_execution_report_YYYYMMDD_HHMMSS.md

# GraphRAG 지식베이스 요약
cat graphrag/knowledge/batch-executions/batch_YYYYMMDD_HHMMSS.md
```

---

## 🔧 설정 및 커스터마이징

### 실행 순서 설정

#### uow-execution-order.yaml 구조
```yaml
execution_phases:
  - phase: 1
    name: "Foundation Layer"
    parallel_groups:
      - uows: ["UoW-001", "UoW-002"]
        max_parallel: 2
  - phase: 2
    name: "Infrastructure Layer"
    parallel_groups:
      - uows: ["UoW-003"]
        dependencies: ["UoW-001", "UoW-002"]

uow_metadata:
  UoW-001:
    name: "Database Layer"
    layer: "Foundation"
    estimated_hours: 4
    dependencies: []
```

#### 실행 순서 재생성
```bash
# 의존성 변경 후 실행 순서 업데이트
python demeter/batch/tools/generate-execution-order.py \
    --input merged-ssot.yaml \
    --output demeter/batch/configs/uow-execution-order.yaml \
    --optimize-parallel
```

### 프롬프트 커스터마이징

#### 템플릿 수정
```bash
# 프롬프트 템플릿 편집
nano demeter/batch/templates/uow-prompt-template.md

# 프롬프트 재생성
python demeter/batch/tools/generate-uow-prompts.py \
    --input merged-ssot.yaml \
    --output-dir demeter/batch/prompts/ \
    --project-name "My Project" \
    --regenerate
```

#### 프로젝트별 컨벤션 추가
```bash
# 프로젝트 개요 편집
nano graphrag/knowledge/project-overview.md

# 패턴 문서 추가
echo "## New Pattern\n..." >> graphrag/knowledge/patterns/common-patterns.md
```

---

## 🚨 문제 해결

### 일반적인 문제들

#### UoW 실행 실패
```bash
# 1. 로그 확인
tail -50 demeter/batch/logs/UoW-XXX_*.log

# 2. 계약 검증
python demeter/core/ssot/tools/verify-contracts.py --uow UoW-XXX

# 3. 의존성 확인
python demeter/batch/tools/validate-uow-dependencies.py --focus UoW-XXX

# 4. 수동 재실행
./demeter/batch/scripts/execute-uow.sh UoW-XXX --verbose
```

#### GraphRAG 지식 누락
```bash
# 지식베이스 상태 확인
ls -la graphrag/knowledge/implementations/

# 누락된 지식 문서 수동 요청
# Claude에게 "UoW-XXX 구현 후 지식 문서를 생성해주세요" 요청
```

#### 의존성 순환 참조
```bash
# 의존성 그래프 분석
python demeter/batch/tools/validate-uow-dependencies.py \
    --input merged-ssot.yaml \
    --check-cycles

# 순환 참조 해결 후 실행 순서 재생성
python demeter/batch/tools/generate-execution-order.py \
    --input merged-ssot.yaml \
    --output demeter/batch/configs/uow-execution-order.yaml
```

#### Claude Code 연결 실패
```bash
# Claude CLI 상태 확인
claude --version

# 프로젝트 권한 확인
claude auth status

# 재연결
claude auth login
```

### 복구 절차

#### 배치 실행 중단 후 재시작
```bash
# 1. 마지막 성공한 UoW 확인
grep "completed successfully" demeter/batch/logs/batch_execution_*.log

# 2. 해당 UoW 다음부터 재시작
./demeter/batch/scripts/batch-execute-uows.sh --start-from=UoW-XXX

# 3. 실패한 UoW만 재실행
./demeter/batch/scripts/execute-uow.sh UoW-FAILED --verbose
```

#### 지식베이스 복구
```bash
# 1. 백업에서 복원
tar -xzf graphrag-knowledge-backup.tar.gz

# 2. 누락된 구현 지식 재생성
# 각 완료된 UoW에 대해 Claude에게 지식 문서 생성 요청

# 3. 패턴 문서 재구성
# 기존 구현들을 분석하여 패턴 추출
```

---

## 📈 성능 및 최적화

### 실행 시간 최적화

#### 병렬 실행 설정
```yaml
# uow-execution-order.yaml에서 병렬 그룹 최적화
parallel_groups:
  - uows: ["UoW-001", "UoW-002", "UoW-003"]
    max_parallel: 3  # 동시 실행 개수
```

#### 타임아웃 조정
```bash
# 복잡한 UoW의 경우 타임아웃 증가
./demeter/batch/scripts/execute-uow.sh UoW-COMPLEX --timeout=10800  # 3시간
```

### 리소스 사용량 모니터링
```bash
# CPU/메모리 사용량 모니터링
top -p $(pgrep -f "batch-execute-uows")

# 디스크 사용량 확인
du -sh demeter/batch/logs/
du -sh graphrag/knowledge/
```

### 지식베이스 최적화
```bash
# 오래된 로그 정리
find demeter/batch/logs/ -name "*.log" -mtime +30 -delete

# 지식베이스 압축
tar -czf graphrag-knowledge-archive-$(date +%Y%m%d).tar.gz graphrag/knowledge/
```

---

## 🔮 고급 기능

### 커스텀 UoW 실행 훅

#### Pre-execution 훅
```bash
# demeter/batch/hooks/pre-uow-hook.sh 생성
#!/bin/bash
UOW_ID=$1
echo "Starting custom preparation for $UOW_ID"
# 사용자 정의 준비 작업
```

#### Post-execution 훅
```bash
# demeter/batch/hooks/post-uow-hook.sh 생성
#!/bin/bash
UOW_ID=$1
SUCCESS=$2
echo "Completed $UOW_ID with status: $SUCCESS"
# 사용자 정의 후처리 작업
```

### 외부 도구 통합

#### CI/CD 파이프라인 통합
```yaml
# .github/workflows/uow-batch.yml
name: UoW Batch Execution
on:
  push:
    branches: [main]
jobs:
  batch-execution:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run UoW Batch
        run: ./demeter/batch/scripts/batch-execute-uows.sh --no-parallel
```

#### Slack 알림 통합
```bash
# demeter/batch/hooks/slack-notify.sh
#!/bin/bash
curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"UoW '$1' completed: '$2'"}' \
    $SLACK_WEBHOOK_URL
```

### 지식베이스 쿼리 인터페이스

#### 웹 인터페이스 (선택사항)
```bash
# GraphRAG 지식 검색 웹 서버 시작
python demeter/batch/tools/knowledge-server.py --port 8080

# 브라우저에서 접근
open http://localhost:8080
```

#### API 쿼리
```bash
# RESTful API로 지식 검색
curl "http://localhost:8080/api/search?q=authentication&type=implementations"
```

---

## 📚 참고 자료

### 관련 문서
- [전체 개발 라이프사이클 가이드](../docs/LIFECYCLE.md)
- [SSOT 작성 가이드](../demeter/core/ssot/README.md)
- [GraphRAG 사용법](../graphrag/README.md)

### 예제 프로젝트
- `demeter/examples/`: 다양한 도메인 예제
- `demeter/references/`: 언어별 구현 가이드

### 커뮤니티
- GitHub Issues: 버그 리포트 및 기능 요청
- Discussions: 사용 경험 공유
- Wiki: 고급 패턴 및 확장 가이드

---

## 🎯 베스트 프랙티스

### 배치 실행
1. **점진적 실행**: 전체 배치 전에 작은 그룹으로 테스트
2. **모니터링**: 실행 중 로그 실시간 확인
3. **백업**: 중요한 단계 전 지식베이스 백업
4. **검증**: 각 단계 완료 후 품질 검증

### 지식 관리
1. **일관성**: 지식 문서 작성 표준 준수
2. **완전성**: 모든 구현에 대한 지식 문서화
3. **검색성**: 키워드 기반 검색 지원
4. **진화**: 지식베이스 지속적 개선

### 문제 해결
1. **로그 우선**: 문제 발생 시 로그 먼저 확인
2. **격리**: 문제 UoW 분리하여 분석
3. **재현**: 문제 상황 재현 가능한 환경 구성
4. **문서화**: 해결 과정 지식베이스에 기록

---

**🤖 AI와 함께하는 효율적인 배치 실행으로 프로젝트 성공을 이루세요!**

*"Automated Excellence, Guided by Knowledge"*