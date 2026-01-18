from sqlalchemy.orm import Session
from app.models.attendance import Attendance

HOURLY_RATE = 500  # configurable later

def calculate_invoice_amount(work_order_id: int, db: Session) -> float:
    records = db.query(Attendance).filter(
        Attendance.work_order_id == work_order_id
    ).all()

    total_hours = sum(r.hours_worked for r in records)
    return total_hours * HOURLY_RATE
