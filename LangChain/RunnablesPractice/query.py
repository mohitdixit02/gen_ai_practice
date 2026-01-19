class Query:
    def request_topic(self):
        choice = input("Select a topic to generate the content about: ")
        return choice
    
    def request_feedback(self):
        rating = input("Please provide your feedback on the generated content (1-5): ")
        return rating