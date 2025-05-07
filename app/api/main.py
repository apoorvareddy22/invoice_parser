from fastapi import FastAPI, UploadFile, File, HTTPException
from app.services.preprocess import preprocess_image
from app.services.ocr_model import ask_question
from app.services.extraction_logic import FIELDS, generate_question
from app.db.crud import insert_invoice
from app.services.postprocess import clean_field, estimate_due_date
import io
from PIL import Image
from fastapi import Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Invoice
import os
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi import Request


app = FastAPI()

# Confidence thresholds per field
FIELD_THRESHOLDS = {
    "Invoice Number": 0.8,
    "Invoice Date": 0.7,
    "Total Amount": 0.7,
    "Tax Amount": 0.6,
    "Due Date": 0.5,
    "Vendor Name": 0.5,
    "Billing Address": 0.6,
    "Shipping Address": 0.6,
}

@app.post("/parse-invoice")
async def parse_invoice(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Only PNG/JPG images are supported.")

    try:
        contents = await file.read()
        image = preprocess_image(contents)

        extracted_data = {}
        for field in FIELDS:
            question = generate_question(field)
            answer = ask_question(image, question)

            if answer and answer[0]["score"] > FIELD_THRESHOLDS.get(field, 0.6):
                raw_value = answer[0]["answer"]
                extracted_data[field] = clean_field(field, raw_value)
            else:
                extracted_data[field] = None

        # Fallback: If Due Date is missing, estimate from Invoice Date
        if not extracted_data["Due Date"]:
            extracted_data["Due Date"] = estimate_due_date(extracted_data.get("Invoice Date"))

        insert_invoice(file.filename, extracted_data)

        return {"file": file.filename, "fields": extracted_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/invoices/search")
def search_invoices(
    request: Request,
    invoice_number: Optional[str] = Query(None),
    vendor_name: Optional[str] = Query(None),
    total_amount: Optional[str] = Query(None),
    invoice_date: Optional[str] = Query(None)
):
    session: Session = SessionLocal()
    try:
        query = session.query(Invoice)

        # Add filters dynamically based on query params
        if invoice_number:
            query = query.filter(Invoice.invoice_number == invoice_number)
        if vendor_name:
            query = query.filter(Invoice.vendor_name.ilike(f"%{vendor_name}%"))
        if total_amount:
            query = query.filter(Invoice.total_amount == total_amount)
        if invoice_date:
            query = query.filter(Invoice.invoice_date == invoice_date)

        results = query.all()
    finally:
        session.close()

    if not results:
        raise HTTPException(status_code=404, detail="No matching invoices found")

    # Return metadata about matches (not images yet)
    response = [
        {
            "id": invoice.id,
            "file_name": invoice.file_name,
            "invoice_number": invoice.invoice_number,
            "vendor_name": invoice.vendor_name,
            "total_amount": invoice.total_amount,
            "invoice_date": invoice.invoice_date,
            "created_at": invoice.created_at,
            "image_url": f"{request.base_url}invoices/image/{invoice.file_name}"
        }
        for invoice in results
    ]

    return JSONResponse(content=response)

@app.get("/invoices/image/{filename}")
def get_invoice_image(filename: str):
    image_path = os.path.join("data/images", filename)

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path, media_type="image/png", filename=filename)

