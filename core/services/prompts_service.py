from flexgenprompterlib import PromptFactory
from core.models import Prompt

class PromptsService:
    def _load_prompts(self):
        prompts = Prompt.objects.all()
        for prompt in prompts:
            PromptFactory.register(
                technique=prompt.technique,
                node=prompt.node,
                dataset_name=prompt.dataset,
                prompt=prompt.prompt
            )

    def get_prompts(self, technique, dataset_name):
         PromptFactory.clear()
         self._load_prompts()
         nodes = PromptFactory.prompts_factory.get(technique).prompts.keys()
         nodes_with_prompts = [{'prompt': PromptFactory.get(technique, node, dataset_name), 'node': node } for node in nodes]
         return nodes_with_prompts
    
    def initialize_dataset_prompts(self, dataset_name):
        techniques = PromptFactory.prompts_factory.keys()

        default_prompts = {
            'zero_shot': {
                'answer_node': "{prompt}",
            },
            'few_shot': {
                'answer_node': "{prompt}",
            },
            'chain_of_thoughts': {
                'answer_node': "{prompt}",
            },
            'generate_knowledge': {
                'knowledge_generator_node': "",
                'answer_node': "{knowledge}\n\n{prompt}",
            },
            'self_consistency': {
                'answers_generator_node': "{prompt}",
            },
            'tree_of_thoughts': {
                'expand_node': "{problem}\n\n{strategy}",
                'evaluate_node': "{problem}\n\n{strategy}\n\n{choices}",
            },
        }

        for technique in techniques:
            nodes = PromptFactory.prompts_factory.get(technique).prompts.keys()
            for node in nodes:
                existing_prompt = Prompt.objects.filter(technique=technique, dataset=dataset_name, node=node).first()

                if not existing_prompt:
                    Prompt.objects.update_or_create(
                        technique=technique,
                        dataset=dataset_name,
                        node=node,
                        defaults={'prompt': default_prompts.get(technique).get(node) }
                    )

    def update_prompt(self, technique, dataset_name, node, new_prompt):

        PromptFactory.register(
            technique=technique, 
            dataset_name=dataset_name, 
            node=node, 
            prompt=new_prompt
        )

        prompt_obj = Prompt.objects.filter(
            technique=technique,
            dataset=dataset_name,
            node=node,
        ).first()

        if prompt_obj:
            prompt_obj.prompt = new_prompt
            prompt_obj.save()

        return True