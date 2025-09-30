from core.prompting_techniques.base_node import BaseNode
from .state import TreeOfThoughtPromptingState
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate

class ThoughtProposerNode(BaseNode):
    def __init__(self, model):
        super().__init__(model)

    def invoke(self, state) -> TreeOfThoughtPromptingState:
        problem = state["prompt"].replace('\nPlease output your answer at the end as ##<your answer (arabic numerals)>', '')

        thoughts = state.get("thoughts", [])

        existing_thoughts = "No reasoning yet." if "\n".join(thoughts) == "" else "\n".join(thoughts)

        G = state.get("G", {})
        if len(thoughts) == 0:
            G[problem] = []

        prompt = f"""
        You are an expert mathematician. You are given a math problem and the reasoning steps taken so far.
        Your task is to propose the next single, logical reasoning step to solve the problem.
        Think step-by-step and propose a clear, concise action.

        Problem: {problem}
        Reasoning so far:
        {existing_thoughts}

        Propose the very next step. For example: "Calculate the cost of all the apples."

        If is the final step, you must say: "The final step is..."
        """

        response = self.model.invoke(prompt)

        return { "new_thought": response.content, "G": G }


class Evaluation(BaseModel):
    evaluation: int = Field(description="An integer score from 1 to 10 evaluating the quality of the new thought.")


class EvaluatorNode(BaseNode):
    def __init__(self, model, min_score=8):
        super().__init__(model)
        self.min_score = min_score
    
    def invoke(self, state) -> TreeOfThoughtPromptingState:
        problem = state["prompt"].replace('\nPlease output your answer at the end as ##<your answer (arabic numerals)>', '')
        new_thought = state["new_thought"]
        thoughts = state.get("thoughts", [])
        thought_process = "No reasoning yet." if "\n".join(thoughts) == "" else "\n".join(thoughts)

        prompt = """
        You are an expert mathematician. You are given a math problem and the reasoning steps taken so far.
        Your task is to evaluate whether the new thought step is consistent.
        Evalue in a range of 1-10, which 10 means the new thought is logically optimal and 1 if it is horrible.

        Problem: {problem}
        Reasoning so far:
        {thought_process}

        New Thought:
        {new_thought}
        """
        structured_llm = self.model.with_structured_output(Evaluation)
        chain = PromptTemplate.from_template(template=prompt) | structured_llm
        response = chain.invoke({'problem': problem, 'thought_process': thought_process, 'new_thought': new_thought})

        lateral_thoughts_count = state.get("lateral_thoughts_count", 0)
        deep_thoughts_count = state.get("deep_thoughts_count", 0)

        G = state.get("G", {})
        
        if len(thoughts) > 0:
            last_thought = thoughts[-1]
            G[last_thought].append(new_thought)
            G[new_thought] = []
        else:
            G[problem].append(new_thought)
            G[new_thought] = []

        # print(f'min_score: {self.min_score} | evaluation: {response.evaluation} | lateral_thoughts_count: {lateral_thoughts_count} | deep_thoughts_count: {deep_thoughts_count}')
        if response.evaluation >= self.min_score or lateral_thoughts_count >= 5:
            # print(f'current thought: {new_thought}')
            # print('create deeper thought')
            return { "evaluation": response.evaluation, "thoughts": thoughts + [new_thought], "lateral_thoughts_count": 0, "deep_thoughts_count": deep_thoughts_count + 1, "G": G }
        else:
            # print(f'current thought: {new_thought}')
            # print('create lateral thought')

            return { "evaluation": response.evaluation, "lateral_thoughts_count": lateral_thoughts_count + 1, "deep_thoughts_count": deep_thoughts_count, "G": G  }


class SolverNode(BaseNode):
    def __init__(self, model):
        super().__init__(model)
    
    def invoke(self, state) -> TreeOfThoughtPromptingState:
        problem = state["prompt"]
        thoughts = state.get("thoughts", [])
        thought_process = "\n".join(thoughts)

        prompt = f"""
        You are a math solver. Based on the following problem and the step-by-step reasoning,
        provide only the final numerical answer.

        Problem: {problem}
        Reasoning:
        {thought_process}

        Please output your answer at the end as ##<your answer (arabic numerals)>
        Final Answer:
        """

        return super().invoke(prompt)

