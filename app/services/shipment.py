from datetime import datetime, timedelta
from uuid import UUID
from fastapi import HTTPException, status

from app.database.models import Seller, Shipment, ShipmentStatus
from app.schemas.shipment import ShipmentCreate, ShipmentUpdate
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import BaseService
from app.services.delivery_partner import DeliveryPartnerService


class ShipmentService(BaseService):
    def __init__(
        self, 
        session: AsyncSession, 
        partner_service: DeliveryPartnerService
    ):
        super().__init__(Shipment, session)
        self.partner_service = partner_service

    async def get(self, id: UUID) -> Shipment | None:
        return await self._get(id)

    async def add(
        self, shipment_create: ShipmentCreate, seller: Seller
    ) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=seller.id,
            # seller=seller
        )
        partner = await self.partner_service.assign_shipment(new_shipment)
        new_shipment.delivery_partner_id = partner.id
        return await self._add(new_shipment)

    async def update(
        self, id: UUID, shipment_update: ShipmentUpdate
    ) -> Shipment:

        if not (update_data := shipment_update.model_dump(exclude_none=True)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="None data provided for update",
            )

        if (shipment := await self._get(id)) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Given id doesn't exist",
            )

        shipment.sqlmodel_update(update_data)

        return await self._update(shipment)

    async def delete(self, id: UUID) -> dict[str, str]:

        if (shipment := await self._get(id)) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Given id doesn't exist",
            )

        await self._delete(shipment)

        return {"detail": f"Shipment with id: {id} was deleted successfully"}
