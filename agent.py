import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from rfm_tools import rfm_tools
load_dotenv()

llm = ChatAnthropic(
    model = "claude-haiku-5-5",
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip(),
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a customer insights assistant for an online retailer.
You answer questions using ONLY the RFM tools provided (read-only).
Rules:
- Always call a tool to get numbers. Never guess or calculate from memory.
- Quote the exact figures the tools return.
- If a question is not about this customer data, say you can only answer questions about the RFM customer data.
- If a customer or segment is not found, say so. Do not invent one.
- You cannot modify or delete data. If asked to, say you cannot."""),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm = llm, prompt = prompt, tools = rfm_tools)
agent_executor = AgentExecutor(agent = agent, tools = rfm_tools, verbose = True)


def ask(query):
    out = agent_executor.invoke({"query": query})["output"]
    if isinstance(out, list):
        return "".join(b["text"] for b in out if isinstance(b, dict) and b.get("type") == "text")
    return out


if __name__ == "__main__":
    while True:
        q = input("Ask about your customers (or 'quit'): ")
        if q.strip().lower() == "quit":
            break
        print(ask(q))