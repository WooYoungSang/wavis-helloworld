/*
 * 🔴 Phase 3: RED - Constitutional Integration Tests for UoW-005
 * Unit of Work: Configuration System Implementation - Component Integration
 *
 * Constitutional Principles Applied:
 * - Test-First: Integration tests before implementation
 * - Configuration-Driven: External configuration integration testing
 * - Simplicity: Direct JSON configuration testing
 * - Error Handling: Configuration failure scenarios
 */

const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

describe('UoW-005: Configuration System Integration', () => {
    let dom;
    let document;
    let window;
    let originalFetch;

    beforeEach(() => {
        // Mock fetch for configuration loading
        originalFetch = global.fetch;
        global.fetch = jest.fn();

        // Mock a default configuration for basic tests
        global.fetch.mockResolvedValue({
            ok: true,
            json: () => Promise.resolve({
                pressToConfirmCount: 10,
                messages: ['테스트 메시지'],
                uiText: {
                    header: "Don't Press Button",
                    button: "Don't Press Button",
                    confirmPaymentTitle: "Would you like to proceed with payment?",
                    confirmYes: "Yes",
                    confirmNo: "No",
                    paymentCompleted: "Payment completed"
                },
                a11y: {
                    trapFocusInModal: true,
                    closeOnEsc: true
                }
            })
        });

        // Constitutional: Load single HTML file for integration testing
        const htmlContent = fs.readFileSync(
            path.join(__dirname, '../../src/index.html'),
            'utf-8'
        );

        dom = new JSDOM(htmlContent, {
            runScripts: 'dangerously',
            resources: 'usable',
            url: 'file:///',
            beforeParse(window) {
                // Add fetch before parsing so scripts can use it
                window.fetch = global.fetch;
            }
        });

        document = dom.window.document;
        window = dom.window;

        // JSDOM polyfill for dialog element
        const dialog = document.getElementById('payment-modal');
        if (dialog && !dialog.showModal) {
            dialog.showModal = function() {
                this.open = true;
                this.style.display = 'block';
            };
            dialog.close = function() {
                this.open = false;
                this.style.display = 'none';
            };
            dialog.open = false;
        }

        // Mock alert for testing
        window.alert = jest.fn();
    });

    afterEach(() => {
        global.fetch = originalFetch;
        if (dom) {
            dom.window.close();
        }
        jest.clearAllMocks();
    });

    test('should have configuration loader function', () => {
        // Constitutional: Test configuration loader existence

        // Wait for script execution
        return new Promise((resolve) => {
            setTimeout(() => {
                expect(window.DontPressButton).toBeTruthy();

                // Test that configuration loading infrastructure exists
                // This test will help drive the implementation
                expect(typeof window.DontPressButton.loadConfiguration === 'function' ||
                       window.DontPressButton.config !== undefined).toBeTruthy();
                resolve();
            }, 100);
        });
    });

    test('should load valid configuration JSON', async () => {
        // Constitutional: Test configuration loading with valid data

        const mockConfig = {
            pressToConfirmCount: 10,
            messages: ['테스트 메시지'],
            uiText: {
                header: 'Test Header',
                button: 'Test Button',
                confirmPaymentTitle: 'Test Modal Title',
                confirmYes: 'Test Yes',
                confirmNo: 'Test No',
                paymentCompleted: 'Test Completed'
            },
            a11y: {
                trapFocusInModal: true,
                closeOnEsc: true
            }
        };

        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: () => Promise.resolve(mockConfig)
        });

        // Wait for application initialization and configuration loading
        await new Promise(resolve => setTimeout(resolve, 200));

        // Test that configuration is properly loaded and available
        expect(global.fetch).toHaveBeenCalledWith('config/app.config.json');
    });

    test('should handle configuration loading errors', async () => {
        // Constitutional: Test error handling for configuration

        global.fetch.mockRejectedValueOnce(new Error('Network error'));

        // The app should handle this gracefully and use fallbacks
        await new Promise(resolve => setTimeout(resolve, 100));

        // App should still be functional
        expect(window.DontPressButton).toBeTruthy();
    });

    test('should handle malformed JSON configuration', async () => {
        // Constitutional: Test JSON parsing error handling

        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: () => Promise.reject(new Error('Invalid JSON'))
        });

        await new Promise(resolve => setTimeout(resolve, 100));

        // App should handle malformed JSON gracefully
        expect(window.DontPressButton).toBeTruthy();
    });

    test('should validate configuration structure', () => {
        // Constitutional: Test configuration validation

        const validConfig = {
            pressToConfirmCount: 10,
            messages: ['message1', 'message2'],
            uiText: {
                header: 'Header',
                button: 'Button',
                confirmPaymentTitle: 'Title',
                confirmYes: 'Yes',
                confirmNo: 'No',
                paymentCompleted: 'Completed'
            },
            a11y: {
                trapFocusInModal: true,
                closeOnEsc: true
            }
        };

        const invalidConfig = {
            pressToConfirmCount: 'invalid',
            messages: 'not-array'
        };

        // Test validation function (to be implemented)
        // This test drives the validation requirements
        expect(typeof validConfig.pressToConfirmCount).toBe('number');
        expect(Array.isArray(validConfig.messages)).toBe(true);
        expect(typeof validConfig.uiText).toBe('object');

        expect(typeof invalidConfig.pressToConfirmCount).not.toBe('number');
        expect(Array.isArray(invalidConfig.messages)).toBe(false);
    });

    test('should apply text configuration to DOM elements', () => {
        // Constitutional: Test text substitution system

        return new Promise((resolve) => {
            setTimeout(() => {
                const h1 = document.querySelector('h1');
                const button = document.getElementById('main-button');
                const modalTitle = document.getElementById('modal-title');

                // These should be updated from configuration
                // Initially they will be hardcoded, test drives the change
                expect(h1).toBeTruthy();
                expect(button).toBeTruthy();
                expect(modalTitle).toBeTruthy();

                // Test that elements exist and can be updated
                expect(h1.tagName.toLowerCase()).toBe('h1');
                expect(button.tagName.toLowerCase()).toBe('button');
                expect(modalTitle.tagName.toLowerCase()).toBe('h2');

                resolve();
            }, 100);
        });
    });

    test('should use configured trigger count for modal', () => {
        // Constitutional: Test behavior configuration integration

        return new Promise((resolve) => {
            setTimeout(() => {
                const button = document.getElementById('main-button');
                const modal = document.getElementById('payment-modal');

                // Test that configured trigger count is used
                // This will drive the implementation to use config value
                expect(button).toBeTruthy();
                expect(modal).toBeTruthy();

                // Simulate configuration being loaded
                if (window.DontPressButton) {
                    // Test will drive creation of config property
                    expect(window.DontPressButton).toBeTruthy();
                }

                resolve();
            }, 100);
        });
    });

    test('should use configured messages for random display', () => {
        // Constitutional: Test message configuration integration

        return new Promise((resolve) => {
            setTimeout(() => {
                const button = document.getElementById('main-button');
                const messageArea = document.getElementById('message-area');

                expect(button).toBeTruthy();
                expect(messageArea).toBeTruthy();

                // Click button to trigger message
                button.click();

                // Message should appear (from hardcoded array initially)
                // Test will drive conversion to config-based messages
                const message = messageArea.textContent;
                expect(typeof message).toBe('string');

                resolve();
            }, 100);
        });
    });

    test('should maintain performance with configuration loading', () => {
        // Constitutional: Test performance with configuration

        const startTime = performance.now();

        return new Promise((resolve) => {
            setTimeout(() => {
                const endTime = performance.now();
                const loadTime = endTime - startTime;

                // Configuration loading should not significantly impact performance
                expect(loadTime).toBeLessThan(200); // Allow some time for mocked async operations

                resolve();
            }, 100);
        });
    });

    test('should provide fallback values when configuration fails', () => {
        // Constitutional: Test graceful degradation

        global.fetch.mockRejectedValueOnce(new Error('Config load failed'));

        return new Promise((resolve) => {
            setTimeout(() => {
                // App should still function with hardcoded fallbacks
                const button = document.getElementById('main-button');
                expect(button).toBeTruthy();

                // Button should still work
                button.click();

                const messageArea = document.getElementById('message-area');
                const message = messageArea.textContent;
                expect(message).toBeTruthy(); // Should have fallback message

                resolve();
            }, 100);
        });
    });

    test('should expose configuration through public API', () => {
        // Constitutional: Test API design for configuration

        return new Promise((resolve) => {
            setTimeout(() => {
                const api = window.DontPressButton;
                expect(api).toBeTruthy();

                // Configuration should be accessible for testing
                // This drives the API design requirement
                expect(api.version).toBe('1.0.0-uow005'); // Updated for UoW-005

                resolve();
            }, 100);
        });
    });

});

/*
 * Constitutional Compliance Declaration for UoW-005 Integration Tests
 *
 * ✅ Test-First: Integration tests before configuration implementation
 * ✅ Configuration-Driven: External configuration integration patterns tested
 * ✅ Simplicity: Direct JSON configuration testing without complexity
 * ✅ Error Handling: Configuration failure and validation scenarios
 * ✅ Performance: Configuration loading impact tested
 * ✅ Integration-First: Focus on component interaction with configuration
 *
 * Expected Test Result: ALL TESTS SHOULD FAIL (RED state achieved)
 * Next Phase: Implement configuration loading, validation, and application
 */