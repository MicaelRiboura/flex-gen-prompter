from typing import TypedDict, List

class SelfConsistencyPromptingState(TypedDict):
    prompt: str
    responses: List[str]
    num_responses: int
    answer: str