from fastapi import FastAPI
from app.database import Base, engine

# IMPORTANT: import ALL models here
from app.models.company import Company
from app.models.user import User

from app.routes.company import router as company_router
from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from app.models.purchase_order import PurchaseOrder
from app.routes.purchase_order import router as po_router
from app.models.work_order import WorkOrder
from app.routes.work_order import router as wo_router
from app.models.work_order_assignment import WorkOrderAssignment
from app.routes.work_order_assignment import router as wo_assign_router
from app.models.worker_assignment import WorkerAssignment
from app.routes.worker_assignment import router as worker_assign_router
from app.models.attendance import Attendance
from app.routes.attendance import router as attendance_router
from app.models.job_card import JobCard
from app.routes.job_card import router as job_card_router
from app.models.pre_check import PreCheck
from app.routes.pre_check import router as pre_check_router
from app.models.post_check import PostCheck
from app.models.work_images import WorkImage
from app.routes.post_check import router as post_check_router
from app.routes.work_images import router as work_images_router
from app.models.invoice import Invoice
from app.routes.invoice import router as invoice_router

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app = FastAPI(title="Maintenance Management System")

# Create tables AFTER models are imported
Base.metadata.create_all(bind=engine)

app.include_router(company_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(po_router)
app.include_router(wo_router)
app.include_router(wo_assign_router)
app.include_router(worker_assign_router)
app.include_router(attendance_router)
app.include_router(job_card_router)
app.include_router(pre_check_router)
app.include_router(post_check_router)
app.include_router(work_images_router)
app.include_router(invoice_router)

@app.get("/")
def root():
    return {"status": "Backend running successfully"}
