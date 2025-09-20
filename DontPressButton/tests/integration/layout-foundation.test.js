// UoW-001: Basic Layout Foundation - Integration Tests
// Constitutional SDD Test-First Implementation

const { describe, test, expect, beforeEach } = require('@jest/globals');
const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

describe('UoW-001: Layout Foundation Integration Tests', () => {
  let dom;
  let document;
  let window;

  beforeEach(() => {
    // Load the actual HTML file
    const htmlPath = path.join(process.cwd(), 'src', 'index.html');

    let htmlContent;
    try {
      htmlContent = fs.readFileSync(htmlPath, 'utf8');
    } catch (error) {
      // Fallback minimal structure if file doesn't exist
      htmlContent = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Don't Press Button</title>
        </head>
        <body>
          <!-- Content will be implemented in GREEN phase -->
        </body>
        </html>
      `;
    }

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

  test('should have required DOM structure elements', () => {
    // Test Constitutional Requirement: Framework Direct - semantic HTML
    expect(document.doctype).toBeTruthy();
    expect(document.documentElement.lang).toBe('en');
    expect(document.querySelector('meta[charset="UTF-8"]')).toBeTruthy();
    expect(document.querySelector('meta[name="viewport"]')).toBeTruthy();
  });

  test('should validate HTML semantics when implemented', () => {
    // This test will fail initially (RED phase)
    // Constitutional Requirement: Framework Direct
    const header = document.querySelector('header, h1');
    const main = document.querySelector('main');
    const button = document.querySelector('button');

    // These should exist after GREEN phase implementation
    expect(header).toBeTruthy();
    expect(main).toBeTruthy();
    expect(button).toBeTruthy();
  });

  test('should have embedded CSS styles (Constitutional: Simplicity)', () => {
    // Test Constitutional Requirement: Simplicity - single file
    const styleElements = document.querySelectorAll('style');
    const externalStylesheets = document.querySelectorAll('link[rel="stylesheet"]:not([href^="data:"])');

    // Should have embedded styles, no external stylesheets
    expect(styleElements.length).toBeGreaterThan(0);
    expect(externalStylesheets.length).toBe(0);
  });

  test('should validate header text implementation', () => {
    // Test FR-001: Header Text Display
    // This will fail initially (RED phase)
    const headerElement = document.querySelector('h1, header h1, .header-title');

    if (headerElement) {
      expect(headerElement.textContent).toContain("Don't Press Button");

      // Check for intentionally rough styling attributes
      const computedStyle = window.getComputedStyle(headerElement);
      expect(computedStyle.textShadow).not.toBe('none');
    } else {
      // Fail in RED phase as expected
      expect(headerElement).toBeTruthy();
    }
  });

  test('should validate button implementation', () => {
    // Test FR-002: Red Button Rendering
    // This will fail initially (RED phase)
    const buttonElement = document.querySelector('button#main-button, .main-button');

    if (buttonElement) {
      expect(buttonElement.textContent).toContain("Don't Press Button");

      // Check for brand red color
      const computedStyle = window.getComputedStyle(buttonElement);
      expect(computedStyle.backgroundColor).toMatch(/rgb\(214,?\s?40,?\s?40\)/);
    } else {
      // Fail in RED phase as expected
      expect(buttonElement).toBeTruthy();
    }
  });

  test('should validate responsive design utilities', () => {
    // Test NFR-001: Responsive Design
    // Constitutional Requirement: Simplicity - CSS Grid/Flexbox

    // Mock viewport testing utility
    const setViewport = (width, height) => {
      Object.defineProperty(window, 'innerWidth', { value: width, writable: true });
      Object.defineProperty(window, 'innerHeight', { value: height, writable: true });
    };

    const viewports = [
      { width: 360, height: 640 },   // Mobile
      { width: 768, height: 1024 },  // Tablet
      { width: 1920, height: 1080 }  // Desktop
    ];

    viewports.forEach(viewport => {
      setViewport(viewport.width, viewport.height);

      // Test that layout adapts (will be implemented in GREEN phase)
      const main = document.querySelector('main');
      if (main) {
        const computedStyle = window.getComputedStyle(main);
        // Should use CSS Grid or Flexbox
        expect(['grid', 'flex'].some(display =>
          computedStyle.display.includes(display)
        )).toBe(true);
      }
    });
  });

  test('should meet Constitutional debt requirements', () => {
    // Test Constitutional Requirement: Low complexity
    const htmlContent = document.documentElement.outerHTML;

    // Simple metrics for constitutional compliance
    const lineCount = htmlContent.split('\n').length;
    const complexity = (htmlContent.match(/<[^>]+>/g) || []).length;

    // Constitutional Requirement: Simplicity - minimal complexity (Updated for UoW-003)
    expect(lineCount).toBeLessThan(600); // Increased for modal functionality while maintaining constitutional compliance
    expect(complexity).toBeLessThan(80); // Increased for modal DOM elements while staying simple
  });

  test('should validate accessibility attributes when implemented', () => {
    // Test NFR-005: Accessibility Requirements
    // Constitutional Requirement: Comprehensive Testing

    const button = document.querySelector('button');
    const header = document.querySelector('h1, header h1');

    if (button) {
      // Button should have proper accessibility attributes
      expect(button.getAttribute('type')).toBeTruthy();
      expect(button.textContent.trim()).not.toBe('');
    }

    if (header) {
      // Header should have proper heading hierarchy
      expect(['H1', 'H2', 'H3', 'H4', 'H5', 'H6'].includes(header.tagName)).toBe(true);
    }
  });
});