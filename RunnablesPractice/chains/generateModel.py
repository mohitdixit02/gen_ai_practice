import os
cache_dir = 'D:/Development/ML/Deep Learning/GenAI/.hf_cache'
os.environ['HF_HOME'] = cache_dir
os.environ['TRANSFORMERS_CACHE'] = cache_dir
os.environ['HF_DATASETS_CACHE'] = cache_dir
os.makedirs(cache_dir, exist_ok=True)

# from dotenv import load_dotenv
# load_dotenv()

import time
import re
import json
from langchain_huggingface import HuggingFacePipeline
from chains.templateProvider import TemplateProvider
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

class GenerateModel:
    def __init__(self):
        self.model = HuggingFacePipeline.from_model_id(
            model_id="google/gemma-3-1b-it",
            task="text-generation",
            pipeline_kwargs={"max_new_tokens": 500, "temperature": 0.2},
        )
        self.template_provider = TemplateProvider()
        self.parser = StrOutputParser()
        
    def invokeJSONChain(self, chain, input, topic):
        print(f"Generating {topic}...")
        start_time = time.time()
        res = chain.invoke(input)
        end_time = time.time()
        print(f"{topic} generated in {end_time - start_time:.2f} seconds.")
        
        blocks = []
        if isinstance(res, dict):
            for key, value in res.items():
                str_value = str(value)
                json_res = re.search(r"```json(.*?)```", str_value, re.DOTALL)
                if(json_res is None):
                    blocks.append(value)
                    continue
                try:
                    obj = json.loads(json_res.group(1).strip())
                    blocks.append(obj)
                except Exception as e:
                    print(f"Error parsing JSON for {key}:", e)
            
            return blocks
        else:
            json_res_list = re.findall(r"```json(.*?)```", res, re.DOTALL)
            try:
                for json_res in json_res_list:
                    obj = json.loads(json_res.strip())
                    blocks.append(obj)
                return blocks
            except Exception as e:
                print("Error parsing JSON:", e)
                return None
        

    def generate(self, topic):
        gen_template = self.template_provider.get_generation_template()
        gen_chain = gen_template | self.model | self.parser
        gen_res = self.invokeJSONChain(
            gen_chain,
            {"topic": topic},
            "article"
        )
        
        multi_task_chain = RunnableParallel({
            "summary": self.template_provider.get_summarization_template() | self.model | self.parser,
            "title": self.template_provider.get_title_template() | self.model | self.parser,
            "article": RunnablePassthrough()
        })
        
        res = self.invokeJSONChain(
            multi_task_chain,
            gen_res[0],
            "summary and title"
        )
        return res
