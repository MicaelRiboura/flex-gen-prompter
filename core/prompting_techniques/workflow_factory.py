from core.prompting_techniques.a_zero_shot_prompting import ZeroShotPromptingState, ZeroShotPromptingWorkflow
from core.prompting_techniques.b_few_shot_prompting import FewShotPromptingState, FewShotPromptingWorkflow
from core.prompting_techniques.d_chain_of_thought_prompts.d_a_chain_of_thought_prompting import ChainOfThoughtPromptingState, ChainOfThoughtPromptingWorkflow
from core.prompting_techniques.d_chain_of_thought_prompts.d_b_generate_knowledge_prompting import GenerateKnowledgePromptingState, GenerateKnowledgePromptingWorkflow
from core.prompting_techniques.d_chain_of_thought_prompts.d_c_self_consistency_prompting import SelfConsistencyPromptingState, SelfConsistencyPromptingWorkflow
from core.prompting_techniques.d_chain_of_thought_prompts.d_d_tree_of_thought_prompting import TreeOfThoughtPromptingState, TreeOfThoughtPromptingWorkflow

class WorkflowFactory:
    def __init__(self, model, dataset_name=None):
        self.workflow_factory = {
            "zero_shot": ZeroShotPromptingWorkflow(state=ZeroShotPromptingState, model=model, dataset_name=dataset_name),
            "few_shot": FewShotPromptingWorkflow(state=FewShotPromptingState, model=model, dataset_name=dataset_name),
            "chain_of_thought": ChainOfThoughtPromptingWorkflow(state=ChainOfThoughtPromptingState, model=model, dataset_name=dataset_name),
            "generate_knowledge": GenerateKnowledgePromptingWorkflow(state=GenerateKnowledgePromptingState, model=model, dataset_name=dataset_name),
            "self_consistency": SelfConsistencyPromptingWorkflow(state=SelfConsistencyPromptingState, model=model, dataset_name=dataset_name),
            "tree_of_thoughts": TreeOfThoughtPromptingWorkflow(state=TreeOfThoughtPromptingState, model=model, dataset_name=dataset_name)
        }

    def create_workflow(self, workflow_type: str):
        if not workflow_type or workflow_type not in self.workflow_factory.keys():
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        return self.workflow_factory[workflow_type]