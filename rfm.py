import os
import pandas as pd

DATA_FILE = "online_retail_II.xlsx"
CACHE_FILE = "rfm.csv"


def segment_name(r, f):
    if f >= 4:
        if r >= 4:
            return "Champions"
        if r == 3:
            return "Loyal Customers"
        if r == 2:
            return "At Risk"
        return "Cant Lose Them"
    if f >= 2:
        if r >= 4:
            return "Potential Loyalists"
        if r == 3:
            return "Need Attention"
        if r == 2:
            return "About To Sleep"
        return "Hibernating"
    if r >= 4:
        return "New Customers"
    if r == 3:
        return "Promising"
    if r == 2:
        return "About To Sleep"
    return "Lost"


def build_rfm(path = DATA_FILE):
    df = pd.read_excel(path)
    df = df.dropna(subset = ["Customer ID"]).copy()
    df = df.drop_duplicates()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Revenue"] = df["Price"] * df["Quantity"]
    df["isCancelled"] = df["Invoice"].astype(str).str.startswith("C")

    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days = 1)
    recency = (snapshot_date - df.groupby("Customer ID")["InvoiceDate"].max()).dt.days

    df_valid = df[(~df["isCancelled"]) & (df["Price"] > 0)]
    frequency = df_valid.groupby("Customer ID")["Invoice"].nunique()
    monetary = df_valid.groupby("Customer ID")["Revenue"].sum()

    rfm = pd.concat([recency, frequency, monetary], axis = 1)
    rfm.columns = ["Recency", "Frequency", "Monetary"]
    rfm = rfm.dropna()
    rfm["Frequency"] = rfm["Frequency"].astype(int)

    rfm["R"] = pd.qcut(rfm["Recency"], 5, labels = [5, 4, 3, 2, 1]).astype(int)
    rfm["F"] = pd.qcut(rfm["Frequency"].rank(method = "first"), 5, labels = [1, 2, 3, 4, 5]).astype(int)
    rfm["M"] = pd.qcut(rfm["Monetary"], 5, labels = [1, 2, 3, 4, 5]).astype(int)
    rfm["Segment"] = [segment_name(r, f) for r, f in zip(rfm["R"], rfm["F"])]
    rfm = rfm.reset_index()
    rfm["Customer ID"] = rfm["Customer ID"].astype(int)
    return rfm


def load_rfm():
    if os.path.exists(CACHE_FILE):
        return pd.read_csv(CACHE_FILE)
    rfm = build_rfm()
    rfm.to_csv(CACHE_FILE, index = False)
    return rfm