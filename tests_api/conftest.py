import pytest
from playwright.sync_api import APIRequestContext, Playwright

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api(playwright: Playwright) -> APIRequestContext:
    """提供 API 請求 context，session 層級共用一個連線"""
    context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={"Accept": "application/json"},
        timeout=10_000,
    )
    yield context
    context.dispose()
@pytest.fixture(scope="session")
def browser_name():
    """API 測試不需要瀏覽器，覆寫此 fixture 以消除 [chromium] 參數化"""
    return None