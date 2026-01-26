from model import ChatModel
from query import Query

if __name__ == "__main__":
    query = Query()
    print("\n\n--- Embedding Model 🤖 ---\n")
    sentences = query.request_sentences()
    
    print("Initializing the Embedding model...")
    model = ChatModel()
    print("✅ Model initialized successfully!\n")
    print("Generating embeddings...")
    embeddings = model.generate_embeddings(sentences)
    print("✅ Embeddings generated successfully!\n")
    for i, emb in enumerate(embeddings):
        print(f"Sentence {i+1}:")
        print("Embedding Dimensions:", len(emb))
        print(f"Sentence {i+1} Embedding: {emb}")
    print("\n************************************\n")