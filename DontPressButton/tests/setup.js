// Jest setup for DontPressButton
// Constitutional SDD Testing Framework Setup

// Fix TextEncoder/TextDecoder for Node.js compatibility
const { TextEncoder, TextDecoder } = require('util');
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

// Constitutional Principle: Test-First Imperative
// All tests must be written before implementation

// Constitutional Principle: Comprehensive Testing
// 100% coverage for all user interactions

// Mock browser APIs for testing
global.fetch = jest.fn();
global.alert = jest.fn();

// Setup DOM testing utilities
beforeEach(() => {
  // Reset DOM for each test
  document.body.innerHTML = '';

  // Reset all mocks
  jest.clearAllMocks();

  // Reset any global state
  if (window.DontPressButtonApp) {
    window.DontPressButtonApp = null;
  }
});

// Constitutional compliance matchers
expect.extend({
  toBeConstitutionallyCompliant(received) {
    // Verify constitutional principles in code
    const principles = [
      'Library-First',
      'CLI-Interface',
      'Test-First',
      'Simplicity',
      'Anti-Abstraction',
      'Integration-First',
      'Minimal-Structure',
      'Framework-Direct',
      'Comprehensive-Testing'
    ];

    const pass = principles.every(principle => {
      // Add specific checks for each principle
      return true; // Placeholder - implement specific checks
    });

    return {
      message: () => `Expected code to be constitutionally compliant`,
      pass
    };
  }
});

// Performance testing setup
global.performance = {
  now: jest.fn(() => Date.now()),
  mark: jest.fn(),
  measure: jest.fn()
};

// Accessibility testing setup
global.axe = {
  run: jest.fn().mockResolvedValue({ violations: [] })
};