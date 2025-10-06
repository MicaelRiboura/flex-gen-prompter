from core.prompting_techniques.base_node import BaseNode
from .state import TreeOfThoughtPromptingState
from pydantic import BaseModel, Field
from typing import List
import itertools
import re
import numpy as np
np.float_ = np.float64

class ExpandNode(BaseNode):
    def __init__(self, model, limit_breadth, dataset_name):
        super().__init__(model, temperature=0.7)
        self.limit_breadth = limit_breadth
        self.dataset_prompts_map: dict = {
            'gsm8k': """
                Answer the following question: {problem}
                Make a strategy then write. Your output should be of the following format:
                Strategy:
                Your strategy about how to answer the question.
                Answer:
                Your answer to the question. It should end with "the answer is n" where n is a number.
            """
        }

    def get_samples(self, prompt, candidate, n_generate_sample, graph):
        samples = []
        for _ in range(n_generate_sample):
            res = self.model.invoke(prompt + f"\n{candidate}")
            graph[res.content] = []
            samples.append(res.content)
        
        return samples

    def invoke(self, state) -> TreeOfThoughtPromptingState:
        problem: str = state.get('problem', '').replace('\nPlease output your answer at the end as ##<your answer (arabic numerals)>', '')
        candidates: List[str] = state.get('candidates', [''])
        prompt: str = self.dataset_prompts_map['gsm8k'].format(problem=problem)
        graph: dict = state.get('G', {})

        # Adiciona o problema no grafo
        if len(graph) == 0:
            graph[problem] = []

        new_candidates = []
        for candidate in candidates:
            samples = self.get_samples(
                prompt=prompt, 
                candidate=candidate, 
                n_generate_sample=self.limit_breadth, 
                graph=graph
            )
            if candidate != '':
                graph[candidate] = samples
            new_candidates.append(samples)

        new_candidates = list(itertools.chain(*new_candidates))

        print('ExpandNode::candidates: ', new_candidates)

        # Adiciona os primeiros candidatos no grafo
        if len(candidates) == 1 and candidates[0] == '':
            graph[problem] = new_candidates

        return { "candidates": new_candidates, "G": graph }


class Evaluation(BaseModel):
    evaluation: int = Field(description="An integer score from 1 to 10 evaluating the quality of the new thought.")


class EvaluateNode(BaseNode):
    def __init__(self, model, n_evaluate, dataset_name):
        super().__init__(model, temperature=0.7)
        self.n_evaluate = n_evaluate
        self.dataset_prompts_map = {
            'gsm8k': """
                Given an instruction and several choices,
                decide which choice is most promising.
                Analyze each choice in detail, then conclude in the last line
                "The best choice is {s}", where s the integer id of the choice.
            """
        }

    def count_votes(self, vote_outputs, n_candidates):
        vote_results = [0] * n_candidates
        for vote_output in vote_outputs:
            pattern = r".*best choice is .*(\d+).*"
            match = re.match(pattern, vote_output, re.DOTALL)
            if match:
                vote = int(match.groups()[0]) - 1
                if vote in range(n_candidates):
                    vote_results[vote] += 1
        
        return vote_results
    
    def get_votes(self, prompt, candidates, n_evaluate):
        vote_outputs = []
        for _ in range(n_evaluate):
            res = self.model.invoke(prompt)
            vote_outputs.append(res.content)
        
        values = self.count_votes(vote_outputs, len(candidates))

        return values
        
    def invoke(self, state) -> TreeOfThoughtPromptingState:
        candidates: List[str] = state.get('candidates', [])
        prompt = self.dataset_prompts_map['gsm8k']

        # Adiciona escolhas dos candidatos no prompt
        for i, candidate in enumerate(candidates, 1):
            prompt += f'\nChoice {i}:\n{candidate}\n'

        values = self.get_votes(
            prompt=prompt, 
            candidates=candidates, 
            n_evaluate=self.n_evaluate
        )

        print('EvaluateNode::values: ', values)

        return { "values": values }


class PruneNode(BaseNode):
    def __init__(self, model, n_select, limit_depth, dataset_name):
        super().__init__(model, temperature=0.7)
        self.n_select: int = n_select
        self.limit_depth = limit_depth
    
    def invoke(self, state) -> TreeOfThoughtPromptingState:
        values = state.get('values', [])
        candidates = state.get('candidates', [])
        depth: int = state.get('depth', 0)

        ps = np.array(values, dtype=np.float64) / sum(values)

        ids = [i for i, _ in enumerate(candidates)]

        if depth == self.limit_depth - 1:
            select_ids = np.random.choice(ids, size=1, p=ps).tolist()
        else:
            select_ids = np.random.choice(ids, size=self.n_select, p=ps).tolist()

        select_new_candidates = [candidates[select_id] for select_id in select_ids]

        print('PruneNode::candidates_selected: ', select_new_candidates)
        print('PruneNode::depth: ', depth)
        
        new_state = {'candidates': select_new_candidates, 'depth': depth + 1 }

        if depth == self.limit_depth - 1:
            new_state['answer'] = select_new_candidates[0].lower()\
                .replace('the answer is ', '##')\
                .replace('.', '')
            print(f'state: {new_state}')
        
        return new_state

