from app.database.models import Seller
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.schemas.seller import SellerCreate

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, seller_create: SellerCreate) -> Seller:
        new_seller = Seller(
            **seller_create.model_dump(exclude={"password"}),
            password_hash=password_context.hash(seller_create.password)
        )

        self.session.add(new_seller)
        await self.session.commit()
        await self.session.refresh(new_seller)

        return new_seller
