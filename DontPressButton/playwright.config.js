// Playwright Configuration for DontPressButton
// Constitutional SDD E2E Testing Framework

import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',

  // Constitutional Principle: Integration-First Testing
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results/constitutional-compliance.json' }]
  ],

  use: {
    // Constitutional Principle: Comprehensive Testing
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',

    // Base URL for testing
    baseURL: 'http://localhost:8000',
  },

  // Constitutional testing across devices (Mobile-First principle)
  projects: [
    {
      name: 'chromium-desktop',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1280, height: 720 }
      },
    },
    {
      name: 'chromium-mobile',
      use: {
        ...devices['Pixel 5'],
        viewport: { width: 360, height: 640 }
      },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'accessibility',
      use: {
        ...devices['Desktop Chrome'],
        // Force accessibility testing
        extraHTTPHeaders: {
          'X-Test-Type': 'accessibility'
        }
      },
    }
  ],

  // Local dev server
  webServer: {
    command: 'npm run dev',
    port: 8000,
    reuseExistingServer: !process.env.CI,
  },

  // Constitutional compliance thresholds
  expect: {
    // Performance requirements from constitution
    timeout: 5000,
  },

  // Test timeout aligned with constitutional requirements
  timeout: 30000,

  // Global test configuration
  globalSetup: './tests/global-setup.js',
  globalTeardown: './tests/global-teardown.js',
});