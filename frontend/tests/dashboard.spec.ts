import { expect, test } from "@playwright/test";

test("dashboard renders the operating surface", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Personal AI OS" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Workflow Control" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Master Agent" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Scholarship Intelligence" })).toBeVisible();
});

