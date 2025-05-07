from app.db.models import Invoice
from app.db.database import SessionLocal
from sqlalchemy.exc import IntegrityError

def insert_invoice(filename, data: dict):
    session = SessionLocal()

    invoice = Invoice(
        file_name=filename,
        invoice_number=data.get("Invoice Number"),
        invoice_date=data.get("Invoice Date"),
        total_amount=data.get("Total Amount"),
        vendor_name=data.get("Vendor Name"),
        billing_address=data.get("Billing Address"),
        shipping_address=data.get("Shipping Address"),
    )

    try:
        session.add(invoice)
        session.commit()
    except IntegrityError:
        session.rollback()
        print(f"⚠️ Invoice {filename} already exists, skipping.")
    finally:
        session.close()
