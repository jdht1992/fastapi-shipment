from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from app.database.models import Shipment
from app.dependencies import SellerDep, ShipmentServiceDep
from app.schemas.shipment import ShipmentCreate, ShipmentUpdate

router_shipment = APIRouter(prefix="/shipment", tags=["Shipment"])


@router_shipment.get("/{uuid}")
async def get_shipment(
    uuid: UUID, _: SellerDep, service: ShipmentServiceDep
) -> Shipment:
    shipment = await service.get_shipment(uuid)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Given id: {uuid} doesn't exist",
        )

    return shipment
    # return shipment.dict()
    # return Shipment(**shipment.model_dump())


@router_shipment.post("/", response_model=None)
async def create_shipment(
    seller: SellerDep, shipment: ShipmentCreate, service: ShipmentServiceDep
) -> Shipment:

    return await service.add_shipment(shipment, seller)


@router_shipment.patch("/shipment/{id}", response_model=Shipment)
async def update_shipment(
    id: int, shipment_update: ShipmentUpdate, service: ShipmentServiceDep
) -> Shipment:

    return await service.update_shipment(id, shipment_update)


@router_shipment.delete("/shipment/{id}", response_model=None)
async def delete_shipment(id: int, service: ShipmentServiceDep) -> dict[str, str]:

    return await service.delete_shipment(id)
