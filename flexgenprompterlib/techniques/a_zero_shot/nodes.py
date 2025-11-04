from flexgenprompterlib.techniques.base_node import BaseNode
from .state import ZeroShotPromptingState
from ..schemas import schemas
from .prompts import prompts

class AnswerNode(BaseNode):
    def __init__(self, model, dataset_name):
        self.dataset_name = dataset_name
        response_schema = schemas.get(self.dataset_name, None)
        super().__init__(model=model, response_schema=response_schema)
        self.prompting_map = prompts.get('answer_node')
    
    def invoke(self, state) -> ZeroShotPromptingState:
        template = self.prompting_map.get(self.dataset_name)
        
        return super().invoke(template=template, input={'prompt': state['prompt'] })
        