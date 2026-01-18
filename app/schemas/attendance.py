from pydantic import BaseModel
from datetime import date

class AttendanceCreate(BaseModel):
    work_order_id: int
    worker_id: int
    date: date
    hours_worked: float
