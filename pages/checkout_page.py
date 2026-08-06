from playwright.sync_api import Page


class CheckoutPage:
    """SauceDemo 結帳流程（收件資訊 → 訂單確認 → 完成）"""

    STEP_ONE_URL = "https://www.saucedemo.com/checkout-step-one.html"
    STEP_TWO_URL = "https://www.saucedemo.com/checkout-step-two.html"
    COMPLETE_URL = "https://www.saucedemo.com/checkout-complete.html"

    def __init__(self, page: Page):
        self.page = page
        # Step One：收件資訊
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.error_message = page.locator("[data-test='error']")
        # Step Two：訂單確認
        self.total_label = page.locator(".summary_total_label")
        self.finish_button = page.locator("[data-test='finish']")
        # Complete：完成頁
        self.complete_header = page.locator(".complete-header")

    def fill_information(self, first_name: str, last_name: str, postal_code: str):
        """填寫收件資訊並繼續"""
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    def finish(self):
        """完成訂單"""
        self.finish_button.click()