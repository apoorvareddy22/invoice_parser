import json
import pandas as pd
from app.analytics.analytics_engine import clean_invoice_data
import matplotlib.pyplot as plt

# Load output.json as a dict
with open("data/output.json", "r") as f:
    invoice_dict = json.load(f)

# Convert to DataFrame where each row is an invoice with filename and fields
records = []
for filename, invoice in invoice_dict.items():
    parsed = invoice.get("parsed", {})
    record = {
        "filename": filename,
        "invoice_number": parsed.get("Invoice Number"),
        "invoice_date": parsed.get("Invoice Date"),
        "vendor_name": parsed.get("Vendor Name"),
        "total_amount": parsed.get("Total Amount")
    }
    records.append(record)

df = pd.DataFrame(records)
df = clean_invoice_data(df)

# Visualize invoice counts per year
if not df["invoice_date"].isna().all():
    invoices_per_year = df["invoice_date"].dt.year.value_counts().sort_index()
    invoices_per_year.plot(kind="bar", title="Number of Invoices per Year")
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()
else:
    print("❗ No valid invoice_date values found for plotting.")
