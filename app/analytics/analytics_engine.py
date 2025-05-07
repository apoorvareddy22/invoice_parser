import pandas as pd

def clean_invoice_data(df):
    """
    Extract key fields from nested invoice JSON and normalize into a flat DataFrame.
    """

    cleaned_rows = []

    for _, row in df.iterrows():
        parsed = row.get("parsed", {})
        ground = row.get("ground_truth", {})

        invoice_number = parsed.get("Invoice Number") or ground.get("invoice", {}).get("number")
        invoice_date = parsed.get("Invoice Date") or ground.get("invoice", {}).get("date")
        vendor_name = parsed.get("Vendor Name") or ground.get("seller", {}).get("name")
        total_amount = parsed.get("Total Amount") or ground.get("payment", {}).get("total")

        cleaned_rows.append({
            "invoice_number": invoice_number,
            "invoice_date": invoice_date,
            "vendor_name": vendor_name,
            "total_amount": total_amount,
        })

    clean_df = pd.DataFrame(cleaned_rows)

    # Handle types
    clean_df["invoice_date"] = pd.to_datetime(clean_df["invoice_date"], errors="coerce")
    clean_df["total_amount_clean"] = pd.to_numeric(
        clean_df["total_amount"]
        .astype(str)
        .str.replace(r"[^\d\.]", "", regex=True),
        errors="coerce"
    )

    return clean_df


def total_spend(df: pd.DataFrame) -> float:
    return df["total_amount_clean"].sum()


def monthly_spend(df: pd.DataFrame) -> pd.Series:
    return df.groupby(df["invoice_date"].dt.to_period("M"))["total_amount_clean"].sum()


def top_vendors(df: pd.DataFrame, n=5) -> pd.Series:
    return df.groupby("vendor_name")["total_amount_clean"].sum().nlargest(n)


def average_payment_duration(df: pd.DataFrame) -> float:
    durations = (df["due_date"] - df["invoice_date"]).dt.days
    return durations.mean()


def missing_field_stats(df: pd.DataFrame) -> pd.Series:
    return df.isna().sum().sort_values(ascending=False)
