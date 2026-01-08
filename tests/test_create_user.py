import allure
import pytest

from helpers.api_client import StellarBurgersAPI
from helpers.api_data import ApiData


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создать уникального пользователя")
    def test_create_unique_user(self, user_data):
        api = StellarBurgersAPI()

        r = api.register(user_data["email"], user_data["password"], user_data["name"])
        assert r.status_code == ApiData.HTTP_OK

        body = r.json()
        assert body.get(ApiData.KEY_SUCCESS) is True
        assert ApiData.KEY_ACCESS_TOKEN in body

        token = api._extract_bearer(body.get(ApiData.KEY_ACCESS_TOKEN))
        api.delete_user(token)

    @allure.title("Создать пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, registered_user):
        api = StellarBurgersAPI()

        user_data, _ = registered_user
        r = api.register(user_data["email"], user_data["password"], user_data["name"])
        assert r.status_code == ApiData.HTTP_FORBIDDEN

        body = r.json()
        assert body.get(ApiData.KEY_SUCCESS) is False

    @allure.title("Создать пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field(self, user_data, missing_field):
        api = StellarBurgersAPI()

        payload = dict(user_data)
        payload[missing_field] = ""

        r = api.register(payload["email"], payload["password"], payload["name"])
        assert r.status_code == ApiData.HTTP_FORBIDDEN

        body = r.json()
        assert body.get(ApiData.KEY_SUCCESS) is False
