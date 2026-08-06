from playwright.sync_api import Page


class InventoryPage:
    """SauceDemo 商品列表頁"""

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        self.page = page
        self.inventory_items = page.locator(".inventory_item")
        self.cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def add_item_to_cart(self, item_name: str):
        """依商品名稱加入購物車，例如 'Sauce Labs Backpack'"""
        self.inventory_items.filter(has_text=item_name).get_by_role(
            "button", name="Add to cart"
        ).click()

    def add_first_item_to_cart(self):
        """將列表第一個商品加入購物車"""
        self.inventory_items.first.get_by_role("button", name="Add to cart").click()

    def get_cart_count(self) -> str:
        """取得購物車數量（badge 文字）"""
        return self.cart_badge.inner_text()

    def go_to_cart(self):
        """點擊購物車圖示，進入購物車頁"""
        self.cart_link.click()