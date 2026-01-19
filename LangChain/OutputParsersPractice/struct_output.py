from typing import TypedDict, Annotated, Optional, Literal
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from pprint import pprint

class ReviewTypedDict(TypedDict):
    title: Annotated[str, "Title of the review"]
    summary: Annotated[str, "20 words summary of the review"]
    sentiment: Annotated[Literal["positive", "negative"], "Sentiment of the review"]
    pros: Annotated[Optional[list[str]], "List of pros mentioned in the review"]
    cons: Annotated[Optional[list[str]], "List of cons mentioned in the review"]
    author_name: Annotated[Optional[str], "Name of the review author"]
    
class ReviewPydantic(BaseModel):
    title: Annotated[str, Field(description="Title of the review")]
    summary: Annotated[str, Field(description="20 words summary of the review")]
    sentiment: Annotated[Literal["positive", "negative", "mixed"], Field(description="Sentiment of the review")]
    pros: Annotated[Optional[list[str]], Field(default=None, description="List of pros mentioned in the review")]
    cons: Annotated[Optional[list[str]], Field(default=None, description="List of cons mentioned in the review")]
    author_name: Annotated[Optional[str], Field(default=None, description="Name of the review author")]
    
JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Title of the review"},
        "summary": {"type": "string", "description": "20 words summary of the review"},
        "sentiment": {
            "type": "string",
            "enum": ["positive", "negative", "mixed"],
            "description": "Sentiment of the review"
        },
        "pros": {
            "type": ["array", "null"],
            "items": {"type": "string"},
            "description": "List of pros mentioned in the review"
        },
        "cons": {
            "type": ["array", "null"],
            "items": {"type": "string"},
            "description": "List of cons mentioned in the review"
        },
        "author_name": {
            "type": ["string", "null"],
            "description": "Name of the review author"
        },
    },
    "required": ["title", "summary", "sentiment"]
}

class StructOutput:
    def __init__(self, type="pydantic", is_structured_output=False):
        self.type = type
        self.is_structured_output = is_structured_output
        if is_structured_output:
            if self.type == "json":
                print("Using JSON Schema for structured output...")
                self.parser = JSON_SCHEMA
            elif self.type == "typed_dict":
                print("Using TypedDict for structured output...")
                self.parser = ReviewTypedDict
            else:
                print("Using Pydantic Model for structured output...")
                self.parser = ReviewPydantic
        else:
            if self.type == "json":
                print("Using JSON Output Parser...")
                self.parser = JsonOutputParser(schema=JSON_SCHEMA)
            else:
                print("Using Pydantic Output Parser...")
                self.parser = PydanticOutputParser(pydantic_object=ReviewPydantic)
        
    def get_parser(self):
        return self.parser
    
    def get_instructions(self):
        if self.is_structured_output:
            return ""
        else:
            return self.parser.get_format_instructions()
        
    def post_process_output(self, output):
        print("\n--- Post Parsed Output ---\n")
        if self.is_structured_output:
            print(output)
        else:
            if self.type == "json":
                pprint(output, sort_dicts=False)
            elif self.type == "pydantic":
                pprint(output.model_dump(), sort_dicts=False)
            else:
                print(output)
        

