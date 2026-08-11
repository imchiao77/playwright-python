"""
problem_user 已知缺陷驗證

SauceDemo 提供 problem_user 帳號以模擬前端異常。
本檔案以 standard_user 作為基準線，對照出 problem_user 的實際缺陷，
並以 @pytest.mark.xfail(strict=True) 記錄「正確的期待」與「目前已知失敗」。

strict=True 的作用：若缺陷被修復導致測試意外通過，pytest 會回報 FAILED，
提醒開發者移除標記，避免 repo 累積過期的缺陷記錄。
"""

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def go_to_checkout_step_one(page: Page) -> CheckoutPage:
    """共用流程：加入商品 → 進購物車 → 進入收件資訊頁"""
    inventory = InventoryPage(page)
    inventory.add_item_to_cart("Sauce Labs Backpack")
    inventory.go_to_cart()
    CartPage(page).checkout()
    return CheckoutPage(page)


# ==================== 商品圖片 ====================

def test_product_images_are_unique_baseline(page: Page):
    """基準線：standard_user 的六個商品應各有不同圖片"""
    LoginPage(page).login_as(LoginPage.STANDARD_USER)

    sources = InventoryPage(page).get_image_sources()

    assert len(sources) == 6, f"商品數量應為 6，實際為 {len(sources)}"
    assert len(set(sources)) == len(sources), "商品圖片出現重複"


@pytest.mark.xfail(
    reason="problem_user 已知缺陷：所有商品圖片皆載入 404 佔位圖 sl-404.jpg",
    strict=True,
)
def test_product_images_are_unique_problem_user(problem_user_page: Page):
    """problem_user 的商品圖片應各不相同（已知失敗）"""
    sources = InventoryPage(problem_user_page).get_image_sources()

    assert len(set(sources)) == len(sources), (
        f"圖片重複，共 {len(sources)} 張但僅 {len(set(sources))} 種：{set(sources)}"
    )


# ==================== 價格排序 ====================

def test_sort_by_price_low_to_high_baseline(page: Page):
    """基準線：standard_user 依價格低到高排序應正確遞增"""
    LoginPage(page).login_as(LoginPage.STANDARD_USER)
    inventory = InventoryPage(page)

    inventory.sort_by("Price (low to high)")
    prices = inventory.get_item_prices()

    assert prices == sorted(prices), f"價格未正確遞增：{prices}"


@pytest.mark.xfail(
    reason="problem_user 已知缺陷：排序下拉選單值改變，但商品列表順序不變",
    strict=True,
)
def test_sort_by_price_low_to_high_problem_user(problem_user_page: Page):
    """problem_user 依價格低到高排序應正確遞增（已知失敗）"""
    inventory = InventoryPage(problem_user_page)

    inventory.sort_by("Price (low to high)")
    prices = inventory.get_item_prices()

    assert prices == sorted(prices), f"價格未正確遞增：{prices}"


# ==================== 名稱排序 ====================

def test_sort_by_name_z_to_a_baseline(page: Page):
    """基準線：standard_user 依名稱 Z-A 排序應正確遞減"""
    LoginPage(page).login_as(LoginPage.STANDARD_USER)
    inventory = InventoryPage(page)

    inventory.sort_by("Name (Z to A)")
    names = inventory.get_item_names()

    assert names == sorted(names, reverse=True), f"名稱未正確遞減：{names}"


@pytest.mark.xfail(
    reason="problem_user 已知缺陷：排序下拉選單值改變，但商品列表順序不變",
    strict=True,
)
def test_sort_by_name_z_to_a_problem_user(problem_user_page: Page):
    """problem_user 依名稱 Z-A 排序應正確遞減（已知失敗）"""
    inventory = InventoryPage(problem_user_page)

    inventory.sort_by("Name (Z to A)")
    names = inventory.get_item_names()

    assert names == sorted(names, reverse=True), f"名稱未正確遞減：{names}"


# ==================== 結帳表單 ====================

def test_checkout_form_retains_input_baseline(page: Page):
    """基準線：standard_user 的收件資訊三欄應各自保留輸入值"""
    LoginPage(page).login_as(LoginPage.STANDARD_USER)
    checkout = go_to_checkout_step_one(page)

    checkout.first_name_input.fill("Elisa")
    checkout.last_name_input.fill("Luo")
    checkout.postal_code_input.fill("10001")

    assert checkout.first_name_input.input_value() == "Elisa"
    assert checkout.last_name_input.input_value() == "Luo"
    assert checkout.postal_code_input.input_value() == "10001"


@pytest.mark.xfail(
    reason=(
        "problem_user 已知缺陷：Last Name 欄位的輸入被寫入 First Name，"
        "導致 Last Name 恆為空值"
    ),
    strict=True,
)
def test_checkout_form_retains_input_problem_user(problem_user_page: Page):
    """problem_user 的收件資訊三欄應各自保留輸入值（已知失敗）"""
    checkout = go_to_checkout_step_one(problem_user_page)

    checkout.first_name_input.fill("Elisa")
    checkout.last_name_input.fill("Luo")
    checkout.postal_code_input.fill("10001")

    actual = {
        "first_name": checkout.first_name_input.input_value(),
        "last_name": checkout.last_name_input.input_value(),
        "postal_code": checkout.postal_code_input.input_value(),
    }

    assert actual == {
        "first_name": "Elisa",
        "last_name": "Luo",
        "postal_code": "10001",
    }, f"欄位值與輸入不符：{actual}"


@pytest.mark.xfail(
    reason=(
        "problem_user 已知缺陷：因 Last Name 無法填入，"
        "表單驗證恆失敗，無法進入訂單確認頁"
    ),
    strict=True,
)
def test_problem_user_can_proceed_to_order_review(problem_user_page: Page):
    """problem_user 填妥收件資訊後應能進入訂單確認頁（已知失敗）"""
    page = problem_user_page
    checkout = go_to_checkout_step_one(page)

    checkout.fill_information("Elisa", "Luo", "10001")

    expect(page).to_have_url(CheckoutPage.STEP_TWO_URL, timeout=3000)