#!/bin/bash

# 🌾 Demeter WAVIS v1.3 - Minimal TDD Iteration Script
# Prompt-based TDD processing with Claude Code
#
# Usage: ./demeter-iterate.sh [uow-id] [phase] [execution-plan.yaml]

set -e

# Configuration
UOW_ID="${1:-all}"
PHASE="${2:-all}"
EXECUTION_PLAN="${3:-batch/execution-plan.yaml}"
PROJECT_PATH="$(pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_info() { echo -e "${CYAN}ℹ️  $1${NC}"; }

main() {
    echo -e "${GREEN}🌾 Demeter v1.3 - Minimal TDD Iteration Script${NC}"
    echo "Parameters: $UOW_ID | $PHASE | $EXECUTION_PLAN"
    echo ""

    # Create minimal directory structure
    mkdir -p ".demeter/prompts"

    # Generate master TDD iteration prompt
    cat > ".demeter/TDD_ITERATION.prompt" << EOF
# 🌾 Demeter v1.3 - Complete TDD Iteration Workflow

## Project Information
- **Project**: $(basename "$PROJECT_PATH")
- **UoW Target**: $UOW_ID
- **Phase Target**: $PHASE
- **Execution Plan**: $EXECUTION_PLAN
- **Framework**: Demeter WAVIS v1.3 with Constitutional SDD

## 🎯 TDD Iteration Process

### Phase 3-5: UoW TDD Cycles (RED-GREEN-REFACTOR)

#### For Each UoW in dependency order:

**🔴 Phase 3: RED (Test Specification)**
1. Query GraphRAG knowledge for testing patterns
2. Convert acceptance criteria to failing tests:
   - Unit tests for individual components
   - Integration tests for dependencies
   - Edge cases and error scenarios
   - Constitutional compliance tests
3. Verify all tests FAIL initially
4. Document test coverage plan

**🟢 Phase 4: GREEN (Minimal Implementation)**
1. Apply constitutional principles:
   - Library-first implementation strategy
   - CLI interface compliance
   - Test-first verification
   - Simplicity and anti-abstraction
2. Implement minimal code to pass tests:
   - Write ONLY enough code to make tests pass
   - Follow complexity-based approach (simple/medium/complex)
   - Maintain constitutional compliance
3. Ensure all tests pass (GREEN state)

**🔵 Phase 5: REFACTOR (Code Enhancement)**
1. Apply refactoring principles:
   - Remove duplication (DRY)
   - Improve naming and readability
   - Apply SOLID principles
   - Optimize performance where needed
2. Enhance constitutional compliance:
   - Strengthen library-first adoption
   - Improve CLI interface quality
   - Add constitutional validation tests
3. Capture knowledge in GraphRAG system
4. Maintain GREEN state throughout

### Phase 6-7: Project Quality & Deployment

**📊 Phase 6: Quality Verification**
1. Contract compliance verification
2. Test coverage analysis (>80% foundation, >60% business)
3. Performance validation
4. Security assessment
5. Constitutional principle compliance audit
6. Integration testing

**🚀 Phase 7: Deployment Preparation**
1. Docker Compose configuration
2. Environment and security setup
3. Monitoring and observability
4. Deployment execution
5. Documentation and runbook
6. Production readiness verification

## 🎯 Execution Strategy

### Target Specific Execution:
- **UoW**: $UOW_ID
- **Phase**: $PHASE

### Constitutional Integration:
- All implementations must follow the 9 Constitutional Principles
- Library-first approach mandatory
- CLI interface compliance required
- Test-first development enforced
- Simplicity and anti-abstraction principles applied

### GraphRAG Knowledge Utilization:
- Query development patterns before implementation
- Capture lessons learned during refactoring
- Build reusable component library
- Document constitutional compliance patterns

## 🚀 Execution Instructions

1. **Load Execution Plan**: Parse $EXECUTION_PLAN for UoW dependencies
2. **Execute TDD Cycles**: Follow RED-GREEN-REFACTOR for each UoW
3. **Apply Constitutional Principles**: Ensure compliance throughout
4. **Capture Knowledge**: Update GraphRAG with patterns and lessons
5. **Quality Gates**: Verify constitutional and traditional quality metrics
6. **Deploy**: Prepare production-ready system

## Success Criteria
- [ ] All UoWs completed with full TDD cycle
- [ ] Constitutional principles compliance verified
- [ ] Test coverage meets quality gates
- [ ] GraphRAG knowledge base updated
- [ ] All acceptance criteria validated
- [ ] Production deployment ready

Execute this prompt in Claude Code to run the complete TDD iteration workflow.
EOF

    log_success "Master TDD iteration prompt created: .demeter/TDD_ITERATION.prompt"
    echo ""
    echo -e "${YELLOW}🚀 Next Steps:${NC}"
    echo "1. Execute in Claude Code: .demeter/TDD_ITERATION.prompt"
    echo "2. Follow constitutional TDD principles throughout"
    echo "3. Monitor GraphRAG knowledge accumulation"
    echo ""
    log_info "Minimal script complete - all TDD processing delegated to Claude Code!"
}

main "$@"