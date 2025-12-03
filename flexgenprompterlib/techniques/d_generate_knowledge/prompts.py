from flexgenprompterlib.techniques.base_prompts import BasePrompts

class GenerateKnowledgePrompts(BasePrompts):
    prompts = {
        'knowledge_generator_node': {
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
        },
        'answer_node': {
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
                Here is some knowledge about the topic:
                
                {knowledge}
                Make a strategy then write. Your output should be of the following format:
                Product Description:
                {prompt}
                Strategy:
                Your strategy about how to classify the product based on product description enumerated step-by-step.
                Answer:
                Your answer to the question.
                You are only allowed to choose one of the following 4 categories: 
                - Households
                - Books
                - Clothing & Accessories 
                - Electronics
                It should end with "the answer is ##c", where c is the name of one of the 4 categories above. Please, keep '##' symbol.
            """,
        }
    }
