# app/services/extraction_logic.py

FIELDS = [
    "Invoice Number",
    "Invoice Date",
    "Vendor Name",
    "Billing Address",
    "Shipping Address",
    "Total Amount",
    "Tax Amount",
    "Due Date"
]

def generate_question(field: str) -> str:
    overrides = {
        "Tax Amount": "What is the total tax amount?",
        "Vendor Name": "Who is the vendor or supplier?",
        "Billing Address": "What is the billing address?",
        "Shipping Address": "What is the shipping address?",
        "Due Date": "When is the payment due?",
    }
    return overrides.get(field, f"What is the {field}?")

    #return field_to_question.get(field_name, f"What is the {field_name.lower()}?")
