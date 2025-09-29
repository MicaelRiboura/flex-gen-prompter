from typing import TypedDict, List

class TreeOfThoughtPromptingState(TypedDict):
    prompt: str
    thoughts: List[str]
    new_thought: str
    evaluation: int
    answer: str
    lateral_thoughts_count: int
    deep_thoughts_count: int
    G: dict