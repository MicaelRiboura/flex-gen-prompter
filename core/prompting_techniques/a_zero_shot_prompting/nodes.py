from core.prompting_techniques.base_node import BaseNode
from core.prompting_techniques.a_zero_shot_prompting.state import ZeroShotPromptingState

class AnswerNode(BaseNode):
    def __init__(self, model, dataset_name):
        super().__init__(model)
        self.dataset_name = dataset_name
        self.prompting_map = {
            'gsm8k': """
                {prompt}
                
                Please output your answer at the end as ##<your answer (arabic numerals)>
            """,
            'ecommerce_classification': """
            You are an AI assistant and you are very good at doing ecommerce products classification.
                You are going to help a customer to classify the products in the ecommerce website.
                Product Description:
                {prompt}
                Answer:
                Your answer to the question.
                You are only allowed to choose one of the following 4 categories: 
                - Household
                - Books
                - Clothing & Accessories 
                - Electronics
                It should end with "the answer is ##c", where c is the name of one of the 4 categories above.  Please, keep '##' symbol.
            """
        }
    
    def invoke(self, state) -> ZeroShotPromptingState:
        prompt = self.prompting_map.get(self.dataset_name).format(prompt=state['prompt'])
        return super().invoke(prompt)
        