from langchain_openai import ChatOpenAI, AzureChatOpenAI
from httpx import Client
import os

class BaseNode:
    def __init__(self, model, temperature=0.3):
        if 'azure' in os.getenv('OPENAI_BASE_URL'):
            self.model = AzureChatOpenAI(
                model=os.getenv('DEPLOYMENT_NAME', default='test'),
                openai_api_key=os.getenv('OPENAI_API_KEY', default='test'),
                openai_api_version=os.getenv('OPENAI_API_VERSION', default='test'),
                base_url=f'{os.getenv("OPENAI_BASE_URL", default="http://openai-azure")}/{os.getenv("DEPLOYMENT_NAME", default="")}',
                verbose=True,
                http_client=Client(verify='petrobras_certificado.pem'),
                temperature=0
            )
        else:
            self.model = ChatOpenAI(model=model, temperature=temperature)
    
    def invoke(self, prompt: str):
        response = self.model.invoke(prompt)
        return { "answer": response.content }