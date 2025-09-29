from core.prompting_techniques.base_node import BaseNode
from .state import ChainOfThoughtPromptingState

class AnswerNode(BaseNode):
    def __init__(self, model):
        super().__init__(model)
    
    def invoke(self, state) -> ChainOfThoughtPromptingState:
        prompt = f'You are expert mathematician in solving logical reasoning problems. Solve the following problem by thinking step-by-step.\n\n {state['prompt']}'
        return super().invoke(prompt)
        