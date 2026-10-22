from langchain_core.tools import tool
from rfm import load_rfm

rfm = load_rfm()


@tool
def overall_stats() -> str:
    """Total customers, total revenue, and average recency, frequency and monetary value across all customers."""
    return (
        f"Customers: {len(rfm)}\n"
        f"Total revenue: {rfm['Monetary'].sum():.2f}\n"
        f"Avg recency (days): {rfm['Recency'].mean():.1f}\n"
        f"Avg frequency (orders): {rfm['Frequency'].mean():.1f}\n"
        f"Avg monetary per customer: {rfm['Monetary'].mean():.2f}"
    )


@tool
def segment_summary() -> str:
    """Customer count, average recency, frequency, monetary value and total revenue for every RFM segment."""
    summary = rfm.groupby("Segment").agg(
        Customers = ("Customer ID", "count"),
        AvgRecency = ("Recency", "mean"),
        AvgFrequency = ("Frequency", "mean"),
        AvgMonetary = ("Monetary", "mean"),
        TotalRevenue = ("Monetary", "sum"),
    ).round(1).sort_values("TotalRevenue", ascending = False)
    return summary.to_string()


@tool
def segment_customers(segment: str, top_n: int = 5) -> str:
    """Top customers by monetary value inside one segment. Segment names: Champions, Loyal Customers, Potential Loyalists, New Customers, Promising, Need Attention, About To Sleep, At Risk, Cant Lose Them, Hibernating, Lost."""
    sub = rfm[rfm["Segment"].str.lower() == segment.strip().lower()]
    if sub.empty:
        return f"No segment named '{segment}'. Valid: {', '.join(sorted(rfm['Segment'].unique()))}"
    top = sub.sort_values("Monetary", ascending = False).head(int(top_n))
    return top[["Customer ID", "Recency", "Frequency", "Monetary"]].round(1).to_string(index = False)


@tool
def customer_lookup(customer_id: int) -> str:
    """RFM values, scores and segment for one customer ID."""
    row = rfm[rfm["Customer ID"] == int(customer_id)]
    if row.empty:
        return f"Customer {customer_id} not found."
    r = row.iloc[0]
    return (
        f"Customer {int(r['Customer ID'])}\n"
        f"Recency (days): {int(r['Recency'])}\n"
        f"Frequency (orders): {int(r['Frequency'])}\n"
        f"Monetary: {r['Monetary']:.2f}\n"
        f"R/F/M scores: {r['R']}/{r['F']}/{r['M']}\n"
        f"Segment: {r['Segment']}"
    )


rfm_tools = [overall_stats, segment_summary, segment_customers, customer_lookup]