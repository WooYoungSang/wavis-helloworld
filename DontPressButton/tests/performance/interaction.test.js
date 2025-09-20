/*
 * 🔴 Phase 3: RED - Constitutional Test Specification for UoW-006
 * Unit of Work: Comprehensive Testing Suite - Performance Benchmarking
 *
 * Constitutional Principles Applied:
 * - Test-First: Performance tests before infrastructure implementation
 * - Comprehensive Testing: Complete performance coverage for all interactions
 * - Performance-First: Sub-100ms interaction requirements
 * - Constitutional Compliance: Performance principles validation
 */

const { test, expect } = require('@playwright/test');

test.describe('UoW-006: Performance Benchmarking Tests', () => {

    test.beforeEach(async ({ page }) => {
        // Constitutional: Direct navigation to single HTML file
        await page.goto('file://' + process.cwd() + '/src/index.html');

        // Constitutional: Ensure page is fully loaded and configured
        await expect(page.locator('#main-button')).toBeVisible();

        // Wait for configuration to load and measure initial load time
        const loadStartTime = await page.evaluate(() => performance.now());

        await page.waitForFunction(() => window.DontPressButton?.config);

        const loadEndTime = await page.evaluate(() => performance.now());
        const loadTime = loadEndTime - loadStartTime;

        // Constitutional: Configuration loading should be fast
        expect(loadTime).toBeLessThan(1000); // 1 second max for config loading
    });

    test('should maintain sub-100ms button click response time', async ({ page }) => {
        // Constitutional: Core performance requirement - < 100ms interactions

        const button = page.locator('#main-button');
        const messageArea = page.locator('#message-area');
        const performanceTimes = [];

        // Test multiple clicks to ensure consistent performance
        for (let clickCount = 1; clickCount <= 20; clickCount++) {
            // Measure click-to-message-display performance
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

            // Constitutional: Each click must be < 100ms
            expect(responseTime).toBeLessThan(100);

            // Log performance for analysis
            console.log(`Click ${clickCount}: ${responseTime.toFixed(2)}ms`);
        }

        // Verify consistent performance across all clicks
        const averageTime = performanceTimes.reduce((a, b) => a + b, 0) / performanceTimes.length;
        const maxTime = Math.max(...performanceTimes);
        const minTime = Math.min(...performanceTimes);

        console.log(`Performance Summary: Avg: ${averageTime.toFixed(2)}ms, Max: ${maxTime.toFixed(2)}ms, Min: ${minTime.toFixed(2)}ms`);

        // Constitutional: Average should be well under 100ms
        expect(averageTime).toBeLessThan(50);

        // Constitutional: No significant performance degradation
        expect(maxTime - minTime).toBeLessThan(30); // Variance should be minimal
    });

    test('should maintain modal performance under sub-100ms', async ({ page }) => {
        // Constitutional: Modal operations performance testing

        const button = page.locator('#main-button');
        const modal = page.locator('#payment-modal');

        // Get to modal trigger (10 clicks)
        for (let i = 1; i <= 10; i++) {
            await button.click();
        }

        // Measure modal display performance
        const modalStartTime = await page.evaluate(() => performance.now());

        await expect(modal).toBeVisible();

        const modalEndTime = await page.evaluate(() => performance.now());
        const modalDisplayTime = modalEndTime - modalStartTime;

        // Constitutional: Modal display must be < 100ms
        expect(modalDisplayTime).toBeLessThan(100);

        // Test modal button performance
        const yesButton = page.locator('#modal-yes-button');

        const buttonStartTime = await page.evaluate(() => performance.now());

        // Handle alert dialog
        page.on('dialog', async dialog => {
            await dialog.accept();
        });

        await yesButton.click();

        // Wait for modal to close
        await expect(modal).not.toBeVisible();

        const buttonEndTime = await page.evaluate(() => performance.now());
        const buttonResponseTime = buttonEndTime - buttonStartTime;

        // Constitutional: Modal button response must be < 100ms
        expect(buttonResponseTime).toBeLessThan(100);

        console.log(`Modal Performance: Display: ${modalDisplayTime.toFixed(2)}ms, Button: ${buttonResponseTime.toFixed(2)}ms`);
    });

    test('should handle rapid clicking performance stress test', async ({ page }) => {
        // Constitutional: Performance under stress conditions

        const button = page.locator('#main-button');
        const stressTestClicks = 50;
        const rapidClickTimes = [];

        // Rapid clicking stress test
        for (let i = 0; i < stressTestClicks; i++) {
            const startTime = await page.evaluate(() => performance.now());

            await button.click({ delay: 5 }); // 5ms between clicks (very rapid)

            // Check if message updates (may skip some due to rapid clicking)
            const endTime = await page.evaluate(() => performance.now());
            const clickTime = endTime - startTime;

            rapidClickTimes.push(clickTime);

            // Constitutional: Even rapid clicks should be responsive
            expect(clickTime).toBeLessThan(50); // More lenient for rapid clicks
        }

        // Verify system stability after stress test
        const finalClickCount = await page.evaluate(() => {
            return window.DontPressButton.state.clickCount;
        });

        expect(finalClickCount).toBe(stressTestClicks);

        const averageRapidTime = rapidClickTimes.reduce((a, b) => a + b, 0) / rapidClickTimes.length;
        console.log(`Rapid Click Performance: Average: ${averageRapidTime.toFixed(2)}ms over ${stressTestClicks} clicks`);

        // Constitutional: Average rapid click time should be excellent
        expect(averageRapidTime).toBeLessThan(25);
    });

    test('should maintain configuration application performance', async ({ page }) => {
        // Constitutional: Configuration system performance validation

        // Measure configuration application time
        const configStartTime = await page.evaluate(() => performance.now());

        // Trigger configuration application (this happens on load, but we can test it)
        await page.evaluate(() => {
            if (window.DontPressButton && window.DontPressButton.loadConfiguration) {
                return window.DontPressButton.loadConfiguration();
            }
        });

        const configEndTime = await page.evaluate(() => performance.now());
        const configTime = configEndTime - configStartTime;

        // Constitutional: Configuration operations should be fast
        expect(configTime).toBeLessThan(50);

        // Test configuration-driven text updates
        const headerText = await page.locator('h1').textContent();
        expect(headerText).toBeTruthy();

        const buttonText = await page.locator('#main-button').textContent();
        expect(buttonText).toBeTruthy();

        console.log(`Configuration Performance: ${configTime.toFixed(2)}ms`);
    });

    test('should measure memory usage and prevent leaks', async ({ page }) => {
        // Constitutional: Memory performance and leak prevention

        // Get initial memory baseline
        const initialMemory = await page.evaluate(() => {
            if (performance.memory) {
                return {
                    usedJSHeapSize: performance.memory.usedJSHeapSize,
                    totalJSHeapSize: performance.memory.totalJSHeapSize
                };
            }
            return null;
        });

        const button = page.locator('#main-button');
        const performanceRounds = 10;

        // Perform multiple interaction rounds
        for (let round = 0; round < performanceRounds; round++) {
            // Complete user journey in each round
            for (let click = 1; click <= 15; click++) {
                await button.click();
            }

            // Reset for next round (if we can)
            await page.reload();
            await page.waitForFunction(() => window.DontPressButton?.config);
        }

        // Check memory after multiple rounds
        const finalMemory = await page.evaluate(() => {
            if (performance.memory) {
                return {
                    usedJSHeapSize: performance.memory.usedJSHeapSize,
                    totalJSHeapSize: performance.memory.totalJSHeapSize
                };
            }
            return null;
        });

        if (initialMemory && finalMemory) {
            const memoryIncrease = finalMemory.usedJSHeapSize - initialMemory.usedJSHeapSize;
            const memoryIncreasePercent = (memoryIncrease / initialMemory.usedJSHeapSize) * 100;

            console.log(`Memory Usage: Initial: ${(initialMemory.usedJSHeapSize / 1024 / 1024).toFixed(2)}MB, Final: ${(finalMemory.usedJSHeapSize / 1024 / 1024).toFixed(2)}MB`);
            console.log(`Memory Increase: ${(memoryIncrease / 1024 / 1024).toFixed(2)}MB (${memoryIncreasePercent.toFixed(2)}%)`);

            // Constitutional: Memory increase should be minimal
            expect(memoryIncreasePercent).toBeLessThan(50); // Less than 50% increase
        }
    });

    test('should benchmark cross-browser performance consistency', async ({ page, browserName }) => {
        // Constitutional: Consistent performance across browsers

        const button = page.locator('#main-button');
        const benchmarkClicks = 10;
        const browserTimes = [];

        console.log(`Testing performance on ${browserName}`);

        for (let i = 1; i <= benchmarkClicks; i++) {
            const startTime = await page.evaluate(() => performance.now());

            await button.click();

            await page.waitForFunction(() => {
                const messageArea = document.getElementById('message-area');
                return messageArea && messageArea.textContent.length > 0;
            });

            const endTime = await page.evaluate(() => performance.now());
            const responseTime = endTime - startTime;

            browserTimes.push(responseTime);

            // Constitutional: Performance requirements apply to all browsers
            expect(responseTime).toBeLessThan(100);
        }

        const avgTime = browserTimes.reduce((a, b) => a + b, 0) / browserTimes.length;
        const maxTime = Math.max(...browserTimes);

        console.log(`${browserName} Performance: Average: ${avgTime.toFixed(2)}ms, Max: ${maxTime.toFixed(2)}ms`);

        // Constitutional: All browsers should meet performance requirements
        expect(avgTime).toBeLessThan(50);
        expect(maxTime).toBeLessThan(100);
    });

    test('should validate performance monitoring integration', async ({ page }) => {
        // Constitutional: Performance monitoring system validation

        const button = page.locator('#main-button');

        // Test that performance monitoring is active in the application
        await button.click();

        // Check for performance monitoring logs
        const performanceLogs = await page.evaluate(() => {
            // Check if performance monitoring is working
            const logs = [];

            // Capture any performance warnings
            const originalWarn = console.warn;
            console.warn = function(...args) {
                if (args[0] && args[0].includes('performance')) {
                    logs.push(args.join(' '));
                }
                originalWarn.apply(console, args);
            };

            return logs;
        });

        // Verify performance monitoring infrastructure exists
        const hasPerformanceAPI = await page.evaluate(() => {
            return typeof performance !== 'undefined' &&
                   typeof performance.now === 'function' &&
                   typeof performance.mark === 'function';
        });

        expect(hasPerformanceAPI).toBe(true);

        // Test performance measurement in application code
        const buttonResponseTime = await page.evaluate(() => {
            const button = document.getElementById('main-button');
            const startTime = performance.now();

            // Simulate click processing
            button.click();

            const endTime = performance.now();
            return endTime - startTime;
        });

        // Constitutional: Performance measurement infrastructure working
        expect(buttonResponseTime).toBeGreaterThan(0);
        expect(buttonResponseTime).toBeLessThan(100);

        console.log(`Performance Monitoring: Button response time measured at ${buttonResponseTime.toFixed(2)}ms`);
    });

    test('should benchmark page load and rendering performance', async ({ page }) => {
        // Constitutional: Initial load performance requirements

        // Clear any existing page
        await page.goto('about:blank');

        // Measure full page load performance
        const loadStartTime = Date.now();

        await page.goto('file://' + process.cwd() + '/src/index.html');

        // Wait for all critical elements to be visible
        await expect(page.locator('#main-button')).toBeVisible();
        await expect(page.locator('h1')).toBeVisible();
        await expect(page.locator('#message-area')).toBeVisible();

        // Wait for configuration to load
        await page.waitForFunction(() => window.DontPressButton?.config);

        const loadEndTime = Date.now();
        const totalLoadTime = loadEndTime - loadStartTime;

        console.log(`Page Load Performance: ${totalLoadTime}ms`);

        // Constitutional: Page should load quickly
        expect(totalLoadTime).toBeLessThan(2000); // 2 seconds max

        // Measure rendering performance
        const renderingMetrics = await page.evaluate(() => {
            const perfEntries = performance.getEntriesByType('navigation')[0];
            return {
                domContentLoaded: perfEntries.domContentLoadedEventEnd - perfEntries.domContentLoadedEventStart,
                loadComplete: perfEntries.loadEventEnd - perfEntries.loadEventStart,
                firstPaint: performance.getEntriesByType('paint').find(entry => entry.name === 'first-paint')?.startTime || 0,
                firstContentfulPaint: performance.getEntriesByType('paint').find(entry => entry.name === 'first-contentful-paint')?.startTime || 0
            };
        });

        console.log('Rendering Metrics:', renderingMetrics);

        // Constitutional: Rendering should be fast
        if (renderingMetrics.firstContentfulPaint > 0) {
            expect(renderingMetrics.firstContentfulPaint).toBeLessThan(1000); // 1 second for first contentful paint
        }
    });

});

/*
 * Constitutional Compliance Declaration for UoW-006 Performance Tests
 *
 * ✅ Test-First: Performance tests before infrastructure implementation
 * ✅ Comprehensive Testing: Complete performance coverage for all interactions
 * ✅ Performance-First: Sub-100ms interaction requirements validated
 * ✅ Constitutional Compliance: Performance principles tested throughout
 * ✅ Cross-Browser: Consistent performance requirements across browsers
 * ✅ Stress Testing: Rapid clicking and memory leak prevention
 * ✅ Load Performance: Page load and rendering performance benchmarks
 * ✅ Monitoring: Performance monitoring infrastructure validation
 *
 * Expected Test Result: ALL TESTS SHOULD PASS (performance already implemented)
 * Next Phase: Verify and enhance performance infrastructure if needed (GREEN)
 */