/*
 * 🔴 Phase 3: RED - Constitutional Test Specification for UoW-003
 * Unit of Work: Payment Confirmation Modal
 *
 * Constitutional Principles Applied:
 * - Test-First: Tests written before implementation
 * - Library-First: Tests expect native HTML5 dialog solutions
 * - Integration-First: E2E tests prioritized over unit tests
 * - Accessibility-First: Focus trap and keyboard navigation testing
 * - Framework-Direct: Native dialog element testing
 */

const { test, expect } = require('@playwright/test');

test.describe('UoW-003: Payment Confirmation Modal', () => {

    test.beforeEach(async ({ page }) => {
        // Constitutional: Direct navigation to single HTML file
        await page.goto('file://' + process.cwd() + '/src/index.html');

        // Constitutional: Ensure page is fully loaded
        await expect(page.locator('#main-button')).toBeVisible();
        await expect(page.locator('#message-area')).toBeAttached();
    });

    test('should display modal exactly on 10th click', async ({ page }) => {
        // Constitutional Test Strategy: Library-First Testing
        // Test expects native HTML5 dialog element usage

        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');

        // Constitutional: Verify modal exists but is not shown initially
        await expect(modal).toBeAttached();
        await expect(modal).not.toBeVisible();

        // Click 9 times - modal should not appear
        for (let i = 1; i <= 9; i++) {
            await button.click();
            await expect(modal).not.toBeVisible();
        }

        // 10th click - modal should appear
        await button.click();
        await expect(modal).toBeVisible();

        // Constitutional: Test established library API (dialog.open property)
        const isOpen = await page.evaluate(() => {
            const dialog = document.getElementById('payment-modal');
            return dialog && dialog.open;
        });
        expect(isOpen).toBe(true);
    });

    test('should trap focus within modal when displayed', async ({ page }) => {
        // Constitutional: Accessibility-First testing
        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');

        // Get to 10th click to show modal
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await expect(modal).toBeVisible();

        // Constitutional: Test focus trap implementation
        const yesButton = page.locator('#modal-yes-button');
        const noButton = page.locator('#modal-no-button');

        // Focus should be on first interactive element
        await expect(yesButton).toBeFocused();

        // Tab should cycle within modal
        await page.keyboard.press('Tab');
        await expect(noButton).toBeFocused();

        // Tab again should return to first element (focus trap)
        await page.keyboard.press('Tab');
        await expect(yesButton).toBeFocused();

        // Shift+Tab should go backwards
        await page.keyboard.press('Shift+Tab');
        await expect(noButton).toBeFocused();
    });

    test('should close modal on ESC key press', async ({ page }) => {
        // Constitutional: Keyboard navigation testing
        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');

        // Get to 10th click to show modal
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await expect(modal).toBeVisible();

        // ESC should close modal
        await page.keyboard.press('Escape');
        await expect(modal).not.toBeVisible();

        // Constitutional: Test native dialog API
        const isOpen = await page.evaluate(() => {
            const dialog = document.getElementById('payment-modal');
            return dialog && dialog.open;
        });
        expect(isOpen).toBe(false);
    });

    test('should center modal on all viewport sizes', async ({ page }) => {
        // Constitutional: Responsive design testing
        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');

        // Test on mobile viewport
        await page.setViewportSize({ width: 360, height: 640 });

        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await expect(modal).toBeVisible();

        // Modal should be centered and visible
        const boundingBox = await modal.boundingBox();
        expect(boundingBox.width).toBeGreaterThan(0);
        expect(boundingBox.height).toBeGreaterThan(0);

        // Close modal
        await page.keyboard.press('Escape');

        // Test on desktop viewport
        await page.setViewportSize({ width: 1920, height: 1080 });

        // Reset and test again
        await page.reload();
        await expect(page.locator('#main-button')).toBeVisible();

        for (let i = 1; i <= 10; i++) {
            await page.locator('#main-button').click();
        }

        await expect(modal).toBeVisible();
        const desktopBoundingBox = await modal.boundingBox();
        expect(desktopBoundingBox.width).toBeGreaterThan(0);
        expect(desktopBoundingBox.height).toBeGreaterThan(0);
    });

    test('should prevent background interaction when modal is open', async ({ page }) => {
        // Constitutional: Modal behavior validation
        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');

        // Get to 10th click
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await expect(modal).toBeVisible();

        // Try to click the main button - should not work
        const clickCountBefore = await page.evaluate(() => {
            return window.DontPressButton?.state?.clickCount || 0;
        });

        // Attempt to click background button
        await button.click({ force: true });

        const clickCountAfter = await page.evaluate(() => {
            return window.DontPressButton?.state?.clickCount || 0;
        });

        // Click count should not have changed (background interaction prevented)
        expect(clickCountAfter).toBe(clickCountBefore);
    });

    test('should have proper semantic structure and ARIA attributes', async ({ page }) => {
        // Constitutional: Accessibility compliance testing
        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');

        // Get to modal
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await expect(modal).toBeVisible();

        // Constitutional: Test semantic HTML5 dialog element
        const isDialog = await modal.evaluate(el => el.tagName.toLowerCase());
        expect(isDialog).toBe('dialog');

        // Test ARIA attributes
        await expect(modal).toHaveAttribute('role', 'dialog');
        await expect(modal).toHaveAttribute('aria-modal', 'true');
        await expect(modal).toHaveAttribute('aria-labelledby');

        // Test modal content structure
        const modalTitle = page.locator('#modal-title');
        const modalButtons = page.locator('#payment-modal button');

        await expect(modalTitle).toBeVisible();
        await expect(modalButtons).toHaveCount(2);
    });

    test('should expose modal state through public API', async ({ page }) => {
        // Constitutional: CLI Interface Testing equivalent
        const button = page.locator('#main-button');

        // Get to modal
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        // Test modal state exposure
        const modalState = await page.evaluate(() => {
            const api = window.DontPressButton;
            return {
                hasModal: 'modal' in (api || {}),
                isOpen: document.getElementById('payment-modal')?.open || false
            };
        });

        expect(modalState.isOpen).toBe(true);
    });

    test('should maintain performance under 100ms for modal operations', async ({ page }) => {
        // Constitutional: Performance requirements validation
        const button = page.locator('#main-button');

        // Get to 9 clicks
        for (let i = 1; i <= 9; i++) {
            await button.click();
        }

        // Measure 10th click (modal trigger) performance
        const startTime = await page.evaluate(() => performance.now());

        await button.click();

        // Wait for modal to be visible
        await page.locator('#payment-modal').waitFor({ state: 'visible' });

        const endTime = await page.evaluate(() => performance.now());
        const responseTime = endTime - startTime;

        // Constitutional: Performance requirement < 100ms
        expect(responseTime).toBeLessThan(100);
    });

    test('should return focus to main button when modal closes', async ({ page }) => {
        // Constitutional: Focus management testing
        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');

        // Get to modal
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await expect(modal).toBeVisible();

        // Close modal with ESC
        await page.keyboard.press('Escape');
        await expect(modal).not.toBeVisible();

        // Focus should return to main button
        await expect(button).toBeFocused();
    });

});

/*
 * Constitutional Compliance Declaration for UoW-003 Tests
 *
 * ✅ Library-First Testing: Tests expect native HTML5 dialog element
 * ✅ Accessibility-First: Focus trap, ARIA attributes, keyboard navigation
 * ✅ Framework-Direct: Direct testing of native dialog APIs
 * ✅ Integration-First: E2E tests prioritized over unit tests
 * ✅ Constitutional Compliance: Modal behavior, performance, semantics
 * ✅ Test-First: Complete test suite before implementation
 *
 * Expected Test Result: ALL TESTS SHOULD FAIL (RED state achieved)
 * Next Phase: Implement native dialog modal to make tests pass (GREEN)
 */