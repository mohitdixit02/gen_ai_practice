from model import ChatModel
from query import Query

if __name__ == "__main__":
    query = Query()
    print("\n\n--- Dynamic Prompt Model 🤖 ---\n")
    choice = query.request_behaviour()
    
    print("Initializing the model...")
    model = ChatModel()
    model.setBehaviour(choice)
    print("✅ Model initialized successfully!\n")
    
    while(True):
        user_input = input("👤 > ")
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Goodbye!")
            print("\n************************************\n")
            print("Conversation History:")
            for msg in model.get_model_history():
                print(msg)
            print("\n************************************\n")
            break
        response = model.query(user_input)
        print("🤖 > ", response, "\n")
        
