from playwright.sync_api import Page, expect

# 測試一：登入成功
def test_login_success(page: Page):
    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

# 測試二：登入失敗（錯誤密碼）
def test_login_fail(page: Page):
    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "wrong_password")
    page.click("#login-button")
    expect(page.locator("[data-test='error']")).to_be_visible()

# 測試三：加入購物車
def test_add_to_cart(page: Page):
    # 先登入
    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    # 加入第一個商品到購物車
    page.click(".btn_inventory:first-of-type")

    # 確認購物車數量顯示 1
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")

# 測試三：加入購物車
def test_add_to_cart(page: Page):
    # 先登入
    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    # 加入第一個商品到購物車
    page.click(".btn_inventory:first-of-type")

    # 確認購物車數量顯示 1
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")

# 測試四：完整結帳流程
def test_checkout(page: Page):
    # 登入
    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    # 加入商品
    page.click(".btn_inventory:first-of-type")

    # 進入購物車
    page.click(".shopping_cart_link")
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")

    # 點擊結帳
    page.click("[data-test='checkout']")
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")

    # 填寫收件資訊
    page.fill("[data-test='firstName']", "Elisa")
    page.fill("[data-test='lastName']", "Luo")
    page.fill("[data-test='postalCode']", "10001")
    page.click("[data-test='continue']")

    # 確認訂單頁
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")

    # 完成訂單
    page.click("[data-test='finish']")
    expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
