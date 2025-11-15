from flexgenprompterlib.techniques.a_zero_shot.prompts import ZeroShotPrompts
from flexgenprompterlib.techniques.b_few_shot.prompts import FewShotPrompts
from flexgenprompterlib.techniques.c_chain_of_thoughts.prompts import ChainOfThoughtsPrompts
from flexgenprompterlib.techniques.d_generate_knowledge.prompts import GenerateKnowledgePrompts
from flexgenprompterlib.techniques.e_self_consistency.prompts import SelfConsistencyPrompts
from flexgenprompterlib.techniques.f_tree_of_thoughts.prompts import TreeOfThoughtsPrompts
from flexgenprompterlib.interfaces.iprompt import IPrompt

class PromptFactory:
    prompts_factory = {
        "zero_shot": ZeroShotPrompts,
        "few_shot": FewShotPrompts,
        "chain_of_thoughts": ChainOfThoughtsPrompts,
        "generate_knowledge": GenerateKnowledgePrompts,
        "self_consistency": SelfConsistencyPrompts,
        "tree_of_thoughts": TreeOfThoughtsPrompts,
    }
    
    @classmethod
    def register(cls, technique: str, node: str, dataset_name: str, prompt: str):
        technique_prompt_class = cls.prompts_factory.get(technique)
        technique_prompt_class.register(node, dataset_name, prompt)
    
    @classmethod
    def extend_technique(cls, technique: str, prompt_class: IPrompt):
        cls.prompts_factory[technique] = prompt_class

    @classmethod
    def clear(cls):
        cls.prompts_factory = {
            "zero_shot": ZeroShotPrompts,
            "few_shot": FewShotPrompts,
            "chain_of_thoughts": ChainOfThoughtsPrompts,
            "generate_knowledge": GenerateKnowledgePrompts,
            "self_consistency": SelfConsistencyPrompts,
            "tree_of_thoughts": TreeOfThoughtsPrompts,
        }

    @classmethod
    def get(cls, technique: str, node: str, dataset_name: str) -> str:
        technique_class = cls.prompts_factory.get(technique)
        return technique_class.get(node, dataset_name)