# 🧪 TDD Cycle Workflow

## Overview
This workflow guides you through the Test-Driven Development (TDD) cycle using the minimized demeter-uow-executor.sh and Claude Code prompt-based processing.

## Prerequisites
- Completed project initialization (SSOT and execution plan ready)
- batch/execution-plan.yaml file exists
- .demeter-dev/knowledge/ GraphRAG knowledge base available

## Workflow Steps

### Step 1: Execute Minimal TDD Script
```bash
./demeter-uow-executor.sh [execution-plan.yaml]
```

**Examples:**
```bash
# Use default execution plan
./demeter-uow-executor.sh

# Use custom execution plan
./demeter-uow-executor.sh custom-execution-plan.yaml

# Use specific batch configuration
./demeter-uow-executor.sh batch/configs/sprint-1-plan.yaml
```

**Script Output:**
- Creates `.demeter/logs/` directory
- Generates `.demeter/TDD_EXECUTOR.prompt`
- Provides execution instructions

### Step 2: Execute TDD Master Prompt
```bash
# Open .demeter/TDD_EXECUTOR.prompt in Claude Code
```

**Claude Code TDD Processing:**

#### Phase 1: Load and Parse Execution Plan
1. **Execution Plan Analysis**
   - Parse UoW sequences and dependencies
   - Identify complexity levels for each UoW
   - Extract acceptance criteria
   - Create execution timeline

2. **Dependency Resolution**
   - Map prerequisite UoWs
   - Identify parallel execution opportunities
   - Plan integration points

#### Phase 2: Sequential TDD Execution

For each UoW in dependency order:

##### 🔴 RED Phase
1. **GraphRAG Query for Testing Patterns**
   ```
   Query: "Testing patterns for [UoW-type] in [domain]"
   Source: .demeter-dev/knowledge/patterns/
   ```

2. **Create Failing Tests**
   - Unit tests for individual components
   - Integration tests for dependencies
   - Edge cases and error scenarios
   - Performance tests (if applicable)

3. **Verify RED State**
   - Run test suite
   - Confirm all tests fail as expected
   - Document test coverage plan

**Output**: Complete failing test suite

##### 🟢 GREEN Phase
1. **Apply Implementation Patterns**
   ```
   Query: "Implementation strategies for [requirement-type]"
   Source: .demeter-dev/knowledge/patterns/
   ```

2. **Complexity-Based Implementation**
   - **Simple UoWs**: Direct implementation, clarity focus
   - **Medium UoWs**: Modular design, single agent approach
   - **Complex UoWs**: Parallel agents, advanced patterns

3. **Minimal Code Implementation**
   - Write ONLY enough code to pass tests
   - No premature optimization
   - Follow incremental development

**Output**: All tests passing with minimal implementation

##### 🔵 REFACTOR Phase
1. **Code Quality Improvements**
   - Remove duplication (DRY principle)
   - Improve naming and readability
   - Apply SOLID principles
   - Optimize performance where needed

2. **Enhanced Testing**
   - Add edge cases discovered during implementation
   - Improve test descriptions
   - Add performance benchmarks

3. **GraphRAG Knowledge Capture**
   ```
   Update: .demeter-dev/knowledge/lessons/
   - Document new patterns discovered
   - Capture implementation insights
   - Register reusable components
   ```

**Output**: Refactored code with enhanced quality

#### Phase 3: Progress Tracking
1. **Update Progress File**
   - `.demeter/tdd-progress.md`
   - Individual UoW completion status
   - Quality metrics and coverage

2. **Generate Phase Prompts**
   - `.demeter/logs/[UoW-ID]_red.prompt`
   - `.demeter/logs/[UoW-ID]_green.prompt`
   - `.demeter/logs/[UoW-ID]_refactor.prompt`

#### Phase 4: Integration Validation
1. **Full Test Suite Execution**
2. **Acceptance Criteria Validation**
3. **Integration Testing**
4. **Quality Gate Verification**

### Step 3: Monitor and Track Progress

#### Real-time Monitoring
```bash
# Check progress
cat .demeter/tdd-progress.md

# Review individual UoW logs
ls .demeter/logs/

# Check GraphRAG knowledge updates
ls .demeter-dev/knowledge/lessons/
```

#### Quality Gates Validation
- **Foundation Layer**: 80%+ test coverage, security scan
- **Application Layer**: 60%+ test coverage, business logic validation
- **Integration Layer**: Integration tests, end-to-end tests
- **Deployment Layer**: Security scanning, performance testing

### Step 4: Handle Complex UoWs

#### Parallel Agent Coordination
For complex UoWs, Claude Code will:
1. **Decompose into sub-tasks**
2. **Launch parallel agents**
3. **Coordinate through shared interfaces**
4. **Apply advanced patterns from GraphRAG**

#### Example Complex UoW: Authentication System
```
Sub-tasks:
- User registration (Agent 1)
- Password hashing (Agent 2)
- JWT token generation (Agent 3)
- Token validation (Agent 4)
- Integration layer (Coordination)
```

## Success Indicators

### ✅ TDD Cycle Complete
- [ ] All UoWs completed with RED-GREEN-REFACTOR cycle
- [ ] Test coverage meets quality gate requirements
- [ ] GraphRAG knowledge base updated with lessons
- [ ] All acceptance criteria validated
- [ ] Integration tests passing
- [ ] Code quality standards met

### ✅ Knowledge Capture
- [ ] New patterns documented in .demeter-dev/knowledge/patterns/
- [ ] Implementation lessons captured in .demeter-dev/knowledge/lessons/
- [ ] Reusable components registered
- [ ] Query examples updated

## Troubleshooting

### Common Issues

**Issue: Tests not failing in RED phase**
- **Solution**: Review acceptance criteria clarity
- **Action**: Use GraphRAG to query similar testing patterns

**Issue: Complex UoW overwhelming single agent**
- **Solution**: Decompose into smaller sub-UoWs
- **Action**: Use parallel agent coordination

**Issue: Integration tests failing**
- **Solution**: Check UoW dependency sequence
- **Action**: Review execution plan ordering

**Issue: Quality gates not met**
- **Solution**: Review test coverage and quality metrics
- **Action**: Add additional tests in REFACTOR phase

### Recovery Steps

1. **Restart Individual UoW:**
   ```bash
   # Remove UoW logs and restart
   rm .demeter/logs/UoW-XXX_*
   # Re-execute TDD prompt for specific UoW
   ```

2. **Manual Phase Execution:**
   - Use individual phase prompts in .demeter/logs/
   - Execute RED, GREEN, REFACTOR phases separately

3. **Quality Gate Recovery:**
   - Focus on failing quality metrics
   - Use GraphRAG to find improvement strategies

## Advanced Features

### GraphRAG-Enhanced Development
```
Queries during development:
- "Best practices for [technology] in [domain]"
- "Testing strategies for [component-type]"
- "Performance optimization for [use-case]"
- "Security considerations for [feature]"
```

### Continuous Knowledge Learning
- Every TDD cycle enhances the knowledge base
- Patterns emerge and become reusable
- Team expertise is captured and shared
- Future UoWs benefit from past learnings

## Next Steps
After TDD completion:
1. Execute quality verification scripts
2. Prepare for deployment phase
3. Update project documentation
4. Review and refine development processes