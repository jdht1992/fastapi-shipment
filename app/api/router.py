from fastapi import APIRouter

from app.api.routers import delivery_partner, seller, shipment

master_router = APIRouter()

master_router.include_router(shipment.router_shipment)
master_router.include_router(seller.router_seller)
master_router.include_router(delivery_partner.router_partner)
