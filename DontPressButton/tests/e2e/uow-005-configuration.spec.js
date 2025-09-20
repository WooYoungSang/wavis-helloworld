/*
 * 🔴 Phase 3: RED - Constitutional Test Specification for UoW-005
 * Unit of Work: Configuration System Implementation
 *
 * Constitutional Principles Applied:
 * - Test-First: Tests written before implementation
 * - Configuration-Driven: Externalized content and behavior testing
 * - Simplicity: JSON configuration without complexity
 * - Integration-First: E2E tests prioritized for complete configuration flows
 */

const { test, expect } = require('@playwright/test');

test.describe('UoW-005: Configuration System Implementation', () => {

    test.beforeEach(async ({ page }) => {
        // Constitutional: Direct navigation to single HTML file
        await page.goto('file://' + process.cwd() + '/src/index.html');

        // Constitutional: Ensure page is fully loaded and configured
        await expect(page.locator('#main-button')).toBeVisible();
    });

    test('should load configuration at startup', async ({ page }) => {
        // Constitutional Test Strategy: Configuration-Driven Testing
        // Test that configuration is loaded and applied at startup

        // Wait for configuration to be loaded
        await page.waitForFunction(() => {
            return window.DontPressButton && window.DontPressButton.config;
        });

        // Test configuration structure exists
        const configLoaded = await page.evaluate(() => {
            const config = window.DontPressButton.config;
            return {
                hasConfig: !!config,
                hasPressToConfirmCount: 'pressToConfirmCount' in config,
                hasMessages: Array.isArray(config.messages),
                hasUiText: !!config.uiText,
                hasA11y: !!config.a11y
            };
        });

        expect(configLoaded.hasConfig).toBe(true);
        expect(configLoaded.hasPressToConfirmCount).toBe(true);
        expect(configLoaded.hasMessages).toBe(true);
        expect(configLoaded.hasUiText).toBe(true);
        expect(configLoaded.hasA11y).toBe(true);
    });

    test('should use configured header text', async ({ page }) => {
        // Constitutional: Test text externalization from configuration

        // Wait for configuration to load
        await page.waitForFunction(() => window.DontPressButton?.config);

        const headerText = await page.locator('h1').textContent();

        // Get expected text from configuration
        const expectedText = await page.evaluate(() => {
            return window.DontPressButton.config.uiText.header;
        });

        expect(headerText).toBe(expectedText);
        expect(headerText).toBe('Don\'t Press Button'); // Verify it matches config
    });

    test('should use configured button text', async ({ page }) => {
        // Constitutional: Test UI text from configuration

        await page.waitForFunction(() => window.DontPressButton?.config);

        const buttonText = await page.locator('#main-button').textContent();

        const expectedText = await page.evaluate(() => {
            return window.DontPressButton.config.uiText.button;
        });

        expect(buttonText.trim()).toBe(expectedText);
        expect(buttonText.trim()).toBe('Don\'t Press Button');
    });

    test('should use configured modal text', async ({ page }) => {
        // Constitutional: Test modal content from configuration

        await page.waitForFunction(() => window.DontPressButton?.config);

        // Get to modal by using configured trigger count
        const triggerCount = await page.evaluate(() => {
            return window.DontPressButton.config.pressToConfirmCount;
        });

        for (let i = 1; i <= triggerCount; i++) {
            await page.locator('#main-button').click();
        }

        await expect(page.locator('#payment-modal')).toBeVisible();

        // Test modal title
        const modalTitle = await page.locator('#modal-title').textContent();
        const expectedTitle = await page.evaluate(() => {
            return window.DontPressButton.config.uiText.confirmPaymentTitle;
        });
        expect(modalTitle).toBe(expectedTitle);

        // Test button texts
        const yesButtonText = await page.locator('#modal-yes-button').textContent();
        const noButtonText = await page.locator('#modal-no-button').textContent();

        const expectedYes = await page.evaluate(() => {
            return window.DontPressButton.config.uiText.confirmYes;
        });
        const expectedNo = await page.evaluate(() => {
            return window.DontPressButton.config.uiText.confirmNo;
        });

        expect(yesButtonText).toBe(expectedYes);
        expect(noButtonText).toBe(expectedNo);
    });

    test('should use configured alert message', async ({ page }) => {
        // Constitutional: Test alert text from configuration

        await page.waitForFunction(() => window.DontPressButton?.config);

        // Get to modal
        const triggerCount = await page.evaluate(() => {
            return window.DontPressButton.config.pressToConfirmCount;
        });

        for (let i = 1; i <= triggerCount; i++) {
            await page.locator('#main-button').click();
        }

        let alertMessage = '';
        page.on('dialog', async dialog => {
            alertMessage = dialog.message();
            await dialog.accept();
        });

        await page.locator('#modal-yes-button').click();

        // Test alert message matches configuration
        const expectedMessage = await page.evaluate(() => {
            return window.DontPressButton.config.uiText.paymentCompleted;
        });

        expect(alertMessage).toBe(expectedMessage);
        expect(alertMessage).toBe('Payment completed');
    });

    test('should use configured Korean warning messages', async ({ page }) => {
        // Constitutional: Test message externalization

        await page.waitForFunction(() => window.DontPressButton?.config);

        const messageArea = page.locator('#message-area');

        // Click button to trigger message
        await page.locator('#main-button').click();

        const displayedMessage = await messageArea.textContent();

        // Verify message is from configuration
        const configMessages = await page.evaluate(() => {
            return window.DontPressButton.config.messages;
        });

        expect(configMessages).toContain(displayedMessage);
        expect(displayedMessage).toBeTruthy();
        expect(displayedMessage.length).toBeGreaterThan(0);
    });

    test('should use configurable trigger count', async ({ page }) => {
        // Constitutional: Test behavior configuration

        await page.waitForFunction(() => window.DontPressButton?.config);

        const modal = page.locator('#payment-modal');

        // Get configured trigger count
        const triggerCount = await page.evaluate(() => {
            return window.DontPressButton.config.pressToConfirmCount;
        });

        // Click trigger count - 1 times (should not show modal)
        for (let i = 1; i < triggerCount; i++) {
            await page.locator('#main-button').click();
        }

        await expect(modal).not.toBeVisible();

        // Click one more time (should show modal)
        await page.locator('#main-button').click();
        await expect(modal).toBeVisible();

        // Verify it's exactly the configured count
        expect(triggerCount).toBe(10); // Default from config
    });

    test('should handle configuration loading errors gracefully', async ({ page }) => {
        // Constitutional: Test error handling for configuration

        // Intercept config request and make it fail
        await page.route('**/config/app.config.json', route => {
            route.abort();
        });

        // Navigate to page with failing config
        await page.goto('file://' + process.cwd() + '/src/index.html');

        // App should still function with fallback values
        await expect(page.locator('#main-button')).toBeVisible();

        // Button should still work (fallback behavior)
        await page.locator('#main-button').click();

        // Should still show some message (fallback)
        const messageArea = page.locator('#message-area');
        const message = await messageArea.textContent();
        expect(message).toBeTruthy();
    });

    test('should validate configuration structure', async ({ page }) => {
        // Constitutional: Test configuration validation

        await page.waitForFunction(() => window.DontPressButton?.config);

        const validation = await page.evaluate(() => {
            const config = window.DontPressButton.config;

            return {
                hasRequiredKeys: !!(
                    config.pressToConfirmCount &&
                    config.messages &&
                    config.uiText &&
                    config.a11y
                ),
                pressToConfirmCountValid: typeof config.pressToConfirmCount === 'number',
                messagesValid: Array.isArray(config.messages) && config.messages.length > 0,
                uiTextValid: !!(
                    config.uiText.header &&
                    config.uiText.button &&
                    config.uiText.confirmPaymentTitle &&
                    config.uiText.confirmYes &&
                    config.uiText.confirmNo &&
                    config.uiText.paymentCompleted
                ),
                a11yValid: typeof config.a11y === 'object'
            };
        });

        expect(validation.hasRequiredKeys).toBe(true);
        expect(validation.pressToConfirmCountValid).toBe(true);
        expect(validation.messagesValid).toBe(true);
        expect(validation.uiTextValid).toBe(true);
        expect(validation.a11yValid).toBe(true);
    });

    test('should apply accessibility configuration', async ({ page }) => {
        // Constitutional: Test accessibility behavior configuration

        await page.waitForFunction(() => window.DontPressButton?.config);

        // Get a11y settings from config
        const a11yConfig = await page.evaluate(() => {
            return window.DontPressButton.config.a11y;
        });

        // Get to modal to test a11y features
        const triggerCount = await page.evaluate(() => {
            return window.DontPressButton.config.pressToConfirmCount;
        });

        for (let i = 1; i <= triggerCount; i++) {
            await page.locator('#main-button').click();
        }

        await expect(page.locator('#payment-modal')).toBeVisible();

        // Test ESC key behavior if configured
        if (a11yConfig.closeOnEsc) {
            await page.keyboard.press('Escape');
            await expect(page.locator('#payment-modal')).not.toBeVisible();
        }
    });

    test('should maintain performance with configuration loading', async ({ page }) => {
        // Constitutional: Performance requirements with configuration

        const startTime = await page.evaluate(() => performance.now());

        // Wait for app to be fully loaded and configured
        await page.waitForFunction(() => {
            return window.DontPressButton &&
                   window.DontPressButton.config &&
                   document.getElementById('main-button');
        });

        const endTime = await page.evaluate(() => performance.now());
        const loadTime = endTime - startTime;

        // Constitutional: Configuration loading should not violate performance
        expect(loadTime).toBeLessThan(1000); // Allow more time for config loading

        // Test button interaction performance after config loading
        const buttonStartTime = await page.evaluate(() => performance.now());
        await page.locator('#main-button').click();

        await page.waitForFunction(() => {
            const messageArea = document.getElementById('message-area');
            return messageArea && messageArea.textContent.length > 0;
        });

        const buttonEndTime = await page.evaluate(() => performance.now());
        const buttonResponseTime = buttonEndTime - buttonStartTime;

        // Constitutional: Button interaction should maintain < 100ms
        expect(buttonResponseTime).toBeLessThan(100);
    });

});

/*
 * Constitutional Compliance Declaration for UoW-005 Tests
 *
 * ✅ Test-First: Complete test suite before configuration implementation
 * ✅ Configuration-Driven: All externalized content and behavior tested
 * ✅ Simplicity: Direct JSON configuration testing without complexity
 * ✅ Integration-First: E2E tests prioritizing complete configuration flows
 * ✅ Error Handling: Configuration failure scenarios covered
 * ✅ Performance: Configuration loading performance validated
 *
 * Expected Test Result: ALL TESTS SHOULD FAIL (RED state achieved)
 * Next Phase: Implement configuration loading and application (GREEN)
 */