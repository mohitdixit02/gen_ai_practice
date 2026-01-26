from langchain_huggingface import HuggingFacePipeline
from chains.templateProvider import TemplateProvider
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableBranch
import time
import re
import json

class ReviewModel:
    def __init__(self):
        self.model = HuggingFacePipeline.from_model_id(
            model_id="google/gemma-3-1b-it",
            task="text-generation",
            pipeline_kwargs={"max_new_tokens": 80, "temperature": 0.2},
        )
        self.template_provider = TemplateProvider()
        self.parser = StrOutputParser()
        
    def invokeJSONChain(self, chain, input, topic):
        print(f"Processing {topic}...")
        start_time = time.time()
        res = chain.invoke(input)
        end_time = time.time()
        print(f"{topic} generated in {end_time - start_time:.2f} seconds.")
        
        json_res_list = re.search(r"```json(.*?)```", res, re.DOTALL)
        if not json_res_list:
            return res
        try:
            obj = json.loads(json_res_list.group(1).strip())
            return obj['response']
        except Exception as e:
            print("Error parsing JSON:", e)
            return None

    def generate(self, feedback):
        review_feedback_chain = RunnableLambda(
            lambda x: "Positive" if int(x) > 3 else "Negative"
        )
        review_condition_chain = RunnableBranch(
            (lambda x: x == "Positive", self.template_provider.get_positive_feedback_template() | self.model | self.parser),
            (lambda x: x == "Negative", self.template_provider.get_negative_feedback_template() | self.model | self.parser),
            RunnableLambda(lambda x: "Feedback not recognized.")
        )
        main_chain = review_feedback_chain | review_condition_chain
        return self.invokeJSONChain(
            main_chain,
            feedback,
            "feedback response"
        )
        
        
        