import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.invoice import Invoice
from app.models.work_order import WorkOrder
from app.models.purchase_order import PurchaseOrder
from app.models.company import Company
from app.services.invoice_service import calculate_invoice_amount
from app.services.pdf_service import generate_invoice_pdf
from app.core.dependencies import require_admin

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.post("/generate/{work_order_id}")

def generate_invoice(
    work_order_id: int,
    user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    work_order = db.query(WorkOrder).filter(
        WorkOrder.id == work_order_id,
        WorkOrder.company_id == user["company_id"],
        WorkOrder.status == "COMPLETED"
    ).first()

    if not work_order:
        raise HTTPException(status_code=400, detail="Work Order not completed")

    company = db.query(Company).filter(
        Company.id == work_order.company_id
    ).first()

    if not company:
        raise HTTPException(status_code=400, detail="Company not found")

    amount = calculate_invoice_amount(work_order_id, db)
    invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"

    invoice = Invoice(
        work_order_id=work_order_id,
        invoice_number=invoice_number,
        total_amount=amount,
        company_id=company.id
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    context = {
    "company": company,
    "invoice": invoice,
    "client_name": "Client",
    "site_name": work_order.site_name or "Site"
}


    pdf_filename = f"{invoice.invoice_number}.pdf"
    pdf_path = generate_invoice_pdf(context, pdf_filename)

    invoice.pdf_path = pdf_path
    db.commit()

    return {
        "message": "Invoice generated successfully",
        "invoice_number": invoice.invoice_number,
        "amount": invoice.total_amount,
        "pdf_path": pdf_path
    }