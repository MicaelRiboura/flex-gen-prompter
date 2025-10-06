from typing import TypedDict, List
class TreeOfThoughtPromptingState(TypedDict):
    problem: str
    candidates: List[str]
    values: List[int]
    answer: str | None = None
    depth: int = 0
    G: dict