from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline, HuggingFaceEmbeddings, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

class Model:
    def __init__(self):
        print("Initializing the Model...")
        self.hf_llm = HuggingFaceEndpoint(
            repo_id="meta-llama/Meta-Llama-3.1-8B-Instruct",
            task="conversational",
            max_new_tokens=120,
            temperature=0.7,
        )
        self.llm = ChatHuggingFace(llm=self.hf_llm)
        
    def generate_title(self, story):
        prompt = f"Generate one creative title for the following story:\n\n{story}"
        res = self.llm.invoke(prompt)
        return res.content.strip()
    
    def generate_content(self, title):
        prompt = f"Write a short story based on the following title:\n\n{title}"
        res = self.llm.invoke(prompt) 
        return res.content.strip()