# NOTE: utils means the helper functions, that's why it's name is utils


import bcrypt

def get_hashed_password(plain_password: str) -> str:
    password = bcrypt.hashpw(plain_password.encode("utf-8"),bcrypt.gensalt())
    return password.decode("utf-8")

def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )