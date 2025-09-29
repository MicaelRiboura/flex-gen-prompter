from core.prompting_techniques.base_node import BaseNode
from core.prompting_techniques.a_zero_shot_prompting.state import ZeroShotPromptingState

class AnswerNode(BaseNode):
    def __init__(self, model):
        super().__init__(model)
    
    def invoke(self, state) -> ZeroShotPromptingState:
        prompt = state['prompt']
        return super().invoke(prompt)
        