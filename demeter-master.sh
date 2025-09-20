#!/bin/bash

# 🌾 Demeter WAVIS v1.3 - Minimal Master Script
# Prompt-based complete lifecycle processing with Claude Code
#
# Usage: ./demeter-master.sh [project-name]

set -e

# Configuration
PROJECT_NAME="${1:-my-project}"
FRAMEWORK_PATH="${WAVIS_TEMPLATE_PATH:-$(pwd)}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_info() { echo -e "${CYAN}ℹ️  $1${NC}"; }

main() {
    echo -e "${GREEN}🌾 Demeter v1.3 - Minimal Master Script${NC}"
    echo "Project: $PROJECT_NAME"
    echo ""

    # Create project directory and structure
    mkdir -p "${PROJECT_NAME}/.demeter/prompts"
    cd "${PROJECT_NAME}"

    # Generate master lifecycle prompt
    cat > ".demeter/MASTER_LIFECYCLE.prompt" << EOF
# 🌾 Demeter v1.3 - Complete Lifecycle Automation

## Project Information
- **Name**: $PROJECT_NAME
- **Framework**: Demeter WAVIS v1.3 with Constitutional SDD
- **Template Path**: $FRAMEWORK_PATH

## 🎯 Complete Lifecycle Execution (Phase 0-7)

### Phase 0: Constitutional Project Initialization
1. **Create project structure**:
   - Standard directories (docs, src, tests, config, deployments)
   - GraphRAG knowledge base (.demeter-dev/knowledge/)
   - Constitutional governance structure
   - Batch execution system directories

2. **Initialize Constitutional Foundation**:
   - Generate PROJECT-constitution.yaml
   - Setup governance rules and enforcement
   - Create constitutional compliance templates
   - Initialize AI development guidelines (CLAUDE.md)

3. **SSOT System Bootstrap**:
   - Apply domain-specific SSOT templates
   - Generate base requirements structure
   - Setup constitutional compliance integration
   - Create execution planning framework

### Phase 1: Requirements & SSOT Generation
1. **Analyze domain and generate SSOT**:
   - Use wavis-template SSOT system: $FRAMEWORK_PATH/demeter/core/ssot/
   - Apply constitutional principles to requirements
   - Generate merged-ssot.yaml with governance integration
   - Create comprehensive SSOT documentation

2. **Constitutional Requirements Enhancement**:
   - Integrate 9 Constitutional Principles into requirements
   - Add governance compliance specifications
   - Generate constitutional quality gates
   - Create principle implementation guidelines

### Phase 2: Planning & Architecture
1. **Generate execution plan** (batch/execution-plan.yaml):
   - UoW dependency analysis with constitutional constraints
   - Constitutional principle implementation roadmap
   - Quality gate and governance checkpoints
   - Resource allocation and timeline

2. **Constitutional Architecture Design**:
   - Library-first architecture specification
   - CLI interface design standards
   - Test-first development framework
   - Simplicity and anti-abstraction guidelines

### Phase 3-5: TDD Development Cycles
**Execute complete RED-GREEN-REFACTOR cycles for all UoWs**:

#### 🔴 Phase 3: RED (Constitutional Test Specification)
- Query GraphRAG for testing patterns
- Create constitutional compliance tests
- Generate functional acceptance tests
- Verify all tests FAIL initially
- Document test coverage plan

#### 🟢 Phase 4: GREEN (Constitutional Implementation)
- Apply constitutional principles:
  - Library-first implementation
  - CLI interface compliance
  - Test-first verification
  - Simplicity and anti-abstraction
- Implement minimal code to pass tests
- Maintain constitutional compliance
- Ensure GREEN state achievement

#### 🔵 Phase 5: REFACTOR (Constitutional Enhancement)
- Apply refactoring with constitutional focus
- Enhance constitutional compliance
- Capture knowledge in GraphRAG system
- Improve CLI interface quality
- Reduce constitutional debt
- Maintain GREEN state throughout

### Phase 6: Constitutional Quality Verification
1. **Comprehensive Quality Assessment**:
   - Constitutional principle compliance audit
   - Traditional test coverage analysis (>80% foundation, >60% business)
   - Performance and security validation
   - Constitutional debt measurement
   - Governance rule adherence verification

2. **Quality Gates Validation**:
   - Library-first implementation: >95%
   - CLI interface compliance: 100%
   - Test-first development: 100%
   - Simplicity metrics: <10 complexity
   - Constitutional test coverage: >90%

### Phase 7: Constitutional Deployment Preparation
1. **Production Readiness with Constitutional Compliance**:
   - Constitutional Docker Compose configuration
   - Constitutional production environment setup
   - Constitutional monitoring and observability
   - Constitutional compliance validation in production

2. **Governance-Aware Deployment**:
   - Constitutional principle enforcement in production
   - Governance rule monitoring setup
   - Constitutional debt tracking
   - Principle compliance alerting

## 🎯 Constitutional Success Criteria

### Technical Success Metrics
- [ ] Complete project structure with constitutional foundation
- [ ] SSOT generated with constitutional integration
- [ ] All UoWs completed with constitutional TDD cycles
- [ ] Constitutional quality gates passed
- [ ] Production deployment with constitutional compliance

### Constitutional Compliance Metrics
- [ ] Library-first principle: >95% compliance
- [ ] CLI interface standards: 100% compliance
- [ ] Test-first development: 100% adherence
- [ ] Simplicity principle: <10 average complexity
- [ ] Anti-abstraction: <3 maximum layers
- [ ] Constitutional debt: <5% ratio
- [ ] Governance compliance: >85% score

### Knowledge and Governance Metrics
- [ ] GraphRAG knowledge base established and populated
- [ ] Constitutional patterns documented and reusable
- [ ] Governance decisions tracked and justified
- [ ] AI development guidelines operational
- [ ] Constitutional monitoring active

## 🚀 Execution Instructions

1. **Execute Complete Lifecycle**: Process all phases 0-7 automatically
2. **Apply Constitutional Principles**: Ensure governance compliance throughout
3. **Utilize GraphRAG Knowledge**: Leverage AI-enhanced development patterns
4. **Monitor Constitutional Compliance**: Track governance metrics continuously
5. **Capture Constitutional Knowledge**: Document patterns and decisions

## Constitutional Framework Integration
- **9 Constitutional Principles**: Fully integrated into all phases
- **Governance Rules**: Applied consistently across development
- **GraphRAG Knowledge**: Constitutional patterns and lessons captured
- **AI Enhancement**: Constitutional compliance assistance throughout

Execute this prompt in Claude Code to run the complete constitutional development lifecycle.
EOF

    log_success "Master lifecycle prompt created: .demeter/MASTER_LIFECYCLE.prompt"
    echo ""
    echo -e "${YELLOW}🚀 Next Steps:${NC}"
    echo "1. Execute in Claude Code: .demeter/MASTER_LIFECYCLE.prompt"
    echo "2. Monitor constitutional compliance throughout"
    echo "3. Review GraphRAG knowledge accumulation"
    echo ""
    log_info "Minimal script complete - entire lifecycle delegated to Claude Code!"
}

main "$@"