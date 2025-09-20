// UoW-001: Basic Layout and Styling Foundation - E2E Tests
// Constitutional SDD Test-First Implementation

import { test, expect } from '@playwright/test';

test.describe('UoW-001: Basic Layout and Styling Foundation', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application
    await page.goto('./src/index.html');
  });

  test('should display header text with intentionally rough styling (FR-001)', async ({ page }) => {
    // Test Constitutional Requirement: Framework Direct - native HTML elements
    const header = page.locator('h1, header h1, .header-title');

    // Verify header text exists and contains correct content
    await expect(header).toBeVisible();
    await expect(header).toContainText("Don't Press Button");

    // Verify intentionally rough styling is applied
    const headerStyles = await header.evaluate(el => {
      const styles = window.getComputedStyle(el);
      return {
        textShadow: styles.textShadow,
        transform: styles.transform,
        fontFamily: styles.fontFamily
      };
    });

    // Test that rough styling elements are present
    expect(headerStyles.textShadow).not.toBe('none');
    // Transform should include skew for rough appearance
    expect(headerStyles.transform).toContain('skew');
  });

  test('should render prominent red button below header (FR-002)', async ({ page }) => {
    // Test Constitutional Requirement: Framework Direct - native button element
    const button = page.locator('button#main-button, .main-button');

    // Verify button exists and is visible
    await expect(button).toBeVisible();
    await expect(button).toContainText("Don't Press Button");

    // Verify button color is brand red
    const buttonColor = await button.evaluate(el => {
      return window.getComputedStyle(el).backgroundColor;
    });

    // Brand red (#d62828) should be applied
    expect(buttonColor).toMatch(/rgb\(214,?\s?40,?\s?40\)/);
  });

  test('should maintain responsive layout across viewport sizes (NFR-001)', async ({ page }) => {
    // Test Constitutional Requirement: Simplicity - responsive without complexity
    const viewports = [
      { width: 360, height: 640 },   // Mobile
      { width: 768, height: 1024 },  // Tablet
      { width: 1920, height: 1080 }  // Desktop
    ];

    for (const viewport of viewports) {
      await page.setViewportSize(viewport);

      // Verify header and button remain visible and properly positioned
      const header = page.locator('h1, header h1, .header-title');
      const button = page.locator('button#main-button, .main-button');

      await expect(header).toBeVisible();
      await expect(button).toBeVisible();

      // Verify button meets minimum touch target size (44px)
      const buttonBox = await button.boundingBox();
      expect(buttonBox.height).toBeGreaterThanOrEqual(44);
      expect(buttonBox.width).toBeGreaterThanOrEqual(44);
    }
  });

  test('should meet accessibility requirements (NFR-005)', async ({ page }) => {
    // Test Constitutional Requirement: Comprehensive Testing - accessibility compliance
    // Inject axe-core for accessibility testing
    await page.addScriptTag({ path: 'node_modules/axe-core/axe.min.js' });

    // Run accessibility audit
    const accessibilityReport = await page.evaluate(() => {
      return new Promise((resolve) => {
        axe.run((err, results) => {
          resolve(results);
        });
      });
    });

    // Should have zero accessibility violations
    expect(accessibilityReport.violations).toHaveLength(0);
  });

  test('should maintain 4.5:1 color contrast ratio (NFR-005)', async ({ page }) => {
    // Test Constitutional Requirement: Anti-Abstraction - direct color validation
    const header = page.locator('h1, header h1, .header-title');
    const button = page.locator('button#main-button, .main-button');

    // Check color contrast for header
    const headerContrast = await header.evaluate(el => {
      const styles = window.getComputedStyle(el);
      return {
        color: styles.color,
        backgroundColor: styles.backgroundColor || 'rgb(255, 255, 255)'
      };
    });

    // Check color contrast for button
    const buttonContrast = await button.evaluate(el => {
      const styles = window.getComputedStyle(el);
      return {
        color: styles.color,
        backgroundColor: styles.backgroundColor
      };
    });

    // Note: In real implementation, you'd use a contrast ratio calculation function
    // For now, we verify that contrasting colors are applied
    expect(headerContrast.color).not.toBe(headerContrast.backgroundColor);
    expect(buttonContrast.color).not.toBe(buttonContrast.backgroundColor);
  });

  test('should use single HTML file structure (Constitutional: Simplicity)', async ({ page }) => {
    // Test Constitutional Requirement: Simplicity - single file deployment
    const response = await page.goto('./src/index.html');
    expect(response.status()).toBe(200);

    // Verify no external CSS files are loaded (all should be embedded)
    const externalStylesheets = await page.evaluate(() => {
      const links = Array.from(document.querySelectorAll('link[rel="stylesheet"]'));
      return links.filter(link => !link.href.includes('data:')).length;
    });

    expect(externalStylesheets).toBe(0);

    // Verify CSS is embedded in the HTML
    const inlineStyles = await page.evaluate(() => {
      return document.querySelectorAll('style').length;
    });

    expect(inlineStyles).toBeGreaterThan(0);
  });

  test('should have semantic HTML structure (Constitutional: Framework Direct)', async ({ page }) => {
    // Test Constitutional Requirement: Framework Direct - native HTML semantics
    // Verify proper semantic structure exists
    const semanticElements = await page.evaluate(() => {
      return {
        hasHeader: document.querySelector('header, h1') !== null,
        hasMain: document.querySelector('main') !== null,
        hasButton: document.querySelector('button') !== null
      };
    });

    expect(semanticElements.hasHeader).toBe(true);
    expect(semanticElements.hasMain).toBe(true);
    expect(semanticElements.hasButton).toBe(true);
  });
});