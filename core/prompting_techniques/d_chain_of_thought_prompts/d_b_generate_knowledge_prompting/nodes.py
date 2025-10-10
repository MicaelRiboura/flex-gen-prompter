from core.prompting_techniques.base_node import BaseNode
from .state import GenerateKnowledgePromptingState

class KnowledgeGeneratorNode(BaseNode):
    def __init__(self, model, dataset_name):
        super().__init__(model)
        self.dataset_name = dataset_name
        self.prompting_map = {
            'gsm8k': """
                You are an expert mathematician. 
                Your task is to provide a concise list of key tips to solve high quality, linguistically diverse grade school math word problems.
            """,
            'ecommerce_classification': """
                You are an expert in classifying e-commerce products based on their descriptions. 
                Your task is to provide concise key concepts that help identify the category of an e-commerce product, based on the following categories: 
                * Household 
                * Books 
                * Clothing & Accessories 
                * Electronics
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
                Here is some knowledge about the topic:
                
                {knowledge}
                
                Based on this knowledge, please answer the following question: 
                
                {prompt}
                
                Please output your answer at the end as ##<your answer (arabic numerals)>
            """,
            'ecommerce_classification': """
                You are an AI assistant and you are very good at doing ecommerce products classification.
                You are going to help a customer to classify the products in the ecommerce website.
                Make a strategy then write. Your output should be of the following format:
                Product Description:
                {prompt}
                Strategy:
                Your strategy about how to classify the product based on product description enumerated step-by-step.
                Answer:
                Your answer to the question.
                You are only allowed to choose one of the following 4 categories: 
                - Household
                - Books
                - Clothing & Accessories 
                - Electronics
                It should end with "the answer is ##c", where c is the name of one of the 4 categories above. Please, keep '##' symbol.
            """,
        }
    
    def invoke(self, state) -> GenerateKnowledgePromptingState:
        prompt = self.prompting_map\
            .get(self.dataset_name).format(prompt=state['prompt'], knowledge=state['knowledge'])
        return super().invoke(prompt)
        