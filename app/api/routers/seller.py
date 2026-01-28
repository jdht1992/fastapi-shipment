from fastapi import APIRouter
from app.dependencies import SellerServiceDep
from app.schemas.seller import SellerCreate, SellerRead

router_seller = APIRouter(prefix="/seller", tags=["Seller"])


@router_seller.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    await service.add(seller)
