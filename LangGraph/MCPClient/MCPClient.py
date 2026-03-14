from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from Model import llm_node
from langgraph.prebuilt import ToolNode, tools_condition
import asyncio
from pathlib import Path

# MCP Client
from langchain_mcp_adapters.client import MultiServerMCPClient

BASE_DIR = Path(__file__).resolve().parent
BACKEND_PATH = BASE_DIR / "MCPBackend.py"
PYTHON_EXE = r"D:\Softwares\DL\conda\envs\lc_env\python.exe"

client = MultiServerMCPClient(
    {
        "demo": {
            "transport": "stdio",
            "command": PYTHON_EXE,          
            "args": [str(BACKEND_PATH)],
        },
    }
)

# State
class ModelState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages] # add message reducer append new messages to the list by merge strategy

async def build_graph():
    tools = await client.get_tools(
        server_name="demo"
    )
    tool_node = ToolNode(tools=tools)
    
    # Graph
    print("Building the graph...")
    graph = StateGraph(ModelState)
    graph.add_node("LLM", llm_node)
    graph.add_node("tools", tool_node)

    # Edges
    graph.add_edge(START, "LLM")
    graph.add_conditional_edges("LLM", tools_condition)
    graph.add_edge("tools", "LLM")

    worflow = graph.compile()
    return worflow

async def main():
    worflow = await build_graph()
    print("Invoking the workflow...")
    res = worflow.invoke(input={
        "messages": [
            HumanMessage(content="what is 5 + 3?"),
        ]}
    )
    print(res)
    
if __name__ == "__main__":
    asyncio.run(main())