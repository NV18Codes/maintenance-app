from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.job_card import JobCard
from app.models.work_order import WorkOrder
from app.models.user import User
from app.schemas.job_card import JobCardCreate
from app.core.dependencies import require_manager

router = APIRouter(prefix="/job-cards", tags=["Job Cards"])

@router.post("/")
def create_job_card(
    data: JobCardCreate,
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

    job_card = JobCard(**data.dict())
    db.add(job_card)
    db.commit()

    return {"message": "Job card created"}
