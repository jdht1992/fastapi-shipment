from datetime import datetime, timedelta
from uuid import UUID
from fastapi import HTTPException, status

from app.database.models import Seller, Shipment, ShipmentStatus
from app.schemas.shipment import ShipmentCreate, ShipmentUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_shipment(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=seller.id,
            #seller=seller
        )
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)

        return new_shipment

    async def get_shipment(self, shipment_id: UUID) -> Shipment | None:
        return await self.session.get(Shipment, shipment_id)

    async def update_shipment(
        self, shipment_id: int, shipment_update: ShipmentUpdate
    ) -> Shipment:
        update = shipment_update.model_dump(exclude_none=True)

        if not update:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="None data provided for update",
            )

        shipment = await self.session.get(Shipment, shipment_id)

        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Given id doesn't exist",
            )

        shipment.sqlmodel_update(update)

        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment

    async def delete_shipment(self, shipment_id: int) -> dict[str, str]:
        shipment = await self.session.get(Shipment, shipment_id)

        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Given id doesn't exist",
            )

        await self.session.delete(shipment)
        await self.session.commit()

        return {"detail": f"Shipment with id: {shipment_id} was deleted successfully"}
