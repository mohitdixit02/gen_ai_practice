from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException
from struct_output import StructOutput
from review_text import get_review_text

def get_parameters(model):
    if(model == "gemma"):
        print("Using Google Gemma-2 model...")
        return {
            "repo_id": "google/gemma-2-2b-it",
            "task": "text-generation"
        }
    else:
        print("Using Meta Llama 3.1 model...")
        return {
            "repo_id": "meta-llama/Meta-Llama-3.1-8B-Instruct",
            "task": "conversational",
            "max_new_tokens": 120,
            "temperature": 0.7,
        }

class Model:
    def __init__(self, model="meta"):
        hf_llm = HuggingFaceEndpoint(**get_parameters(model))
        if getattr(hf_llm, 'structured_outputs', False):
            self.is_structured_output = True
            print("Structured outputs are supported !!")
        else:
            self.is_structured_output = False
            print("Structured outputs are not supported, using output parsers from LangChain.")
        self.llm = ChatHuggingFace(llm=hf_llm)

    def query(self, parser="pydantic"):        
        if(self.is_structured_output):
            struct_parser = StructOutput(type=parser, is_structured_output=True).get_parser()
            structured_llm = self.llm.with_structured_output(struct_parser)
            try:
                response = structured_llm.invoke(get_review_text())
                return response
            except OutputParserException as e:
                print("❌ Parser detected errors")
                print(e.__cause__)
                return
            
        else:
            parser = StructOutput(type=parser, is_structured_output=False)
            template = PromptTemplate(
                template="Analyze the following product review and provide a structured output as per the format instructions: \n Review: {review_text} \n {format_instructions}",
                input_variables=['review_text'],
                partial_variables={'format_instructions': parser.get_instructions()}
            )
            
            seq = template | self.llm | parser.get_parser()
            try:
                res = seq.invoke({"review_text": get_review_text()})
            except OutputParserException as e:
                print("❌ Parser detected errors")
                print(e.__cause__)
                return
                
            parser.post_process_output(res)
            
    def is_structured_output_supported(self):
        return self.is_structured_output

