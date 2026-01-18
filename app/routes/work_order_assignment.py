from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.work_order_assignment import WorkOrderAssignment
from app.models.work_order import WorkOrder
from app.models.user import User
from app.schemas.work_order_assignment import AssignManagerRequest
from app.core.dependencies import require_admin

router = APIRouter(prefix="/work-order-assignments", tags=["Work Order Assignments"])

@router.post("/assign-manager")
def assign_manager(
    data: AssignManagerRequest,
    user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    work_order = db.query(WorkOrder).filter(
        WorkOrder.id == data.work_order_id,
        WorkOrder.company_id == user["company_id"]
    ).first()

    if not work_order:
        raise HTTPException(status_code=404, detail="Work Order not found")

    manager = db.query(User).filter(
        User.id == data.manager_id,
        User.role == "manager",
        User.company_id == user["company_id"]
    ).first()

    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")

    assignment = WorkOrderAssignment(
        work_order_id=data.work_order_id,
        manager_id=data.manager_id
    )

    work_order.status = "ASSIGNED"

    db.add(assignment)
    db.commit()

    return {"message": "Manager assigned to Work Order"}
