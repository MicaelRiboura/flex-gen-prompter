import itertools
import re
import numpy as np
np.float_ = np.float64
from typing import List
from flexgenprompterlib.techniques.base_node import BaseNode
from ..schemas import schemas
from .prompts import prompts
from .state import TreeOfThoughtPromptingState

class ExpandNode(BaseNode):
    def __init__(self, model, limit_breadth, dataset_name):
        self.limit_breadth = limit_breadth
        self.dataset_name = dataset_name
        super().__init__(model, temperature=0.7)
        self.prompting_map: dict = prompts.get('expand_node')

    def get_samples(self, problem, strategy, candidate, n_generate_sample, graph):
        template = self.prompting_map.get(self.dataset_name)
        samples = []
        for _ in range(n_generate_sample):
            res = super().invoke(
                template=template, 
                input={
                    'prompt': problem, 
                    'strategy': strategy + f"\n{candidate}"
                }
            )['answer']
            graph[res] = []
            samples.append(res)
        
        return samples

    def invoke(self, state) -> TreeOfThoughtPromptingState:
        problem: str = state.get('problem', '')
        candidates: List[str] = state.get('candidates', [''])
        steps: List[str] = state.get('steps', [''])
        steps_str = '\n'.join(steps) if len(steps) > 0 else 'No steps yet.'
        graph: dict = state.get('G', {})

        # Adiciona o problema no grafo
        if len(graph) == 0:
            graph[problem] = []
        
        if len(graph) == 1:
            graph[problem] = candidates

        new_candidates = []
        for candidate in candidates:
            samples = self.get_samples(
                problem=problem,
                strategy=steps_str, 
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

class EvaluateNode(BaseNode):
    def __init__(self, model, n_evaluate, dataset_name):
        self.dataset_name = dataset_name
        super().__init__(model, temperature=0.7)
        self.n_evaluate = n_evaluate
        self.prompting_map = prompts.get('evaluate_node')

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
    
    def get_votes(self, problem, strategy, candidates, n_evaluate):
        template = self.prompting_map.get(self.dataset_name)
        
        choices_str = ''
        # Adiciona escolhas dos candidatos no prompt
        for i, candidate in enumerate(candidates, 1):
            choices_str += f'\nChoice {i}:\n{candidate}\n'
        
        vote_outputs = []
        for _ in range(n_evaluate):
            res = super().invoke(
                template=template, 
                input={
                    'prompt': problem, 
                    'strategy': strategy,
                    'choices': choices_str,
                }
            )['answer']
            
            vote_outputs.append(res)
        
        values = self.count_votes(vote_outputs, len(candidates))

        return values
        
    def invoke(self, state) -> TreeOfThoughtPromptingState:
        candidates: List[str] = state.get('candidates', [])
        problem: str = state.get('problem', '')
        steps: List[str] = state.get('steps', [''])
        steps_str = '\n'.join(steps)

        values = self.get_votes(
            problem=problem,
            strategy=steps_str,
            candidates=candidates, 
            n_evaluate=self.n_evaluate
        )

        print('EvaluateNode::values: ', values)

        return { "values": values }


class PruneNode(BaseNode):
    def __init__(self, model, n_select, limit_depth, dataset_name):
        self.dataset_name = dataset_name
        response_schema = schemas.get(self.dataset_name)
        super().__init__(model, temperature=0.7, response_schema=response_schema)
        self.n_select: int = n_select
        self.limit_depth = limit_depth
    
    def invoke(self, state) -> TreeOfThoughtPromptingState:
        values = state.get('values', [])
        candidates = state.get('candidates', [])
        depth: int = state.get('depth', 0)
        steps: List[str] = state.get('steps', [''])

        ps = np.array(values, dtype=np.float64) / sum(values)

        ids = [i for i, _ in enumerate(candidates)]

        if depth == self.limit_depth - 1:
            select_ids = np.random.choice(ids, size=1, p=ps).tolist()
        else:
            select_ids = np.random.choice(ids, size=self.n_select, p=ps).tolist()

        select_new_candidates = [candidates[select_id] for select_id in select_ids]

        print('PruneNode::candidates_selected: ', select_new_candidates)
        print('PruneNode::depth: ', depth)
        
        steps.append(select_new_candidates[0])
        
        new_state = {'candidates': select_new_candidates, 'depth': depth + 1, 'steps': steps }
        
        if depth == self.limit_depth - 1:
            if self.response_schema:
                new_state['answer'] = super().invoke(template="{prompt}", input={'prompt': '\n'.join(steps) })['answer']
            else:
                new_state['answer'] = select_new_candidates[0]\
                    .replace('.', '')
            print(f'state: {new_state}')
        
        return new_state
