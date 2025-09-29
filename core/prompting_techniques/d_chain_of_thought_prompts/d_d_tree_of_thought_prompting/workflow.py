from langgraph.graph import END
from core.prompting_techniques.builder import WorkflowBuilder
from .nodes import ThoughtProposerNode, EvaluatorNode, SolverNode

class TreeOfThoughtPromptingWorkflow(WorkflowBuilder):
    def __init__(self, state):
        super().__init__(state)
        self.min_score = 8

    def evaluate_and_select(self, state):
        deep_thoughts_count = state.get("deep_thoughts_count", 0)
        if (state["evaluation"] >= self.min_score and state['thoughts'][-1].startswith("The final step is")) or deep_thoughts_count == 20:
            return "solve"
        else:
            return "propose"

    def run(self, prompt):
        super().__init__(self.state)
        
        self.add_node("proposer", ThoughtProposerNode().invoke)
        self.add_node("evaluator", EvaluatorNode(min_score=self.min_score).invoke)
        self.add_node("solver", SolverNode().invoke)
        self.set_entry_point("proposer")
        self.add_edge("proposer", "evaluator")
        self.add_conditional_edge(
            "evaluator",
            self.evaluate_and_select,
            {
                "propose": "proposer",
                "solve": "solver",
            },
        )
        self.add_edge("solver", END)
        app = self.compile(save_in="d_d_tree_of_thought_prompting_graph.png")
        result = app.invoke({"prompt": prompt}, {"recursion_limit": 100})
        return result