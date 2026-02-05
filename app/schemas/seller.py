from pydantic import BaseModel, EmailStr


class BaseSeller(BaseModel):
    name: str
    email: EmailStr


class SellerRead(BaseSeller):
    pass


class SellerCreate(BaseSeller):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
