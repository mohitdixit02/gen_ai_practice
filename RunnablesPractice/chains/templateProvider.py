from langchain_core.prompts import PromptTemplate

class TemplateProvider:
    def __init__(self):
        self.gen_template = PromptTemplate(
            template="You are a helpful writer. Give a 200 words article on the topic {topic}. Return the output in JSON format with key 'article'.",
            input_variables=["topic"],
        )
        self.summarize_template = PromptTemplate(
            template="Give me the name of 5 things discussed in the article. Output in JSON format with key 'summary' and value is single array of 5 items: \n\n{article}",
            input_variables=["article"]
        )
        self.title_template = PromptTemplate(
            template="Give me one catchy title for the following article in the form of JSON with key 'title': \n\n{article}",
            input_variables=["article"]
        )
        self.positive_feedback_template = PromptTemplate(
            template = "Act as customer Support. The user has given {feedback} feedback on some product. Give only one appropriate positive response in 30 words in JSON format with key 'response'.",
            input_variables = ["feedback"]
        )
        self.negative_feedback_template = PromptTemplate(
            template = "Act as customer Support. The user has given {feedback} feedback on some product. Give only one appropriate apologetic response in 30 words in JSON format with key 'response'.",
            input_variables = ["feedback"]
        )
        
    def get_generation_template(self):
        return self.gen_template
    
    def get_summarization_template(self):
        return self.summarize_template
    
    def get_title_template(self):
        return self.title_template
    
    def get_positive_feedback_template(self):
        return self.positive_feedback_template
    
    def get_negative_feedback_template(self):
        return self.negative_feedback_template