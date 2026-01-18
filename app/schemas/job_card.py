from pydantic import BaseModel

class JobCardCreate(BaseModel):
    work_order_id: int
    worker_id: int
    description: str
