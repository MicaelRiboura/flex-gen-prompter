from flexgenprompterlib.techniques.base_node import BaseNode
from .state import SelfConsistencyPromptingState
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from collections import Counter
from .prompts import SelfConsistencyPrompts
from ..schemas import schemas
import re
import json
import os

class AnswersGeneratorNode(BaseNode):
    def __init__(self, model, dataset_name):
        self.dataset_name = dataset_name
        response_schema = schemas.get(self.dataset_name)
        super().__init__(model=model, response_schema=response_schema)

    def invoke(self, state) -> SelfConsistencyPromptingState:
        template = SelfConsistencyPrompts.get('answers_generator_node', self.dataset_name)

        responses = []
        for _ in range(state.get('num_responses', 5)):
            response = super().invoke(
                template=template, 
                input={'prompt': state['prompt']}
            )['answer']
            responses.append(response)
        return { 'responses': responses }
        
class AggregatorAndEvaluatorNode(BaseNode):
    def __init__(self, model, dataset_name):
        self.dataset_name = dataset_name
        self.response_schema = schemas.get(self.dataset_name)
        super().__init__(model, response_schema=self.response_schema)
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
        if not self.response_schema:
            answer_pattern = re.compile(r'##(.*)')
            for i, response in enumerate(state.get('responses')):
                match = answer_pattern.search(response)
                if match:
                    answer = match.group(1)
                    final_answers.append(answer)
                    # print(f"Response #{i+1}: Found answer -> {answer}")
                # else:
                    # print(f"Response #{i+1}: Could not find a final answer.")
        else:
            final_answers = [str(response) for response in state.get('responses')]
        
        if not final_answers:
            most_common_answer = "Could not determine a final answer."
        else:
            answer_counts = Counter(final_answers)
            most_common_answer = answer_counts.most_common(1)[0][0]
            if self.response_schema:
                original_responses = state.get('responses')
                index = final_answers.index(most_common_answer)
                most_common_answer = original_responses[index]
        
        return { "answer": most_common_answer }

        
        