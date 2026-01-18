import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime


def generate_invoice_pdf(context: dict, filename: str) -> str:
    """
    Generates a PDF invoice using ReportLab.
    Returns the absolute path of the generated PDF.
    """

    # Output directory
    output_dir = "app/uploads/invoices"
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, filename)

    # Create PDF
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 50

    company = context["company"]
    invoice = context["invoice"]
    client_name = context.get("client_name", "Client")
    site_name = context.get("site_name", "Site")

    # ---------- HEADER ----------
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, company.name if company else "Company")
    y -= 25

    c.setFont("Helvetica", 10)
    if company and company.address:
        c.drawString(50, y, company.address)
        y -= 15

    c.drawString(50, y, f"Invoice Date: {datetime.utcnow().strftime('%d %b %Y')}")
    y -= 30

    # ---------- INVOICE META ----------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Invoice Number: {invoice.invoice_number}")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Billed To: {client_name}")
    y -= 15

    c.drawString(50, y, f"Site: {site_name}")
    y -= 30

    # ---------- LINE ----------
    c.line(50, y, width - 50, y)
    y -= 30

    # ---------- AMOUNT ----------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Total Amount")
    c.drawRightString(width - 50, y, f"₹ {invoice.total_amount:.2f}")
    y -= 40

    # ---------- FOOTER ----------
    c.setFont("Helvetica", 9)
    c.drawString(50, y, "Thank you for your business.")
    y -= 15
    c.drawString(50, y, "This is a system-generated invoice.")

    # Finalize
    c.showPage()
    c.save()

    return file_path
