import allure
from playwright.sync_api import Page

from src.main.ui.pages.checkout_page import CheckoutPage


class CheckoutSteps:
    def __init__(self, page: Page):
        self.page = page
        self.checkout_page = CheckoutPage(page)

    @allure.step("Начинаем Checkout: {first_name} {last_name}, {postal_code}")
    def start_checkout(self, first_name: str, last_name: str, postal_code: str):
        self.checkout_page.start_checkout(first_name, last_name, postal_code)
        return self

    @allure.step("Завершаем Checkout")
    def finish_checkout(self):
        self.checkout_page.finish_checkout()
        return self

    @allure.step("Получаем сумму товаров после Continue")
    def get_item_total_after_continue(self):
        return self.checkout_page.get_item_total_after_continue()

    @allure.step("Получаем текст успеха на Checkout")
    def get_success_message(self):
        return self.checkout_page.get_success_message()

    @allure.step("Получаем текст ошибки на Checkout")
    def get_error_message(self):
        return self.checkout_page.get_error_message()