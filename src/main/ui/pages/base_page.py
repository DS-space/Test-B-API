from playwright.sync_api import Page

from src.main.ui.utils.constants import Urls


class BasePage:
    URL = Urls.BASE

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.locator("#login-button")
