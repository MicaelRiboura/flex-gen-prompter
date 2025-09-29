from langchain_openai import ChatOpenAI

class BaseNode:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4.1", temperature=0)
    
    def invoke(self, prompt: str):
        response = self.llm.invoke(prompt)
        return { "answer": response.content }