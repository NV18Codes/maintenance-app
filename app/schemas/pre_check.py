from pydantic import BaseModel
from typing import Optional

class PreCheckCreate(BaseModel):
    work_order_id: int
    tools_ok: bool
    ppe_ok: bool
    site_safe: bool
    remarks: Optional[str] = None
