from core.prompting_techniques.base_node import BaseNode
from .state import GenerateKnowledgePromptingState

class KnowledgeGeneratorNode(BaseNode):
    def __init__(self, model):
        super().__init__(model)
    
    def invoke(self, _state) -> GenerateKnowledgePromptingState:
        prompt = 'You are an expert mathematician. Your task is to provide a concise list of key tips to solve high quality, linguistically diverse grade school math word problems.'
        answer = super().invoke(prompt)['answer']

        return { 'knowledge': answer }
        
class AnswerNode(BaseNode):
    def __init__(self, model):
        super().__init__(model)
    
    def invoke(self, state) -> GenerateKnowledgePromptingState:
        prompt = f'Here is some knowledge about the topic:\n\n{state['knowledge']}\n\nBased on this knowledge, please answer the following question: {state['prompt']}'
        return super().invoke(prompt)
        