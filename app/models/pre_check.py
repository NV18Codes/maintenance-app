from sqlalchemy import Column, Integer, Boolean, Text, ForeignKey
from app.database import Base

class PreCheck(Base):
    __tablename__ = "pre_checks"

    id = Column(Integer, primary_key=True, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id"), nullable=False)

    tools_ok = Column(Boolean, default=False)
    ppe_ok = Column(Boolean, default=False)
    site_safe = Column(Boolean, default=False)

    remarks = Column(Text, nullable=True)
