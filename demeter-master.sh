#!/bin/bash

# 🌾 Demeter WAVIS v2.0 - Master Script (3-Step Workflow)
# Orchestrates Setup → Implementation → Deployment phases
#
# Usage: ./demeter-master.sh [project-name] [requirements-file]

set -e

# Configuration
PROJECT_NAME="${1:-my-project}"
REQUIREMENTS_FILE="${2:-}"
EXTENSIONS=""  # Will be determined by AI analysis of requirements
FRAMEWORK_PATH="${WAVIS_TEMPLATE_PATH:-$(pwd)}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_info() { echo -e "${CYAN}ℹ️  $1${NC}"; }
log_step() { echo -e "${PURPLE}🔄 $1${NC}"; }

main() {
    echo -e "${GREEN}🌾 Demeter v2.0 - Master Script (3-Step Workflow)${NC}"
    echo "Project: $PROJECT_NAME"
    echo "Requirements: ${REQUIREMENTS_FILE:-none}"
    echo "Extensions: Auto-determined by AI analysis"
    echo ""

    echo -e "${PURPLE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}📋 3-Step Constitutional Development Workflow${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════${NC}"
    echo ""

    # Step 1: Setup Phase (Phase 0-2)
    log_step "Step 1: Setup Phase (Phase 0-2) - Constitutional Foundation"
    echo "  • Phase 0: Project initialization & constitutional setup"
    echo "  • Phase 1: Requirements analysis & SSOT generation"
    echo "  • Phase 2: Architecture planning & execution roadmap"
    echo ""

    ./demeter-setup.sh "$PROJECT_NAME" "$REQUIREMENTS_FILE"

    if [ $? -eq 0 ]; then
        log_success "Step 1 completed - Setup phase ready for Claude Code execution"
    else
        echo -e "${RED}❌ Step 1 failed - Setup phase error${NC}"
        exit 1
    fi

    echo ""
    echo -e "${YELLOW}⏸️  PAUSE: Review setup results before proceeding${NC}"
    echo "1. Check .demeter/SETUP_WORKFLOW.prompt"
    echo "2. Execute the setup prompt in Claude Code"
    echo "3. Review generated SSOT and execution plan"
    echo "4. Press Enter when ready for implementation phase..."
    read -r

    # Step 2: Implementation Phase (Phase 3-6)
    log_step "Step 2: Implementation Phase (Phase 3-6) - Constitutional TDD"
    echo "  • Phase 3: RED - Constitutional test specification"
    echo "  • Phase 4: GREEN - Constitutional implementation"
    echo "  • Phase 5: REFACTOR - Constitutional enhancement"
    echo "  • Phase 6: Quality verification & compliance audit"
    echo ""

    cd "$PROJECT_NAME"
    ../demeter-implement.sh

    if [ $? -eq 0 ]; then
        log_success "Step 2 completed - Implementation phase ready for Claude Code execution"
    else
        echo -e "${RED}❌ Step 2 failed - Implementation phase error${NC}"
        exit 1
    fi

    echo ""
    echo -e "${YELLOW}⏸️  PAUSE: Review implementation results before deployment${NC}"
    echo "1. Check .demeter/IMPLEMENTATION_WORKFLOW.prompt"
    echo "2. Execute the implementation prompt in Claude Code"
    echo "3. Verify constitutional compliance and quality gates"
    echo "4. Press Enter when ready for deployment phase..."
    read -r

    # Step 3: Deployment Phase (Phase 7)
    log_step "Step 3: Deployment Phase (Phase 7) - Constitutional Production"
    echo "  • Phase 7: Production deployment & constitutional monitoring"
    echo "  • Constitutional compliance validation in production"
    echo "  • Governance monitoring and alerting setup"
    echo ""

    ./demeter-deploy.sh

    if [ $? -eq 0 ]; then
        log_success "Step 3 completed - Deployment phase ready for Claude Code execution"
    else
        echo -e "${RED}❌ Step 3 failed - Deployment phase error${NC}"
        exit 1
    fi

    echo ""
    echo -e "${GREEN}🎉 All 3 steps completed successfully!${NC}"
    echo ""
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}📋 Next Actions - Execute in Claude Code:${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════${NC}"
    echo "1. 🔧 Setup: .demeter/SETUP_WORKFLOW.prompt"
    echo "2. 💻 Implementation: .demeter/IMPLEMENTATION_WORKFLOW.prompt"
    echo "3. 🚀 Deployment: .demeter/DEPLOYMENT_WORKFLOW.prompt"
    echo ""

    # Generate consolidated master prompt for all-in-one execution (optional)
    cat > ".demeter/CONSOLIDATED_MASTER.prompt" << EOF
# 🌾 Demeter v2.0 - Consolidated Constitutional Development Lifecycle

## Project Information
- **Name**: $PROJECT_NAME
- **Requirements**: ${REQUIREMENTS_FILE:-none}
- **Extensions**: Auto-determined by AI analysis
- **Framework**: Demeter WAVIS v2.0 Constitutional SDD

## 🎯 Option: All-in-One Execution

If you prefer to execute all phases (0-7) in a single prompt, use this consolidated workflow.
Otherwise, use the individual phase prompts for better control:

1. **Setup Phase**: Execute .demeter/SETUP_WORKFLOW.prompt
2. **Implementation Phase**: Execute .demeter/IMPLEMENTATION_WORKFLOW.prompt
3. **Deployment Phase**: Execute .demeter/DEPLOYMENT_WORKFLOW.prompt

### Consolidated Execution Instructions

This prompt combines all three phases for continuous execution:

**Phase 0-2 (Setup)**: Constitutional foundation, SSOT generation, architecture planning
**Phase 3-6 (Implementation)**: Constitutional TDD cycles with RED-GREEN-REFACTOR
**Phase 7 (Deployment)**: Constitutional production deployment and monitoring

Execute all phases with full constitutional compliance and AI-enhanced development assistance.

**Recommended**: Use individual phase prompts for better control and review points.
EOF

    log_success "Consolidated master prompt created (optional): .demeter/CONSOLIDATED_MASTER.prompt"
    echo ""
    echo -e "${GREEN}🌾 Master workflow orchestration complete!${NC}"
    echo -e "${YELLOW}Choose your execution strategy:${NC}"
    echo "  📋 Step-by-step: Use individual phase prompts (RECOMMENDED)"
    echo "  🚀 All-in-one: Use CONSOLIDATED_MASTER.prompt"
}

main "$@"