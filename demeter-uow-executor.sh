#!/bin/bash

# 🧪 Demeter v1.3 - Minimal TDD Executor
# Prompt-based TDD processing with Claude Code
#
# Usage: ./demeter-uow-executor.sh [execution-plan.yaml]

set -e

# Configuration
EXECUTION_PLAN="${1:-.demeter/execution-plan.yaml}"
PROJECT_PATH="$(pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_info() { echo -e "${CYAN}ℹ️  $1${NC}"; }

main() {
    echo -e "${GREEN}🧪 Demeter v1.3 - Minimal TDD Executor${NC}"
    echo "Execution Plan: $EXECUTION_PLAN"
    echo ""

    # Create logs directory
    mkdir -p ".demeter/logs"

    # Generate master TDD execution prompt
    cat > ".demeter/TDD_EXECUTOR.prompt" << EOF
# 🧪 Demeter v1.3 - Complete TDD Execution Workflow

## Project Information
- **Project**: $(basename "$PROJECT_PATH")
- **Execution Plan**: $EXECUTION_PLAN
- **Framework**: Demeter WAVIS v1.3 with TDD

## 🎯 TDD Execution Process

### Phase 1: Load and Parse Execution Plan
1. Load execution plan from: $EXECUTION_PLAN
2. Parse UoW sequences and dependencies
3. Identify complexity levels and acceptance criteria
4. Create execution timeline

### Phase 2: Sequential TDD Execution
For each UoW in dependency order:

#### 🔴 RED Phase
1. **Query GraphRAG** for testing patterns:
   - Find similar UoW testing strategies
   - Apply domain-specific test patterns
   - Use proven edge case scenarios

2. **Create failing tests** based on acceptance criteria:
   - Unit tests for individual components
   - Integration tests for dependencies
   - Edge cases and error scenarios
   - Performance tests if applicable

3. **Verify RED state**: All tests must fail initially

#### 🟢 GREEN Phase
1. **Apply implementation patterns** from GraphRAG:
   - Query for proven implementation strategies
   - Use appropriate complexity-based approach:
     - **Simple**: Direct implementation, clarity focus
     - **Medium**: Modular design, single agent
     - **Complex**: Parallel agents, advanced patterns

2. **Implement minimal code** to pass tests:
   - Write ONLY enough code to make tests pass
   - No premature optimization
   - Follow incremental development

3. **Maintain GREEN state**: All tests passing

#### 🔵 REFACTOR Phase
1. **Code quality improvements**:
   - Remove duplication (DRY principle)
   - Improve naming and readability
   - Apply SOLID principles
   - Optimize performance where needed

2. **Enhanced testing and documentation**:
   - Add edge cases discovered during implementation
   - Improve test descriptions
   - Document API contracts

3. **GraphRAG knowledge capture**:
   - Document new patterns discovered
   - Capture implementation lessons
   - Register reusable components
   - Update query examples in .demeter-dev/knowledge/

4. **Maintain GREEN state**: No functionality regression

### Phase 3: Progress Tracking
1. Update .demeter/tdd-progress.md after each UoW
2. Create individual phase prompts in .demeter/logs/
3. Track quality gates and coverage metrics

### Phase 4: Integration Validation
1. Run full test suite after all UoWs
2. Validate all acceptance criteria met
3. Check integration between UoWs
4. Prepare for deployment phase

## 🚀 Execution Instructions

1. **Execute this prompt** to start complete TDD workflow
2. **Follow RED-GREEN-REFACTOR** cycle for each UoW
3. **Capture knowledge** in GraphRAG system
4. **Track progress** throughout development

## Success Criteria
- [ ] All UoWs completed with RED-GREEN-REFACTOR cycle
- [ ] Test coverage meets quality gate requirements
- [ ] GraphRAG knowledge base updated with lessons
- [ ] All acceptance criteria validated
- [ ] Integration tests passing
- [ ] Code quality standards met

Execute this prompt in Claude Code to run the complete TDD development cycle.
EOF

    log_success "Master TDD execution prompt created: .demeter/TDD_EXECUTOR.prompt"
    echo ""
    echo -e "${YELLOW}🚀 Next Steps:${NC}"
    echo "1. Execute in Claude Code: .demeter/TDD_EXECUTOR.prompt"
    echo "2. Follow RED-GREEN-REFACTOR cycle for each UoW"
    echo "3. Monitor progress in .demeter/tdd-progress.md"
    echo ""
    log_info "Minimal script complete - TDD execution delegated to Claude Code!"
}

main "$@"