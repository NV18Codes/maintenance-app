from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class WorkOrderAssignment(Base):
    __tablename__ = "work_order_assignments"

    id = Column(Integer, primary_key=True, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)
