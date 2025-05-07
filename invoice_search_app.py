import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os
import json
import re
from collections import Counter

# ----- Load and preprocess data -----
with open("data/output.json") as f:
    raw_data = json.load(f)

records = []
for file, entry in raw_data.items():
    parsed = entry.get("parsed", {})
    record = {
        "filename": file,
        "invoice_number": parsed.get("Invoice Number"),
        "invoice_date": parsed.get("Invoice Date"),
        "vendor_name": parsed.get("Vendor Name"),
        "total_amount": parsed.get("Total Amount"),
        "due_date": parsed.get("Due Date")
    }
    records.append(record)

df = pd.DataFrame(records)
df.columns = [col.lower().replace(" ", "_") for col in df.columns]

def extract_float(text):
    if not isinstance(text, str):
        return None
    matches = re.findall(r"\d+\.\d+|\d+", text)
    return float(matches[-1]) if matches else None

df["total_amount_clean"] = df["total_amount"].apply(extract_float)
df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
df["year_month"] = df["invoice_date"].dt.to_period("M")
df = df.dropna(subset=["invoice_date"])

# ----- Streamlit App -----
st.set_page_config("Invoice Explorer", layout="wide")

# 🌟 Creative Introduction
st.title("🧾 Invoice Search & Insights")
st.markdown("""
Welcome to your intelligent invoice dashboard!  
Track financial flows, explore vendor activity, and dive deep into the data extracted from scanned invoices.  
Use filters, search by keywords, and uncover hidden trends with interactive charts.
""")

# 🔍 Search & Filter
with st.sidebar:
    st.header("🔍 Filter Options")
    vendor = st.selectbox("Filter by vendor", ["All"] + sorted(df["vendor_name"].dropna().unique().tolist()))
    min_date, max_date = df["invoice_date"].min(), df["invoice_date"].max()
    date_range = st.date_input("Invoice date range", [min_date, max_date])
    search_query = st.text_input("Search keyword (vendor, invoice number, etc.)")

# Apply filters
filtered_df = df.copy()
if vendor != "All":
    filtered_df = filtered_df[filtered_df["vendor_name"] == vendor]
filtered_df = filtered_df[
    (filtered_df["invoice_date"] >= pd.to_datetime(date_range[0])) &
    (filtered_df["invoice_date"] <= pd.to_datetime(date_range[1]))
]
if search_query:
    query_lower = search_query.lower()
    filtered_df = filtered_df[
        filtered_df["vendor_name"].fillna("").str.lower().str.contains(query_lower)
        | filtered_df["invoice_number"].fillna("").astype(str).str.lower().str.contains(query_lower)
        | filtered_df["filename"].str.lower().str.contains(query_lower)
    ]

# 📊 Summary Stats
st.subheader("📈 Quick Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Number of Invoices", len(filtered_df))
col2.metric("Total Amount", f"${filtered_df['total_amount_clean'].sum():,.2f}")
col3.metric("Vendors", filtered_df["vendor_name"].nunique())

# 📈 Visualizations (2x2 Layout)
st.subheader("📊 Visual Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📅 Invoice Volume Over Time")
    volumes = filtered_df["year_month"].value_counts().sort_index()
    st.line_chart(volumes)

with col2:
    st.markdown("#### 🏢 Top Vendors by Total Amount")
    top_vendors = (
        df.groupby("vendor_name")["total_amount_clean"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(top_vendors)

col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 💸 Invoice Amount Distribution")
    threshold = st.slider("Max invoice amount (for histogram)", 0, int(df["total_amount_clean"].max()), 1000, step=100)
    subset = filtered_df[filtered_df["total_amount_clean"] < threshold]
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.hist(subset["total_amount_clean"], bins=30, color='skyblue', edgecolor='black')
    ax.set_xlabel("Invoice Amount")
    ax.set_ylabel("Count")
    st.pyplot(fig)

with col4:
    st.markdown("#### 🔠 Top Product Description Terms")
    all_terms = []
    for v in raw_data.values():
        for item in v.get("ground_truth", {}).get("products", []):
            desc = item.get("description", "")
            words = re.findall(r"\w+", desc.lower())
            all_terms.extend(words)

    if all_terms:
        top_terms = Counter(all_terms).most_common(10)
        term_df = pd.DataFrame(top_terms, columns=["term", "count"]).set_index("term")
        st.bar_chart(term_df)
    else:
        st.info("No product descriptions found.")

# 🖼️ Image Preview
st.subheader("🖼️ Preview Invoices")

if not filtered_df.empty:
    selected_file = st.selectbox("Select invoice file", filtered_df["filename"].tolist())
    img_path = os.path.join("data/images", selected_file)

    if os.path.exists(img_path):
        col_img, _ = st.columns([1, 3])  # small column for image
        with col_img:
            st.image(Image.open(img_path), caption=selected_file, width=800)
    else:
        st.warning("Invoice image not found.")
else:
    st.info("No invoices match the selected filters.")
