from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader, WebBaseLoader, CSVLoader

class DocLoader:
    def __init__(self):
        self.text_path = "./files/sample.txt"
        self.pdf_path = "./files/sample.pdf"
        self.url = "https://docs.langchain.com/"
        self.csv = "./files/sample.csv"
    
    def load_text(self):
        loader = TextLoader(self.text_path, encoding="utf-8")
        documents = loader.load()
        return documents
    
    def load_pdf(self):
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        return documents
    
    def load_directory(self):
        loader = DirectoryLoader(
            path="./files/",
            glob="*.txt",
            loader_cls=TextLoader,
        )
        documents = loader.load()
        return documents
    
    def web_page_loader(self):
        loader = WebBaseLoader(self.url)
        documents = loader.load()
        return documents
     
    def load_csv(self):
        loader = CSVLoader(file_path=self.csv)
        documents = loader.load()
        return documents
    
    def load(self, loader_type='1'):
        if loader_type == '1':
            docs = self.load_text()
            print(f"Loaded {len(docs)} document(s) using Text Loader.")
        elif loader_type == '2':
            docs = self.load_pdf()
            print(f"Loaded {len(docs)} document(s) using PDF Loader.")
        elif loader_type == '3':
            docs = self.load_directory()
            print(f"Loaded {len(docs)} document(s) using Directory Loader.")
        elif loader_type == '4':
            docs = self.web_page_loader()
            print(f"Loaded {len(docs)} document(s) using Web Page Loader.")
        else:
            docs = self.load_csv()
            print(f"Loaded {len(docs)} document(s) using CSV Loader.")
        
        print(type(docs))
        for doc in docs:
            print("\n--- Document Content ---\n")
            print(doc.metadata)
            print(doc.page_content)
        print("\n")
        
        