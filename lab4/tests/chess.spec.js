import { expect, test } from '@playwright/test'

test('player can move and Stockfish replies locally', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByRole('heading', { name: 'Play Stockfish' })).toBeVisible()
  await expect(page.getByRole('grid', { name: 'Chess board' })).toBeVisible()
  await expect(page.locator('.square')).toHaveCount(64)
  await expect(page.getByText('Loading Stockfish.')).toBeHidden({ timeout: 15_000 })
  await expect(page.getByText('Stockfish failed to load.')).toHaveCount(0)

  await page.getByRole('gridcell', { name: /e2 white p/ }).click()
  await page.getByRole('gridcell', { name: 'e4' }).click()

  await expect(page.locator('.move-list li')).toHaveCount(2, { timeout: 20_000 })
  await expect(page.locator('.move-list li').first()).toContainText('e4')
  await expect(page.getByText('Your move.')).toBeVisible({ timeout: 5_000 })
})
