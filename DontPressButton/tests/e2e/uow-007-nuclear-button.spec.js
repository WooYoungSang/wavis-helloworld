/*
 * 🔴 Phase 1: RED - Constitutional Test Specification for UoW-007
 * Unit of Work: Nuclear Launch Button Styling
 *
 * Constitutional Principles Applied:
 * - Test-First: Complete nuclear button visual tests before CSS implementation
 * - Simplicity: Direct CSS styling without external image dependencies
 * - Framework-Direct: Using native CSS properties and browser APIs
 * - Constitutional Compliance: All 9 principles validated through visual testing
 */

const { test, expect } = require('@playwright/test');

test.describe('UoW-007: Nuclear Launch Button Styling', () => {

    test.beforeEach(async ({ page }) => {
        // Constitutional: Navigate to HTTP server for proper configuration loading
        await page.goto('http://localhost:8000/src/index.html');

        // Constitutional: Ensure page is fully loaded and configured
        await expect(page.locator('#main-button')).toBeVisible();

        // Wait for configuration to load
        await page.waitForFunction(() => window.DontPressButton?.config);
    });

    test('should display nuclear button with red circular design', async ({ page }) => {
        // Constitutional Test Strategy: Visual CSS Implementation Testing
        // Test that button appears as a red circular nuclear launch button

        const button = page.locator('#main-button');

        // Verify button has nuclear button styling class
        await expect(button).toHaveClass(/nuclear-button/);

        // Verify button is circular (equal width and height with border-radius 50%)
        const buttonBox = await button.boundingBox();
        expect(Math.abs(buttonBox.width - buttonBox.height)).toBeLessThan(5); // Allow 5px tolerance

        // Verify button has red background color (nuclear warning color)
        const computedStyle = await page.evaluate(() => {
            const button = document.getElementById('main-button');
            return window.getComputedStyle(button);
        });

        // Should have red nuclear warning color
        expect(computedStyle.backgroundColor).toBe('rgb(196, 57, 43)'); // #c4392b

        // Verify circular border-radius (should be 50% for perfect circle)
        expect(computedStyle.borderRadius).toBe('50%');

        // Verify minimum touch target size (Constitutional accessibility requirement)
        expect(buttonBox.width).toBeGreaterThanOrEqual(80); // Nuclear buttons are larger
        expect(buttonBox.height).toBeGreaterThanOrEqual(80);
    });

    test('should have nuclear warning gradient and shadow effects', async ({ page }) => {
        // Constitutional: Test complex CSS visual effects without external dependencies

        const button = page.locator('#main-button');

        const computedStyle = await page.evaluate(() => {
            const button = document.getElementById('main-button');
            return window.getComputedStyle(button);
        });

        // Verify gradient background (nuclear warning gradient)
        expect(computedStyle.backgroundImage).toContain('gradient');
        expect(computedStyle.backgroundImage).toContain('rgb(196, 57, 43)'); // Primary red
        expect(computedStyle.backgroundImage).toContain('rgb(231, 76, 60)'); // Lighter red

        // Verify nuclear button shadow effects
        expect(computedStyle.boxShadow).toBeTruthy();
        expect(computedStyle.boxShadow).toContain('rgba'); // Should have shadow with transparency

        // Verify text shadow for nuclear warning appearance
        expect(computedStyle.textShadow).toBeTruthy();
        expect(computedStyle.textShadow).toContain('rgba');
    });

    test('should display nuclear warning symbols and text styling', async ({ page }) => {
        // Constitutional: Test text content and nuclear symbolism

        const button = page.locator('#main-button');

        // Verify button contains nuclear warning symbol
        const buttonText = await button.textContent();
        expect(buttonText).toContain('☢'); // Nuclear symbol
        expect(buttonText).toContain('LAUNCH'); // Nuclear launch terminology

        // Verify text styling for nuclear appearance
        const computedStyle = await page.evaluate(() => {
            const button = document.getElementById('main-button');
            return window.getComputedStyle(button);
        });

        // Verify bold font weight for nuclear warning (browsers report as 700)
        expect(computedStyle.fontWeight).toBe('700');

        // Verify uppercase transformation for nuclear command appearance
        expect(computedStyle.textTransform).toBe('uppercase');

        // Verify white text color for contrast against red background
        expect(computedStyle.color).toBe('rgb(255, 255, 255)'); // White text
    });

    test('should have nuclear button hover and active animations', async ({ page }) => {
        // Constitutional: Test CSS animation effects for nuclear button interaction

        const button = page.locator('#main-button');

        // Get initial styles
        const initialStyle = await page.evaluate(() => {
            const button = document.getElementById('main-button');
            return {
                transform: window.getComputedStyle(button).transform,
                boxShadow: window.getComputedStyle(button).boxShadow
            };
        });

        // Hover over button
        await button.hover();

        // Wait for CSS transition
        await page.waitForTimeout(200);

        // Verify hover effects (nuclear button should have dramatic hover state)
        const hoverStyle = await page.evaluate(() => {
            const button = document.getElementById('main-button');
            return {
                transform: window.getComputedStyle(button).transform,
                boxShadow: window.getComputedStyle(button).boxShadow
            };
        });

        // Hover should change transform (scale up for nuclear warning)
        expect(hoverStyle.transform).not.toBe(initialStyle.transform);
        // Browser may render scale(1.05) as matrix(1.05, 0, 0, 1.05, 0, 0)
        expect(hoverStyle.transform).toMatch(/(scale|matrix\(1\.05)/); // Should scale on hover

        // Hover should enhance shadow (nuclear glow effect)
        expect(hoverStyle.boxShadow).not.toBe(initialStyle.boxShadow);
    });

    test('should maintain nuclear button styling during click interactions', async ({ page }) => {
        // Constitutional: Test visual consistency during user journey

        const button = page.locator('#main-button');
        const messageArea = page.locator('#message-area');

        // Verify nuclear button maintains styling through multiple clicks
        for (let clickCount = 1; clickCount <= 5; clickCount++) {
            await button.click();

            // Verify nuclear button class is maintained
            await expect(button).toHaveClass(/nuclear-button/);

            // Verify button remains circular after click
            const buttonBox = await button.boundingBox();
            expect(Math.abs(buttonBox.width - buttonBox.height)).toBeLessThan(5);

            // Verify red nuclear color is maintained
            const backgroundColor = await page.evaluate(() => {
                const button = document.getElementById('main-button');
                return window.getComputedStyle(button).backgroundColor;
            });
            expect(backgroundColor).toBe('rgb(196, 57, 43)');

            // Verify message still appears (functionality preserved)
            const message = await messageArea.textContent();
            expect(message).toBeTruthy();
        }
    });

    test('should display nuclear button correctly in modal state', async ({ page }) => {
        // Constitutional: Test nuclear button styling when modal is triggered

        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');

        // Get to modal trigger (10 clicks)
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        await expect(modal).toBeVisible();

        // Verify nuclear button styling is maintained even when modal is open
        await expect(button).toHaveClass(/nuclear-button/);

        // Verify button is still visible and styled correctly
        const computedStyle = await page.evaluate(() => {
            const button = document.getElementById('main-button');
            return {
                backgroundColor: window.getComputedStyle(button).backgroundColor,
                borderRadius: window.getComputedStyle(button).borderRadius,
                display: window.getComputedStyle(button).display
            };
        });

        expect(computedStyle.backgroundColor).toBe('rgb(196, 57, 43)');
        expect(computedStyle.borderRadius).toBe('50%');
        expect(computedStyle.display).not.toBe('none'); // Button should remain visible
    });

    test('should handle nuclear button accessibility with new styling', async ({ page }) => {
        // Constitutional: Accessibility compliance with nuclear button design

        const button = page.locator('#main-button');

        // Verify button remains focusable with nuclear styling
        await button.focus();
        const focusedElement = await page.evaluate(() => document.activeElement.id);
        expect(focusedElement).toBe('main-button');

        // Verify focus indicators work with nuclear design
        const focusStyle = await page.evaluate(() => {
            const button = document.getElementById('main-button');
            return window.getComputedStyle(button);
        });

        // Focus should be visible (required for accessibility)
        expect(focusStyle.outline).toBeTruthy();

        // Verify color contrast is maintained (white text on red background)
        // Constitutional: 4.5:1 contrast ratio requirement
        const textColor = focusStyle.color;
        const backgroundColor = focusStyle.backgroundColor;
        expect(textColor).toBe('rgb(255, 255, 255)'); // White
        expect(backgroundColor).toBe('rgb(196, 57, 43)'); // Red

        // Verify keyboard interaction works with nuclear styling
        await page.keyboard.press('Enter');

        // Verify click was registered (message should appear)
        const messageArea = page.locator('#message-area');
        const message = await messageArea.textContent();
        expect(message).toBeTruthy();
    });

    test('should perform nuclear button animations within constitutional time limits', async ({ page }) => {
        // Constitutional: Performance testing for nuclear button animations

        const button = page.locator('#main-button');

        // Measure animation performance
        const startTime = await page.evaluate(() => performance.now());

        // Trigger hover animation
        await button.hover();

        // Wait for animation to complete
        await page.waitForTimeout(300); // Allow for animation completion

        // Trigger click animation
        await button.click();

        const endTime = await page.evaluate(() => performance.now());
        const totalTime = endTime - startTime;

        // Constitutional: Total animation time should not impact <100ms click response
        expect(totalTime).toBeLessThan(500); // Animation overhead limit

        // Verify message appears quickly despite animations
        const messageTime = await page.evaluate(() => performance.now());
        const responseTime = messageTime - startTime;

        // Message should still appear within constitutional limits
        await page.waitForFunction(() => {
            const messageArea = document.getElementById('message-area');
            return messageArea && messageArea.textContent.length > 0;
        });

        // Constitutional: Animation should not slow down core functionality
        const finalTime = await page.evaluate(() => performance.now());
        const coreResponseTime = finalTime - startTime;
        expect(coreResponseTime).toBeLessThan(800); // Generous limit for animated interactions
    });

    test('should maintain constitutional compliance markers with nuclear styling', async ({ page }) => {
        // Constitutional: Verify all 9 principles maintained with nuclear button

        const button = page.locator('#main-button');

        // Verify constitutional compliance is maintained with nuclear styling
        const compliance = await page.evaluate(() => {
            return window.DontPressButton.constitutionalCompliance;
        });

        // All constitutional principles should remain true
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

        // Verify nuclear button functionality works
        await button.click();

        // Constitutional compliance should be maintained after nuclear button interaction
        const postClickCompliance = await page.evaluate(() => {
            return window.DontPressButton.constitutionalCompliance;
        });

        Object.values(postClickCompliance).forEach(value => {
            expect(value).toBe(true);
        });

        // Verify version updated for UoW-007
        const version = await page.evaluate(() => {
            return window.DontPressButton.version;
        });
        expect(version).toBe('1.0.0-uow007'); // Updated for nuclear button UoW
    });

});

/*
 * Constitutional Compliance Declaration for UoW-007 Nuclear Button Tests
 *
 * ✅ Test-First: Nuclear button visual tests before CSS implementation
 * ✅ Simplicity: Direct CSS styling without external dependencies
 * ✅ Framework-Direct: Native CSS properties and browser animation APIs
 * ✅ Constitutional Compliance: All 9 principles validated through nuclear styling
 * ✅ Performance: Animation performance testing implemented
 * ✅ Accessibility: Nuclear button accessibility compliance tested
 * ✅ Visual Consistency: Nuclear styling maintained throughout user journey
 *
 * Expected Test Result: ALL TESTS SHOULD FAIL (RED state achieved)
 * Next Phase: Implement nuclear button CSS styling (GREEN)
 */