# Customer Insight Agent

A small agent that answers questions about customer segments in plain English. I built it on top of an RFM (Recency, Frequency, Monetary) analysis of the Online Retail II dataset. It uses Claude with tool calling, so the numbers it gives come from the data, not from the model's guesses.


## What it can do

- Which segment brings the most revenue?
- Show the top 5 Champions by spend
- Tell me about customer 12347
- Which customers should we win back first?

It is read-only. If you ask it to delete something, or ask something unrelated to the data, it says it can't.

## Run it

You need Python 3.10+ and an Anthropic API key.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Make a `.env` file with this one line:

```
ANTHROPIC_API_KEY=your-key-here
```

Download `online_retail_II.xlsx` (UCI Machine Learning Repository) into the project folder. The first run takes about a minute to build `rfm.csv`.

```bash
streamlit run app.py     # chat in the browser
python agent.py          # chat in the terminal
python eval.py           # run the test questions
```

## Files

- `rfm.py`: cleans the data and builds the RFM scores and segments
- `rfm_tools.py`: the four tools the agent can call
- `agent.py`: the agent and its rules
- `app.py`: the Streamlit chat page
- `eval.py`: 16 test questions with answers worked out from the data
- `rfm_analysis.ipynb`: my original analysis notebook

## Testing

I wrote 16 questions with known answers (counts, top segment, a customer that doesn't exist, a delete request, a weather question). Result: 16/16.


## Future scope

- Product-level questions (which product sells the most in each segment)
- Charts in the answers
- Smarter evaluation: a second model checks whether answers are correct, instead of matching words
