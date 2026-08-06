from playwright.sync_api import Page, expect

def test_title(page: Page):
    page.goto("https://www.saucedemo.com")
    expect(page).to_have_title("Swag Labs")
