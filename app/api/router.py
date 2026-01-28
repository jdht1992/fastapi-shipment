from fastapi import APIRouter

from app.api.routers import seller, shipment

master_router = APIRouter()

master_router.include_router(shipment.router_shipment)
master_router.include_router(seller.router_seller)
