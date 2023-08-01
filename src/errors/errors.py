from enum import Enum


class ErrorModel:
    def __init__(self, message, code):
        self.message = message
        self.code = code


class Errors(Enum):
    USER_NOT_FOUND_1002 = ErrorModel(message='USER_NOT_FOUND', code=1001)
    USER_DUPLICATE_LOGIN_1002 = ErrorModel(
        message='USER_DUPLICATE_LOGIN', code=1002)

    AUTH_MALFORMED_CREDENTIALS_2001 = ErrorModel(
        message='AUTH_MALFORMED_CREDENTIALS', code=2001)
    AUTH_INVALID_TOKEN_2002 = ErrorModel(
        message='AUTH_INVALID_TOKEN', code=2002)
    AUTH_FORBIDDEN_2003 = ErrorModel(
        message='AUTH_FORBIDDEN', code=2003)

    DUPLICATE_PROPERTIES_NAME_3001 = ErrorModel(
        message="DUPLICATE_PROPERTIES_NAME", code=3001)

# 725d3cd5-61c9-447f-b335-c132660fe1cd 777
# c20b562d-89c5-419d-9694-667e3c301c97 66
# 04429caa-ae61-464b-92a2-4f509aa243d6 admin
# 30fbdf7b-ee46-4ac1-b6e3-4d717a1e0a15 moderator
# 291a2437-78ab-4ab2-8980-14f3d898c868 one
# f259c64c-b8d8-447e-b702-2ed76d70a8db user