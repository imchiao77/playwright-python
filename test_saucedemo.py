from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


# 測試一：登入成功
def test_login_success(page: Page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url(InventoryPage.URL)


# 測試二：登入失敗（錯誤密碼）
def test_login_fail(page: Page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("standard_user", "wrong_password")

    expect(login_page.error_message).to_be_visible()


# 測試三：加入購物車
def test_add_to_cart(page: Page):
    LoginPage(page).login_as_standard_user()

    inventory_page = InventoryPage(page)
    inventory_page.add_item_to_cart("Sauce Labs Backpack")

    expect(inventory_page.cart_badge).to_have_text("1")


# 測試四：完整結帳流程
def test_checkout(page: Page):
    LoginPage(page).login_as_standard_user()

    inventory_page = InventoryPage(page)
    inventory_page.add_item_to_cart("Sauce Labs Backpack")
    inventory_page.go_to_cart()

    cart_page = CartPage(page)
    expect(page).to_have_url(CartPage.URL)
    cart_page.checkout()

    checkout_page = CheckoutPage(page)
    expect(page).to_have_url(CheckoutPage.STEP_ONE_URL)
    checkout_page.fill_information("Elisa", "Luo", "10001")

    expect(page).to_have_url(CheckoutPage.STEP_TWO_URL)
    checkout_page.finish()

    expect(checkout_page.complete_header).to_have_text("Thank you for your order!")