from chains.generateModel import GenerateModel
from chains.reviewModel import ReviewModel

class Model:
    def __init__(self):
        self.gen_model = GenerateModel()
        self.rev_model = ReviewModel()
        
    def print_response(self, response):
        if isinstance(response, list):
            print("\n")
            for idx, block in enumerate(response):
                print(f"--- Block {idx + 1} ---")
                if isinstance(block, dict):
                    for key, value in block.items():
                        print(f"{key.title()}")
                        if isinstance(value, list):
                            for idx, item in enumerate(value):
                                print(f"{idx + 1}. {item}")
                        else:
                            print(value)
                else:
                    print(block)
                print("\n")
        else:
            print(response)
    
    def generate_content(self, topic):
        res = self.gen_model.generate(topic)
        self.print_response(res)
        return True
    
    def process_feedback(self, feedback):
        res = self.rev_model.generate(feedback)
        self.print_response(res)