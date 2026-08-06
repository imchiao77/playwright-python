from playwright.sync_api import Page


class LoginPage:
    """SauceDemo 登入頁面"""

    URL = "https://www.saucedemo.com"

    def __init__(self, page: Page):
        self.page = page
        # 集中管理 selector，網站改版只需改這裡
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    def goto(self):
        """開啟登入頁"""
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        """填入帳密並送出"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def login_as_standard_user(self):
        """以標準使用者登入（開啟頁面 + 登入，一步完成）"""
        self.goto()
        self.login("standard_user", "secret_sauce")