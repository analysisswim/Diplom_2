import allure
from helpers.api_data import ApiData


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, api, registered_user):
        _, token = registered_user
        ingredients = api.get_any_ingredient_ids(limit=2)

        r = api.create_order(ingredients, token=token)
        assert r.status_code == ApiData.HTTP_OK

        body = r.json()
        assert body.get(ApiData.KEY_SUCCESS) is True
        assert ApiData.KEY_ORDER in body

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, api):
        ingredients = api.get_any_ingredient_ids(limit=2)
        r = api.create_order(ingredients)
        assert r.status_code == ApiData.HTTP_OK

        body = r.json()
        assert body.get(ApiData.KEY_SUCCESS) is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, api, registered_user):
        _, token = registered_user
        r = api.create_order([], token=token)
        assert r.status_code == ApiData.HTTP_BAD_REQUEST

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredients(self, api, registered_user):
        _, token = registered_user
        r = api.create_order(["invalid_hash"], token=token)
        assert r.status_code in (ApiData.HTTP_BAD_REQUEST, ApiData.HTTP_SERVER_ERROR)
