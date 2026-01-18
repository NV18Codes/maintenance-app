from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.attendance import Attendance
from app.models.work_order import WorkOrder
from app.models.user import User
from app.schemas.attendance import AttendanceCreate
from app.core.dependencies import require_manager

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/")
def mark_attendance(
    data: AttendanceCreate,
    user=Depends(require_manager),
    db: Session = Depends(get_db)
):
    work_order = db.query(WorkOrder).filter(
        WorkOrder.id == data.work_order_id,
        WorkOrder.company_id == user["company_id"]
    ).first()

    if not work_order:
        raise HTTPException(status_code=404, detail="Work Order not found")

    worker = db.query(User).filter(
        User.id == data.worker_id,
        User.role == "worker",
        User.company_id == user["company_id"]
    ).first()

    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    attendance = Attendance(**data.dict())
    db.add(attendance)
    db.commit()

    return {"message": "Attendance recorded"}
