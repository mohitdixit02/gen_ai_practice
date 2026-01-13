import os
cache_dir = 'D:/Development/ML/Deep Learning/GenAI/.hf_cache'
os.environ['HF_HOME'] = cache_dir
os.environ['TRANSFORMERS_CACHE'] = cache_dir
os.environ['HF_DATASETS_CACHE'] = cache_dir
os.makedirs(cache_dir, exist_ok=True)
from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline, HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def get_prompt_template(choice):
    if choice == '1':
        prompt_template = "You are a helpful, creative, and very friendly AI assistant. Always respond to the user's specific request."
    elif choice == '2':
        prompt_template = "You are a motivational coach. Always respond to the user's specific request and provide encouraging, goal-oriented advice."
    elif choice == '3':
        prompt_template = "You are a logical and blunt advisor. Always directly address the user's question."
    else:
        prompt_template = "You are a helpful AI assistant. Always respond directly to what the user asks."
    return prompt_template

# Model
class ChatModel:
    def __init__(self):
        hf_llm = HuggingFaceEndpoint(
            repo_id="meta-llama/Meta-Llama-3.1-8B-Instruct",
            task="conversational",
            max_new_tokens=120,
            temperature=0.7,
        )
        hf_embd = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.llm = ChatHuggingFace(llm=hf_llm)
        self.embd = hf_embd
        self.history = []
        
    def setBehaviour(self, choice):
        system_prompt = get_prompt_template(choice)
        self.prompt_template = ChatPromptTemplate([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])
        
    def query(self, prompt):        
        model_prompt = self.prompt_template.format_prompt(
            input=prompt,
            history=self.history
        ).to_messages()
        
        response = self.llm.invoke(model_prompt)
        clean_response = response.content.strip()
        
        self.history.append(HumanMessage(content=prompt))
        self.history.append(AIMessage(content=clean_response))
        
        return clean_response
    
    def generate_embeddings(self, text):
        docs = text.split('. ')
        embedding = self.embd.embed_documents(docs)
        return embedding
    
    def get_model_history(self):
        res_history = []
        for msg in self.history:
            role = "Human" if isinstance(msg, HumanMessage) else "AI Agent"
            res_history.append(f"{role}: {msg.content}")
        return res_history