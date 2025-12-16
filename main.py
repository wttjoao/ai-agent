from typing import TypedDict, Optional
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langchain.tools import tool
import requests
import os
import re

@tool("get_stock_price", description="Get the current stock price for a given ticker symbol.")
def get_stock_price(ticker: str) -> str:
    api_key = os.getenv("d50hmd9r01qsabpth2ggd50hmd9r01qsabpth2h0")
    if not api_key:
        return "ERROR: FINNHUB_API_KEY is missing"

    url = "https://finnhub.io/api/v1/quote"
    params = {"symbol": ticker, "token": api_key}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return "ERROR: Failed to fetch stock price"

    data = response.json()
    price = data.get("c")

    if not price:
        return "ERROR: No price available"

    return f"{price} USD"


class AgentState(TypedDict):
    question: str
    ticker: Optional[str]
    tool_result: Optional[str]
    final_answer: Optional[str]


llm = ChatOllama(
    model="qwen2.5:7b-instruct",
    temperature=0
)

def extract_ticker(state: AgentState) -> AgentState:
    q = state["question"].lower()

    # Deterministic rules (extendable)
    if "apple" in q:
        state["ticker"] = "AAPL"
    elif "tesla" in q:
        state["ticker"] = "TSLA"
    else:
        state["ticker"] = None

    return state


def execute_tool(state: AgentState) -> AgentState:
    if not state["ticker"]:
        state["tool_result"] = "ERROR: Unknown ticker"
        return state

    state["tool_result"] = get_stock_price.invoke(
        {"ticker": state["ticker"]}
    )
    return state


def generate_final_answer(state: AgentState) -> AgentState:
    prompt = f"""
You are an assistant.

The user asked:
{state['question']}

The stock price tool returned:
{state['tool_result']}

Provide a clear, concise answer.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    state["final_answer"] = response.content
    return state


graph = StateGraph(AgentState)

graph.add_node("extract", extract_ticker)
graph.add_node("tool", execute_tool)
graph.add_node("final", generate_final_answer)

graph.set_entry_point("extract")

graph.add_conditional_edges(
    "extract",
    lambda s: "tool" if s["ticker"] else "final",
    {
        "tool": "tool",
        "final": "final"
    }
)

graph.add_edge("tool", "final")
graph.add_edge("final", END)

agent = graph.compile()

if __name__ == "__main__":
    result = agent.invoke({
        "question": "What is the stock price of Apple?",
        "ticker": None,
        "tool_result": None,
        "final_answer": None
    })

    print(result["final_answer"])
