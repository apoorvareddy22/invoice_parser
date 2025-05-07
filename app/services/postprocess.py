import re
from datetime import datetime, timedelta

def extract_first_number(text):
    match = re.search(r"\d[\d.,]*", text)
    return match.group(0) if match else text

def normalize_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%d.%m.%Y")
        return dt.strftime("%Y-%m-%d")
    except:
        return date_str

def clean_vendor(text):
    return text.split("\n")[0].strip()

def estimate_due_date(invoice_date_str):
    try:
        invoice_date = datetime.strptime(invoice_date_str, "%Y-%m-%d")
        return (invoice_date + timedelta(days=30)).strftime("%Y-%m-%d")
    except:
        return None

def clean_field(field_name, value):
    if not value:
        return None
    if field_name in ["Total Amount", "Tax Amount"]:
        return extract_first_number(value)
    elif field_name in ["Invoice Date", "Due Date"]:
        return normalize_date(value)
    elif field_name == "Vendor Name":
        return clean_vendor(value)
    return value
