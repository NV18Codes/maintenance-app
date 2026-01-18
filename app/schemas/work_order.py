from pydantic import BaseModel
from typing import Optional
from datetime import date

class WorkOrderCreate(BaseModel):
    po_id: int
    site_name: str
    priority: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
