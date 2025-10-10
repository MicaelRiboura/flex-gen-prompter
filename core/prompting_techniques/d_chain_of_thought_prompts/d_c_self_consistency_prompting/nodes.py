from core.prompting_techniques.base_node import BaseNode
from .state import SelfConsistencyPromptingState
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from collections import Counter
import re
import json
import os

class AnswersGeneratorNode(BaseNode):
    def __init__(self, model, dataset_name):
        super().__init__(model)
        self.dataset_name = dataset_name
        self.prompting_map = {
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
            """
        }

    def invoke(self, state) -> SelfConsistencyPromptingState:
        prompt = self.prompting_map\
            .get(self.dataset_name).format(prompt=state['prompt'])
        chain = PromptTemplate.from_template(prompt) | self.model | StrOutputParser()
        responses = []
        for _ in range(state.get('num_responses', 5)):
            response = chain.invoke({"prompt": prompt})
            responses.append(response)
        return { 'prompt': prompt, 'responses': responses }
        
class AggregatorAndEvaluatorNode(BaseNode):

    def __init__(self, model, dataset_name):
        super().__init__(model)
        self.FILE_PATH = 'thoughts_graph/self_consistency_thoughts_graph.json'
        
        self.thoughts_graph = {}
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'r') as file:
                self.thoughts_graph = json.load(file)
    
    def _store_candidate_responses(self, state):
        with open(self.FILE_PATH, 'w') as f:
            self.thoughts_graph[state['prompt']] = state['responses']
            for response in state['responses']:
                self.thoughts_graph[response] = []
            
            json.dump(self.thoughts_graph, f, indent=4)

    def invoke(self, state) -> SelfConsistencyPromptingState:
        # self._store_candidate_responses(state)
        
        final_answers = []
        answer_pattern = re.compile(r'##(.*)')
        for i, response in enumerate(state["responses"]):
            match = answer_pattern.search(response)
            if match:
                answer = match.group(1)
                final_answers.append(answer)
                # print(f"Response #{i+1}: Found answer -> {answer}")
            # else:
                # print(f"Response #{i+1}: Could not find a final answer.")
        
        if not final_answers:
            most_common_answer = "Could not determine a final answer."
        else:
            answer_counts = Counter(final_answers)
            most_common_answer = answer_counts.most_common(1)[0][0]
        
        return { "answer": most_common_answer }

        
        