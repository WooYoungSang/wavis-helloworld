#!/bin/bash

# 🌾 Demeter WAVIS v2.0 - Setup Phase (Phase 0-2)
# Constitutional project initialization, requirements analysis, and architecture planning
#
# Usage: ./demeter-setup.sh [project-name] [requirements-file]

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
NC='\033[0m'

log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_info() { echo -e "${CYAN}ℹ️  $1${NC}"; }

main() {
    echo -e "${GREEN}🌾 Demeter v2.0 - Setup Phase (Phase 0-2)${NC}"
    echo "Project: $PROJECT_NAME"
    echo "Requirements: ${REQUIREMENTS_FILE:-none}"
    echo "Extensions: Auto-determined by AI analysis"
    echo ""

    # Create project directory and structure
    mkdir -p "${PROJECT_NAME}/.demeter/prompts"
    cd "${PROJECT_NAME}"

    # Generate setup workflow prompt
    cat > ".demeter/SETUP_WORKFLOW.prompt" << EOF
# 🌾 Demeter v2.0 - Setup Workflow (Phase 0-2)

## Project Information
- **Name**: $PROJECT_NAME
- **Requirements File**: ${REQUIREMENTS_FILE:-none}
- **Framework**: Demeter WAVIS v2.0 Constitutional SDD
- **Template Path**: $FRAMEWORK_PATH
- **Extensions**: AI will analyze requirements and auto-determine appropriate extensions

## 🎯 Setup Phase Execution (Phase 0-2)

### Phase 0: Constitutional Project Initialization
1. **Create Constitutional Foundation**:
   - Generate PROJECT-constitution.yaml with 9 Constitutional Principles
   - Setup governance rules and enforcement mechanisms
   - Create constitutional compliance templates
   - Initialize AI development guidelines (CLAUDE.md)

2. **Project Structure Setup**:
   - Standard directories (docs, src, tests, config, deployments)
   - GraphRAG knowledge base (.demeter-dev/knowledge/)
   - Constitutional governance structure
   - Batch execution system directories

3. **AI-Driven Extension Analysis**:
   - Analyze requirements file to determine appropriate domain extensions
   - Auto-detect: e-commerce, fintech, healthcare, iot, gdpr, security, etc.
   - Apply domain-specific configurations based on analysis
   - Setup extension-specific constitutional requirements
   - Configure compliance frameworks as needed

### Phase 1: Requirements & SSOT Generation
1. **AI-Enhanced Requirements Analysis**:
   $(if [ -n "$REQUIREMENTS_FILE" ]; then
     echo "   - Analyze provided requirements file: $REQUIREMENTS_FILE"
     echo "   - Auto-determine domain extensions from requirements content"
     echo "   - Apply constitutional principles to requirements"
     echo "   - Generate constitutional compliance specifications"
     echo "   - Set up domain-specific configurations based on AI analysis"
   else
     echo "   - Generate base requirements structure for general domain"
     echo "   - Create template requirements following constitutional principles"
     echo "   - Setup requirements gathering framework"
     echo "   - Prepare for future requirements analysis"
   fi)

2. **SSOT System Generation**:
   - Use wavis-template SSOT system: $FRAMEWORK_PATH/demeter/core/ssot/
   - Generate merged-ssot.yaml with constitutional integration
   - Create comprehensive SSOT documentation
   - Setup constitutional quality gates

3. **Constitutional Requirements Enhancement**:
   - Integrate 9 Constitutional Principles:
     * Library-First: Prioritize existing libraries over custom implementations
     * CLI Interface: Standardized command-line interface design
     * Test-First: Test-driven development methodology
     * Simplicity: Simple, readable, and maintainable code
     * Anti-Abstraction: Avoid unnecessary abstraction layers
     * Integration-First: Prioritize system integration capabilities
     * Minimal Structure: Minimal project structure and complexity
     * Framework Direct: Direct framework usage without wrappers
     * Comprehensive Testing: Complete test coverage requirements

### Phase 2: Planning & Architecture Design
1. **Execution Plan Generation**:
   - Create batch/execution-plan.yaml
   - UoW dependency analysis with constitutional constraints
   - Constitutional principle implementation roadmap
   - Quality gate and governance checkpoints
   - Resource allocation and timeline

2. **Constitutional Architecture Design**:
   - Library-first architecture specification
   - CLI interface design standards
   - Test-first development framework
   - Simplicity and anti-abstraction guidelines
   - Integration patterns and standards

3. **Development Framework Setup**:
   - Constitutional TDD cycle templates
   - Quality verification frameworks
   - Governance compliance monitoring
   - Knowledge capture and sharing systems

## 🏛️ Constitutional Principles Integration

Ensure all setup phases integrate the 9 Constitutional Principles:

1. **Library-First Setup**: Configure dependency management prioritizing existing libraries
2. **CLI Interface Setup**: Establish standardized command structure and help systems
3. **Test-First Setup**: Configure testing frameworks and TDD infrastructure
4. **Simplicity Setup**: Minimize configuration complexity and setup overhead
5. **Anti-Abstraction Setup**: Direct configuration without unnecessary abstraction layers
6. **Integration-First Setup**: Configure for maximum integration capabilities
7. **Minimal Structure Setup**: Create only essential project structure
8. **Framework Direct Setup**: Direct framework usage without wrapper layers
9. **Comprehensive Testing Setup**: Complete test infrastructure configuration

## 🎯 Setup Success Criteria

### Technical Setup Verification
- [ ] Project directory structure created with constitutional foundation
- [ ] Constitutional governance framework operational
- [ ] SSOT system generated and validated
- [ ] Execution plan created with dependencies mapped
- [ ] Development framework configured

### Constitutional Compliance Verification
- [ ] All 9 Constitutional Principles integrated into project foundation
- [ ] Governance rules established and documented
- [ ] Quality gates configured with constitutional requirements
- [ ] Constitutional debt tracking system operational

### Knowledge Management Setup
- [ ] GraphRAG knowledge base initialized
- [ ] Constitutional patterns repository created
- [ ] Project-specific governance documentation complete

## 🚀 Next Steps

After successful setup completion:
1. Review generated SSOT and execution plan
2. Validate constitutional compliance configuration
3. Proceed to Implementation Phase: \`./demeter-implement.sh\`

Execute this prompt in Claude Code to complete the Setup Phase (Phase 0-2).
EOF

    log_success "Setup workflow prompt created: .demeter/SETUP_WORKFLOW.prompt"
    echo ""
    echo -e "${YELLOW}🚀 Next Steps:${NC}"
    echo "1. Execute in Claude Code: .demeter/SETUP_WORKFLOW.prompt"
    echo "2. Review generated SSOT and execution plan"
    echo "3. Proceed with: ./demeter-implement.sh"
    echo ""
    log_info "Setup phase complete - ready for Claude Code execution!"
}

main "$@"