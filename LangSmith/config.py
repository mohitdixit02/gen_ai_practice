from typing import TypedDict, Annotated, Literal

class StoryState(TypedDict):
    topic: str
    title: str
    content: str
    
WRITE_CONFIG = {
    "configurable": {
        "thread_id": "story_generation_thread",
        "checkpoint_ns": ""
    }
}

READ_CONFIG = {
    "configurable": {
        "thread_id": "story_generation_thread",
    }
}

LANGSMITH_TRACE_CONFIG = {
    "configurable": {
        "thread_id": "story_gen_thread",
    },
    "metadata": {
        "thread_id": "story_gen_thread",
    },
    "run_name": "story_gen_run"
}