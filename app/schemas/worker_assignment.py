from pydantic import BaseModel
from typing import List

class AssignWorkersRequest(BaseModel):
    work_order_id: int
    worker_ids: List[int]
