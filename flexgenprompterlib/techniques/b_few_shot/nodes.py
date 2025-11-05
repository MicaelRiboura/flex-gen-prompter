from flexgenprompterlib.techniques.base_node import BaseNode
from core.prompting_techniques.b_few_shot_prompting.state import FewShotPromptingState
from langchain.prompts import PromptTemplate
from ..schemas import schemas
from .prompts import FewShotPrompts

class FewShotAnswerNode(BaseNode):
    def __init__(self, model, dataset_name):
        self.dataset_name = dataset_name
        response_schema = schemas.get(self.dataset_name, None)
        super().__init__(model=model, response_schema=response_schema)
    
    def invoke(self, state) -> FewShotPromptingState:
        template = FewShotPrompts.get('answer_node', self.dataset_name)

        return super().invoke(template=template, input={'prompt': state['prompt'] })