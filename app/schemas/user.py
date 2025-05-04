from .base import SchemaBase


class UserCreate(SchemaBase):
    username: str
    email: str
    password: str

class Token(SchemaBase):
    access_token: str
    token_type: str
