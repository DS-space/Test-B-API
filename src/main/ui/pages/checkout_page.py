from playwright.sync_api import Page, expect

from src.main.ui.utils.constants import Urls


class CheckoutPage:
    URL = Urls.CHECKOUT

    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.postal_code_input = page.get_by_placeholder("Zip/Postal Code")
        self.cancel_button = page.locator('[data-test="cancel"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.success_message = page.locator('h2[data-test="complete-header"]')
        self.error_message = page.locator('h3[data-test="error"]')
        self.item_total = page.locator('[data-test="subtotal-label"]')


    def start_checkout(self, name: str, last_name: str, postal_code: str) -> None:
        """Заполняем поля, нажимаем на кнопку Continue и переходим к следующему шагу"""
        self.first_name_input.fill(name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    def finish_checkout(self):
        """Нажимаем на кнопку Finish, завершаем оформление заказа"""
        self.finish_button.click()

    def get_success_message(self) -> str:
        """Возвращаем сообщение об успехе оформления заказа"""
        return self.success_message.inner_text()

    def get_error_message(self) -> str:
        """Возвращаем сообщение об ошибке при оформлении заказа"""
        return self.error_message.inner_text()

    def get_item_total_after_continue(self) -> float:
        """Возвращаем сумму всех товаров"""
        expect(self.item_total).to_be_visible()
        total_text = self.item_total.inner_text().split("$")[1]
        return float(total_text)

