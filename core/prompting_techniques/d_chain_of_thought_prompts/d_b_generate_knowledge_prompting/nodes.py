from core.prompting_techniques.base_node import BaseNode
from .state import GenerateKnowledgePromptingState

class KnowledgeGeneratorNode(BaseNode):
    def __init__(self, model, dataset_name):
        super().__init__(model)
        self.dataset_name = dataset_name
        self.prompting_map = {
            'gsm8k': """
                You are an expert mathematician. Your task is to provide a concise list of key tips to solve high quality, linguistically diverse grade school math word problems.
            """,
        }
    
    def invoke(self, _state) -> GenerateKnowledgePromptingState:
        prompt = self.prompting_map\
            .get(self.dataset_name)
        answer = super().invoke(prompt)['answer']

        return { 'knowledge': answer }
        
class AnswerNode(BaseNode):
    def __init__(self, model, dataset_name):
        super().__init__(model)
        self.dataset_name = dataset_name
        self.prompting_map = {
            'gsm8k': """
                Here is some knowledge about the topic:\n\n{knowledge}\n\nBased on this knowledge, please answer the following question: {prompt}
            """,
        }
    
    def invoke(self, state) -> GenerateKnowledgePromptingState:
        prompt = self.prompting_map\
            .get(self.dataset_name).format(prompt=state['prompt'], knowledge=state['knowledge'])
        return super().invoke(prompt)
        