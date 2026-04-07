from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.database.redis import add_jti_to_blacklist
from app.dependencies import DeliveryPartnerDep, DeliveryPartnerServiceDep, get_partner_access_token
from app.schemas.delivery_partner import DeliveryPartnerCreate, DeliveryPartnerRead, DeliveryPartnerUpdate
from app.schemas.seller import Token

router_partner = APIRouter(prefix="/partner", tags=["Delivery Partner"])


@router_partner.post("/signup", response_model=DeliveryPartnerRead)
async def register_delivery_partner(
    delivery_partner: DeliveryPartnerCreate, 
    service: DeliveryPartnerServiceDep
):
    return await service.add(delivery_partner)


@router_partner.post("/token")
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: DeliveryPartnerServiceDep,
) -> Token:
    token = await service.token(request_form.username, request_form.password)

    return Token(access_token=token, token_type="jwt")


@router_partner.put("/", response_model=DeliveryPartnerRead)
async def update_delivery_partner(
    id: UUID,
    partner_update: DeliveryPartnerUpdate,
    partner: DeliveryPartnerDep,
    service: DeliveryPartnerServiceDep,
):
    update = partner_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update"
        )

    return await service.update(
        partner.sqlmodel_update(partner_update)
    )

    # return await service.update(id, shipment_update)


@router_partner.get("/logout")
async def logout_delivery_partner(token_data: Annotated[dict, Depends(get_partner_access_token)]):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out"}
