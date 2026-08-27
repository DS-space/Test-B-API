from typing import List

from playwright.sync_api import Page, Locator

from src.main.ui.pages.base_page import BasePage


class CatalogPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.product_cards = page.locator(".inventory_item")
        self.sort_select = page.locator('[data-test="product-sort-container"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator('[data-test="logout-sidebar-link"]')

    def open(self) -> None:
        """Переход на страницу авторизации"""
        self.page.goto(self.URL)

    def login(self, username: str, password: str) -> None:
        """Авторизация"""
        self.open()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def logout(self) -> None:
        """Выходим из аккаунта, нажимая Logout в меню"""
        self.menu_button.click()
        self.logout_link.click()

    def sort_items(self, option: str) -> None:
        """Сортируем товары по свойству"""
        self.sort_select.select_option(option)

    def add_to_cart(self, product_name: str) -> Locator:
        """Добавляем товар в корзину по имени"""
        card = self.product_cards.filter(has_text=product_name)
        button = card.locator("button")
        if button.inner_text() == "Add to cart":
            button.click()
        return button

    def remove_from_cart(self, product_name: str) -> Locator:
        """Удаляем товар из корзины по имени"""
        card = self.product_cards.filter(has_text=product_name)
        button = card.locator("button")
        if button.inner_text() == "Remove":
            button.click()
        return button

    def get_products_count(self) -> int:
        """Возвращаем количество товаров в каталоге"""
        return self.product_cards.count()

    def get_product_names(self) -> List[str]:
        """Возвращаем названия товаров в каталоге"""
        return self.product_cards.locator(".inventory_item_name").all_text_contents()

    def get_product_prices(self) -> list[float]:
        """Возвращаем цены товаров в каталоге"""
        prices_text = self.product_cards.locator(".inventory_item_price").all_text_contents()
        return [float(p.replace("$", "")) for p in prices_text]

    def get_cart_count(self) -> int:
        """Возвращаем количество товаров в корзине, получаем из badge"""
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0

    def open_product_details(self, product_name: str) -> tuple[str, float, str, float]:
        """Открываем детали товара,
        возвращаем название и цену из карточки и со страницы деталей,
        возвращаемся назад"""
        card = self.product_cards.filter(has_text=product_name)
        name = card.locator(".inventory_item_name").inner_text()
        price_text = card.locator(".inventory_item_price").inner_text()
        price = float(price_text.replace("$", ""))

        card.locator(".inventory_item_name").click()
        detail_name = self.page.locator('[data-test="inventory-item-name"]').inner_text()
        detail_price_text = self.page.locator('[data-test="inventory-item-price"]').inner_text()
        detail_price = float(detail_price_text.replace("$", ""))

        self.page.go_back()
        return name, price, detail_name, detail_price