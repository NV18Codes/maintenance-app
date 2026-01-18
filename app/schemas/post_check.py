from pydantic import BaseModel
from typing import Optional

class PostCheckCreate(BaseModel):
    work_order_id: int
    work_completed: bool
    quality_ok: bool
    remarks: Optional[str] = None
