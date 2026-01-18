from pydantic import BaseModel

class PurchaseOrderCreate(BaseModel):
    po_number: str
    client_name: str
    amount: float
