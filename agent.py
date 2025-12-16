from typing import TypedDict, Optional
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langchain.tools import tool
import requests
import os
import re

@tool("get_case_info", description="Get information about a case given its ID.")
def get_case_info(case_id: str) -> str: 
    url = f"https://api.example.com/cases/{case_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data["artifact-schema-code"]
    else:
        raise ValueError(f"Failed to fetch case info for ID {case_id}")


llm = ChatOllama(
    model="qwen2.5:7b-instruct",
    temperature=0
)