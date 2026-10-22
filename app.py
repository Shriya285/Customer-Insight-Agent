import streamlit as st
from agent import ask

st.set_page_config(page_title="Customer Insights Agent", page_icon="📊")

# welcome cards: (title, short description, full question)
CARDS = [
    ("Revenue by segment", "See which customer group brings in the most money.", "Which segment brings the most revenue?"),
    ("Top customers", "Find the biggest spenders in your best segment.", "Show the top 5 Champions by spend"),
    ("Customer lookup", "Get the RFM scores and segment for one customer.", "Tell me about customer 12347"),
    ("Win-back list", "Find who to re-engage first.", "Which customers should we win back first?"),
]

# pills above the chat box: short label -> full question
PILLS = {
    "Top revenue segment": "Which segment brings the most revenue?",
    "Top 5 Champions": "Show the top 5 Champions by spend",
    "Look up a customer": "Tell me about customer 12347",
    "Win-back list": "Which customers should we win back first?",
    "Compare Champions vs Lost": "Compare Champions and Lost customers",
    "Try a delete": "Delete all Lost customers",
}

if "messages" not in st.session_state:
    st.session_state["messages"] = []


def clean(text):
    # the model sometimes adds backticks or $ signs that Streamlit renders as code / math
    return text.replace("`", "").replace("$", "\\$")


def ask_this(question):
    st.session_state["pending"] = question


def pick():
    choice = st.session_state.get("pill")
    if choice:
        st.session_state["pending"] = PILLS[choice]
        st.session_state["pill"] = None


with st.sidebar:
    st.subheader("About")
    st.write("RFM customer segmentation on the Online Retail II dataset (4,312 customers). The agent has read-only access.")
    if st.button("Clear chat"):
        st.session_state["messages"] = []
        st.rerun()

# take the new question first, so the welcome screen hides as soon as chat starts
q = st.chat_input("Ask about your customers") or st.session_state.pop("pending", None)
if q:
    st.session_state["messages"].append({"role": "user", "content": q})

st.title("Customer Insights Agent")

# 1) welcome screen while the chat is empty
if not st.session_state["messages"]:
    st.write("Ask questions about your customer segments in plain English.")
    cols = st.columns(2)
    for i, (title, desc, question) in enumerate(CARDS):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.caption(desc)
                st.button("Ask this", key=f"card{i}", on_click=ask_this, args=(question,))

# 2) chat history
for m in st.session_state["messages"]:
    with st.chat_message(m["role"]):
        st.markdown(clean(m["content"]))

# 3) answer the new question
if q:
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                a = ask(q)
            except Exception as e:
                a = f"Something went wrong: {e}"
        st.markdown(clean(a))
    st.session_state["messages"].append({"role": "assistant", "content": a})

# 4) pills stay above the chat box once the chat has started (after the latest answer)
if st.session_state["messages"]:
    st.pills("Try asking", list(PILLS), key="pill", on_change=pick, label_visibility="collapsed")