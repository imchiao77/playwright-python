import pytest
from playwright.sync_api import APIRequestContext

pytestmark = pytest.mark.api


def test_api_context_works(api: APIRequestContext):
    """確認 API fixture 可用"""
    response = api.get("/users/2")

    assert response.status == 200