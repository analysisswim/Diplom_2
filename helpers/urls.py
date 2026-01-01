import os


class Urls:
    """
    BASE_URL можно переопределять переменной окружения:
    STELLAR_BURGERS_BASE_URL="https://...."
    """
    BASE_URL = os.getenv("STELLAR_BURGERS_BASE_URL", "https://stellarburgers.education-services.ru")

    API_PREFIX = "/api"

    # Auth
    REGISTER = f"{BASE_URL}{API_PREFIX}/auth/register"
    LOGIN = f"{BASE_URL}{API_PREFIX}/auth/login"
    USER = f"{BASE_URL}{API_PREFIX}/auth/user"

    # Ingredients
    INGREDIENTS = f"{BASE_URL}{API_PREFIX}/ingredients"

    # Orders
    ORDERS = f"{BASE_URL}{API_PREFIX}/orders"
