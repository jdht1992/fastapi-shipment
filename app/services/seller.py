from app.database.models import Seller
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from sqlalchemy import select

from app.schemas.seller import SellerCreate

from fastapi import HTTPException, status

from app.utils import generate_access_token

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, seller_create: SellerCreate) -> Seller:
        new_seller = Seller(
            name=seller_create.name,
            email=seller_create.email,
            password_hash=password_context.hash(seller_create.password),
        )

        self.session.add(new_seller)
        await self.session.commit()
        await self.session.refresh(new_seller)

        return new_seller

    async def token(self, email, password) -> str:
        result = await self.session.execute(select(Seller).where(Seller.email == email))

        # seller = result.scalars().first()
        seller = result.scalar()

        if seller is None or not password_context.verify(
            password, seller.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"seller with email: {email} is not found",
            )

        token = generate_access_token(
            data={
                "user": {
                    "name": seller.name,
                    "email": seller.email,
                }
            }
        )

        return token
