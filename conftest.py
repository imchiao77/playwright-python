import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """提供已登入狀態的 page，供不需測試登入本身的測試使用"""
    LoginPage(page).login_as_standard_user()
    return page