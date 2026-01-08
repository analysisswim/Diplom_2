import os
import pytest

from helpers.api_client import StellarBurgersAPI
from helpers.api_data import ApiData
from helpers.data_generator import generate_user


@pytest.fixture(scope="session", autouse=True)
def check_api_available():
    """
    Если API совсем недоступен (DNS/сеть), тесты будут падать понятной ошибкой.
    Можно временно пропустить проверку так:
    export SKIP_API_CHECK=1
    """
    if os.getenv("SKIP_API_CHECK") == "1":
        return

    api = StellarBurgersAPI()
    r = api.get_ingredients()
    if r.status_code == ApiData.NETWORK_ERROR:
        pytest.fail(
            "API недоступен (DNS/сеть). "
            "Проверь, открывается ли /api/ingredients в браузере или задай "
            "STELLAR_BURGERS_BASE_URL из документации твоего потока."
        )


@pytest.fixture
def user_data():
    return generate_user()


@pytest.fixture
def registered_user(user_data):
    """
    Сложная логика предусловия/постусловия — норм для фикстуры:
    регистрируем пользователя и удаляем после теста.
    """
    api = StellarBurgersAPI()

    reg = api.register(user_data["email"], user_data["password"], user_data["name"])
    assert reg.status_code == ApiData.HTTP_OK, f"Register failed: {reg.status_code} {reg.text}"

    token = None
    try:
        token = reg.json().get(ApiData.KEY_ACCESS_TOKEN)
        token = api._extract_bearer(token)
    except Exception:
        token = None

    yield user_data, token

    if token:
        api.delete_user(token)
