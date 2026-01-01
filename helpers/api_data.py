class ApiData:
    # HTTP codes
    HTTP_OK = 200
    HTTP_CREATED = 201
    HTTP_BAD_REQUEST = 400
    HTTP_UNAUTHORIZED = 401
    HTTP_FORBIDDEN = 403
    HTTP_SERVER_ERROR = 500

    # Custom code for network errors (so tests don't crash)
    NETWORK_ERROR = 599

    # Response keys
    KEY_SUCCESS = "success"
    KEY_MESSAGE = "message"
    KEY_ACCESS_TOKEN = "accessToken"
    KEY_REFRESH_TOKEN = "refreshToken"
    KEY_USER = "user"
    KEY_DATA = "data"
    KEY_ORDER = "order"
    KEY_NUMBER = "number"
    KEY_NAME = "name"
    KEY_ID = "_id"
