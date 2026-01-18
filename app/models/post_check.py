from sqlalchemy import Column, Integer, Boolean, Text, ForeignKey
from app.database import Base

class PostCheck(Base):
    __tablename__ = "post_checks"

    id = Column(Integer, primary_key=True, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id"), nullable=False)

    work_completed = Column(Boolean, default=False)
    quality_ok = Column(Boolean, default=False)

    remarks = Column(Text, nullable=True)
