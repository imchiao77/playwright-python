from playwright.sync_api import Page


class CartPage:
    """SauceDemo 購物車頁"""

    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.continue_shopping_button = page.locator("[data-test='continue-shopping']")

    def get_item_count(self) -> int:
        """取得購物車內商品筆數"""
        return self.cart_items.count()

    def remove_item(self, item_name: str):
        """依商品名稱移除"""
        self.cart_items.filter(has_text=item_name).get_by_role(
            "button", name="Remove"
        ).click()

    def checkout(self):
        """點擊結帳，進入填寫收件資訊頁"""
        self.checkout_button.click()