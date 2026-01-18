from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.purchase_order import PurchaseOrder
from app.schemas.purchase_order import PurchaseOrderCreate
from app.core.dependencies import require_admin

router = APIRouter(prefix="/purchase-orders", tags=["Purchase Orders"])

@router.post("/")
def create_po(
    data: PurchaseOrderCreate,
    user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    po = PurchaseOrder(
        po_number=data.po_number,
        client_name=data.client_name,
        amount=data.amount,
        company_id=user["company_id"]
    )

    db.add(po)
    db.commit()
    db.refresh(po)

    return {
        "message": "Purchase Order created",
        "po_id": po.id
    }
