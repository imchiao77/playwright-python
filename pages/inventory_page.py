from playwright.sync_api import Page


class InventoryPage:
    """SauceDemo 商品列表頁"""

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        self.page = page
        self.inventory_items = page.locator(".inventory_item")
        self.cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.item_images = page.locator(".inventory_item_img img")
        self.item_names = page.locator(".inventory_item_name")
        self.item_prices = page.locator(".inventory_item_price")
        # 注意：class 用底線，data-test 用連字號
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")

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

    def get_image_sources(self) -> list[str]:
        """取得所有商品圖片的 src"""
        return [img.get_attribute("src") for img in self.item_images.all()]

    def get_item_names(self) -> list[str]:
        """取得所有商品名稱"""
        return self.item_names.all_inner_texts()

    def get_item_prices(self) -> list[float]:
        """取得所有商品價格（去掉 $ 轉成數字）"""
        return [
            float(text.replace("$", "")) for text in self.item_prices.all_inner_texts()
        ]

    def sort_by(self, label: str):
        """依下拉選單標籤排序，例如 'Price (low to high)'"""
        self.sort_dropdown.select_option(label=label)
