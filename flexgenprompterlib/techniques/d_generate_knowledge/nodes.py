from flexgenprompterlib.techniques.base_node import BaseNode
from .state import GenerateKnowledgePromptingState
from ..schemas import schemas
from .prompts import prompts

class KnowledgeGeneratorNode(BaseNode):
    def __init__(self, model, dataset_name):
        self.dataset_name = dataset_name
        super().__init__(model=model)
        self.prompting_map = prompts.get('knowledge_generator_node')
    
    def invoke(self, _state) -> GenerateKnowledgePromptingState:
        template = self.prompting_map.get(self.dataset_name)
        
        answer = super().invoke(template=template, input=None)['answer']
        
        return { 'knowledge': answer }
        
class AnswerNode(BaseNode):
    def __init__(self, model, dataset_name):
        self.dataset_name = dataset_name
        response_schema = schemas.get(self.dataset_name, None)
        super().__init__(model=model, response_schema=response_schema)
        self.prompting_map = prompts.get('answer_node')
    
    def invoke(self, state) -> GenerateKnowledgePromptingState:
        template = self.prompting_map.get(self.dataset_name)

        return super().invoke(
            template=template, 
            input={
                'knowledge': state['knowledge'], 
                'prompt': state['prompt'] 
            }
        )
        