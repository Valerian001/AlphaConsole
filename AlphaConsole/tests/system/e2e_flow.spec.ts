import { test, expect } from '@playwright/test';

test.describe('AlphaConsole: End-to-End Orchestration Flow', () => {
  
  test('should complete a full project lifecycle from intake to delivery', async ({ page }) => {
    // 1. Dashboard Initialization
    await page.goto('http://localhost:3000');
    await expect(page.locator('h1')).toContainText('ALPHACONSOLE');
    
    // 2. Project Intake Phase
    await page.click('button:has-text("New Objective")');
    await page.fill('textarea[placeholder*="Describe your objective"]', 'Implement JWT Auth and Secure Routes');
    await page.click('button:has-text("Start Orchestration")');
    
    // 3. Planning & Review Feedback Loop
    // Wait for Planner node to appear on the canvas
    const plannerNode = page.locator('div:has-text("Planner")');
    await expect(plannerNode).toBeVisible({ timeout: 10000 });
    
    // Wait for Reviewer to approve and show Human Gate
    const approvalNode = page.locator('div:has-text("Human Gate")');
    await expect(approvalNode).toBeVisible({ timeout: 20000 });
    
    // 4. Human Approval
    await page.click('button:has-text("Approve Plan")');
    
    // 5. Parallel Fleet Execution
    // Verify that multiple Developer nodes appear (1:1 Task Mapping)
    const developerNodes = page.locator('div:has-text("Developer")');
    await expect(developerNodes).toHaveCount(3, { timeout: 30000 });
    
    // 6. Completion & Delivery
    const successPulse = page.locator('span:has-text("System Healthy")');
    await expect(successPulse).toBeVisible();
    
    // 7. Verify Assets in Utility Panel
    await page.click('button:has-text("Project Assets")');
    await expect(page.locator('text=Auth_Integration_Report.pdf')).toBeVisible();
  });

});
