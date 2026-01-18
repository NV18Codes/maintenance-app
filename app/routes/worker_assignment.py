from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.worker_assignment import WorkerAssignment
from app.models.work_order import WorkOrder
from app.models.user import User
from app.schemas.worker_assignment import AssignWorkersRequest
from app.core.dependencies import require_manager

router = APIRouter(prefix="/worker-assignments", tags=["Worker Assignments"])

@router.post("/assign")
def assign_workers(
    data: AssignWorkersRequest,
    user=Depends(require_manager),
    db: Session = Depends(get_db)
):
    work_order = db.query(WorkOrder).filter(
        WorkOrder.id == data.work_order_id,
        WorkOrder.company_id == user["company_id"]
    ).first()

    if not work_order:
        raise HTTPException(status_code=404, detail="Work Order not found")

    for worker_id in data.worker_ids:
        worker = db.query(User).filter(
            User.id == worker_id,
            User.role == "worker",
            User.company_id == user["company_id"]
        ).first()

        if not worker:
            raise HTTPException(
                status_code=404,
                detail=f"Worker {worker_id} not found"
            )

        assignment = WorkerAssignment(
            work_order_id=data.work_order_id,
            worker_id=worker_id
        )
        db.add(assignment)

    work_order.status = "IN_PROGRESS"
    db.commit()

    return {"message": "Workers assigned successfully"}
