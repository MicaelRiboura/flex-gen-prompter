from core.prompting_techniques.a_zero_shot_prompting import ZeroShotPromptingState, ZeroShotPromptingWorkflow
from core.prompting_techniques.b_few_shot_prompting import FewShotPromptingState, FewShotPromptingWorkflow
from core.prompting_techniques.d_chain_of_thought_prompts.d_a_chain_of_thought_prompting import ChainOfThoughtPromptingState, ChainOfThoughtPromptingWorkflow
from core.prompting_techniques.d_chain_of_thought_prompts.d_b_generate_knowledge_prompting import GenerateKnowledgePromptingState, GenerateKnowledgePromptingWorkflow
from core.prompting_techniques.d_chain_of_thought_prompts.d_c_self_consistency_prompting import SelfConsistencyPromptingState, SelfConsistencyPromptingWorkflow
from core.prompting_techniques.d_chain_of_thought_prompts.d_d_tree_of_thought_prompting import TreeOfThoughtPromptingState, TreeOfThoughtPromptingWorkflow

class WorflowFactory:
    workflow_factory = {
        "zero_shot": ZeroShotPromptingWorkflow(state=ZeroShotPromptingState),
        "few_shot": FewShotPromptingWorkflow(state=FewShotPromptingState),
        "chain_of_thought": ChainOfThoughtPromptingWorkflow(state=ChainOfThoughtPromptingState),
        "generate_knowledge": GenerateKnowledgePromptingWorkflow(state=GenerateKnowledgePromptingState),
        "self_consistency": SelfConsistencyPromptingWorkflow(state=SelfConsistencyPromptingState),
        "tree_of_thoughts": TreeOfThoughtPromptingWorkflow(state=TreeOfThoughtPromptingState)
    }

    @staticmethod
    def create_workflow(workflow_type: str):
        if not workflow_type or workflow_type not in WorflowFactory.workflow_factory:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        return WorflowFactory.workflow_factory[workflow_type]