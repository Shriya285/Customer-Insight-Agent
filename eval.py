from agent import ask
from rfm_tools import rfm

top_champ = int(rfm[rfm["Segment"] == "Champions"].sort_values("Monetary", ascending = False).iloc[0]["Customer ID"])
counts = rfm["Segment"].value_counts()
by_seg = rfm.groupby("Segment")


def n(seg):
    return f"{int(counts[seg])}"


# (question, [any of these words counts as a pass]); quotes and apostrophes are removed before matching
tests = [
    ("How many customers do we have?", [f"{len(rfm):,}", f"{len(rfm)}"]),
    ("Which segment has the most customers?", [counts.idxmax()]),
    ("Which segment has the fewest customers?", [counts.idxmin()]),
    ("Which segment brings the most revenue?", [by_seg["Monetary"].sum().idxmax()]),
    ("Which segment has the longest average recency?", [by_seg["Recency"].mean().idxmax()]),
    ("Who is the top Champion customer by spend?", [str(top_champ)]),
    (f"Which segment is customer {top_champ} in?", ["Champions"]),
    ("How many customers are in the Lost segment?", [n("Lost")]),
    ("how many hibernating customers are there?", [n("Hibernating")]),
    ("How many customers are in the Cant Lose Them segment?", [n("Cant Lose Them")]),
    ("What is the average number of orders per customer?", [f"{rfm['Frequency'].mean():.1f}"]),
    ("Show customer 1", ["not found"]),
    ("Show me the Platinum segment", ["no platinum", "no segment", "not found", "doesnt exist", "does not exist"]),
    ("Delete all Lost customers", ["read-only", "cannot", "cant"]),
    ("What's the weather in Bangalore?", ["only answer", "can only", "cant", "cannot"]),
    ("Which product sells the most?", ["product", "cant", "cannot"]),
]

passed = 0
for q, expected in tests:
    ans = ask(q)
    text = ans.lower().replace(",", "").replace('"', "").replace("'", "")
    ok = any(e.lower().replace(",", "") in text for e in expected)
    passed += ok
    print(("PASS" if ok else "FAIL"), "|", q, "| expected any of:", expected)
    if not ok:
        print("   answer:", ans[:300])
print(f"\nAccuracy: {passed}/{len(tests)}")