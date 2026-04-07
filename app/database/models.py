from datetime import datetime
from enum import auto, StrEnum

from pydantic import EmailStr
from sqlalchemy import ARRAY, INTEGER
from sqlmodel import Field, DateTime, Relationship, func, SQLModel, Column

from uuid import UUID, uuid4

from sqlalchemy.dialects import postgresql


# class ShipmentStatus(str, Enum):
#     placed = "placed"
#     in_transit = "in_transit"
#     out_for_delivery = "out_for_delivery"
#     delivered = "delivered"

# class  Color(StrEnum): 
#     RED = "red"
#     GREEN = "green"
#     BLUE = "blue"

class ShipmentStatus(StrEnum):
    placed = auto() # Se convierte automáticamente en "placed"
    in_transit = auto()
    out_for_delivery = auto()
    delivered = auto()
 

class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    # id: int | None = Field(default=None, primary_key=True)
    id: UUID = Field(sa_column=Column(postgresql.UUID, default=uuid4, primary_key=True))
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), 
            server_default=func.now(), 
            nullable=False
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )
    )
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime

    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(
        back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"}
    )
    delivery_partner_id: UUID = Field(foreign_key="delivery_partner.id")
    delivery_partner: "DeliveryPartner" = Relationship(
        back_populates="shipments"
    )



class User(SQLModel):
    name: str
    email: EmailStr
    password_hash: str = Field(exclude=True)

class Seller(SQLModel, table=True):
    __tablename__="seller"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            # postgresql.UUID(as_uuid=True), Without as_uuid=True, PostgreSQL returns strings instead of UUID objects.
            default=uuid4,
            primary_key=True,
        )
    )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), 
            server_default=func.now(), 
            nullable=False
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )
    )
    name: str
    email: EmailStr
    # password: str
    password_hash: str

    shipments: list[Shipment] = Relationship(
        back_populates="seller", sa_relationship_kwargs={"lazy": "selectin"}
    )


class DeliveryPartner(User, table=True):
    __tablename__="delivery_partner"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            # postgresql.UUID(as_uuid=True),
            default=uuid4,
            primary_key=True,
        )
    )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), 
            server_default=func.now(),# This tells the database (PostgreSQL, SQLite, etc.) to use its own clock.
            nullable=False
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),#It prevents the nightmare of trying to figure out if a timestamp was UTC or local time
            server_default=func.now(),
            onupdate=func.now(), # SQLAlchemy magic: updates on every save
            nullable=False
        )
    )
    serviceable_zip_codes: list[int] = Field(
        sa_column=Column(ARRAY(INTEGER))
    )
    max_handling_capacity: int
    shipments: list[Shipment] = Relationship(
        back_populates="delivery_partner",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
   

    @property
    def active_shipments(self):
        return [
            shipment
            for shipment in self.shipments
            if shipment.status != ShipmentStatus.delivered
        ]
    
    @property
    def current_handling_capacity(self):
        return self.max_handling_capacity - len(self.active_shipments)
