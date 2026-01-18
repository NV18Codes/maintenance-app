from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String, unique=True, nullable=False)
    client_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
