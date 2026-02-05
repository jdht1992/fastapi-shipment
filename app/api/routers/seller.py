from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database.models import Seller
from app.database.redis import add_jti_to_blacklist
from app.dependencies import SellerServiceDep, get_access_token
from app.schemas.seller import SellerCreate, Token

router_seller = APIRouter(prefix="/seller", tags=["Seller"])


@router_seller.post("/signup", response_model=Seller)
async def register_seller(seller: SellerCreate, service: SellerServiceDep) -> Seller:
    new_seller = await service.add(seller)

    return new_seller


@router_seller.post("/token")
async def login_for_access_token(
    service: SellerServiceDep,
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    token = await service.token(request_form.username, request_form.password)

    return Token(access_token=token, token_type="JWT")


@router_seller.get("/logout")
async def logout_seller(token_data: Annotated[dict, Depends(get_access_token)]):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out"}
