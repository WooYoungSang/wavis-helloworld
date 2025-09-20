# 🧪 TDD-Driven UoW Executor - [UOW_ID]

## 🎯 UoW Information
- **ID**: [UOW_ID]
- **Name**: [UOW_NAME]
- **Complexity**: [COMPLEXITY]
- **Acceptance Criteria Count**: [AC_COUNT]
- **Estimated Duration**: [DURATION]

## 📋 TDD Implementation Overview
This UoW will be implemented following the **RED → GREEN → REFACTOR** cycle, ensuring all acceptance criteria are first converted to failing tests, then implemented with minimal code, and finally refactored for quality.

---

## 🔴 Phase 3: Test Specification (RED) with GraphRAG

### 3.1 GraphRAG Knowledge Injection
**Command**: `"Inject GraphRAG knowledge for [UOW_ID] testing patterns and acceptance criteria conversion"`

```markdown
## Pre-RED Phase Knowledge Integration
1. **Pattern Query**: "Find testing patterns for [UOW_TYPE] and test creation strategies"
2. **Lesson Review**: "Query testing challenges and solutions for [DOMAIN/TECHNOLOGY]"
3. **Component Discovery**: "Find reusable test utilities and testing frameworks"
4. **Strategy Formation**: Apply proven testing patterns to UoW requirements
```

### 3.2 Acceptance Criteria Analysis
**Command**: `"Analyze acceptance criteria for [UOW_ID] and convert to comprehensive test specifications using GraphRAG patterns"`

```markdown
## AC-to-Test Conversion

### AC-1: [ACCEPTANCE_CRITERIA_1]
**Given**: [GIVEN_CONDITION]
**When**: [WHEN_ACTION]
**Then**: [THEN_RESULT]

→ **Test**: `test_[specific_behavior_1]()`
→ **Purpose**: Verify that [specific_behavior]
→ **Expected**: FAIL initially (Red)

### AC-2: [ACCEPTANCE_CRITERIA_2]
**Given**: [GIVEN_CONDITION]
**When**: [WHEN_ACTION]
**Then**: [THEN_RESULT]

→ **Test**: `test_[specific_behavior_2]()`
→ **Purpose**: Verify that [specific_behavior]
→ **Expected**: FAIL initially (Red)

[Continue for all acceptance criteria...]
```

### 3.3 Test-First Implementation with GraphRAG
**Command**: `"Create comprehensive failing test suite for [UOW_ID] using GraphRAG testing patterns and strategies"`

**Implementation Strategy by Complexity**:

#### Simple UoW (1-2 AC)
```markdown
## Direct Test Creation
1. Write all tests based on acceptance criteria
2. Ensure all tests FAIL initially
3. Verify test completeness and clarity
4. Document expected behavior in test names
```

#### Medium UoW (3-4 AC)
```markdown
## Agent-Assisted Test Creation with GraphRAG
"Launch general-purpose agent to create comprehensive test suite for [UOW_ID] using GraphRAG knowledge:

1. **Apply GraphRAG Testing Patterns**
   - Use proven test creation strategies from knowledge base
   - Apply domain-specific testing patterns
   - Leverage lessons learned from similar UoWs

2. **Analyze Acceptance Criteria**
   - Convert each AC to specific test scenarios using patterns
   - Include edge cases based on historical lessons
   - Ensure testable assertions using proven approaches

3. **Write Failing Tests**
   - Create test file: test_[uow_name].py/js/go
   - Apply test naming conventions from GraphRAG
   - All tests must initially FAIL
   - Use reusable test utilities from component library

4. **Verify Test Coverage**
   - Each AC maps to at least one test
   - Edge cases covered based on lessons learned
   - Error scenarios from GraphRAG knowledge included
   - Test independence verified using patterns"
```

#### Complex UoW (5+ AC)
```markdown
## Multi-Agent Test Development with GraphRAG
"Launch general-purpose agent for comprehensive test development of complex [UOW_ID] using GraphRAG knowledge:

1. **Apply GraphRAG Test Organization Patterns**
   - Use proven test grouping strategies
   - Apply complex UoW testing patterns from knowledge base
   - Leverage lessons from similar complex implementations

2. **Group Related Acceptance Criteria**
   - Group 1: Core functionality (AC-1, AC-2)
   - Group 2: Edge cases (AC-3, AC-4) based on historical patterns
   - Group 3: Error handling (AC-5, AC-6, AC-7) using proven strategies

3. **Create Test Suites by Group**
   - TestGroup1: Core behavior tests using established patterns
   - TestGroup2: Edge case tests based on lessons learned
   - TestGroup3: Error scenario tests from GraphRAG knowledge

4. **Ensure Comprehensive Coverage**
   - Minimum 1 test per acceptance criterion
   - Cross-cutting concerns from pattern library
   - Integration points validated using integration patterns
   - Performance criteria from quality patterns

5. **Test Quality Verification**
   - All tests initially FAIL (Red phase)
   - Clear test documentation using documentation patterns
   - Independent test execution following proven practices
   - Proper test data setup/teardown from component library"
```

### 3.3 Test Validation
```markdown
## RED Phase Verification
- [ ] All acceptance criteria converted to tests
- [ ] All tests written and executable
- [ ] All tests currently FAIL (Red)
- [ ] Test names clearly describe expected behavior
- [ ] Test coverage includes edge cases
- [ ] Tests are independent and isolated
```

---

## 🟢 Phase 4: Minimal Implementation (GREEN) with GraphRAG

### 4.1 GraphRAG Pattern Application
**Command**: `"Apply GraphRAG implementation patterns and strategies for [UOW_ID] GREEN phase"`

```markdown
## GREEN Phase Knowledge Integration
1. **Pattern Application**: "Find minimal implementation patterns for [FEATURE_TYPE]"
2. **Solution Strategies**: "Query proven implementation approaches for [DOMAIN]"
3. **Debugging Knowledge**: "Find debugging techniques and troubleshooting for [TECHNOLOGY]"
4. **Quality Patterns**: Apply established coding standards and practices
```

### 4.2 Implementation Strategy
**Command**: `"Implement minimal code to make all tests pass for [UOW_ID] using GraphRAG knowledge and TDD principles"`

```markdown
## TDD Implementation Rules
1. **Write ONLY enough code to pass tests**
   - No premature optimization
   - No extra features beyond AC
   - Focus solely on test satisfaction

2. **Incremental Development**
   - Implement one test at a time
   - Run tests after each change
   - Move to next test only when current passes

3. **Continuous Verification**
   - Run test suite frequently
   - Ensure no regression
   - Maintain GREEN state
```

### 4.2 Implementation by Complexity

#### Simple UoW (1-2 AC)
```markdown
## Direct Implementation
"Implement [UOW_ID] step by step:

1. **Test 1 Implementation**
   - Write minimal code for first failing test
   - Run test to verify it passes
   - Commit working state

2. **Test 2 Implementation**
   - Write minimal code for second failing test
   - Run full test suite
   - Ensure all tests pass

3. **Final Verification**
   - All tests GREEN
   - Code is minimal and focused
   - No unnecessary complexity added"
```

#### Medium UoW (3-4 AC)
```markdown
## Agent-Assisted Implementation
"Launch general-purpose agent to implement [UOW_ID] using TDD GREEN phase:

1. **Incremental Implementation**
   - Start with simplest failing test
   - Write minimal code to pass each test
   - Run tests after each implementation
   - Ensure continuous GREEN state

2. **Code Organization**
   - Create necessary files and structures
   - Implement core functionality first
   - Add error handling as needed
   - Keep code simple and focused

3. **Integration Points**
   - Implement interface contracts
   - Handle dependencies properly
   - Ensure clean integration
   - Maintain test isolation

4. **Continuous Validation**
   - Run full test suite regularly
   - Fix any breaking changes immediately
   - Document implementation decisions
   - Prepare for refactoring phase"
```

#### Complex UoW (5+ AC)
```markdown
## Multi-Phase Implementation
"Launch general-purpose agent for complex [UOW_ID] implementation:

1. **Phase 1: Core Functionality**
   - Implement tests for basic features
   - Focus on primary use cases
   - Establish main code structure
   - Verify core tests pass

2. **Phase 2: Edge Cases**
   - Implement edge case handling
   - Add input validation
   - Handle boundary conditions
   - Verify edge case tests pass

3. **Phase 3: Error Handling**
   - Implement error scenarios
   - Add proper exception handling
   - Create error recovery mechanisms
   - Verify error tests pass

4. **Phase 4: Integration**
   - Connect all components
   - Ensure proper data flow
   - Validate integration points
   - Run complete test suite

5. **Final Verification**
   - All 5+ acceptance criteria tested
   - All tests consistently GREEN
   - Code coverage exceeds 80%
   - No unnecessary complexity added"
```

### 4.3 Implementation Verification
```markdown
## GREEN Phase Verification
- [ ] All tests now PASS (Green)
- [ ] Code implements all acceptance criteria
- [ ] Implementation is minimal and focused
- [ ] No premature optimization added
- [ ] Test coverage meets requirements
- [ ] Code is ready for refactoring
```

---

## 🔵 Phase 5: Code Enhancement (REFACTOR) with GraphRAG

### 5.1 GraphRAG Knowledge Capture
**Command**: `"Capture and document GraphRAG knowledge from [UOW_ID] implementation"`

```markdown
## REFACTOR Phase Knowledge Enhancement
1. **Pattern Documentation**: "Document [PATTERN_NAME] discovered during implementation"
2. **Lesson Capture**: "Capture implementation lessons and insights from [UOW_ID]"
3. **Component Registration**: "Register reusable [COMPONENT_TYPE] for future use"
4. **Cross-Reference**: Link new knowledge to existing patterns and lessons
```

### 5.2 Refactoring Strategy
**Command**: `"Refactor [UOW_ID] implementation using GraphRAG patterns while maintaining all passing tests"`

```markdown
## Refactoring Principles
1. **Maintain Test Success**
   - All tests must remain GREEN
   - Run tests after each refactoring
   - Never break existing functionality

2. **Code Quality Improvement**
   - Remove code duplication
   - Improve naming and readability
   - Apply SOLID principles
   - Enhance maintainability

3. **Performance Optimization**
   - Optimize algorithms where beneficial
   - Improve resource usage
   - Add caching if appropriate
   - Maintain simplicity
```

### 5.2 Refactoring Checklist

#### Code Structure Improvements
```markdown
## Structural Refactoring
- [ ] **Extract Methods**: Break down large functions
- [ ] **Remove Duplication**: DRY principle application
- [ ] **Improve Naming**: Clear, descriptive names
- [ ] **Organize Imports**: Clean dependencies
- [ ] **Apply Patterns**: Use appropriate design patterns
```

#### Performance & Quality
```markdown
## Quality Enhancement
- [ ] **Code Documentation**: Add comprehensive docstrings
- [ ] **Type Safety**: Add type hints/annotations
- [ ] **Error Handling**: Improve exception management
- [ ] **Logging**: Add appropriate logging
- [ ] **Security**: Apply security best practices
```

#### Test Enhancement
```markdown
## Test Suite Improvement
- [ ] **Add Edge Cases**: Discovered during implementation
- [ ] **Performance Tests**: If NFR requirements exist
- [ ] **Integration Tests**: Cross-component validation
- [ ] **Test Documentation**: Clear test descriptions
- [ ] **Test Coverage**: Verify >80% coverage maintained
```

### 5.3 Refactoring by Complexity

#### Simple UoW (1-2 AC)
```markdown
## Direct Refactoring
"Refactor [UOW_ID] focusing on code quality:

1. **Code Cleanup**
   - Improve variable and function names
   - Remove any code duplication
   - Add proper documentation
   - Ensure consistent formatting

2. **Quality Verification**
   - Run all tests to ensure GREEN
   - Check code readability
   - Verify maintainability
   - Update documentation"
```

#### Medium UoW (3-4 AC)
```markdown
## Agent-Assisted Refactoring
"Launch general-purpose agent for [UOW_ID] refactoring:

1. **Structural Improvements**
   - Extract reusable functions
   - Organize code into logical modules
   - Apply appropriate design patterns
   - Improve code organization

2. **Quality Enhancements**
   - Add comprehensive documentation
   - Improve error handling
   - Add type safety features
   - Apply coding standards

3. **Performance Optimization**
   - Identify optimization opportunities
   - Improve algorithm efficiency
   - Add appropriate caching
   - Maintain code simplicity

4. **Continuous Testing**
   - Run tests after each refactoring
   - Ensure 100% tests remain GREEN
   - Add any missing edge case tests
   - Verify code coverage maintained"
```

#### Complex UoW (5+ AC)
```markdown
## Comprehensive Refactoring
"Launch general-purpose agent for complex [UOW_ID] refactoring:

1. **Architecture Review**
   - Analyze overall code structure
   - Identify architectural improvements
   - Plan refactoring strategy
   - Ensure design pattern consistency

2. **Modular Refactoring**
   - Refactor core functionality module
   - Improve edge case handling
   - Enhance error management
   - Optimize integration points

3. **Quality Assurance**
   - Comprehensive documentation
   - Advanced error handling
   - Performance optimization
   - Security hardening

4. **Final Validation**
   - All tests remain GREEN
   - Code coverage >80%
   - Performance meets NFR
   - Security requirements satisfied
   - Documentation complete"
```

### 5.4 Comprehensive GraphRAG Knowledge Documentation
```markdown
## Complete GraphRAG Knowledge Integration
"Document comprehensive implementation insights and update GraphRAG knowledge base from [UOW_ID]:

1. **Pattern Documentation**
   - Register architectural patterns discovered
   - Document design patterns applied successfully
   - Create pattern templates with usage examples
   - Update pattern cross-references and relationships

2. **Lesson Learned Integration**
   - Document challenges and solutions discovered
   - Capture performance optimization insights
   - Record quality improvement techniques
   - Create lesson templates for similar scenarios

3. **Component Library Enhancement**
   - Extract and register reusable components
   - Document component interfaces and usage
   - Create component integration examples
   - Update component dependency mappings

4. **Query Knowledge Enhancement**
   - Add new query examples based on implementation
   - Update query effectiveness based on usage
   - Document successful knowledge application patterns
   - Create domain-specific query templates

5. **Knowledge Metrics Update**
   - Track pattern reuse effectiveness
   - Measure knowledge application success
   - Document time savings from knowledge use
   - Update knowledge quality metrics"
```

---

## ✅ Phase 5 Completion Verification

### Final Quality Gates with GraphRAG
```markdown
## TDD Cycle Completion Checklist with GraphRAG Integration
- [ ] **RED Phase**: All tests initially failed using GraphRAG patterns ✅
- [ ] **GREEN Phase**: All tests now pass using proven strategies ✅
- [ ] **REFACTOR Phase**: Code quality improved with GraphRAG patterns ✅
- [ ] **Test Coverage**: Minimum 80% achieved following quality patterns ✅
- [ ] **Acceptance Criteria**: 100% implemented using established approaches ✅
- [ ] **Documentation**: Complete and accurate following documentation patterns ✅
- [ ] **GraphRAG Enhanced**: New patterns, lessons, and components documented ✅
- [ ] **Knowledge Reuse**: Successfully applied existing knowledge ✅
- [ ] **Knowledge Creation**: Generated new reusable knowledge ✅
- [ ] **Performance**: Meets NFR requirements using optimization patterns ✅
- [ ] **Security**: Best practices applied from security patterns ✅
- [ ] **Integration**: Works with existing code using integration patterns ✅
```

### Success Metrics with GraphRAG
```markdown
## UoW Implementation Results with Knowledge Integration
- **Test Count**: [TOTAL_TESTS] tests created using GraphRAG patterns
- **Coverage**: [COVERAGE_PERCENTAGE]% code coverage (Target: 80%+)
- **Performance**: [PERFORMANCE_METRICS] using optimization patterns
- **Quality Score**: [QUALITY_RATING] with GraphRAG quality patterns
- **Time Taken**: [ACTUAL_DURATION] vs [ESTIMATED_DURATION]
- **Knowledge Reused**: [PATTERNS_APPLIED] patterns applied
- **Knowledge Created**: [NEW_PATTERNS] new patterns documented
- **Components Registered**: [COMPONENTS_CREATED] reusable components
- **Lessons Learned**: [LESSONS_CAPTURED] lessons documented
- **Knowledge Effectiveness**: [EFFECTIVENESS_RATING] application success rate
```

---

## 🔄 Integration Preparation

### Next Steps
```markdown
## Post-Implementation Actions
1. **Integration Testing**: Verify compatibility with other UoWs
2. **Dependency Updates**: Update dependent UoWs if needed
3. **Documentation**: Update project documentation
4. **Knowledge Sharing**: Share insights with team
5. **Progress Tracking**: Update project progress status
```

---

**🧪 TDD Success: [UOW_ID] Complete**

> *RED → GREEN → REFACTOR: Quality through disciplined development*