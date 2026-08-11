from datetime import datetime
from pathlib import Path

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage

SCREENSHOT_DIR = Path("screenshots")


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """提供已登入狀態的 page，供不需測試登入本身的測試使用"""
    LoginPage(page).login_as_standard_user()
    return page

@pytest.fixture
def problem_user_page(page: Page) -> Page:
    """以 problem_user 登入，用於驗證已知缺陷"""
    LoginPage(page).login_as(LoginPage.PROBLEM_USER)
    return page

@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """把每個階段的測試結果掛回 item，讓 fixture 能判斷成功或失敗"""
    report = yield
    setattr(item, f"rep_{report.when}", report)
    return report


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    """測試失敗時自動截圖，存到 screenshots/"""
    yield  # 先讓測試跑完

    report = getattr(request.node, "rep_call", None)
    if report is None or not report.failed:
        return

    SCREENSHOT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 測試名稱含 [chromium] 等參數，把不適合當檔名的字元換掉
    safe_name = request.node.name.replace("[", "_").replace("]", "")
    file_path = SCREENSHOT_DIR / f"{safe_name}_{timestamp}.png"

    page.screenshot(path=str(file_path), full_page=True)
    print(f"\n[截圖] 測試失敗畫面已儲存：{file_path}")
    print(f"[截圖] 失敗時所在頁面：{page.url}")