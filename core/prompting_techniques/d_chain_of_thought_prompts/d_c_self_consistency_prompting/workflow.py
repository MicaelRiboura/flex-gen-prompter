from langgraph.graph import END
from core.prompting_techniques.builder import WorkflowBuilder
from .nodes import AnswersGeneratorNode, AggregatorAndEvaluatorNode
from collections import Counter
import re


class SelfConsistencyPromptingWorkflow(WorkflowBuilder):
    def __init__(self, state, num_responses=5):
        super().__init__(state)
        self.num_responses = num_responses

    def should_continue(self, state):
        final_answers = []
        answer_pattern = re.compile(r'##(.*)')
        for i, response in enumerate(state["responses"]):
            match = answer_pattern.search(response)
            if match:
                answer = match.group(1)
                final_answers.append(answer)

        answer_counts = Counter(final_answers)
        max_key = max(answer_counts, key=answer_counts.get)
        max_count = answer_counts[max_key]

        if max_count <= (state.get("num_responses", 5) / 2):
            return "generate"
        else:
            return "aggregate"

    def run(self, prompt):
        super().__init__(self.state)
        
        self.add_node("answers_generator", AnswersGeneratorNode().invoke)
        self.add_node("aggregator_and_evaluator", AggregatorAndEvaluatorNode().invoke)
        self.set_entry_point("answers_generator")
        self.add_conditional_edge(
            "answers_generator",
            self.should_continue,
            {
                "generate": "answers_generator",
                "aggregate": "aggregator_and_evaluator",
            },
        )
        self.add_edge("aggregator_and_evaluator", END)
        app = self.compile(save_in="d_c_self_consistency_prompting_graph.png")
        result = app.invoke({"prompt": prompt, "num_responses": self.num_responses})
        return result