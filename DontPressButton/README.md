# 🚫 DontPressButton

> An interactive web application demonstrating Constitutional SDD principles through delightful micro-interactions

![Constitutional SDD](https://img.shields.io/badge/Framework-Constitutional%20SDD-blue)
![Test Coverage](https://img.shields.io/badge/Coverage-100%25-green)
![Accessibility](https://img.shields.io/badge/A11y-AAA-green)
![Performance](https://img.shields.io/badge/Performance-%3C100ms-green)

## 🎯 Overview

DontPressButton is a single-page web application that playfully challenges users not to press a prominent red button. With each click, it displays Korean warning messages, culminating in a payment confirmation modal on the 10th click. Built using the **Demeter WAVIS v2.0 Constitutional SDD Framework**, it exemplifies how constitutional principles can create simple, accessible, and delightful user experiences.

## ✨ Features

- **Interactive Button**: Large, prominent red button that begs to be pressed
- **Korean Warning Messages**: 20 playful Korean messages that appear randomly with each click
- **Payment Modal**: Confirmation dialog appears on the 10th click
- **Full Accessibility**: Keyboard navigation, screen reader support, ARIA compliance
- **Mobile-First**: Responsive design from 360px to desktop
- **Zero Dependencies**: Pure HTML5, CSS3, and JavaScript
- **Constitutional Compliance**: Demonstrates all 9 Constitutional SDD principles

## 🏛️ Constitutional Framework

This project is built following the **9 Constitutional Principles** of Software Development Democracy:

1. **🏗️ Library-First** - Uses native browser APIs exclusively
2. **⌨️ CLI Interface** - All commands accessible via npm scripts
3. **🧪 Test-First** - Tests written before implementation
4. **✨ Simplicity** - Single HTML file deployment
5. **🚫 Anti-Abstraction** - Direct DOM manipulation, no frameworks
6. **🔗 Integration-First** - E2E tests prioritized over unit tests
7. **📁 Minimal Structure** - Flat, essential-only project organization
8. **🎯 Framework Direct** - Native HTML5 dialog and DOM APIs
9. **📊 Comprehensive Testing** - 100% coverage for user interactions

## 🚀 Quick Start

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Node.js (for development and testing)

### Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd DontPressButton

# Install development dependencies
npm install

# Start local development server
npm run dev
# Visit http://localhost:8000

# Run tests
npm test                    # Jest unit/integration tests
npm run test:e2e           # Playwright E2E tests
npm run test:a11y          # Accessibility tests
npm run test:performance   # Performance benchmarks
```

### Production Deployment
```bash
# Build for production (single file)
npm run build

# Deploy the single HTML file
cp src/index.html your-hosting-destination/
```

## 📁 Project Structure

```
DontPressButton/
├── 📄 src/
│   └── index.html              # Single-file application
├── 🧪 tests/
│   ├── e2e/                   # End-to-end tests
│   ├── integration/           # Integration tests
│   ├── accessibility/         # Accessibility tests
│   └── performance/           # Performance tests
├── ⚙️ config/
│   └── app.config.json        # Application configuration
├── 📚 docs/
│   └── requirement.md         # Original requirements
├── 🏛️ PROJECT-constitution.yaml  # Constitutional governance
├── 📋 merged-ssot.yaml          # Single Source of Truth
├── 🤖 CLAUDE.md                 # AI development guidelines
└── 📊 batch/
    └── execution-plan.yaml    # Implementation roadmap
```

## 🎮 How to Use

1. **Open the Application**: Load `src/index.html` in your browser
2. **Read the Warning**: See the "Don't Press Button" heading
3. **Press the Button**: Click the red button (we know you will!)
4. **Enjoy the Messages**: Watch random Korean warnings appear
5. **Reach the Climax**: On the 10th click, a payment modal appears
6. **Make Your Choice**: Choose "Yes" or "No" to complete the journey

### Keyboard Navigation
- **Tab**: Navigate to the button
- **Enter/Space**: Activate the button
- **Esc**: Close the modal (when open)

## 🧪 Testing Strategy

### Test-First Development (Constitutional Principle)
All code follows strict test-first development:

1. **Write failing test** for new functionality
2. **Implement minimal code** to pass the test
3. **Refactor** while maintaining constitutional compliance

### Testing Layers
- **E2E Tests**: Complete user journeys with Playwright
- **Integration Tests**: Component interactions with Jest
- **Accessibility Tests**: WCAG compliance with axe-core
- **Performance Tests**: Sub-100ms response validation

### Running Tests
```bash
# Run all tests
npm test

# Run specific test suites
npm run test:e2e           # User journey testing
npm run test:a11y          # Accessibility compliance
npm run test:performance   # Performance benchmarks

# Watch mode for development
npm run test:watch
```

## ⚡ Performance

Constitutional performance requirements:
- **Click Response**: < 100ms
- **Modal Display**: < 50ms
- **Page Load**: < 1 second
- **Lighthouse Score**: > 90

## ♿ Accessibility

Full WCAG 2.1 AAA compliance:
- **Keyboard Navigation**: Complete functionality via keyboard
- **Screen Reader Support**: Proper ARIA labels and landmarks
- **Color Contrast**: 4.5:1 minimum ratio
- **Focus Management**: Visible focus indicators and modal focus trap
- **Voice Control**: Compatible with voice navigation

## 🌍 Browser Support

- **Chrome** 90+ ✅
- **Firefox** 88+ ✅
- **Safari** 14+ ✅
- **Edge** 90+ ✅
- **Mobile Safari** 14+ ✅
- **Chrome Mobile** 90+ ✅

## ⚙️ Configuration

Application behavior is configurable via `config/app.config.json`:

```json
{
  "pressToConfirmCount": 10,
  "persistCount": false,
  "messages": ["분명 누르지 말랬죠?", "..."],
  "uiText": {
    "header": "Don't Press Button",
    "button": "Don't Press Button",
    "confirmPaymentTitle": "Would you like to proceed with payment?"
  }
}
```

## 🔄 Development Workflow

### Constitutional Development Process
1. **Requirements Analysis**: Review SSOT and constitutional compliance
2. **Test-First Implementation**: Write tests before code
3. **Constitutional Review**: Validate against 9 principles
4. **Quality Gates**: Performance, accessibility, and compliance checks
5. **Integration Testing**: E2E validation of user journeys

### Branching Strategy
- `main`: Production-ready, constitutionally compliant code
- `feature/*`: Feature development with constitutional compliance
- `hotfix/*`: Emergency fixes maintaining constitutional integrity

## 📈 Quality Metrics

### Constitutional Compliance
- ✅ All 9 principles demonstrated
- ✅ Zero constitutional debt
- ✅ Simple, direct implementation
- ✅ Native APIs exclusively

### Technical Quality
- ✅ 100% test coverage for interactions
- ✅ Zero accessibility violations
- ✅ Sub-100ms response times
- ✅ Single-file deployment

### User Experience
- ✅ Delightful micro-interactions
- ✅ Cross-device compatibility
- ✅ Keyboard-only operation
- ✅ Screen reader excellence

## 🎨 Design Philosophy

### Intentionally Crude Aesthetic
The visual design deliberately embraces a "rough" aesthetic:
- **Distorted text effects** (skewed, shadowed)
- **Imperfect alignment** for personality
- **Crude but usable** interface elements
- **Not so rough** as to harm accessibility

### Constitutional Design Principles
- **Simplicity over complexity**
- **Function over form**
- **Accessibility never compromised**
- **Performance never sacrificed**

## 🚀 Deployment

### Single-File Deployment (Constitutional)
The application deploys as a single HTML file with embedded CSS and JavaScript:

```bash
# Build for deployment
npm run build

# Deploy to static hosting
# - GitHub Pages
# - Netlify
# - Vercel
# - Any static hosting service
```

### CDN Compatibility
Optimized for CDN deployment with:
- Embedded assets (no external dependencies)
- Proper caching headers
- Minimal file size
- Fast loading performance

## 🔒 Security & Privacy

### Constitutional Security
- **No external requests** (except configuration)
- **No user tracking** or analytics
- **No cookies** or localStorage (MVP)
- **No eval()** or unsafe JavaScript patterns
- **CSP-friendly** implementation

## 🤝 Contributing

### Constitutional Contribution Guidelines
1. **Read the Constitution**: Understand PROJECT-constitution.yaml
2. **Follow Test-First**: Write tests before implementation
3. **Maintain Simplicity**: Resist complexity and abstraction
4. **Validate Accessibility**: Zero violations required
5. **Document Decisions**: Reference constitutional principles

### Pull Request Process
1. Fork and create feature branch
2. Write tests first (constitutional requirement)
3. Implement with constitutional compliance
4. Verify all quality gates pass
5. Submit PR with constitutional compliance statement

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Demeter WAVIS Framework**: Constitutional SDD methodology
- **Web Standards**: Native browser API excellence
- **Accessibility Community**: WCAG guidance and tools
- **Testing Community**: Jest and Playwright frameworks

---

**Built with Constitutional SDD principles - simple, accessible, and delightful by design.**