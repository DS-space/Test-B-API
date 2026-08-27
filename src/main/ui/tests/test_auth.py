from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.login_steps import LoginSteps


def test_auth(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")

    assert page.url == "https://www.saucedemo.com/inventory.html", \
        "Ожидаем, что страница после авторизации - 'https://www.saucedemo.com/inventory.html'"

def test_auth_locked_out_user(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("locked_out_user", "secret_sauce")

    assert page.url == "https://www.saucedemo.com/"
    error_text = steps.get_error_text()
    assert "locked out" in error_text, \
        f"Ожидаем сообщение о заблокированном пользователе, сообщение: {error_text}"

def test_logout(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    assert catalog.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

    catalog.logout()
    assert page.url == "https://www.saucedemo.com/", "Ожидаем возврат на страницу авторизации"

def test_visual_user_logaut(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login("visual_user", "secret_sauce")
    assert catalog.get_products_count() > 0

    catalog.logout()
    assert page.url == "https://www.saucedemo.com/", "Ожидаем возврат на страницу авторизации"