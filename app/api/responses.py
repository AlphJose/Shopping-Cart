# Responses
from fastapi import HTTPException, status


# Exceptions
def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return token_exception_response


def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return credentials_exception


def http_exception():
    return HTTPException(status_code=404, detail="Not found")


def user_exists_exception():
    return HTTPException(status_code=409, detail="User with the given username or email exists.")


def item_exists_exception():
    return HTTPException(status_code=409, detail="Item with the given item name exists.")


def admin_access_exception():
    return HTTPException(status_code=401, detail="Admin access is required to create an item.")
