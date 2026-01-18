from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.pre_check import PreCheck
from app.models.work_order import WorkOrder
from app.schemas.pre_check import PreCheckCreate
from app.core.dependencies import require_manager

router = APIRouter(prefix="/pre-checks", tags=["Pre Checks"])

@router.post("/")
def create_pre_check(
    data: PreCheckCreate,
    user=Depends(require_manager),
    db: Session = Depends(get_db)
):
    work_order = db.query(WorkOrder).filter(
        WorkOrder.id == data.work_order_id,
        WorkOrder.company_id == user["company_id"]
    ).first()

    if not work_order:
        raise HTTPException(status_code=404, detail="Work Order not found")

    pre_check = PreCheck(**data.dict())
    db.add(pre_check)
    db.commit()

    return {"message": "Pre-check completed"}
