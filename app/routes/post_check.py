from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.post_check import PostCheck
from app.models.work_order import WorkOrder
from app.schemas.post_check import PostCheckCreate
from app.core.dependencies import require_manager

router = APIRouter(prefix="/post-checks", tags=["Post Checks"])

@router.post("/")
def create_post_check(
    data: PostCheckCreate,
    user=Depends(require_manager),
    db: Session = Depends(get_db)
):
    work_order = db.query(WorkOrder).filter(
        WorkOrder.id == data.work_order_id,
        WorkOrder.company_id == user["company_id"]
    ).first()

    if not work_order:
        raise HTTPException(status_code=404, detail="Work Order not found")

    post_check = PostCheck(**data.dict())
    work_order.status = "COMPLETED"

    db.add(post_check)
    db.commit()

    return {"message": "Post-check completed"}
