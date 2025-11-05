from flexgenprompterlib.techniques.base_node import BaseNode
from .state import ChainOfThoughtPromptingState
from langchain.prompts import PromptTemplate
from ..schemas import schemas
from .prompts import ChainOfThoughtsPrompts

class AnswerNode(BaseNode):
    def __init__(self, model, dataset_name):
        self.dataset_name = dataset_name
        response_schema = schemas.get(self.dataset_name)
        super().__init__(model=model, response_schema=response_schema)
        self.response_schema = response_schema
    
    def invoke(self, state) -> ChainOfThoughtPromptingState:
        template = ChainOfThoughtsPrompts.get('answer_node', self.dataset_name)

        return super().invoke(template=template, input={'prompt': state['prompt'] })
        