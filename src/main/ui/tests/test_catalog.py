from src.main.ui.steps.catalog_steps import CatalogSteps


def test_count_catalog(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    products_count = steps.get_products_count()
    assert products_count == 6, \
        f"Ожидаем, что количество товаров 6, количество товаров: {products_count}"

def test_sorted_by_name(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.sort_items("az")
    names = steps.get_product_names()
    assert names == sorted(names), \
        f"Ожидаем, что товары отсортированы по имени A-Z, товары: {names}"

    steps.sort_items("za")
    names = steps.get_product_names()
    assert names == sorted(names, reverse=True), \
        f"Ожидаем, что товары отсортированы по имени Z-A, товары: {names}"

def test_sort_by_price(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.sort_items("lohi")
    prices = steps.get_product_prices()
    assert prices == sorted(prices), \
        f"Ожидалем, что товары отсортированы по цене low -> high, prices: {prices}"

    prices = steps.sort_items("hilo").get_product_prices()
    assert prices == sorted(prices, reverse=True), \
        f"Ожидаем, что товары отсортированы по цене high -> low, prices: {prices}"

def test_add_to_card(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Bike Light")
    cart_count = steps.get_cart_count()
    assert cart_count == 1, \
        f"Ожидаем, что количество товаров в корзине соответсвует 1, количество: {cart_count}"

def test_add_and_remove_onesie(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Onesie")
    assert steps.get_cart_count() == 1

    steps.remove_from_cart("Sauce Labs Onesie")
    assert steps.get_cart_count() == 0

def test_product_details_onesie(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    name, price, detail_name, detail_price = steps.open_product_details("Sauce Labs Onesie")
    assert name == detail_name, \
        f"Ожидаем, что название в карточке: {name!r}, совпадает с названием на странице товара: {detail_name!r}"
    assert price == detail_price, \
        f"Ожидаем, что цена в карточке:{price}, совпадает с ценой на странице товара: {detail_price}"

def test_product_details_fleece_jacket(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    name, price, detail_name, detail_price = steps.open_product_details("Sauce Labs Fleece Jacket")
    assert name == detail_name, \
        f"Ожидаем, что название в карточке: {name!r}, совпадает с названием на странице товара: {detail_name!r}"
    assert price == detail_price, \
        f"Ожидаем, что цена в карточке:{price}, совпадает с ценой на странице товара: {detail_price}"

def test_remove_item_from_catalog(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Test.allTheThings() T-Shirt (Red)")
    steps.remove_from_cart("Test.allTheThings() T-Shirt (Red)")
    assert steps.get_cart_count() == 0