from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base

class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(Integer, primary_key=True, index=True)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)

    site_name = Column(String, nullable=False)
    priority = Column(String, nullable=False)  # Low | Medium | High | Emergency
    status = Column(String, default="CREATED")  # CREATED | ASSIGNED | IN_PROGRESS | COMPLETED

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    company_id = Column(Integer, ForeignKey("companies.id"))
