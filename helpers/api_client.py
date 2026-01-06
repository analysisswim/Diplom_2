import allure
import requests
from requests.models import Response

from helpers.urls import Urls
from helpers.api_data import ApiData


class StellarBurgersAPI:
    def __init__(self):
        self.urls = Urls()
        self.session = requests.Session()

    @staticmethod
    def _extract_bearer(access_token: str):
        # обычно приходит строка вида "Bearer <token>"
        if not access_token:
            return None
        return access_token.replace("Bearer ", "").strip()

    def _request(self, method: str, url: str, **kwargs) -> Response:
        try:
            kwargs.setdefault("timeout", 15)
            return self.session.request(method, url, **kwargs)
        except requests.RequestException as e:
            r = Response()
            r.status_code = ApiData.NETWORK_ERROR
            r._content = str.encode(f"Network error: {e}")
            return r

    @allure.step("Регистрация пользователя")
    def register(self, email: str, password: str, name: str) -> Response:
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        return self._request("POST", self.urls.REGISTER, json=payload)

    @allure.step("Логин пользователя")
    def login(self, email: str, password: str) -> Response:
        payload = {"email": email, "password": password}
        return self._request("POST", self.urls.LOGIN, json=payload)

    @allure.step("Удаление пользователя")
    def delete_user(self, token: str) -> Response:
        headers = {"Authorization": f"Bearer {token}"}
        return self._request("DELETE", self.urls.USER, headers=headers)

    @allure.step("Получить ингредиенты")
    def get_ingredients(self) -> Response:
        return self._request("GET", self.urls.INGREDIENTS)

    @allure.step("Создать заказ")
    def create_order(self, ingredients: list, token: str = None) -> Response:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        payload = {"ingredients": ingredients}
        return self._request("POST", self.urls.ORDERS, json=payload, headers=headers)

    def get_any_ingredient_ids(self, limit: int = 2):
        r = self.get_ingredients()
        if r.status_code != ApiData.HTTP_OK:
            return []

        data = r.json().get(ApiData.KEY_DATA, [])
        return [item.get(ApiData.KEY_ID) for item in data[:limit] if item.get(ApiData.KEY_ID)]
