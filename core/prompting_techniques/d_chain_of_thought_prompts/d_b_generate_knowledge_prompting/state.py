from typing import TypedDict

class GenerateKnowledgePromptingState(TypedDict):
    prompt: str
    knowledge: str
    answer: str