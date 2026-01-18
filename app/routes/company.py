import os
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.company import Company
from app.core.dependencies import require_admin  # ✅ FIXED IMPORT

router = APIRouter(prefix="/companies", tags=["Companies"])

UPLOAD_DIR = "app/uploads/logos"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
def create_company(
    name: str = Form(...),
    address: str = Form(None),
    tax_number: str = Form(None),
    logo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    logo_path = None

    if logo:
        filename = f"{name.replace(' ', '_')}_{logo.filename}"
        logo_path = os.path.join(UPLOAD_DIR, filename)

        with open(logo_path, "wb") as f:
            f.write(logo.file.read())

    company = Company(
        name=name,
        address=address,
        tax_number=tax_number,
        logo=logo_path
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return {
        "message": "Company registered successfully",
        "company_id": company.id
    }


@router.get("/")
def list_companies(
    user=Depends(require_admin),   # ✅ RBAC enforced here
    db: Session = Depends(get_db)
):
    companies = db.query(Company).all()
    return companies
