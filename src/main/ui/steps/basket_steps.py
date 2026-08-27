from typing import List

import allure
from playwright.sync_api import Page

from src.main.ui.pages.basket_page import BasketPage


class BasketSteps:
    def __init__(self, page: Page):
        self.page = page
        self.basket_page = BasketPage(page)

    @allure.step("Открываем корзину")
    def open_cart(self):
        self.basket_page.open_cart()
        return self

    @allure.step("Переходим на страницу Checkout")
    def checkout(self):
        self.basket_page.checkout()
        return self

    @allure.step("Получаем список названий товаров в корзине")
    def get_item_names(self) -> List[str]:
        return self.basket_page.get_item_names()

    @allure.step("Удаляем товар их корзины: {product_name}")
    def remove_item(self, product_name: str):
        self.basket_page.remove_item(product_name)
        return self

    @allure.step("Берем сумму товаров из корзины")
    def get_items_total_price(self) -> float:
        return self.basket_page.get_items_total_price()

    @allure.step("Проверяем, что товар есть в корзине: {product_name}")
    def expect_item_in_cart(self, product_name: str):
        self.basket_page.expect_item_in_cart(product_name)
        return self

    @allure.step("Проверяем, что товара нет в корзине: {product_name}")
    def expect_item_not_in_cart(self, product_name: str):
        self.basket_page.expect_item_not_in_cart(product_name)
        return self
