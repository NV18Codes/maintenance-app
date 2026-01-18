from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id"), nullable=False)

    invoice_number = Column(String, unique=True, nullable=False)
    total_amount = Column(Float, nullable=False)
    pdf_path = Column(String, nullable=True)

    company_id = Column(Integer, ForeignKey("companies.id"))
