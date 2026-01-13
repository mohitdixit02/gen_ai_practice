class Query:
    def request_behaviour(self):
        print("Please select the Model Behavior:")
        print("1. 😄 Friendly Chatbot")
        print("2. 🎯 Motivational Coach")
        print("3. 💡 Logical - Blunt Advisor\n")
        choice = input("Enter choice (1/2/3): ").strip()
        return choice
    
    def request_sentences(self):
        sentences = input("Enter sentences to embed (separate by '. '): ").strip()
        return sentences