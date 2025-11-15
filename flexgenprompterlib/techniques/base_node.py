from langchain_openai import ChatOpenAI, AzureChatOpenAI
from httpx import Client
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

class BaseNode:
    def __init__(self, model, temperature=0.3, response_schema=None):
        self.response_schema = response_schema
        # if 'azure' in os.getenv('OPENAI_BASE_URL', ''):
        #     self.model = AzureChatOpenAI(
        #         model=os.getenv('DEPLOYMENT_NAME', default='test'),
        #         openai_api_key=os.getenv('OPENAI_API_KEY', default='test'),
        #         openai_api_version=os.getenv('OPENAI_API_VERSION', default='test'),
        #         base_url=f'{os.getenv("OPENAI_BASE_URL", default="http://openai-azure")}/{os.getenv("DEPLOYMENT_NAME", default="")}',
        #         verbose=True,
        #         http_client=Client(verify='petrobras_certificado.pem'),
        #         temperature=0
        #     )
        # else:
        self.model = ChatOpenAI(model=model, temperature=temperature)
        
    def invoke(self, template: str, input: dict | None):
        prompt = PromptTemplate.from_template(template=template)
        
        if self.response_schema:
            self.llm_with_structured_output = self.model.with_structured_output(self.response_schema)
            self.chain = prompt | self.llm_with_structured_output
            if input:
                response =  self.chain.invoke(input).model_dump()
            else:
                response =  self.chain.invoke(template).model_dump()
        else:
            self.chain = prompt | self.model | StrOutputParser()
            if input:
                response = self.chain.invoke(input)
            else:
                response =  self.chain.invoke(template)
        
        return { "answer": response }
            