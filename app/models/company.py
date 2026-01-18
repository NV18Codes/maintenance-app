from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel
from typing import Optional

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    logo = Column(String, nullable=True)
    address = Column(String, nullable=True)
    tax_number = Column(String, nullable=True)

class CompanyCreate(BaseModel):
    name: str
    address: Optional[str] = None
    tax_number: Optional[str] = None
