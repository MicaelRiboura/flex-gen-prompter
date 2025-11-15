from .a_zero_shot import ZeroShotPromptingState, ZeroShotPromptingWorkflow
from .b_few_shot import FewShotPromptingState, FewShotPromptingWorkflow
from .c_chain_of_thoughts import ChainOfThoughtPromptingState, ChainOfThoughtPromptingWorkflow
from .d_generate_knowledge import GenerateKnowledgePromptingState, GenerateKnowledgePromptingWorkflow
from .e_self_consistency import SelfConsistencyPromptingState, SelfConsistencyPromptingWorkflow
from .f_tree_of_thoughts import TreeOfThoughtPromptingState, TreeOfThoughtPromptingWorkflow

class WorkflowFactory:
    def __init__(self, model, dataset_name=None):
        self.workflow_factory = {
            "zero_shot": ZeroShotPromptingWorkflow(state=ZeroShotPromptingState, model=model, dataset_name=dataset_name),
            "few_shot": FewShotPromptingWorkflow(state=FewShotPromptingState, model=model, dataset_name=dataset_name),
            "chain_of_thoughts": ChainOfThoughtPromptingWorkflow(state=ChainOfThoughtPromptingState, model=model, dataset_name=dataset_name),
            "generate_knowledge": GenerateKnowledgePromptingWorkflow(state=GenerateKnowledgePromptingState, model=model, dataset_name=dataset_name),
            "self_consistency": SelfConsistencyPromptingWorkflow(state=SelfConsistencyPromptingState, model=model, dataset_name=dataset_name),
            "tree_of_thoughts": TreeOfThoughtPromptingWorkflow(state=TreeOfThoughtPromptingState, model=model, dataset_name=dataset_name)
        }

    def create_workflow(self, workflow_type: str):
        if not workflow_type or workflow_type not in self.workflow_factory.keys():
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        return self.workflow_factory[workflow_type]