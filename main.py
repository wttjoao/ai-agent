import ast
from typing import Annotated, TypedDict

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain.agents import create_agent

from langchain_core.messages import SystemMessage


@tool
def calculator(query: str) -> str:
    """A simple calculator tool."""
    return ast.literal_eval(query)  # nosec


search = DuckDuckGoSearchRun()
tools = [search, calculator]

llm = ChatOllama(
    model="qwen2.5:7b-instruct",
    temperature=0
)

agent = create_agent(llm, tools)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def agent_node(state: State):
    result = agent.invoke(state)
    return {"messages": result["messages"]}


builder = StateGraph(State)
builder.add_node("agent", agent_node)
builder.add_edge(START, "agent")

graph = builder.compile()


input_data = {
    "messages": [
        SystemMessage(
            "You must use tools when external information or calculations are required."
        ),
        HumanMessage("How old was the 30th president of the United States when he died?")
    ]
}

for step in graph.stream(input_data):
    print(step)
