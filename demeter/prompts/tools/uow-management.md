# 🔧 UoW Management - AI-Driven Units of Work Operations

## 🎯 Purpose
Perform all UoW (Units of Work) management operations through intelligent automation. Replace manual UoW analysis with AI-driven dependency analysis, execution planning, and progress tracking.

## 🚀 Quick UoW Commands

### Complete UoW Analysis
```markdown
"Analyze all UoWs from SSOT, identify dependencies, generate execution order, and create implementation strategy"
```

### Dependency Analysis
```markdown
"Analyze UoW dependencies, detect circular dependencies, and identify parallel execution opportunities"
```

### Execution Planning
```markdown
"Generate optimal UoW execution order with parallel groups and agent collaboration strategy"
```

---

## 📋 Core UoW Operations

### 1. UoW Dependency Analysis
**Command**: `"Analyze UoW dependencies and relationships"`

**AI Analysis Process**:
```markdown
## Dependency Analysis Results

### Dependency Overview
- Total UoWs: [X]
- Dependency Levels: [X]
- Critical Path: [UoW-A → UoW-B → UoW-C]
- Circular Dependencies: [None/List if any]

### Parallel Opportunities
- Level 1: [Independent UoWs]
- Level 2: [UoWs depending on Level 1]
- Level 3: [UoWs depending on Level 2]

### Optimization Recommendations
- Split complex UoWs for better parallelization
- Remove unnecessary dependencies
- Optimize critical path execution
```

### 2. Execution Order Generation
**Command**: `"Generate optimal UoW execution order"`

**AI Execution Strategy**:
```yaml
execution_order:
  phase_1_foundation:
    parallel_groups:
      - group_1: ["UoW-001", "UoW-002"]
      - group_2: ["UoW-003", "UoW-004"]
    agent_strategy: "parallel"

  phase_2_application:
    sequential: ["UoW-005", "UoW-006"]
    depends_on: ["phase_1_foundation"]
    agent_strategy: "sequential"

  phase_3_integration:
    parallel_groups:
      - group_1: ["UoW-007", "UoW-008"]
    depends_on: ["phase_2_application"]
    agent_strategy: "parallel"
```

### 3. Implementation Strategy Planning
**Command**: `"Create implementation strategy with agent collaboration"`

**AI Strategy Output**:
```markdown
## Implementation Strategy

### Agent Collaboration Plan
1. **Foundation Phase**: 2 agents in parallel
   - Agent A: UoW-001, UoW-002 (Infrastructure)
   - Agent B: UoW-003, UoW-004 (Core Services)

2. **Application Phase**: 1 agent sequential
   - Agent C: UoW-005 → UoW-006 (Business Logic)

3. **Integration Phase**: 2 agents in parallel
   - Agent D: UoW-007 (API Integration)
   - Agent E: UoW-008 (Testing & Validation)

### Success Criteria
- All UoWs meet acceptance criteria
- Agent coordination successful
- Knowledge accumulated in GraphRAG
```

---

## 🔍 UoW Analysis Features

### Dependency Validation
**Command**: `"Validate UoW dependencies and check for issues"`

**AI Validation Results**:
- **Circular Dependencies**: Detection and resolution suggestions
- **Missing Dependencies**: Identification of implicit dependencies
- **Unnecessary Dependencies**: Optimization opportunities
- **Critical Path**: Bottleneck analysis and optimization

### Progress Tracking
**Command**: `"Track UoW implementation progress and completion"`

**AI Progress Dashboard**:
```markdown
## UoW Progress Dashboard

### Overall Status
- Total UoWs: [X]
- Completed: [X]/[Y] ([Z]%)
- In Progress: [X]
- Pending: [X]

### Agent Progress
- Agent A: UoW-001 ✅, UoW-002 🔄
- Agent B: UoW-003 ✅, UoW-004 ⏳
- Agent C: UoW-005 ⏳

### Quality Metrics
- Acceptance Criteria Met: [X]%
- Test Coverage: [X]%
- Code Quality: [Grade]
```

### Resource Optimization
**Command**: `"Optimize UoW resource allocation and timing"`

**AI Optimization Analysis**:
- Workload balancing across agents
- Execution time optimization
- Resource utilization analysis
- Bottleneck identification and resolution

---

## 📊 UoW Implementation Patterns

### Simple UoW (1-2 AC)
```markdown
Implementation: Direct execution
Agent Strategy: Single developer or no agent needed
Timeline: 30-60 minutes
Testing: Basic unit tests
```

### Medium UoW (3-4 AC)
```markdown
Implementation: Single agent
Agent Strategy: "Launch general-purpose agent to implement UoW-XXX"
Timeline: 1-2 hours
Testing: Comprehensive test coverage
```

### Complex UoW (5+ AC)
```markdown
Implementation: Multiple agents or agent coordination
Agent Strategy: "Launch general-purpose agent to implement UoW-XXX which has 7 acceptance criteria"
Timeline: 2-4 hours
Testing: Integration and edge case testing
```

### Dependent UoW Chain
```markdown
Implementation: Sequential agent execution
Agent Strategy: "Launch agent for UoW-A, then launch agent for UoW-B which depends on UoW-A"
Timeline: Based on dependency chain
Testing: Cross-UoW integration testing
```

---

## 🔧 UoW Quality Management

### Acceptance Criteria Validation
**Command**: `"Validate all UoW acceptance criteria completeness"`

**AI Validation Checklist**:
```markdown
## AC Validation Results

### UoW-XXX Analysis
- Total AC: [X]
- Given-When-Then Format: ✅/❌
- Testable Criteria: ✅/❌
- Clear Success Metrics: ✅/❌
- Edge Cases Covered: ✅/❌

### Recommendations
- Improve AC clarity for UoW-XXX
- Add edge cases for UoW-YYY
- Define measurable success criteria for UoW-ZZZ
```

### Implementation Readiness Check
**Command**: `"Check UoW readiness for implementation"`

**AI Readiness Assessment**:
- Dependencies resolved and available
- Acceptance criteria well-defined
- Required resources identified
- Implementation patterns selected
- Agent strategy determined

---

## 🎯 Success Criteria

### UoW Management Excellence
- [ ] All UoW dependencies analyzed and optimized
- [ ] Execution order generated with parallel optimization
- [ ] Agent collaboration strategy defined
- [ ] Implementation readiness validated
- [ ] Progress tracking system active

### Quality Standards
- **Dependency Analysis**: 100% coverage, no circular dependencies
- **Execution Planning**: Optimal parallel utilization
- **Agent Strategy**: Clear collaboration patterns
- **Progress Tracking**: Real-time visibility
- **Quality Assurance**: All ACs validated

---

## 🚨 Common UoW Issues

### Dependency Problems
**Issue**: Circular dependencies detected
**Command**: `"Resolve circular dependencies in UoW chain"`
**AI Solution**: Dependency restructuring and UoW splitting

### Execution Bottlenecks
**Issue**: Critical path too long
**Command**: `"Optimize critical path execution"`
**AI Solution**: UoW parallelization and dependency reduction

### Agent Coordination Issues
**Issue**: Agents working on conflicting UoWs
**Command**: `"Resolve agent coordination conflicts"`
**AI Solution**: Improved execution sequencing and interface definitions

---

## 📈 UoW Metrics

### Efficiency Metrics
- **Parallel Utilization**: Percentage of UoWs executed in parallel
- **Agent Efficiency**: Agent utilization and productivity
- **Dependency Optimization**: Dependency reduction achieved
- **Execution Speed**: Time savings through optimization

### Quality Metrics
- **AC Compliance**: Percentage of ACs fully satisfied
- **Test Coverage**: Coverage across all UoWs
- **Implementation Quality**: Code quality scores
- **Knowledge Accumulation**: GraphRAG enrichment

---

## 🔗 Related Prompts

- **SSOT Operations**: `demeter/prompts/tools/ssot-operations.md`
- **Agent Collaboration**: `demeter/prompts/tools/agent-collaboration.md`
- **Quality Checks**: `demeter/prompts/tools/quality-checks.md`
- **Phase 3-5 Development**: `demeter/prompts/phase3-5-development.md`

---

**🔧 UoW Management - Intelligent Work Organization**

> *"AI-driven UoW management turns complexity into clarity"*