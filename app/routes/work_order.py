from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.work_order import WorkOrder
from app.models.purchase_order import PurchaseOrder
from app.schemas.work_order import WorkOrderCreate
from app.core.dependencies import require_admin

router = APIRouter(prefix="/work-orders", tags=["Work Orders"])

@router.post("/")
def create_work_order(
    data: WorkOrderCreate,
    user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    # Ensure PO exists and belongs to same company
    po = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == data.po_id,
        PurchaseOrder.company_id == user["company_id"]
    ).first()

    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")

    work_order = WorkOrder(
        po_id=data.po_id,
        site_name=data.site_name,
        priority=data.priority,
        start_date=data.start_date,
        end_date=data.end_date,
        company_id=user["company_id"]
    )

    db.add(work_order)
    db.commit()
    db.refresh(work_order)

    return {
        "message": "Work Order created",
        "work_order_id": work_order.id
    }
