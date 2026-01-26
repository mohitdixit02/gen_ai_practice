from model import Model

if __name__ == "__main__":
    print("\n\n--- Output Parser Practice 🤖 ---\n")
    print("Select the Model:")
    print("1. Meta Llama 3.1")
    print("2. Google Gemma-2")
    model_choice = input("Enter choice (1/2) or 'exit' to quit: ")
    if(model_choice.lower() in ['exit', 'quit']):
        print("👋 Goodbye!")
        exit(0)
    
    print("Initializing the model...")
    model = Model(model=("meta" if model_choice=="1" else "gemma"))
    print("✅ Model initialized successfully!\n")
    
    while(True):
        print("Select Output Format Type:")
        print("1. Pydantic Model")
        print("2. JSON Schema")
        if model.is_structured_output_supported():
            print("3. TypedDict")
        parser_choice = input("Enter choice (1/2..) or 'exit' to quit: ")
        if(parser_choice.lower() in ['exit', 'quit']):
            print("👋 Goodbye!")
            break
        
        parser_types = {"1": "pydantic", "2": "json", "3": "typed_dict"}
        model.query(parser=parser_types.get(parser_choice, "pydantic"))
        print("-----\n")
        
        