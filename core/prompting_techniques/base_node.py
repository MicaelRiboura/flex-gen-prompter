from langchain_openai import ChatOpenAI

class BaseNode:
    def __init__(self, model):
        self.model = ChatOpenAI(model=model, temperature=0)
    
    def invoke(self, prompt: str):
        response = self.model.invoke(prompt)
        return { "answer": response.content }