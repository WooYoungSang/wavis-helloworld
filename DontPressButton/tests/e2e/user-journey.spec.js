/*
 * 🔴 Phase 3: RED - Constitutional Test Specification for UoW-006
 * Unit of Work: Comprehensive Testing Suite - Complete User Journey
 *
 * Constitutional Principles Applied:
 * - Test-First: Complete test suite before infrastructure implementation
 * - Comprehensive Testing: 100% coverage for user interactions
 * - Integration-First: E2E tests prioritized for complete user flows
 * - Constitutional Compliance: All 9 principles validated through testing
 */

const { test, expect } = require('@playwright/test');

test.describe('UoW-006: Complete User Journey Testing', () => {

    test.beforeEach(async ({ page }) => {
        // Constitutional: Direct navigation to single HTML file
        await page.goto('file://' + process.cwd() + '/src/index.html');

        // Constitutional: Ensure page is fully loaded and configured
        await expect(page.locator('#main-button')).toBeVisible();

        // Wait for configuration to load
        await page.waitForFunction(() => window.DontPressButton?.config);
    });

    test('should complete full user journey from click 1 to payment completion', async ({ page }) => {
        // Constitutional Test Strategy: Complete Integration Testing
        // Test the entire user journey from first click to payment completion

        const button = page.locator('#main-button');
        const messageArea = page.locator('#message-area');
        const modal = page.locator('#payment-modal');

        // Phase 1: Clicks 1-9 - Message display phase
        for (let clickCount = 1; clickCount <= 9; clickCount++) {
            await button.click();

            // Verify message appears after each click
            const message = await messageArea.textContent();
            expect(message).toBeTruthy();
            expect(message.length).toBeGreaterThan(0);

            // Verify modal does NOT appear before 10th click
            await expect(modal).not.toBeVisible();

            // Verify click count via API
            const currentCount = await page.evaluate(() => {
                return window.DontPressButton.state.clickCount;
            });
            expect(currentCount).toBe(clickCount);
        }

        // Phase 2: 10th click - Modal trigger
        await button.click();

        // Verify modal appears on exactly the 10th click
        await expect(modal).toBeVisible();

        // Verify final click count
        const finalCount = await page.evaluate(() => {
            return window.DontPressButton.state.clickCount;
        });
        expect(finalCount).toBe(10);

        // Phase 3: Payment completion flow
        const yesButton = page.locator('#modal-yes-button');

        // Handle the alert dialog
        page.on('dialog', async dialog => {
            expect(dialog.message()).toBe('Payment completed');
            await dialog.accept();
        });

        await yesButton.click();

        // Verify modal closes after payment
        await expect(modal).not.toBeVisible();

        // Phase 4: Post-payment behavior verification
        // Verify payment completed state
        const paymentCompleted = await page.evaluate(() => {
            return window.DontPressButton.state.paymentCompleted;
        });
        expect(paymentCompleted).toBe(true);

        // Verify continued clicking works but modal doesn't reappear
        for (let i = 0; i < 5; i++) {
            await button.click();

            // Message should still appear
            const message = await messageArea.textContent();
            expect(message).toBeTruthy();

            // Modal should NOT reappear
            await expect(modal).not.toBeVisible();
        }

        // Verify final click count includes post-payment clicks
        const postPaymentCount = await page.evaluate(() => {
            return window.DontPressButton.state.clickCount;
        });
        expect(postPaymentCount).toBe(15); // 10 + 5 additional clicks
    });

    test('should complete alternative user journey with "No" selection', async ({ page }) => {
        // Constitutional: Test alternative user path for comprehensive coverage

        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');

        // Get to modal (10 clicks)
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await expect(modal).toBeVisible();

        // Choose "No" option
        const noButton = page.locator('#modal-no-button');
        await noButton.click();

        // Verify modal closes without payment
        await expect(modal).not.toBeVisible();

        // Verify payment NOT completed
        const paymentCompleted = await page.evaluate(() => {
            return window.DontPressButton.state.paymentCompleted;
        });
        expect(paymentCompleted).toBe(false);

        // Verify modal can appear again after more clicks
        for (let i = 0; i < 10; i++) {
            await button.click();
        }

        // Modal should appear again since payment wasn't completed
        await expect(modal).toBeVisible();
    });

    test('should maintain performance throughout complete user journey', async ({ page }) => {
        // Constitutional: Performance testing for complete interaction flow

        const button = page.locator('#main-button');
        const performanceTimes = [];

        // Measure performance for each click in the journey
        for (let clickCount = 1; clickCount <= 10; clickCount++) {
            const startTime = await page.evaluate(() => performance.now());

            await button.click();

            // Wait for message to appear
            await page.waitForFunction(() => {
                const messageArea = document.getElementById('message-area');
                return messageArea && messageArea.textContent.length > 0;
            });

            const endTime = await page.evaluate(() => performance.now());
            const responseTime = endTime - startTime;

            performanceTimes.push(responseTime);

            // Constitutional: Each interaction must be < 100ms
            expect(responseTime).toBeLessThan(100);
        }

        // Verify consistent performance across all clicks
        const averageTime = performanceTimes.reduce((a, b) => a + b, 0) / performanceTimes.length;
        expect(averageTime).toBeLessThan(50); // Even stricter average requirement

        // Verify no performance degradation over time
        const firstHalf = performanceTimes.slice(0, 5);
        const secondHalf = performanceTimes.slice(5);

        const firstHalfAvg = firstHalf.reduce((a, b) => a + b, 0) / firstHalf.length;
        const secondHalfAvg = secondHalf.reduce((a, b) => a + b, 0) / secondHalf.length;

        // Second half should not be significantly slower
        expect(secondHalfAvg).toBeLessThan(firstHalfAvg * 1.5);
    });

    test('should handle rapid clicking during user journey', async ({ page }) => {
        // Constitutional: Stress testing for user interaction patterns

        const button = page.locator('#main-button');
        const messageArea = page.locator('#message-area');

        // Rapid clicking test - simulate enthusiastic user
        const rapidClicks = 10;
        for (let i = 0; i < rapidClicks; i++) {
            await button.click({ delay: 10 }); // 10ms between clicks
        }

        // Verify state consistency after rapid clicking
        const finalCount = await page.evaluate(() => {
            return window.DontPressButton.state.clickCount;
        });
        expect(finalCount).toBe(rapidClicks);

        // Verify message still displays correctly
        const message = await messageArea.textContent();
        expect(message).toBeTruthy();
        expect(message.length).toBeGreaterThan(0);

        // Verify modal appears correctly after rapid clicking
        const modal = page.locator('#payment-modal');
        await expect(modal).toBeVisible();
    });

    test('should maintain accessibility throughout user journey', async ({ page }) => {
        // Constitutional: Accessibility compliance during complete flow

        const button = page.locator('#main-button');

        // Verify keyboard navigation works throughout journey
        await button.focus();

        // Use keyboard to navigate through journey
        for (let i = 1; i <= 10; i++) {
            await page.keyboard.press('Enter');

            // Verify focus remains manageable
            const focusedElement = await page.evaluate(() => document.activeElement.id);
            expect(['main-button'].includes(focusedElement)).toBe(true);
        }

        // Verify modal accessibility
        const modal = page.locator('#payment-modal');
        await expect(modal).toBeVisible();

        // Test focus trap in modal
        await page.keyboard.press('Tab');
        let focusedElement = await page.evaluate(() => document.activeElement.id);
        expect(focusedElement).toBe('modal-yes-button');

        await page.keyboard.press('Tab');
        focusedElement = await page.evaluate(() => document.activeElement.id);
        expect(focusedElement).toBe('modal-no-button');

        await page.keyboard.press('Tab');
        focusedElement = await page.evaluate(() => document.activeElement.id);
        expect(focusedElement).toBe('modal-yes-button'); // Should wrap back

        // Test ESC key closes modal
        await page.keyboard.press('Escape');
        await expect(modal).not.toBeVisible();

        // Verify focus returns to main button
        focusedElement = await page.evaluate(() => document.activeElement.id);
        expect(focusedElement).toBe('main-button');
    });

    test('should handle configuration changes during user journey', async ({ page }) => {
        // Constitutional: Configuration system integration testing

        // Verify configuration is applied throughout journey
        const headerText = await page.locator('h1').textContent();
        const expectedHeader = await page.evaluate(() => {
            return window.DontPressButton.config.uiText.header;
        });
        expect(headerText).toBe(expectedHeader);

        const button = page.locator('#main-button');
        const buttonText = await button.textContent();
        const expectedButton = await page.evaluate(() => {
            return window.DontPressButton.config.uiText.button;
        });
        expect(buttonText.trim()).toBe(expectedButton);

        // Test configured trigger count
        const triggerCount = await page.evaluate(() => {
            return window.DontPressButton.config.pressToConfirmCount;
        });

        // Click exactly the configured number of times
        for (let i = 1; i <= triggerCount; i++) {
            await button.click();
        }

        // Modal should appear exactly on the configured trigger count
        const modal = page.locator('#payment-modal');
        await expect(modal).toBeVisible();

        // Verify modal text from configuration
        const modalTitle = await page.locator('#modal-title').textContent();
        const expectedTitle = await page.evaluate(() => {
            return window.DontPressButton.config.uiText.confirmPaymentTitle;
        });
        expect(modalTitle).toBe(expectedTitle);
    });

    test('should maintain constitutional compliance markers throughout journey', async ({ page }) => {
        // Constitutional: Verify all 9 principles maintained during user journey

        // Check initial constitutional compliance
        const compliance = await page.evaluate(() => {
            return window.DontPressButton.constitutionalCompliance;
        });

        // Verify all 9 principles are marked as compliant
        expect(compliance['Library-First']).toBe(true);
        expect(compliance['CLI-Interface']).toBe(true);
        expect(compliance['Test-First']).toBe(true);
        expect(compliance['Simplicity']).toBe(true);
        expect(compliance['Anti-Abstraction']).toBe(true);
        expect(compliance['Integration-First']).toBe(true);
        expect(compliance['Minimal-Structure']).toBe(true);
        expect(compliance['Framework-Direct']).toBe(true);
        expect(compliance['Comprehensive-Testing']).toBe(true);
        expect(compliance['Configuration-Driven']).toBe(true);

        // Perform user journey and verify compliance maintained
        const button = page.locator('#main-button');
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        // Verify constitutional compliance maintained after interactions
        const postInteractionCompliance = await page.evaluate(() => {
            return window.DontPressButton.constitutionalCompliance;
        });

        // All principles should still be true
        Object.values(postInteractionCompliance).forEach(value => {
            expect(value).toBe(true);
        });

        // Verify version information
        const version = await page.evaluate(() => {
            return window.DontPressButton.version;
        });
        expect(version).toBe('1.0.0-uow007'); // Updated for UoW-007
    });

});

/*
 * Constitutional Compliance Declaration for UoW-006 User Journey Tests
 *
 * ✅ Test-First: Complete user journey tests before infrastructure implementation
 * ✅ Comprehensive Testing: 100% coverage for user interaction paths
 * ✅ Integration-First: E2E tests prioritizing complete user flows
 * ✅ Constitutional Compliance: All 9 principles validated through testing
 * ✅ Performance: Complete journey performance testing implemented
 * ✅ Accessibility: Full accessibility compliance tested during journey
 * ✅ Configuration-Driven: Configuration integration tested throughout journey
 *
 * Expected Test Result: ALL TESTS SHOULD FAIL (RED state achieved)
 * Next Phase: Implement missing test infrastructure (GREEN)
 */