from typing import List

from playwright.sync_api import Page, expect

from src.main.ui.utils.constants import Urls


class BasketPage:
    URL = Urls.CART

    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')
        self.cart_items = page.locator('[data-test="inventory-item"]')
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.error_message = page.locator('[data-test="error"]')

    def open_cart(self) -> None:
        """Переход в корзину через иконку"""
        self.cart_link.click()

    def checkout(self) -> None:
        """Нажать Checkout и перейти на страницу Checkout"""
        self.checkout_button.click()

    def remove_item(self, product_name: str) -> None:
        """Удаляем товар по имени"""
        card = self.cart_items.filter(has_text=product_name)
        remove_button = card.locator("button")
        remove_button.click()

    def expect_item_in_cart(self, product_name: str) -> None:
        """Проверяем, что товар присутствует в корзине"""
        card = self.cart_items.filter(has_text=product_name)
        expect(card).to_be_visible()

    def expect_item_not_in_cart(self, product_name: str) -> None:
        """Проверяем, что товар отсутствует в корзине"""
        card = self.cart_items.filter(has_text=product_name)
        expect(card).not_to_be_visible()

    def get_item_names(self) -> list[str]:
        """Возвращаем список названий товаров в корзине"""
        return self.cart_items.locator(".inventory_item_name").all_text_contents()

    def get_item_prices(self) -> List:
        """Возвращаем список цен товаров в корзине"""
        prices_text = self.cart_items.locator(".inventory_item_price").all_text_contents()
        return [float(p.replace("$", "")) for p in prices_text]

    def get_items_total_price(self) -> float:
        """Возвращаем сумму цен товаров в корзине"""
        prices_text = self.cart_items.locator(".inventory_item_price").all_text_contents()
        return sum([float(p.replace("$", "")) for p in prices_text])
