from pydantic import BaseModel

class AssignManagerRequest(BaseModel):
    work_order_id: int
    manager_id: int
