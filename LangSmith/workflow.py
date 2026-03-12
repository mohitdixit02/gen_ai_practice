from model import Model
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
from config import StoryState, READ_CONFIG, WRITE_CONFIG, LANGSMITH_TRACE_CONFIG
from langgraph.checkpoint.sqlite import SqliteSaver
from langsmith import traceable
import sqlite3

@traceable(
    metadata={"name": "Sqlite Checkpointer", "thread_id": "story_gen_thread"},
    tags=["database", "checkpoint", "sqlite"]
)
def get_sqlite_checkpointer():
    print("Initializing SQLite Checkpointer...")
    connc = sqlite3.connect(
        database="story_generation.db",
        check_same_thread=False
    )
    return SqliteSaver(conn=connc)

def request_story_topic(story: StoryState) -> Annotated[str, "Request a story topic from the user."]:
    topic = input("Please enter a story topic: ")
    story['topic'] = topic
    return story

def generate_title(story: StoryState) -> StoryState:
    model = Model()
    title = model.generate_title(story['topic'])
    story['title'] = title
    return story

def generate_content(story: StoryState) -> StoryState:
    model = Model()
    content = model.generate_content(story['title'])
    story['content'] = content
    return story

class Workflow:
    def __init__(self):
        pass

    @traceable(
        metadata={"name": "Story Generation Workflow", "thread_id": "story_gen_thread"},
        tags=["workflow", "story_generation"]
    )
    def build_graph(self):
        print("Building the workflow graph...")
        # Graph definition
        graph = StateGraph(StoryState)

        # Nodes
        graph.add_node("request_topic", request_story_topic)
        graph.add_node("generate_title", generate_title)
        graph.add_node("generate_content", generate_content)

        # edges
        graph.add_edge(START, "request_topic")
        graph.add_edge("request_topic", "generate_title")
        graph.add_edge("generate_title", "generate_content")
        graph.add_edge("generate_content", END)

        print("Compiling the workflow graph with checkpointer...")
        workflow = graph.compile(
            checkpointer= get_sqlite_checkpointer(),
        )
        return workflow
    
    @traceable(
        metadata={"name": "Invoke Story Generation Workflow", "thread_id": "story_gen_thread"},
        tags=["workflow", "invoke"]
    )
    def invoke_workflow(self):
        print("Invoking the workflow...")
        Workflow = self.build_graph()
       
        for state in Workflow.stream(
            input=StoryState(topic="", title="", content=""),
            config=LANGSMITH_TRACE_CONFIG,
            stream_mode="values"
        ):
            print("\n--- Current Story State ---")
            print(f"Topic: {state.get('topic', '')}")
            print(f"Title: {state.get('title', '')}")

            content = state.get("content", "")
            print(content)
    