import { expect, test } from '@playwright/test';

test.describe('Project entry visual baseline', () => {
  test('captures the project entry screen', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    await expect(page.getByRole('heading', { name: /LogiQore Reporter/i })).toBeVisible();

    await expect(page.locator('body')).toHaveScreenshot('project-entry.png', {
      animations: 'disabled',
      maxDiffPixelRatio: 0.01,
      fullPage: true,
    });
  });
});
