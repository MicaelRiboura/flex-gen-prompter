from flexgenprompterlib.interfaces.iprompt import IPrompt

class BasePrompts(IPrompt):
    prompts = {}

    @classmethod
    def get(cls, node: str, dataset_name: str) -> str:
        return cls.prompts.get(node).get(dataset_name)
    
    @classmethod
    def register(cls, node: str, dataset_name: str, prompt: str):
        if node not in cls.prompts:
            raise ValueError(f"Node '{node}' is invalid in prompts.")
            
        cls.prompts[node][dataset_name] = prompt
