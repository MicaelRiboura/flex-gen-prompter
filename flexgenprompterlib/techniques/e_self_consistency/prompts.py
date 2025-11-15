from flexgenprompterlib.techniques.base_prompts import BasePrompts

class SelfConsistencyPrompts(BasePrompts):
    prompts = {
        'answers_generator_node':  {
            'gsm8k': """
                You are expert mathematician in solving logical reasoning problems. Solve the following problem by thinking step-by-step.
                
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
    }
