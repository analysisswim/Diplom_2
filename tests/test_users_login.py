import allure
from helpers.api_data import ApiData


@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, api, registered_user):
        user_data, _ = registered_user
        r = api.login(user_data["email"], user_data["password"])
        assert r.status_code == ApiData.HTTP_OK

        body = r.json()
        assert body.get(ApiData.KEY_SUCCESS) is True
        assert ApiData.KEY_ACCESS_TOKEN in body

    @allure.title("Логин с неверным логином и паролем")
    def test_login_wrong_credentials(self, api):
        r = api.login("wrong_email@mail.test", "wrong_password")
        assert r.status_code == ApiData.HTTP_UNAUTHORIZED

        body = r.json()
        assert body.get(ApiData.KEY_SUCCESS) is False
