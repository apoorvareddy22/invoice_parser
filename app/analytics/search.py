import pandas as pd

def filter_by_vendor(df: pd.DataFrame, vendor_name: str) -> pd.DataFrame:
    """Filter invoices by vendor name (case-insensitive match)."""
    return df[df["vendor_name"].str.contains(vendor_name, case=False, na=False)]

def filter_by_amount_range(df: pd.DataFrame, min_amount: float, max_amount: float) -> pd.DataFrame:
    """Filter invoices within a total amount range."""
    return df[
        (df["total_amount_clean"] >= min_amount) &
        (df["total_amount_clean"] <= max_amount)
    ]

def filter_by_date_range(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    """Filter invoices between two dates (inclusive). Dates should be YYYY-MM-DD."""
    return df[
        (df["invoice_date"] >= pd.to_datetime(start_date)) &
        (df["invoice_date"] <= pd.to_datetime(end_date))
    ]

def search_invoice_number(df: pd.DataFrame, invoice_number: str) -> pd.DataFrame:
    """Search for an exact invoice number."""
    return df[df["invoice_number"] == invoice_number]
