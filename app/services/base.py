from typing import Type
from uuid import UUID
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    def __init__(self, model: Type[SQLModel], session: AsyncSession):
        self.model = model
        self.session = session

    async def _get(self, id: UUID):
        return await self.session.get(self.model, id)
    
    async def _add(self, entity: SQLModel):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
    
    async def _update(self, entity: SQLModel):
        return await self._add(entity)
    
    async def _delete(self, entity: SQLModel):
        return self.session.delete(entity)
