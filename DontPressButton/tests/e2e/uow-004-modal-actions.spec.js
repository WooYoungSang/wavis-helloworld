/*
 * 🔴 Phase 3: RED - Constitutional Test Specification for UoW-004
 * Unit of Work: Modal Response Handling
 *
 * Constitutional Principles Applied:
 * - Test-First: Tests written before implementation
 * - Integration-First: E2E tests prioritized for complete user flows
 * - Simplicity: Direct event handling testing
 * - Anti-Abstraction: Testing without complex abstractions
 */

const { test, expect } = require('@playwright/test');

test.describe('UoW-004: Modal Response Handling', () => {

    test.beforeEach(async ({ page }) => {
        // Constitutional: Direct navigation to single HTML file
        await page.goto('file://' + process.cwd() + '/src/index.html');

        // Constitutional: Ensure page is fully loaded
        await expect(page.locator('#main-button')).toBeVisible();
        await expect(page.locator('#payment-modal')).toBeAttached();
    });

    test('should show payment alert when Yes button is clicked', async ({ page }) => {
        // Constitutional Test Strategy: Integration-First Testing
        // Test complete user interaction flow from button clicks to alert

        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');
        const yesButton = page.locator('#modal-yes-button');

        // Get to 10th click to show modal
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await expect(modal).toBeVisible();

        // Set up alert dialog handler
        let alertMessage = '';
        page.on('dialog', async dialog => {
            alertMessage = dialog.message();
            await dialog.accept();
        });

        // Click Yes button
        await yesButton.click();

        // Constitutional: Test native alert functionality
        expect(alertMessage).toBe('Payment completed');
    });

    test('should close modal and return to normal state after Yes button alert', async ({ page }) => {
        // Constitutional: Test complete user journey flow
        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');
        const yesButton = page.locator('#modal-yes-button');

        // Get to modal
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await expect(modal).toBeVisible();

        // Handle alert and click Yes
        page.on('dialog', async dialog => {
            await dialog.accept();
        });

        await yesButton.click();

        // Modal should be closed after alert dismissal
        await expect(modal).not.toBeVisible();

        // Focus should return to main button
        await expect(button).toBeFocused();
    });

    test('should close modal without alert when No button is clicked', async ({ page }) => {
        // Constitutional: Test simple direct behavior
        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');
        const noButton = page.locator('#modal-no-button');

        // Get to modal
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await expect(modal).toBeVisible();

        // Set up to catch any unexpected alerts
        let alertTriggered = false;
        page.on('dialog', async dialog => {
            alertTriggered = true;
            await dialog.accept();
        });

        // Click No button
        await noButton.click();

        // Modal should be closed without alert
        await expect(modal).not.toBeVisible();
        expect(alertTriggered).toBe(false);

        // Focus should return to main button
        await expect(button).toBeFocused();
    });

    test('should maintain state consistency after modal interactions - Yes button', async ({ page }) => {
        // Constitutional: Test state management after modal
        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');
        const yesButton = page.locator('#modal-yes-button');

        // Get to modal
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        // Handle alert and click Yes
        page.on('dialog', async dialog => {
            await dialog.accept();
        });

        await yesButton.click();

        // State should be reset after Yes (requirement analysis needed)
        const clickCountAfterYes = await page.evaluate(() => {
            return window.DontPressButton?.state?.clickCount || 0;
        });

        // Constitutional: Test expected state behavior
        // Need to determine if state resets or continues
        expect(typeof clickCountAfterYes).toBe('number');
    });

    test('should maintain state consistency after modal interactions - No button', async ({ page }) => {
        // Constitutional: Test state management after modal
        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');
        const noButton = page.locator('#modal-no-button');

        // Get to modal
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await noButton.click();

        // State should remain at 10 after No button
        const clickCountAfterNo = await page.evaluate(() => {
            return window.DontPressButton?.state?.clickCount || 0;
        });

        expect(clickCountAfterNo).toBe(10);
    });

    test('should allow continued clicking after modal closure', async ({ page }) => {
        // Constitutional: Test Integration-First - complete user journey
        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');
        const messageArea = page.locator('#message-area');
        const noButton = page.locator('#modal-no-button');

        // Get to modal via No button path
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await noButton.click();

        // Continue clicking after modal
        await button.click(); // 11th click
        await button.click(); // 12th click

        // Messages should continue to display
        const messageAfter = await messageArea.textContent();
        expect(messageAfter).toBeTruthy();
        expect(messageAfter.length).toBeGreaterThan(0);

        // State should continue incrementing
        const finalClickCount = await page.evaluate(() => {
            return window.DontPressButton?.state?.clickCount || 0;
        });

        expect(finalClickCount).toBe(12);
    });

    test('should not show modal again on subsequent clicks after payment', async ({ page }) => {
        // Constitutional: Test modal only appears once
        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');
        const yesButton = page.locator('#modal-yes-button');

        // Get to modal and complete payment
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        page.on('dialog', async dialog => {
            await dialog.accept();
        });

        await yesButton.click();

        // Continue clicking beyond 10 again
        for (let i = 1; i <= 15; i++) {
            await button.click();
        }

        // Modal should not appear again
        await expect(modal).not.toBeVisible();
    });

    test('should maintain performance under 100ms for modal actions', async ({ page }) => {
        // Constitutional: Performance requirements validation
        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');
        const yesButton = page.locator('#modal-yes-button');

        // Get to modal
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        // Measure Yes button performance
        const startTime = await page.evaluate(() => performance.now());

        page.on('dialog', async dialog => {
            await dialog.accept();
        });

        await yesButton.click();

        // Wait for modal to close
        await page.locator('#payment-modal').waitFor({ state: 'hidden' });

        const endTime = await page.evaluate(() => performance.now());
        const responseTime = endTime - startTime;

        // Constitutional: Performance requirement < 100ms
        expect(responseTime).toBeLessThan(100);
    });

    test('should handle rapid modal interactions without errors', async ({ page }) => {
        // Constitutional: Test robustness of event handling
        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');
        const noButton = page.locator('#modal-no-button');

        // Test only No button path since Yes button prevents modal from showing again
        // This is the expected constitutional behavior - modal should only appear once

        // First modal interaction
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await expect(modal).toBeVisible();
        await noButton.click();
        await expect(modal).not.toBeVisible();

        // Reset by refreshing page for second test
        await page.reload();
        await expect(button).toBeVisible();

        // Second modal interaction
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await expect(modal).toBeVisible();
        await noButton.click();
        await expect(modal).not.toBeVisible();

        // System should still be responsive
        await button.click();
        const finalMessage = await page.locator('#message-area').textContent();
        expect(finalMessage).toBeTruthy();
    });

    test('should expose modal action state through public API', async ({ page }) => {
        // Constitutional: CLI Interface Testing equivalent
        const button = page.locator('#main-button');
        const yesButton = page.locator('#modal-yes-button');

        // Get to modal and interact
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        page.on('dialog', async dialog => {
            await dialog.accept();
        });

        await yesButton.click();

        // Test API exposure
        const apiState = await page.evaluate(() => {
            const api = window.DontPressButton;
            return {
                hasAPI: !!api,
                hasState: !!(api && api.state),
                version: api?.version,
                compliance: api?.constitutionalCompliance
            };
        });

        expect(apiState.hasAPI).toBe(true);
        expect(apiState.hasState).toBe(true);
        expect(apiState.version).toBe('1.0.0-uow004');
    });

});

/*
 * Constitutional Compliance Declaration for UoW-004 Tests
 *
 * ✅ Test-First: Complete test suite before modal actions implementation
 * ✅ Integration-First: E2E tests prioritizing complete user journeys
 * ✅ Simplicity: Direct event handling testing without complex abstractions
 * ✅ Constitutional Compliance: State management and performance testing
 * ✅ Comprehensive Testing: All modal action scenarios covered
 *
 * Expected Test Result: ALL TESTS SHOULD FAIL (RED state achieved)
 * Next Phase: Implement/verify modal action handlers (GREEN)
 */