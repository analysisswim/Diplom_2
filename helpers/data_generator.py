import uuid
import random
import string


def generate_user():
    uid = uuid.uuid4().hex[:10]
    password = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    return {
        "email": f"auto_{uid}@mail.test",
        "password": password,
        "name": f"User_{uid}"
    }
