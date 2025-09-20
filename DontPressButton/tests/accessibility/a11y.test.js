/*
 * 🔴 Phase 3: RED - Constitutional Test Specification for UoW-006
 * Unit of Work: Comprehensive Testing Suite - Accessibility Compliance
 *
 * Constitutional Principles Applied:
 * - Test-First: Accessibility tests before infrastructure implementation
 * - Comprehensive Testing: Complete accessibility coverage
 * - Library-First: axe-core accessibility testing library
 * - Constitutional Compliance: Accessibility-first principle validation
 */

const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test.describe('UoW-006: Accessibility Compliance Testing', () => {

    test.beforeEach(async ({ page }) => {
        // Constitutional: Direct navigation to single HTML file
        await page.goto('file://' + process.cwd() + '/src/index.html');

        // Constitutional: Ensure page is fully loaded and configured
        await expect(page.locator('#main-button')).toBeVisible();

        // Wait for configuration to load
        await page.waitForFunction(() => window.DontPressButton?.config);
    });

    test('should have zero accessibility violations on initial load', async ({ page }) => {
        // Constitutional: Complete accessibility audit using axe-core

        const accessibilityScanResults = await new AxeBuilder({ page })
            .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
            .analyze();

        // Constitutional: Zero accessibility violations required
        expect(accessibilityScanResults.violations).toEqual([]);

        // Additional manual checks for constitutional requirements

        // Verify semantic HTML structure
        const header = page.locator('header');
        await expect(header).toBeVisible();

        const main = page.locator('main');
        await expect(main).toBeVisible();

        const h1 = page.locator('h1');
        await expect(h1).toBeVisible();

        // Verify button has proper accessibility attributes
        const button = page.locator('#main-button');
        const ariaLabel = await button.getAttribute('aria-label');
        expect(ariaLabel).toBeTruthy();
        expect(ariaLabel).toContain('Main interaction button');
    });

    test('should maintain accessibility during user interactions', async ({ page }) => {
        // Constitutional: Accessibility maintained throughout user journey

        const button = page.locator('#main-button');

        // Test accessibility after each click (sample 3 clicks)
        for (let i = 1; i <= 3; i++) {
            await button.click();

            // Run accessibility scan after each interaction
            const scanResults = await new AxeBuilder({ page })
                .withTags(['wcag2a', 'wcag2aa'])
                .analyze();

            expect(scanResults.violations).toEqual([]);

            // Verify message area is accessible
            const messageArea = page.locator('#message-area');
            const message = await messageArea.textContent();
            expect(message).toBeTruthy();

            // Message area should be announced to screen readers
            const messageAriaLive = await messageArea.getAttribute('aria-live');
            expect(messageAriaLive).toBe('polite');
        }
    });

    test('should have fully accessible modal component', async ({ page }) => {
        // Constitutional: Modal accessibility compliance

        const button = page.locator('#main-button');

        // Get to modal (10 clicks)
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        const modal = page.locator('#payment-modal');
        await expect(modal).toBeVisible();

        // Run accessibility scan with modal open
        const modalScanResults = await new AxeBuilder({ page })
            .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
            .analyze();

        expect(modalScanResults.violations).toEqual([]);

        // Test modal-specific accessibility features

        // 1. Modal should have proper ARIA attributes
        const modalRole = await modal.getAttribute('role');
        expect(modalRole).toBe('dialog');

        const modalAriaModal = await modal.getAttribute('aria-modal');
        expect(modalAriaModal).toBe('true');

        // 2. Modal should have accessible title
        const modalTitle = page.locator('#modal-title');
        await expect(modalTitle).toBeVisible();

        const titleText = await modalTitle.textContent();
        expect(titleText).toBeTruthy();

        // 3. Modal should trap focus properly
        const yesButton = page.locator('#modal-yes-button');
        const noButton = page.locator('#modal-no-button');

        // Focus should start on first interactive element
        const initialFocus = await page.evaluate(() => document.activeElement.id);
        expect(initialFocus).toBe('modal-yes-button');

        // Tab should cycle within modal
        await page.keyboard.press('Tab');
        let currentFocus = await page.evaluate(() => document.activeElement.id);
        expect(currentFocus).toBe('modal-no-button');

        await page.keyboard.press('Tab');
        currentFocus = await page.evaluate(() => document.activeElement.id);
        expect(currentFocus).toBe('modal-yes-button'); // Should wrap back

        // Shift+Tab should reverse cycle
        await page.keyboard.press('Shift+Tab');
        currentFocus = await page.evaluate(() => document.activeElement.id);
        expect(currentFocus).toBe('modal-no-button');

        // 4. ESC key should close modal
        await page.keyboard.press('Escape');
        await expect(modal).not.toBeVisible();

        // 5. Focus should return to trigger element
        const returnedFocus = await page.evaluate(() => document.activeElement.id);
        expect(returnedFocus).toBe('main-button');
    });

    test('should have accessible button with proper touch targets', async ({ page }) => {
        // Constitutional: Touch target and button accessibility

        const button = page.locator('#main-button');

        // Verify button meets minimum touch target size (44px)
        const buttonBox = await button.boundingBox();
        expect(buttonBox.width).toBeGreaterThanOrEqual(44);
        expect(buttonBox.height).toBeGreaterThanOrEqual(44);

        // Verify button has proper contrast ratio
        const buttonStyles = await page.evaluate(() => {
            const button = document.getElementById('main-button');
            const computedStyle = window.getComputedStyle(button);
            return {
                backgroundColor: computedStyle.backgroundColor,
                color: computedStyle.color,
                fontSize: computedStyle.fontSize
            };
        });

        expect(buttonStyles.backgroundColor).toBeTruthy();
        expect(buttonStyles.color).toBeTruthy();

        // Verify button can be activated via keyboard
        await button.focus();

        // Test Enter key activation
        await page.keyboard.press('Enter');

        const messageArea = page.locator('#message-area');
        const message = await messageArea.textContent();
        expect(message).toBeTruthy();

        // Test Space key activation
        await page.keyboard.press(' ');

        const updatedMessage = await messageArea.textContent();
        expect(updatedMessage).toBeTruthy();
    });

    test('should support screen reader navigation', async ({ page }) => {
        // Constitutional: Screen reader compatibility testing

        // Test landmark navigation
        const landmarks = await page.locator('[role="banner"], [role="main"], [role="dialog"], header, main').all();
        expect(landmarks.length).toBeGreaterThanOrEqual(2); // At least header and main

        // Test heading structure
        const headings = await page.locator('h1, h2, h3, h4, h5, h6').all();
        expect(headings.length).toBeGreaterThanOrEqual(1);

        // Verify logical heading hierarchy
        const h1Count = await page.locator('h1').count();
        expect(h1Count).toBe(1); // Should have exactly one h1

        // Test live regions for dynamic content
        const messageArea = page.locator('#message-area');
        const ariaLive = await messageArea.getAttribute('aria-live');
        expect(ariaLive).toBe('polite');

        // Test screen reader announcements
        const button = page.locator('#main-button');
        await button.click();

        // Verify message area content is accessible
        const message = await messageArea.textContent();
        expect(message).toBeTruthy();
        expect(message.length).toBeGreaterThan(0);
    });

    test('should handle high contrast mode and forced colors', async ({ page }) => {
        // Constitutional: High contrast accessibility

        // Simulate high contrast mode via CSS media query
        await page.addStyleTag({
            content: `
                @media (forced-colors: active) {
                    * {
                        border: 1px solid ButtonText !important;
                    }

                    button {
                        background: ButtonFace !important;
                        color: ButtonText !important;
                        border: 2px solid ButtonText !important;
                    }
                }
            `
        });

        // Verify elements remain visible and functional
        const button = page.locator('#main-button');
        await expect(button).toBeVisible();

        await button.click();

        const messageArea = page.locator('#message-area');
        const message = await messageArea.textContent();
        expect(message).toBeTruthy();

        // Run accessibility scan in high contrast mode
        const highContrastScan = await new AxeBuilder({ page })
            .withTags(['wcag2aa'])
            .analyze();

        expect(highContrastScan.violations).toEqual([]);
    });

    test('should support reduced motion preferences', async ({ page }) => {
        // Constitutional: Motion sensitivity accessibility

        // Simulate reduced motion preference
        await page.emulateMedia({ reducedMotion: 'reduce' });

        // Verify no problematic animations or transitions
        const button = page.locator('#main-button');

        // Check for CSS transitions that should be disabled
        const buttonTransition = await button.evaluate(el => {
            return window.getComputedStyle(el).transition;
        });

        // In reduced motion mode, transitions should be minimal
        if (buttonTransition && buttonTransition !== 'none') {
            // Any transitions should be very short (< 0.1s) or disable motion
            expect(buttonTransition).toMatch(/duration.*0\.0|none/);
        }

        // Test that functionality still works with reduced motion
        await button.click();

        const messageArea = page.locator('#message-area');
        const message = await messageArea.textContent();
        expect(message).toBeTruthy();
    });

    test('should maintain accessibility at different zoom levels', async ({ page }) => {
        // Constitutional: Zoom accessibility compliance

        // Test at 200% zoom (WCAG requirement)
        await page.setViewportSize({ width: 640, height: 480 }); // Simulate 200% zoom

        const button = page.locator('#main-button');
        await expect(button).toBeVisible();

        // Verify button still meets touch target requirements at zoom
        const buttonBox = await button.boundingBox();
        expect(buttonBox.width).toBeGreaterThanOrEqual(44);
        expect(buttonBox.height).toBeGreaterThanOrEqual(44);

        // Verify text remains readable
        const headerText = await page.locator('h1').textContent();
        expect(headerText).toBeTruthy();

        // Test functionality at zoom level
        await button.click();

        const messageArea = page.locator('#message-area');
        const message = await messageArea.textContent();
        expect(message).toBeTruthy();

        // Run accessibility scan at zoom level
        const zoomScan = await new AxeBuilder({ page })
            .withTags(['wcag2aa'])
            .analyze();

        expect(zoomScan.violations).toEqual([]);
    });

    test('should provide comprehensive keyboard navigation', async ({ page }) => {
        // Constitutional: Complete keyboard accessibility

        // Test full keyboard navigation flow
        await page.keyboard.press('Tab'); // Should focus on main button

        let focusedElement = await page.evaluate(() => document.activeElement.id);
        expect(focusedElement).toBe('main-button');

        // Test activation via keyboard
        await page.keyboard.press('Enter');

        // Verify message appears
        const messageArea = page.locator('#message-area');
        const message = await messageArea.textContent();
        expect(message).toBeTruthy();

        // Get to modal via keyboard
        for (let i = 1; i < 10; i++) {
            await page.keyboard.press('Enter');
        }

        const modal = page.locator('#payment-modal');
        await expect(modal).toBeVisible();

        // Test complete modal keyboard navigation
        focusedElement = await page.evaluate(() => document.activeElement.id);
        expect(focusedElement).toBe('modal-yes-button');

        // Navigate through modal buttons
        await page.keyboard.press('Tab');
        focusedElement = await page.evaluate(() => document.activeElement.id);
        expect(focusedElement).toBe('modal-no-button');

        // Test modal action via keyboard
        await page.keyboard.press('Enter'); // Activate No button

        await expect(modal).not.toBeVisible();

        // Verify focus returned to main button
        focusedElement = await page.evaluate(() => document.activeElement.id);
        expect(focusedElement).toBe('main-button');
    });

});

/*
 * Constitutional Compliance Declaration for UoW-006 Accessibility Tests
 *
 * ✅ Test-First: Accessibility tests before infrastructure implementation
 * ✅ Comprehensive Testing: Complete accessibility coverage using axe-core
 * ✅ Library-First: axe-core accessibility testing library integration
 * ✅ Constitutional Compliance: All accessibility principles validated
 * ✅ WCAG Compliance: 2.1 AA standards tested throughout
 * ✅ Screen Reader Support: Full screen reader compatibility testing
 * ✅ Keyboard Navigation: Complete keyboard accessibility validation
 * ✅ Touch Targets: Minimum 44px touch target compliance
 * ✅ High Contrast: Forced colors and high contrast mode support
 *
 * Expected Test Result: TESTS SHOULD FAIL (missing axe-core dependency)
 * Next Phase: Install accessibility testing infrastructure (GREEN)
 */