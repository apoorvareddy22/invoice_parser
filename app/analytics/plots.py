import matplotlib.pyplot as plt
import pandas as pd

def plot_monthly_spend(monthly_series: pd.Series):
    monthly_series = monthly_series.sort_index()
    monthly_series.index = monthly_series.index.astype(str)

    plt.figure(figsize=(10, 5))
    monthly_series.plot(kind="bar")
    plt.title("Monthly Spend")
    plt.xlabel("Month")
    plt.ylabel("Total Amount ($)")
    plt.tight_layout()
    plt.show()


def plot_top_vendors(vendor_series: pd.Series):
    vendor_series = vendor_series.sort_values(ascending=True)

    plt.figure(figsize=(8, 5))
    vendor_series.plot(kind="barh", color="skyblue")
    plt.title("Top Vendors by Spend")
    plt.xlabel("Total Amount ($)")
    plt.tight_layout()
    plt.show()


def plot_missing_fields(missing_series: pd.Series):
    missing_series = missing_series[missing_series > 0].sort_values()

    plt.figure(figsize=(8, 4))
    missing_series.plot(kind="barh", color="salmon")
    plt.title("Missing Field Counts")
    plt.xlabel("Count")
    plt.tight_layout()
    plt.show()
