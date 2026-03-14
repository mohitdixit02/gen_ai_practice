from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline, HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

class ModelState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages] # add message reducer append new messages to the list by merge strategy

load_dotenv()

hf_llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Meta-Llama-3.1-8B-Instruct",
    task="conversational",
    max_new_tokens=120,
    temperature=0.7,
)
llm = ChatHuggingFace(llm=hf_llm)

import re
import uuid
def _parse_args(arg_str: str) -> dict:
    args = {}
    for part in arg_str.split(","):
        k, v = part.split("=", 1)
        k, v = k.strip(), v.strip()

        # basic coercion
        if v.replace(".", "", 1).isdigit():
            v = float(v) if "." in v else int(v)
        args[k] = v
    return args

def llm_node(state: ModelState) -> ModelState:
    """LLM Node that generates a response based on the conversation history."""
    
    # bind_tools() is not supported by current LLM, so prompt is used to know about tools and how to use them
    prompt = """
    You are a helpful assistant. If messages include ToolMessage response from some tool, you can use the conversation to reply to user query
    else you can use the following tools to answer user queries:
    1. add_numbers: Add two numbers together, it has two arguments a and b which are both integers.
    If you use a tool, make sure to provide the necessary arguments in the form of tool call, use the following format:
    [TOOL_NAME](arg1=value1, arg2=value2, ...)
    If you don't need to use a tool, you can directly answer the question based on the conversation history.
    """
    messages = state["messages"] + [prompt]
    print("LLM Invoked...")
    response = llm.invoke(messages).content
    text = response.content if hasattr(response, "content") else str(response)

    # Manually adding tool calls in the response for demonstration purposes
    tool_call_regex = r"\[(\w+)\]\((.*?)\)"
    matches = re.findall(tool_call_regex, text)
    if matches:
        tool_calls = []
        for tool_name, raw_args in matches:
            tool_calls.append({
                "id": f"call_{uuid.uuid4().hex[:8]}",
                "type": "tool_call",
                "name": tool_name,
                "args": _parse_args(raw_args),
            })

        clean_text = re.sub(tool_call_regex, "", text).strip() or "Calling tool..."
        ai_msg = AIMessage(content=clean_text, tool_calls=tool_calls)
    else:
        ai_msg = AIMessage(content=text)
    
    return {"messages": [ai_msg]}