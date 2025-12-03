from flexgenprompterlib.techniques.base_node import BaseNode
from .state import GenerateKnowledgePromptingState
from ..schemas import schemas
from .prompts import GenerateKnowledgePrompts

class KnowledgeGeneratorNode(BaseNode):
    def __init__(self, model, dataset_name):
        self.dataset_name = dataset_name
        super().__init__(model=model)
    
    def invoke(self, _state) -> GenerateKnowledgePromptingState:
        template = GenerateKnowledgePrompts.get('knowledge_generator_node', self.dataset_name)
        print('template generator knowledge: ', template)
        answer = super().invoke(template=template, input={'prompt': 'prompt'})['answer']
        
        return { 'knowledge': answer }
        
class AnswerNode(BaseNode):
    def __init__(self, model, dataset_name):
        self.dataset_name = dataset_name
        response_schema = schemas.get(self.dataset_name, None)
        super().__init__(model=model, response_schema=response_schema) 
    
    def invoke(self, state) -> GenerateKnowledgePromptingState:
        template = GenerateKnowledgePrompts.get('answer_node', self.dataset_name)
        print('template answer: ', template)
        return super().invoke(
            template=template, 
            input={
                'knowledge': state['knowledge'], 
                'prompt': state['prompt'] 
            }
        )
        