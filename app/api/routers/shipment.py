from fastapi import APIRouter, HTTPException, status

from app.database.models import Shipment
from app.dependencies import ShipmentServiceDep
from app.schemas.shipment import ShipmentCreate, ShipmentUpdate

router_shipment = APIRouter(tags=["Shipment"])


@router_shipment.get("/shipment", response_model=Shipment)
async def get_shipment(id: int, service: ShipmentServiceDep) -> Shipment:
    shipment = await service.get_shipment(id)
    print("*20")

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Given id: {id} doesn't exist",
        )

    return shipment
    # return shipment.dict()
    # return Shipment(**shipment.model_dump())


@router_shipment.post("/shipment", response_model=None)
async def create_shipment(
    shipment_create: ShipmentCreate, service: ShipmentServiceDep
) -> Shipment:

    return await service.add_shipment(shipment_create)


@router_shipment.patch("/shipment/{id}", response_model=Shipment)
async def update_shipment(
    id: int, shipment_update: ShipmentUpdate, service: ShipmentServiceDep
) -> Shipment:

    return await service.update_shipment(id, shipment_update)


@router_shipment.delete("/shipment/{id}", response_model=None)
async def delete_shipment(
    id: int, service: ShipmentServiceDep
) -> dict[str, str]:

    return await service.delete_shipment(id)
