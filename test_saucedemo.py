from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# 測試一：登入成功
def test_login_success(page: Page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


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

    expect(page).to_have_url("https://www.saucedemo.com/cart.html")

    # 以下購物車與結帳流程，下一輪重構
    page.click("[data-test='checkout']")
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")

    page.fill("[data-test='firstName']", "Elisa")
    page.fill("[data-test='lastName']", "Luo")
    page.fill("[data-test='postalCode']", "10001")
    page.click("[data-test='continue']")

    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")

    page.click("[data-test='finish']")
    expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")