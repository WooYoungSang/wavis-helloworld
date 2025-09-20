#!/bin/bash

# 🌱 Demeter WAVIS v1.3 - Minimal Project Initializer
# Prompt-based processing with Claude Code
#
# Usage: ./demeter-init.sh [project-name] [extensions] [requirements-file]

set -e

# Configuration
PROJECT_NAME="${1:-my-project}"
EXTENSIONS="${2:-}"
REQUIREMENTS_FILE="${3:-}"
FRAMEWORK_PATH="${WAVIS_TEMPLATE_PATH:-$(pwd)}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_info() { echo -e "${CYAN}ℹ️  $1${NC}"; }

main() {
    echo -e "${GREEN}🌱 Demeter WAVIS v1.3 - Minimal Initializer${NC}"
    echo "Project: $PROJECT_NAME | Extensions: $EXTENSIONS"
    echo ""

    # Create minimal project structure
    mkdir -p "${PROJECT_NAME}/.demeter/prompts"
    cd "${PROJECT_NAME}"

    # Generate master initialization prompt
    cat > ".demeter/MASTER_INIT.prompt" << EOF
# 🌱 Demeter v1.3 - Complete Project Initialization

## Project Information
- **Name**: ${PROJECT_NAME}
- **Extensions**: ${EXTENSIONS}
- **Requirements File**: ${REQUIREMENTS_FILE}
- **Framework**: Demeter WAVIS v1.3

## 🎯 Initialization Tasks

### Phase 1: Project Structure Creation
1. Create comprehensive directory structure:
   - {docs,src,tests,config,scripts,deployments}
   - .demeter-dev/knowledge/{patterns,lessons,components,queries}
   - batch/{configs,prompts,logs,reports}
   - .demeter/{prompts,logs,configs}

2. Initialize project documentation:
   - README.md with project overview
   - CLAUDE.md with AI development guidelines
   - LEARNING.md for progress tracking
   - .gitignore with appropriate exclusions

### Phase 2: SSOT Generation
Use the wavis-template SSOT system to generate project requirements:

1. **Load Base SSOT**: ${FRAMEWORK_PATH}/demeter/core/ssot/base/
2. **Apply Extensions**: ${EXTENSIONS}
3. **Generate Merged SSOT**: docs/merged-ssot.yaml
4. **Create Documentation**: docs/SSOT.md
5. **Build Execution Plan**: batch/execution-plan.yaml

### Phase 3: Requirements Integration (if applicable)
EOF

    # Add requirements integration if file provided
    if [ -n "$REQUIREMENTS_FILE" ] && [ -f "$REQUIREMENTS_FILE" ]; then
        echo "Requirements file: $REQUIREMENTS_FILE" >> ".demeter/MASTER_INIT.prompt"
        echo "\nIntegrate natural language requirements from: $REQUIREMENTS_FILE" >> ".demeter/MASTER_INIT.prompt"
        cp "$REQUIREMENTS_FILE" "docs/PROJECT_REQUIREMENTS.md" 2>/dev/null || true
    else
        echo "\nNo requirements file provided - using domain templates only." >> ".demeter/MASTER_INIT.prompt"
    fi

    cat >> ".demeter/MASTER_INIT.prompt" << EOF

### Phase 4: Development Knowledge Setup
1. Initialize GraphRAG knowledge base in .demeter-dev/knowledge/
2. Create development patterns and lessons
3. Setup query examples for development assistance

## 🚀 Execution Instructions

1. **Execute this prompt** to complete full project initialization
2. **Review generated SSOT** in docs/SSOT.md
3. **Validate execution plan** in batch/execution-plan.yaml
4. **Start development** with ./demeter-iterate.sh

## Success Criteria
- [ ] Complete project structure created
- [ ] SSOT generated with requirements and UoWs
- [ ] Execution plan ready for TDD development
- [ ] GraphRAG knowledge base initialized
- [ ] All configuration files in place

Execute this prompt in Claude Code to initialize the complete Demeter project.
EOF

    log_success "Master initialization prompt created: .demeter/MASTER_INIT.prompt"
    echo ""
    echo -e "${YELLOW}🚀 Next Steps:${NC}"
    echo "1. cd ${PROJECT_NAME}"
    echo "2. Execute in Claude Code: .demeter/MASTER_INIT.prompt"
    echo "3. Review generated files and start development"
    echo ""
    log_info "Minimal script complete - all processing delegated to Claude Code!"
}

main