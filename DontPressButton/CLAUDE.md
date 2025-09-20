# 🤖 DontPressButton - AI Development Guidelines
# Claude Code Constitutional SDD Development Framework
# 🧠 GraphRAG 통합 개발 워크플로우

## 🏛️ Constitutional Development Mandate

You are developing **DontPressButton** under the **Demeter WAVIS v2.0 Constitutional SDD Framework**. Every code decision must align with our **9 Constitutional Principles**. This is not optional—it is the supreme governance framework for this project.

### 📜 Constitutional Principles (Non-Negotiable)

1. **Library-First Development** ⚖️ MANDATORY
   - Use native browser APIs: `dialog`, DOM, events
   - NO external libraries unless absolutely critical
   - Justify any dependency in PR with constitutional impact assessment

2. **CLI Interface Mandate** ⚖️ ADVISORY (Web Application)
   - Ensure all development commands work via npm scripts
   - Build, test, deploy must be CLI accessible

3. **Test-First Imperative** ⚖️ NON-NEGOTIABLE
   - **ABSOLUTE RULE**: Write tests BEFORE implementation
   - PRs cannot merge without tests preceding code
   - 100% coverage for user interactions

4. **Simplicity Over Complexity** ⚖️ MANDATORY
   - Single HTML file with embedded CSS/JS for MVP
   - Direct solutions over complex architectures
   - Question every layer of abstraction

5. **Anti-Premature Abstraction** ⚖️ MANDATORY
   - Direct DOM manipulation
   - No state management libraries
   - No component frameworks for this simple app

6. **Integration-First Testing** ⚖️ MANDATORY
   - Prioritize E2E tests over unit tests
   - Test complete user journeys
   - Minimal unit tests only for complex logic

7. **Minimal Project Structure** ⚖️ MANDATORY
   - Flat structure: src/, tests/, config/, docs/
   - No deep nesting
   - Justify every new directory

8. **Framework Direct Usage** ⚖️ MANDATORY
   - Native HTML5 `<dialog>` element
   - Direct DOM APIs
   - No abstraction layers

9. **Comprehensive Testing** ⚖️ MANDATORY
   - 100% coverage for critical user interactions
   - Accessibility compliance testing
   - Performance validation

## 🎯 Project Context

### What We're Building
Interactive web application with a "Don't Press Button" that:
- Shows Korean warning messages on each click
- Displays payment confirmation modal on 10th click
- Demonstrates delightful micro-interactions
- Maintains constitutional compliance throughout

### Technical Architecture (Constitutional)
- **Single HTML file** with embedded CSS/JS (Principle 4: Simplicity)
- **Native browser APIs** only (Principles 1, 8: Library-First, Framework-Direct)
- **Direct DOM manipulation** (Principle 5: Anti-Abstraction)
- **Configuration via JSON** (externalized content)

### Quality Standards (Constitutional)
- **Sub-100ms click response** (Performance-First domain principle)
- **Zero accessibility violations** (Accessibility-First domain principle)
- **100% test coverage** for user interactions (Principle 9)
- **Mobile-first responsive design** (Mobile-First domain principle)

## 🔥 Development Rules (Enforce Strictly)

### ❌ FORBIDDEN (Constitutional Violations)
- React, Vue, Angular, or any UI framework
- jQuery, Lodash, or utility libraries
- State management libraries (Redux, MobX, etc.)
- CSS frameworks (Bootstrap, Tailwind, etc.)
- Build tools beyond simple bundling
- Complex abstractions or layers
- Skipping tests or writing tests after code

### ✅ REQUIRED (Constitutional Compliance)
- Native HTML5 `<dialog>` for modal
- Direct `addEventListener` for interactions
- Closure pattern for state management
- CSS Grid/Flexbox for layout
- Native `fetch` for configuration loading
- Jest + Playwright for testing
- axe-core for accessibility testing

## 🧪 Testing Strategy (Constitutional)

### Test-First Methodology
1. **Write failing test** for new functionality
2. **Implement minimal code** to make test pass
3. **Refactor** while maintaining constitutional compliance
4. **Verify** constitutional principles in implementation

### Testing Hierarchy (Integration-First)
1. **E2E Tests**: Complete user journeys (primary focus)
2. **Integration Tests**: Component interactions
3. **Unit Tests**: Only for complex algorithms
4. **Accessibility Tests**: Comprehensive a11y validation
5. **Performance Tests**: Sub-100ms interaction benchmarks

### Required Test Coverage
- ✅ 100% for button click handling
- ✅ 100% for modal behavior
- ✅ 100% for state transitions
- ✅ 100% for accessibility features
- ✅ 100% for configuration loading

## 📁 File Organization (Minimal Structure)

```
DontPressButton/
├── src/
│   └── index.html          # Single-file application (Constitutional)
├── tests/
│   ├── e2e/               # Integration-first testing
│   ├── integration/       # Component interaction tests
│   ├── accessibility/     # A11y compliance tests
│   └── performance/       # Performance validation
├── config/
│   └── app.config.json    # Externalized configuration
├── docs/
│   ├── requirement.md     # Original requirements
│   └── README.md          # Project documentation
├── PROJECT-constitution.yaml  # Supreme governance document
├── merged-ssot.yaml       # Single Source of Truth
└── CLAUDE.md             # This file - AI development guidelines
```

## 🎨 Implementation Guidelines

### HTML Structure (Semantic & Accessible)
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Constitutional compliance: Minimal, essential meta tags -->
</head>
<body>
  <header>
    <h1>Don't Press Button</h1>
  </header>
  <main>
    <div id="message-area"></div>
    <button id="main-button">Don't Press Button</button>
  </main>
  <dialog id="payment-modal">
    <!-- Constitutional compliance: Native dialog element -->
  </dialog>
</body>
</html>
```

### CSS Approach (Embedded, Intentionally Crude)
```css
/* Constitutional compliance: Embedded CSS, no external dependencies */
body {
  /* Intentionally crude styling for personality */
  font-family: system-ui, Arial, sans-serif;
  /* Mobile-first responsive design */
}

h1 {
  /* Deliberately rough aesthetic */
  transform: skewX(-2deg);
  text-shadow: 1px 1px 0 #0002;
}

button {
  /* Constitutional: 44px minimum touch target */
  min-height: 44px;
  background: #d62828; /* Brand red */
  /* Accessibility: 4.5:1 contrast ratio */
}
```

### JavaScript Pattern (Constitutional State Management)
```javascript
// Constitutional compliance: Closure pattern, no abstractions
(function DontPressButtonApp() {
  'use strict';

  // State management (Constitutional: simple, direct)
  let clickCount = 0;
  let config = null;

  // Constitutional: Native DOM APIs only
  const elements = {
    button: document.getElementById('main-button'),
    messageArea: document.getElementById('message-area'),
    modal: document.getElementById('payment-modal')
  };

  // Constitutional: Direct event handling
  function handleButtonClick() {
    clickCount++;
    updateMessage();

    if (clickCount === config.pressToConfirmCount) {
      showPaymentModal();
    }
  }

  // Constitutional: Performance requirement < 100ms
  function updateMessage() {
    const randomMessage = getRandomMessage();
    elements.messageArea.textContent = randomMessage;
  }

  // Initialize (Constitutional: Configuration-driven)
  async function init() {
    config = await loadConfiguration();
    setupEventListeners();
  }

  init();
})();
```

## 🔍 Code Review Checklist (Constitutional Compliance)

### Before Writing Code
- [ ] Tests written first (Principle 3: Test-First)
- [ ] Architecture follows simplicity principle (Principle 4)
- [ ] No unnecessary abstractions planned (Principle 5)

### During Implementation
- [ ] Using native browser APIs directly (Principles 1, 8)
- [ ] Maintaining minimal project structure (Principle 7)
- [ ] Focusing on integration over unit tests (Principle 6)
- [ ] Direct DOM manipulation, no frameworks (Principle 5)

### Before PR Submission
- [ ] 100% test coverage achieved (Principle 9)
- [ ] Accessibility requirements met (Domain-specific)
- [ ] Performance benchmarks satisfied (< 100ms)
- [ ] Constitutional compliance validated (All principles)
- [ ] No external dependencies added without justification

## 🚨 Constitutional Debt Monitoring

### Red Flags (Immediate Violation)
- External library usage without constitutional justification
- Tests written after implementation
- Complex abstractions introduced
- Performance degradation below 100ms
- Accessibility violations

### Yellow Flags (Constitutional Debt Risk)
- File structure becoming complex
- Code patterns becoming abstract
- Testing becoming unit-test heavy
- Configuration becoming hardcoded

### Green Flags (Constitutional Compliance)
- Native APIs used throughout
- Tests drive implementation
- Direct, simple solutions
- Excellent performance
- Full accessibility compliance

## 📈 Success Metrics (Constitutional)

### Technical Metrics
- ✅ 100% constitutional principle adherence
- ✅ 0 accessibility violations
- ✅ < 100ms interaction response time
- ✅ 100% test coverage for interactions
- ✅ Single-file deployment achieved

### User Experience Metrics
- ✅ Delightful micro-interaction achieved
- ✅ Cross-device compatibility confirmed
- ✅ Keyboard navigation excellent
- ✅ Screen reader compatibility perfect

## 🎯 Implementation Phases

### Phase 1: Foundation (UoW-001, UoW-002)
- Create HTML structure with semantic elements
- Implement click counting with direct state management
- Add random Korean message display
- Ensure < 100ms response time

### Phase 2: Modal Implementation (UoW-003, UoW-004)
- Implement native `<dialog>` element
- Add focus trap and ESC handling
- Implement Yes/No button actions
- Ensure full accessibility compliance

### Phase 3: Configuration & Testing (UoW-005, UoW-006)
- Externalize all content to configuration
- Implement comprehensive test suite
- Validate constitutional compliance
- Prepare single-file deployment

## 🧠 GraphRAG 통합 개발 워크플로우

**모든 개발 작업은 GraphRAG 통합 시스템을 통해 수행됩니다:**

### 🚀 자동 컨텍스트 쿼리 (모든 프롬프트 시작 시)
```bash
# 개발 작업 시작 전 자동 실행
./.demeter-dev/auto-dev.sh
```

1. **Constitutional 원칙 컨텍스트**: 작업에 적용되는 9가지 원칙 자동 식별
2. **UoW 의존성 분석**: 관련 Units of Work와 의존성 자동 매핑
3. **기술적 가이던스**: 사용할 네이티브 API와 패턴 제안
4. **품질 게이트**: 충족해야 할 성능/접근성 요구사항 제시

### 📤 자동 결과 인제스트 (모든 개발 완료 후)
```bash
# 개발 결과 자동 저장
./.demeter-dev/graphrag/auto-graphrag.sh finalize task-id "작업설명" "수정파일들" "구현노트"
```

1. **구현 세부사항**: 코드 변경사항과 구현 패턴 저장
2. **Constitutional 컴플라이언스**: 원칙 준수 여부 기록
3. **성능 메트릭스**: 측정된 성능 데이터 저장
4. **레슨 학습**: 발견된 패턴과 개선사항 축적

### 🎯 개발 명령어 (GraphRAG 통합)

```bash
# 1. UoW 구현 (자동 컨텍스트 + 인제스트)
./.demeter-dev/auto-dev.sh uow UOW-001 "버튼 클릭 핸들링"

# 2. Test-First 개발
./.demeter-dev/auto-dev.sh test-first Button "버튼 컴포넌트"

# 3. Constitutional 컴플라이언스 체크
./.demeter-dev/auto-dev.sh compliance "Modal 구현"

# 4. 성능 최적화
./.demeter-dev/auto-dev.sh performance "버튼 응답성"

# 5. 접근성 개선
./.demeter-dev/auto-dev.sh accessibility "키보드 네비게이션"

# 6. 대화형 개발 세션
./.demeter-dev/auto-dev.sh interactive
```

## 🤝 AI Assistant Guidelines (GraphRAG 강화)

**모든 개발 작업 전에 반드시 수행:**

1. **🔍 GraphRAG 컨텍스트 쿼리**:
   ```bash
   ./.demeter-dev/graphrag/auto-graphrag.sh context "작업 설명" "작업 타입"
   ```

2. **📜 Constitutional 가이던스 확인**:
   ```bash
   ./.demeter-dev/graphrag/auto-graphrag.sh compliance "구체적 구현 계획"
   ```

3. **🎯 구현 수행**: GraphRAG에서 제공된 컨텍스트와 제약사항 준수

4. **📤 결과 인제스트**:
   ```bash
   ./.demeter-dev/graphrag/auto-graphrag.sh finalize "task-id" "설명" "파일들" "노트"
   ```

### 📋 GraphRAG 기반 체크리스트

**개발 작업 시작 전:**
- [ ] GraphRAG에서 Constitutional 요구사항 확인
- [ ] 관련 UoW 의존성 분석 완료
- [ ] 성능/접근성 품질 게이트 확인
- [ ] 기존 패턴과 컴포넌트 재사용 가능성 검토

**개발 작업 중:**
- [ ] Constitutional 원칙 실시간 준수
- [ ] Test-First 방법론 적용
- [ ] 네이티브 브라우저 API 우선 사용
- [ ] 성능 요구사항 (<100ms) 지속 모니터링

**개발 작업 완료 후:**
- [ ] 모든 변경사항 GraphRAG에 인제스트
- [ ] Constitutional 컴플라이언스 검증
- [ ] 성능/접근성 메트릭스 기록
- [ ] 레슨 학습과 패턴 축적

## 🔄 Next Steps

1. Review PROJECT-constitution.yaml and merged-ssot.yaml
2. Understand batch/execution-plan.yaml dependencies
3. Begin UoW-001 implementation with tests-first
4. Maintain constitutional compliance monitoring
5. Validate quality gates at each milestone

---

**Remember: Constitutional compliance is not optional. Every line of code must demonstrate adherence to our 9 Constitutional Principles. When in doubt, choose the simpler, more direct solution that follows the constitution.**

**This project is a demonstration of Constitutional SDD excellence. Make it exemplary.**