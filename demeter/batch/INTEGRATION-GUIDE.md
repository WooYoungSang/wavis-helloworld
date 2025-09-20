# WAVIS Demeter - UoW 배치 시스템 통합 가이드

이 문서는 WAVIS Demeter 템플릿의 UoW(Unit of Work) 배치 실행 시스템이 어떻게 setup.sh와 통합되어 작동하는지 설명합니다.

## 시스템 개요

### 핵심 구성요소

1. **템플릿화된 스크립트**
   - `scripts/batch-execute-uows.sh.template` - 마스터 배치 실행기
   - `scripts/execute-uow.sh.template` - 개별 UoW 실행기

2. **UoW 관리 도구**
   - `tools/generate-execution-order.py` - 실행 순서 생성기
   - `tools/generate-uow-prompts.py` - 프롬프트 생성기
   - `tools/validate-uow-dependencies.py` - 의존성 검증기

3. **통합 프로세스**
   - `setup.sh`의 `setup_uow_batch_system()` 함수
   - SSOT 병합 후 자동 UoW 시스템 생성

## 작동 원리

### 1. 프로젝트 초기화 시

```bash
./setup.sh
```

1. **사용자 입력** 수집 (프로젝트명, 설명, MVP 단계, 확장 선택)
2. **SSOT 병합** - 기본 요구사항 + 선택된 확장들
3. **UoW 배치 시스템 생성**:
   ```bash
   setup_uow_batch_system()
   ```

### 2. UoW 시스템 생성 과정

#### Step 1: 의존성 검증
```bash
python3 "$DEMETER_DIR/batch/tools/validate-uow-dependencies.py" \
    --input ./merged-ssot.yaml --quiet
```
- 순환 의존성 검사
- 누락된 의존성 확인
- 아키텍처 레이어 규칙 검증

#### Step 2: 실행 순서 생성
```bash
python3 "$DEMETER_DIR/batch/tools/generate-execution-order.py" \
    --input ./merged-ssot.yaml \
    --output ./batch/configs/uow-execution-order.yaml \
    --project-name "$PROJECT_NAME"
```
- 의존성 그래프 분석
- 토폴로지 정렬로 실행 단계 결정
- 병렬 실행 그룹 식별
- YAML 설정 파일 생성

#### Step 3: 프롬프트 생성
```bash
python3 "$DEMETER_DIR/batch/tools/generate-uow-prompts.py" \
    --input ./merged-ssot.yaml \
    --output-dir ./batch/prompts/ \
    --project-name "$PROJECT_NAME"
```
- 각 UoW별 Claude 프롬프트 생성
- 수락 기준(AC) 포함
- 의존성 및 통합 정보 명시
- 기술적 제약사항 추가

#### Step 4: 스크립트 커스터마이징
```bash
sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
    "$DEMETER_DIR/batch/scripts/batch-execute-uows.sh.template" \
    > ./batch/scripts/batch-execute-uows.sh
```
- 템플릿 변수 치환
- 프로젝트별 설정 적용
- 실행 권한 부여

## 생성된 파일 구조

```
project-root/
├── batch/
│   ├── configs/
│   │   └── uow-execution-order.yaml    # 동적 생성
│   ├── scripts/
│   │   ├── batch-execute-uows.sh       # 템플릿에서 생성
│   │   └── execute-uow.sh              # 템플릿에서 생성
│   ├── prompts/
│   │   ├── UoW-000.md                  # 자동 생성
│   │   ├── UoW-001.md                  # 자동 생성
│   │   └── ...                         # 모든 UoW
│   ├── logs/                           # 빈 디렉토리
│   ├── reports/                        # 빈 디렉토리
│   └── README.md                       # setup.sh에서 생성
└── docs/
    └── SSOT.md                         # 병합된 요구사항
```

## 사용 시나리오

### 시나리오 1: 새 프로젝트 시작

```bash
# 1. 프로젝트 초기화
./setup.sh
# → 프로젝트명: "my-saas-project"
# → 프리셋: "Basic SaaS"

# 2. 전체 UoW 실행
./batch/scripts/batch-execute-uows.sh

# 3. 진행 상황 확인
./batch/scripts/batch-execute-uows.sh --dry-run
```

### 시나리오 2: 특정 UoW 디버깅

```bash
# 1. 개별 UoW 실행
./batch/scripts/execute-uow.sh UoW-101 --verbose

# 2. 의존성 확인
./batch/scripts/batch-execute-uows.sh --start-from=UoW-101 --dry-run

# 3. 로그 확인
tail -f batch/logs/UoW-101_*.log
```

### 시나리오 3: CI/CD 파이프라인

```bash
# 1. 배치 실행 (실패 시 중단)
./batch/scripts/batch-execute-uows.sh --timeout=1800

# 2. 테스트 스킵하고 빠른 실행
./batch/scripts/batch-execute-uows.sh --skip-tests --skip-build

# 3. 특정 단계만 배포
./batch/scripts/batch-execute-uows.sh --phase=4
```

## 확장성과 커스터마이징

### 1. 새로운 확장 추가

1. `demeter/core/ssot/extensions/` 디렉토리에 새 확장 추가
2. `setup.sh`에서 확장 선택 옵션 추가
3. 시스템이 자동으로 새 UoW들을 배치 시스템에 통합

### 2. 커스텀 UoW 실행 로직

- `execute-uow.sh.template` 수정으로 실행 로직 커스터마이징
- 테스트 프레임워크별 로직 추가
- 빌드 시스템별 검증 로직 추가

### 3. 프롬프트 템플릿 개선

- `tools/generate-uow-prompts.py`의 템플릿 수정
- 프로젝트별 컨텍스트 추가
- 도메인별 가이드라인 포함

## 모니터링과 디버깅

### 로그 파일들

```bash
# 마스터 배치 로그
tail -f batch/logs/batch_execution_*.log

# 개별 UoW 로그
ls -la batch/logs/UoW-*_*.log

# Claude 실행 로그
ls -la batch/logs/*_claude_*.log
```

### 보고서 확인

```bash
# 배치 실행 보고서
cat batch/reports/batch_execution_report_*.md

# 개별 UoW 보고서
cat batch/reports/UoW-*_*.md
```

### 의존성 문제 해결

```bash
# 의존성 검증
python3 demeter/batch/tools/validate-uow-dependencies.py \
    --input docs/SSOT.yaml --verbose

# 자동 수정 시도
python3 demeter/batch/tools/validate-uow-dependencies.py \
    --input docs/SSOT.yaml --fix-issues --output fixed-ssot.yaml
```

## 성능 최적화

### 병렬 실행

- 시스템이 자동으로 병렬 가능한 UoW 식별
- 같은 레이어의 독립적인 컴포넌트들을 동시 실행
- `--no-parallel` 옵션으로 비활성화 가능

### 선택적 실행

- `--phase=N`으로 특정 단계만 실행
- `--start-from`으로 중간부터 재시작
- `--skip-tests`, `--skip-build`로 단계 생략

### 리소스 관리

- `--timeout` 옵션으로 개별 UoW 타임아웃 설정
- `--retries` 옵션으로 재시도 횟수 조정
- 로그 레벨 조정으로 성능 향상

## 트러블슈팅

### 일반적인 문제들

1. **Python 의존성 오류**
   ```bash
   cd demeter/batch
   ./install-dependencies.sh
   ```

2. **UoW 프롬프트 파일 누락**
   ```bash
   # setup.sh 다시 실행하여 프롬프트 재생성
   python3 demeter/batch/tools/generate-uow-prompts.py \
       --input merged-ssot.yaml --output-dir batch/prompts/
   ```

3. **의존성 순환 오류**
   ```bash
   # 의존성 검증 및 수정
   python3 demeter/batch/tools/validate-uow-dependencies.py \
       --input merged-ssot.yaml --fix-issues
   ```

4. **실행 권한 오류**
   ```bash
   chmod +x batch/scripts/*.sh
   ```

## 결론

이 통합 시스템을 통해:

1. **자동화된 UoW 관리** - SSOT에서 자동으로 실행 계획 생성
2. **프로젝트별 커스터마이징** - 각 프로젝트의 요구사항에 맞는 배치 시스템
3. **확장 가능한 아키텍처** - 새로운 확장과 UoW 자동 통합
4. **강력한 디버깅 도구** - 상세한 로그와 보고서 시스템
5. **병렬 실행 최적화** - 의존성 분석 기반 성능 최적화

WAVIS Demeter 템플릿이 단순한 파일 복사를 넘어 지능적이고 자동화된 프로젝트 초기화 시스템으로 진화했습니다.

---

*이 시스템에 대한 질문이나 개선 제안이 있으시면 프로젝트 이슈 트래커를 통해 문의해 주세요.*