// UoW-001: HTML Structure Integration Tests (Constitutional SDD)

const { describe, test, expect, beforeEach } = require('@jest/globals');
const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

describe('UoW-001: HTML Structure Integration Tests', () => {
  let dom;
  let document;
  let window;

  beforeEach(() => {
    // Load the actual HTML file
    const htmlPath = path.join(process.cwd(), 'src', 'index.html');
    const htmlContent = fs.readFileSync(htmlPath, 'utf8');

    dom = new JSDOM(htmlContent, {
      runScripts: 'dangerously',
      resources: 'usable'
    });
    document = dom.window.document;
    window = dom.window;

    // Make global for testing
    global.document = document;
    global.window = window;
  });

  test('should have proper DOCTYPE and HTML structure (Constitutional: Framework Direct)', () => {
    // Test Constitutional Requirement: Framework Direct - semantic HTML
    expect(document.doctype).toBeTruthy();
    expect(document.doctype.name).toBe('html');
    expect(document.documentElement.lang).toBe('en');
  });

  test('should have required meta tags (Constitutional: Simplicity)', () => {
    // Test Constitutional Requirement: Simplicity - essential meta tags
    const charset = document.querySelector('meta[charset="UTF-8"]');
    const viewport = document.querySelector('meta[name="viewport"]');

    expect(charset).toBeTruthy();
    expect(viewport).toBeTruthy();
    expect(viewport.getAttribute('content')).toContain('width=device-width');
  });

  test('should have semantic HTML structure (Constitutional: Framework Direct)', () => {
    // Test Constitutional Requirement: Framework Direct - semantic elements
    const header = document.querySelector('header');
    const main = document.querySelector('main');
    const h1 = document.querySelector('h1');

    expect(header).toBeTruthy();
    expect(main).toBeTruthy();
    expect(h1).toBeTruthy();
  });

  test('should implement FR-001: Header Text Display', () => {
    // Test Functional Requirement FR-001
    const h1 = document.querySelector('h1');

    expect(h1).toBeTruthy();
    expect(h1.textContent).toBe("Don't Press Button");

    // Check for intentionally rough styling
    const computedStyle = window.getComputedStyle(h1);
    expect(computedStyle.transform).toContain('skew');
    expect(computedStyle.textShadow).not.toBe('none');
  });

  test('should implement FR-002: Red Button Rendering', () => {
    // Test Functional Requirement FR-002
    const button = document.querySelector('#main-button');

    expect(button).toBeTruthy();
    expect(button.textContent.trim()).toBe("Don't Press Button");
    expect(button.tagName.toLowerCase()).toBe('button');

    // Check for brand red color
    const computedStyle = window.getComputedStyle(button);
    expect(computedStyle.backgroundColor).toMatch(/rgb\(214,?\s?40,?\s?40\)/);
  });

  test('should have embedded CSS (Constitutional: Simplicity)', () => {
    // Test Constitutional Requirement: Simplicity - single file deployment
    const styleElements = document.querySelectorAll('style');
    const externalStylesheets = document.querySelectorAll('link[rel="stylesheet"]:not([href^="data:"])');

    expect(styleElements.length).toBeGreaterThan(0);
    expect(externalStylesheets.length).toBe(0);
  });

  test('should have accessibility attributes (NFR-005)', () => {
    // Test Non-Functional Requirement NFR-005
    const button = document.querySelector('#main-button');
    const messageArea = document.querySelector('#message-area');

    // Button accessibility
    expect(button.getAttribute('type')).toBe('button');
    expect(button.getAttribute('aria-label')).toBeTruthy();

    // Message area accessibility
    expect(messageArea.getAttribute('aria-live')).toBe('polite');
    expect(messageArea.getAttribute('aria-atomic')).toBe('true');
  });

  test('should meet minimum touch target size (NFR-005)', () => {
    // Test accessibility requirement - 44px minimum touch target
    const button = document.querySelector('#main-button');
    const computedStyle = window.getComputedStyle(button);

    const minHeight = parseInt(computedStyle.minHeight);
    expect(minHeight).toBeGreaterThanOrEqual(44);
  });

  test('should have JavaScript functionality initialized', () => {
    // Test Constitutional Requirement: Anti-Abstraction - minimal JS
    expect(window.DontPressButton).toBeTruthy();
    expect(window.DontPressButton.elements.button).toBeTruthy();
    expect(window.DontPressButton.elements.messageArea).toBeTruthy();
    expect(window.DontPressButton.version).toBe('1.0.0-uow004');
  });

  test('should validate responsive design structure', () => {
    // Test NFR-001: Responsive Design
    const body = document.querySelector('body');
    const computedStyle = window.getComputedStyle(body);

    // Should use CSS Grid for layout (Constitutional: Framework Direct)
    expect(computedStyle.display).toBe('grid');
  });
});