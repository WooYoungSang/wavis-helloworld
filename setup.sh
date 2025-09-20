#!/bin/bash

# 🌾 Demeter - WAVIS Template Setup Script
# Initializes a new project from Demeter template seed system

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEMETER_DIR="$SCRIPT_DIR/demeter"

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}🌾 $1${NC}"
}

warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Setup UoW batch execution system
setup_uow_batch_system() {
    local uow_batch_setup_success=false

    # Create batch directories
    mkdir -p batch/{configs,scripts,prompts,logs,reports}

    # Check if we have the merged SSOT file
    if [ -f "./merged-ssot.yaml" ]; then
        log "SSOT에서 UoW 정보 추출 중..."

        # Validate dependencies first
        if python3 "$DEMETER_DIR/batch/tools/validate-uow-dependencies.py" \
            --input ./merged-ssot.yaml --quiet; then
            log "UoW 의존성 검증 완료"

            # Generate execution order
            if python3 "$DEMETER_DIR/batch/tools/generate-execution-order.py" \
                --input ./merged-ssot.yaml \
                --output ./batch/configs/uow-execution-order.yaml \
                --project-name "$PROJECT_NAME"; then
                log "UoW 실행 순서 생성 완료"

                # Generate UoW prompts
                if python3 "$DEMETER_DIR/batch/tools/generate-uow-prompts.py" \
                    --input ./merged-ssot.yaml \
                    --output-dir ./batch/prompts/ \
                    --project-name "$PROJECT_NAME"; then
                    log "UoW 프롬프트 생성 완료"
                    uow_batch_setup_success=true
                else
                    warn "UoW 프롬프트 생성 실패"
                fi
            else
                warn "UoW 실행 순서 생성 실패"
            fi
        else
            warn "UoW 의존성 검증 실패 - 배치 시스템을 건너뜁니다"
        fi
    else
        warn "merged-ssot.yaml을 찾을 수 없습니다 - 기본 배치 시스템을 설정합니다"
    fi

    # Copy and customize batch execution scripts
    if [ -f "$DEMETER_DIR/batch/scripts/batch-execute-uows.sh.template" ]; then
        log "배치 실행 스크립트 생성 중..."
        sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
            -e "s/{{PROJECT_DESCRIPTION}}/$PROJECT_DESCRIPTION/g" \
            "$DEMETER_DIR/batch/scripts/batch-execute-uows.sh.template" \
            > ./batch/scripts/batch-execute-uows.sh
        chmod +x ./batch/scripts/batch-execute-uows.sh
    fi

    if [ -f "$DEMETER_DIR/batch/scripts/execute-uow.sh.template" ]; then
        sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
            -e "s/{{PROJECT_DESCRIPTION}}/$PROJECT_DESCRIPTION/g" \
            "$DEMETER_DIR/batch/scripts/execute-uow.sh.template" \
            > ./batch/scripts/execute-uow.sh
        chmod +x ./batch/scripts/execute-uow.sh
    fi

    # Copy additional tools
    if [ -d "$DEMETER_DIR/batch/scripts" ]; then
        for script in "$DEMETER_DIR/batch/scripts"/*.sh; do
            if [ -f "$script" ] && [[ ! "$script" == *".template" ]]; then
                script_name=$(basename "$script")
                if [ ! -f "./batch/scripts/$script_name" ]; then
                    cp "$script" "./batch/scripts/"
                    chmod +x "./batch/scripts/$script_name"
                fi
            fi
        done
    fi

    # Create batch README
    cat > ./batch/README.md << EOF
# $PROJECT_NAME - UoW Batch Execution System

이 디렉토리는 $PROJECT_NAME 프로젝트의 모든 UoW(Unit of Work)를 Claude Code Headless 모드로 자동 실행하는 시스템입니다.

## 구조

\`\`\`
batch/
├── configs/
│   └── uow-execution-order.yaml    # UoW 실행 순서 및 설정
├── scripts/
│   ├── batch-execute-uows.sh       # 전체 배치 실행 마스터 스크립트
│   └── execute-uow.sh              # 개별 UoW 실행 스크립트
├── prompts/                        # 각 UoW별 Claude 프롬프트 파일
├── logs/                           # 실행 로그 저장
└── reports/                        # 실행 보고서 저장
\`\`\`

## 사용법

### 전체 UoW 배치 실행

\`\`\`bash
# 모든 UoW 순차 실행
./batch/scripts/batch-execute-uows.sh

# 드라이런 (실행 계획만 확인)
./batch/scripts/batch-execute-uows.sh --dry-run

# 상세 로그와 함께 실행
./batch/scripts/batch-execute-uows.sh --verbose

# 특정 단계만 실행
./batch/scripts/batch-execute-uows.sh --phase=2

# 특정 UoW부터 시작
./batch/scripts/batch-execute-uows.sh --start-from=UoW-101
\`\`\`

### 개별 UoW 실행

\`\`\`bash
# 개별 UoW 실행
./batch/scripts/execute-uow.sh UoW-001

# 드라이런으로 개별 UoW 확인
./batch/scripts/execute-uow.sh UoW-101 --dry-run

# 타임아웃 설정
./batch/scripts/execute-uow.sh UoW-140 --timeout=7200
\`\`\`

## 환경 변수

- \`CLAUDE_MODEL\`: 사용할 Claude 모델 (기본값: claude-3-5-sonnet-20241022)
- \`PROJECT_NAME\`: 프로젝트 이름 (기본값: $PROJECT_NAME)

## 로그 및 보고서

- \`logs/\`: 실행 로그 파일들
- \`reports/\`: 실행 결과 보고서들

## 문제 해결

일반적인 문제 해결 방법은 각 스크립트의 \`--help\` 옵션을 참조하세요.

---

Generated by Demeter template system on $(date)
EOF

    if [ "$uow_batch_setup_success" = true ]; then
        log "✨ UoW 배치 시스템 설정 완료!"
    else
        warn "UoW 배치 시스템이 부분적으로만 설정되었습니다"
    fi
}

# Initialize GraphRAG knowledge system
initialize_graphrag_system() {
    log "GraphRAG 지식 관리 시스템 초기화 중..."

    # Create basic GraphRAG directory structure
    mkdir -p graphrag/knowledge/{implementations,patterns,lessons,decisions}
    mkdir -p graphrag/knowledge/batch-executions

    # Create project overview knowledge file
    cat > graphrag/knowledge/project-overview.md << EOF
# $PROJECT_NAME - Project Overview

## Project Information
- **Name**: $PROJECT_NAME
- **Created**: $(date '+%Y-%m-%d')
- **Template**: WAVIS Demeter Template System

## Architecture Overview
This project follows a structured Unit of Work (UoW) approach where implementation knowledge is systematically captured and reused.

## Conventions
- Follow established patterns for each architectural layer
- Document implementation decisions for future reference
- Maintain consistent coding standards across all UoWs
- Use dependency injection for external services
- Implement comprehensive error handling and logging

## Knowledge Management
- Implementation knowledge: \`graphrag/knowledge/implementations/\`
- Architecture patterns: \`graphrag/knowledge/patterns/\`
- Lessons learned: \`graphrag/knowledge/lessons/\`
- Technical decisions: \`graphrag/knowledge/decisions/\`

---
*Auto-generated project overview*
EOF

    # Create pattern template files
    cat > graphrag/knowledge/patterns/common-patterns.md << EOF
# Common Architecture Patterns

## Dependency Injection
Standard pattern for managing dependencies across all layers.

## Error Handling
Consistent error handling approach with proper logging and recovery.

## Interface Design
Clean interface definitions for component interactions.

---
*Patterns will be documented as UoWs are implemented*
EOF

    # Create GraphRAG integration marker
    echo "graphrag_enabled=true" > ./.graphrag_config
    echo "graphrag_directory=./graphrag" >> ./.graphrag_config

    log_success "✨ GraphRAG 지식 관리 시스템 설정 완료!"
    log "  • 지식베이스: ./graphrag/knowledge/"
    log "  • 구현 문서: ./graphrag/knowledge/implementations/"
    log "  • 패턴 문서: ./graphrag/knowledge/patterns/"
    log "  • UoW 프롬프트에 통합된 워크플로우"
}

echo -e "${BLUE}"
echo "🌾 =========================================="
echo "   Demeter - WAVIS Template Initialization"
echo "   그리스 신화의 수확의 여신이 축복하는"
echo "   새로운 프로젝트의 탄생"
echo "==========================================${NC}"
echo

# Check if Demeter exists
if [ ! -d "$DEMETER_DIR" ]; then
    error "Demeter directory not found at $DEMETER_DIR"
    exit 1
fi

# Interactive configuration
echo "🎯 프로젝트 설정을 시작합니다..."
echo

read -p "📝 프로젝트 이름을 입력하세요: " PROJECT_NAME
if [ -z "$PROJECT_NAME" ]; then
    error "프로젝트 이름은 필수입니다"
    exit 1
fi

read -p "📝 프로젝트 설명을 입력하세요 (선택사항): " PROJECT_DESCRIPTION

echo
echo "🎯 MVP 단계를 선택하세요:"
echo "1) Phase 1 - Core MVP (핵심 비즈니스 가치 검증)"
echo "2) Phase 2 - Extended MVP (사용자 피드백 반영 및 확장 기능)"
echo "3) Phase 3 - Production Ready (운영 환경 배포 및 확장성 확보)"
read -p "선택 (1-3): " MVP_PHASE_CHOICE

case $MVP_PHASE_CHOICE in
    1) MVP_PHASE="phase_1" ;;
    2) MVP_PHASE="phase_2" ;;
    3) MVP_PHASE="phase_3" ;;
    *) MVP_PHASE="phase_1" ;;
esac

echo
echo "🎯 프로젝트 유형을 선택하세요:"
echo "1) 프리셋 사용 (추천)"
echo "2) 개별 확장 선택 (고급)"
read -p "선택 (1-2): " CONFIG_TYPE

if [ "$CONFIG_TYPE" = "1" ]; then
    echo
    echo "📦 사용 가능한 프리셋:"
    echo "1) Basic SaaS - 기본적인 SaaS 애플리케이션 (4-8주)"
    echo "2) Startup E-Commerce - 전자상거래 스타트업 MVP (8-12주)"
    echo "3) Real-time Streaming - 실시간 데이터 처리 서비스 (12-18주)"
    echo "4) Enterprise FinTech - 엔터프라이즈급 금융 플랫폼 (16-24주)"
    echo "5) Healthcare IoT - 헬스케어 IoT 플랫폼 (20-32주)"
    echo "6) Crypto DeFi - 암호화폐 DeFi 플랫폼 (24-36주)"
    read -p "프리셋 선택 (1-6): " PRESET_CHOICE

    case $PRESET_CHOICE in
        1) PRESET_ID="basic-saas" ;;
        2) PRESET_ID="startup-ecommerce" ;;
        3) PRESET_ID="realtime-streaming" ;;
        4) PRESET_ID="enterprise-fintech" ;;
        5) PRESET_ID="healthcare-iot" ;;
        6) PRESET_ID="crypto-defi" ;;
        *) PRESET_ID="basic-saas" ;;
    esac

    # Load preset configuration
    if [ -f "$DEMETER_DIR/core/ssot/extension-presets.yaml" ]; then
        log "프리셋 '$PRESET_ID' 로딩 중..."
        # Extract extensions from preset (simplified - would need proper YAML parsing)
        case $PRESET_ID in
            "basic-saas")
                DOMAIN_EXTENSION=""
                FEATURE_EXTENSIONS=""
                COMPLIANCE_EXTENSIONS="compliance/gdpr.yaml"
                MVP_PHASE="phase_1"
                ;;
            "startup-ecommerce")
                DOMAIN_EXTENSION="domain/e-commerce.yaml"
                FEATURE_EXTENSIONS="features/ai-ml.yaml"
                COMPLIANCE_EXTENSIONS="compliance/gdpr.yaml"
                MVP_PHASE="phase_2"
                ;;
            "realtime-streaming")
                DOMAIN_EXTENSION=""
                FEATURE_EXTENSIONS="features/streaming.yaml features/iot.yaml features/ai-ml.yaml"
                COMPLIANCE_EXTENSIONS="compliance/gdpr.yaml"
                MVP_PHASE="phase_2"
                ;;
            "enterprise-fintech")
                DOMAIN_EXTENSION="domain/fintech.yaml"
                FEATURE_EXTENSIONS="features/blockchain.yaml features/ai-ml.yaml"
                COMPLIANCE_EXTENSIONS="compliance/pci-dss.yaml compliance/gdpr.yaml"
                MVP_PHASE="phase_3"
                ;;
            "healthcare-iot")
                DOMAIN_EXTENSION="domain/healthcare.yaml"
                FEATURE_EXTENSIONS="features/iot.yaml features/ai-ml.yaml"
                COMPLIANCE_EXTENSIONS="compliance/hipaa.yaml compliance/gdpr.yaml"
                MVP_PHASE="phase_3"
                ;;
            "crypto-defi")
                DOMAIN_EXTENSION="domain/fintech.yaml"
                FEATURE_EXTENSIONS="features/blockchain.yaml"
                COMPLIANCE_EXTENSIONS=""
                MVP_PHASE="phase_3"
                ;;
        esac
    else
        warn "프리셋 파일을 찾을 수 없습니다. 기본 설정을 사용합니다."
        DOMAIN_EXTENSION=""
        FEATURE_EXTENSIONS=""
        COMPLIANCE_EXTENSIONS=""
    fi
else
    echo
    echo "🏢 도메인 확장을 선택하세요 (선택사항):"
    echo "1) 없음 (기본)"
    echo "2) E-Commerce (전자상거래)"
    echo "3) FinTech (금융기술)"
    echo "4) Healthcare (헬스케어)"
    read -p "선택 (1-4): " DOMAIN_CHOICE

    case $DOMAIN_CHOICE in
        1) DOMAIN_EXTENSION="" ;;
        2) DOMAIN_EXTENSION="domain/e-commerce.yaml" ;;
        3) DOMAIN_EXTENSION="domain/fintech.yaml" ;;
        4) DOMAIN_EXTENSION="domain/healthcare.yaml" ;;
        *) DOMAIN_EXTENSION="" ;;
    esac

    echo
    echo "🔧 추가 기능을 선택하세요 (복수 선택 가능, 스페이스로 구분):"
    echo "예: '1 3' 입력 시 AI/ML과 IoT 모두 선택"
    echo "1) AI/ML 통합"
    echo "2) Blockchain"
    echo "3) IoT 디바이스 연동"
    echo "4) 실시간 스트리밍"
    read -p "선택 (번호들을 스페이스로 구분): " FEATURE_CHOICES

    FEATURE_EXTENSIONS=""
    for choice in $FEATURE_CHOICES; do
        case $choice in
            1) FEATURE_EXTENSIONS="$FEATURE_EXTENSIONS features/ai-ml.yaml" ;;
            2) FEATURE_EXTENSIONS="$FEATURE_EXTENSIONS features/blockchain.yaml" ;;
            3) FEATURE_EXTENSIONS="$FEATURE_EXTENSIONS features/iot.yaml" ;;
            4) FEATURE_EXTENSIONS="$FEATURE_EXTENSIONS features/streaming.yaml" ;;
        esac
    done

    echo
    echo "📜 규정 준수 요구사항을 선택하세요 (복수 선택 가능):"
    echo "1) 없음"
    echo "2) GDPR (EU 개인정보보호)"
    echo "3) HIPAA (의료정보)"
    echo "4) PCI-DSS (결제카드)"
    read -p "선택 (번호들을 스페이스로 구분): " COMPLIANCE_CHOICES

    COMPLIANCE_EXTENSIONS=""
    for choice in $COMPLIANCE_CHOICES; do
        case $choice in
            2) COMPLIANCE_EXTENSIONS="$COMPLIANCE_EXTENSIONS compliance/gdpr.yaml" ;;
            3) COMPLIANCE_EXTENSIONS="$COMPLIANCE_EXTENSIONS compliance/hipaa.yaml" ;;
            4) COMPLIANCE_EXTENSIONS="$COMPLIANCE_EXTENSIONS compliance/pci-dss.yaml" ;;
        esac
    done
fi

echo
info "설정 확인:"
info "  프로젝트: $PROJECT_NAME"
if [ -n "$PROJECT_DESCRIPTION" ]; then
    info "  설명: $PROJECT_DESCRIPTION"
fi
info "  MVP 단계: $MVP_PHASE"
if [ "$CONFIG_TYPE" = "1" ] && [ -n "$PRESET_ID" ]; then
    info "  사용 프리셋: $PRESET_ID"
fi
if [ -n "$DOMAIN_EXTENSION" ]; then
    info "  도메인: $DOMAIN_EXTENSION"
fi
if [ -n "$FEATURE_EXTENSIONS" ]; then
    info "  기능: $FEATURE_EXTENSIONS"
fi
if [ -n "$COMPLIANCE_EXTENSIONS" ]; then
    info "  규정: $COMPLIANCE_EXTENSIONS"
fi
echo

read -p "이 설정으로 진행하시겠습니까? (y/N): " CONFIRM
if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    warn "설정이 취소되었습니다"
    exit 0
fi

echo
log "Demeter가 새로운 프로젝트를 준비합니다..."

# Create project directories
mkdir -p docs
mkdir -p src
mkdir -p tests
mkdir -p configs

# Generate custom SSOT using merge script
log "SSOT 요구사항 병합 중..."

# Build extension list
ALL_EXTENSIONS=""
if [ -n "$DOMAIN_EXTENSION" ]; then
    if [ -f "$DEMETER_DIR/core/ssot/extensions/$DOMAIN_EXTENSION" ]; then
        ALL_EXTENSIONS="$ALL_EXTENSIONS $DEMETER_DIR/core/ssot/extensions/$DOMAIN_EXTENSION"
    else
        warn "도메인 확장 파일을 찾을 수 없습니다: $DOMAIN_EXTENSION"
    fi
fi

for ext in $FEATURE_EXTENSIONS; do
    if [ -f "$DEMETER_DIR/core/ssot/extensions/$ext" ]; then
        ALL_EXTENSIONS="$ALL_EXTENSIONS $DEMETER_DIR/core/ssot/extensions/$ext"
    else
        warn "기능 확장 파일을 찾을 수 없습니다: $ext"
    fi
done

for ext in $COMPLIANCE_EXTENSIONS; do
    if [ -f "$DEMETER_DIR/core/ssot/extensions/$ext" ]; then
        ALL_EXTENSIONS="$ALL_EXTENSIONS $DEMETER_DIR/core/ssot/extensions/$ext"
    else
        warn "규정 확장 파일을 찾을 수 없습니다: $ext"
    fi
done

# Check if Python is available for merge script
if command -v python3 &> /dev/null; then
    # Merge SSOT using Python script
    log "SSOT 병합 스크립트 실행 중..."

    MERGE_CMD="python3 $DEMETER_DIR/core/ssot/tools/merge-ssot.py \
        --base $DEMETER_DIR/core/ssot/base \
        --output ./merged-ssot.yaml \
        --project-name \"$PROJECT_NAME\" \
        --mvp-phase \"$MVP_PHASE\""

    if [ -n "$PROJECT_DESCRIPTION" ]; then
        MERGE_CMD="$MERGE_CMD --project-description \"$PROJECT_DESCRIPTION\""
    fi

    if [ -n "$ALL_EXTENSIONS" ]; then
        MERGE_CMD="$MERGE_CMD --extensions $ALL_EXTENSIONS"
    fi

    eval $MERGE_CMD

    if [ $? -eq 0 ]; then
        log "SSOT 병합 완료"

        # Generate final SSOT document
        log "SSOT 문서 생성 중..."
        SSOT_DESCRIPTION="$PROJECT_NAME"
        if [ -n "$PROJECT_DESCRIPTION" ]; then
            SSOT_DESCRIPTION="$PROJECT_DESCRIPTION"
        fi

        python3 "$DEMETER_DIR/core/ssot/tools/generate-template.py" \
            --input ./merged-ssot.yaml \
            --output docs/SSOT.md \
            --project-name "$PROJECT_NAME" \
            --project-description "$SSOT_DESCRIPTION" \
            --mvp-phase "$MVP_PHASE"

        # Initialize UoW tracker with project details
        log "UoW 추적 시스템 초기화 중..."
        if [ -f "$DEMETER_DIR/core/ssot/uow-tracker.yaml" ]; then
            cp "$DEMETER_DIR/core/ssot/uow-tracker.yaml" ./uow-tracker.yaml
            # Update project metadata in tracker
            sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" ./uow-tracker.yaml
            sed -i "s/{{MVP_PHASE}}/$MVP_PHASE/g" ./uow-tracker.yaml
            sed -i "s/{{CREATION_DATE}}/$(date '+%Y-%m-%d')/g" ./uow-tracker.yaml
            sed -i "s/{{LAST_UPDATE_DATE}}/$(date '+%Y-%m-%d %H:%M:%S')/g" ./uow-tracker.yaml
        fi

        # Generate UoW batch execution system
        log "UoW 배치 실행 시스템 생성 중..."
        setup_uow_batch_system

        # Initialize GraphRAG knowledge system
        log "GraphRAG 지식 시스템 초기화 중..."
        initialize_graphrag_system

        # Clean up temporary file
        rm -f ./merged-ssot.yaml
    else
        warn "SSOT 병합에 실패했습니다. 기본 템플릿을 사용합니다."
        # Fallback to basic template
        if [ -f "$DEMETER_DIR/core/ssot/templates/SSOT.md.template" ]; then
            FALLBACK_DESCRIPTION="$PROJECT_NAME"
            if [ -n "$PROJECT_DESCRIPTION" ]; then
                FALLBACK_DESCRIPTION="$PROJECT_DESCRIPTION"
            fi
            sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
                -e "s/{{PROJECT_DESCRIPTION}}/$FALLBACK_DESCRIPTION/g" \
                -e "s/{{MVP_PHASE}}/$MVP_PHASE/g" \
                -e "s/{{CREATION_DATE}}/$(date '+%Y-%m-%d')/g" \
                "$DEMETER_DIR/core/ssot/templates/SSOT.md.template" > docs/SSOT.md
        fi
    fi
else
    warn "Python3을 찾을 수 없습니다. 기본 템플릿을 사용합니다."
    # Fallback to basic template
    if [ -f "$DEMETER_DIR/core/ssot/templates/SSOT.md.template" ]; then
        log "기본 SSOT 문서 생성 중..."
        FALLBACK_DESCRIPTION="$PROJECT_NAME"
        if [ -n "$PROJECT_DESCRIPTION" ]; then
            FALLBACK_DESCRIPTION="$PROJECT_DESCRIPTION"
        fi
        sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
            -e "s/{{PROJECT_DESCRIPTION}}/$FALLBACK_DESCRIPTION/g" \
            -e "s/{{MVP_PHASE}}/$MVP_PHASE/g" \
            -e "s/{{CREATION_DATE}}/$(date '+%Y-%m-%d')/g" \
            "$DEMETER_DIR/core/ssot/templates/SSOT.md.template" > docs/SSOT.md
    fi
fi

# Copy and customize Claude guide
if [ -f "$DEMETER_DIR/core/ssot/templates/CLAUDE.md.template" ]; then
    log "Claude 개발 가이드 생성 중..."
    CLAUDE_DESCRIPTION="$PROJECT_NAME"
    if [ -n "$PROJECT_DESCRIPTION" ]; then
        CLAUDE_DESCRIPTION="$PROJECT_DESCRIPTION"
    fi
    sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
        -e "s/{{PROJECT_DESCRIPTION}}/$CLAUDE_DESCRIPTION/g" \
        -e "s/{{MVP_PHASE}}/$MVP_PHASE/g" \
        -e "s/{{CREATION_DATE}}/$(date '+%Y-%m-%d')/g" \
        "$DEMETER_DIR/core/ssot/templates/CLAUDE.md.template" > CLAUDE.md
fi

# Copy Learning template
if [ -f "$DEMETER_DIR/core/ssot/templates/LEARNING.md.template" ]; then
    log "학습 문서 템플릿 생성 중..."
    LEARNING_DESCRIPTION="$PROJECT_NAME"
    if [ -n "$PROJECT_DESCRIPTION" ]; then
        LEARNING_DESCRIPTION="$PROJECT_DESCRIPTION"
    fi
    sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
        -e "s/{{PROJECT_DESCRIPTION}}/$LEARNING_DESCRIPTION/g" \
        -e "s/{{MVP_PHASE}}/$MVP_PHASE/g" \
        "$DEMETER_DIR/core/ssot/templates/LEARNING.md.template" > LEARNING.md
fi

# Setup GraphRAG if available
if [ -f "$DEMETER_DIR/core/graphrag/scripts/setup-graphrag.sh.template" ]; then
    log "GraphRAG 설정 준비 중..."
    mkdir -p grag/scripts
    GRAPHRAG_DESCRIPTION="$PROJECT_NAME"
    if [ -n "$PROJECT_DESCRIPTION" ]; then
        GRAPHRAG_DESCRIPTION="$PROJECT_DESCRIPTION"
    fi
    sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
        -e "s/{{PROJECT_DESCRIPTION}}/$GRAPHRAG_DESCRIPTION/g" \
        -e "s/{{MVP_PHASE}}/$MVP_PHASE/g" \
        "$DEMETER_DIR/core/graphrag/scripts/setup-graphrag.sh.template" > grag/scripts/setup-graphrag.sh
    chmod +x grag/scripts/setup-graphrag.sh

    # Copy GraphRAG config templates
    if [ -d "$DEMETER_DIR/core/graphrag/templates" ]; then
        cp -r "$DEMETER_DIR/core/graphrag/templates" grag/
    fi
fi

# Technology selection is decoupled from template initialization
# Language-specific templates are available in demeter/references/languages/
# Users should manually select and copy templates based on their chosen tech stack

# Copy Docker setup if available
if [ -f "$DEMETER_DIR/core/docker/docker-compose.yml.template" ]; then
    log "Docker 설정 복사 중..."
    sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
        "$DEMETER_DIR/core/docker/docker-compose.yml.template" > docker-compose.yml
fi

# Create basic project structure
# Technology-agnostic initialization complete

# Create project README if it doesn't exist
if [ ! -f "README.md" ]; then
    README_DESCRIPTION="$PROJECT_NAME"
    if [ -n "$PROJECT_DESCRIPTION" ]; then
        README_DESCRIPTION="$PROJECT_DESCRIPTION"
    fi
    cat > README.md << EOF
# $PROJECT_NAME

$README_DESCRIPTION

## 🌾 Generated by Demeter

This project was initialized using the Demeter template seed system,
named after the Greek goddess of harvest and agriculture.

**MVP Phase**: $MVP_PHASE

## Quick Start

1. Review the project requirements: \`docs/SSOT.md\`
2. Follow development guidelines: \`CLAUDE.md\`
3. Set up technology stack based on your requirements
4. Set up GraphRAG knowledge system: \`./grag/scripts/setup-graphrag.sh\`

## Technology Stack

This project is technology-agnostic. Choose your preferred:
- **Language**: Go, Python, TypeScript, or others
- **Framework**: Based on your project requirements
- **Database**: SQL, NoSQL, or others as needed
- **Infrastructure**: Docker, Kubernetes, cloud services

Refer to \`demeter/references/\` for language-specific templates.

## Development

See \`CLAUDE.md\` for comprehensive development guidelines.

---

*"데메테르의 축복이 이 프로젝트에 풍요로운 결실을 가져다주기를"* 🌾
EOF
fi

echo
log "✨ 프로젝트 초기화가 완료되었습니다!"
echo
info "다음 단계:"
info "1. 📖 docs/SSOT.md에서 프로젝트 요구사항 확인"
info "2. 🤖 CLAUDE.md에서 개발 가이드라인 검토 (MVP 프로세스 포함)"
info "3. 🎯 MVP 진행상황 확인: python demeter/core/ssot/tools/uow-dashboard.py --dashboard"
info "4. 📋 계약 검증: python demeter/core/ssot/tools/verify-contracts.py --all"
info "5. 🧠 GraphRAG 설정: ./grag/scripts/setup-graphrag.sh"
info "6. 📝 .gitignore에서 'demeter/' 주석 해제로 템플릿 제외"
echo
info "새로운 MVP 개발 도구들:"
info "• UoW 대시보드: python demeter/core/ssot/tools/uow-dashboard.py --dashboard"
info "• 계약 검증: python demeter/core/ssot/tools/verify-contracts.py --uow UoW-XXX"
info "• 진행 리포트: python demeter/core/ssot/tools/uow-dashboard.py --report"
info "• 리스크 관리: demeter/core/ssot/risk-registry.yaml 확인"
echo
info "🤖 UoW 자동 실행 시스템:"
if [ -d "./batch" ]; then
    info "• 전체 배치 실행: ./batch/scripts/batch-execute-uows.sh"
    info "• 개별 UoW 실행: ./batch/scripts/execute-uow.sh UoW-XXX"
    info "• 드라이런 테스트: ./batch/scripts/batch-execute-uows.sh --dry-run"
    info "• 배치 시스템 문서: ./batch/README.md"
else
    warn "• 배치 시스템이 설정되지 않았습니다. SSOT 병합 확인이 필요합니다."
fi
echo
info "🧠 GraphRAG 지식 시스템 (통합 워크플로우):"
if [ -f "./.graphrag_config" ] && [ -d "./graphrag" ]; then
    info "• 지식베이스 위치: ./graphrag/knowledge/"
    info "• 구현 지식: 각 UoW 실행 시 자동으로 문서화됨"
    info "• 패턴 발견: UoW 프롬프트에 직접 통합된 워크플로우"
    info "• 지식 활용: Claude가 이전 구현을 분석하여 컨텍스트 제공"
    info "• 프로젝트 개요: ./graphrag/knowledge/project-overview.md"
else
    warn "• GraphRAG 시스템이 설정되지 않았습니다."
fi
echo
warn "Demeter 템플릿을 프로젝트에서 제외하려면:"
warn "  .gitignore 파일에서 '# demeter/' 주석을 해제하세요"
echo
echo -e "${GREEN}🌾 데메테르가 여러분의 MVP 프로젝트에 풍요로운 수확을 약속합니다! ${NC}"
echo -e "${BLUE}MVP 단계: $MVP_PHASE | 프로젝트: $PROJECT_NAME${NC}"