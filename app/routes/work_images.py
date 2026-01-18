import os
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.work_images import WorkImage
from app.core.dependencies import require_manager

router = APIRouter(prefix="/work-images", tags=["Work Images"])

UPLOAD_DIR = "app/uploads/work_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/{work_order_id}/{stage}")
def upload_images(
    work_order_id: int,
    stage: str,  # pre | during | post
    files: list[UploadFile] = File(...),
    user=Depends(require_manager),
    db: Session = Depends(get_db)
):
    for file in files:
        filename = f"{work_order_id}_{stage}_{file.filename}"
        path = os.path.join(UPLOAD_DIR, filename)

        with open(path, "wb") as f:
            f.write(file.file.read())

        image = WorkImage(
            work_order_id=work_order_id,
            image_path=path,
            stage=stage
        )
        db.add(image)

    db.commit()
    return {"message": "Images uploaded successfully"}
