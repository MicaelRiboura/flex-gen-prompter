from langchain_openai import ChatOpenAI

class BaseNode:
    def __init__(self, model, temperature=0.3):
        self.model = ChatOpenAI(model=model, temperature=temperature)
    
    def invoke(self, prompt: str):
        response = self.model.invoke(prompt)
        return { "answer": response.content }