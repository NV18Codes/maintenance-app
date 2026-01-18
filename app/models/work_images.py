from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class WorkImage(Base):
    __tablename__ = "work_images"

    id = Column(Integer, primary_key=True, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id"), nullable=False)
    image_path = Column(String, nullable=False)
    stage = Column(String, nullable=False)  # pre | during | post
