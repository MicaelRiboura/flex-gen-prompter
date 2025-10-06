from langgraph.graph import END
from core.prompting_techniques.builder import WorkflowBuilder
from .nodes import ExpandNode, EvaluateNode, PruneNode

class TreeOfThoughtPromptingWorkflow(WorkflowBuilder):
    def __init__(self, state, model, dataset_name):
        super().__init__(state, model)
        self.limit_depth = 1
        self.limit_breadth = 5
        self.n_evaluate = 5
        self.n_select = 2
        self.dataset_name = dataset_name

    def should_continue(self, state):
        depth: int = state.get('depth', 0)
        if depth < self.limit_depth:
            return "expand"
        else:
            return END

    def run(self, prompt):
        super().__init__(self.state, self.model)
        
        self.add_node("expand", ExpandNode(model=self.model, limit_breadth=self.limit_breadth, dataset_name=self.dataset_name).invoke)
        self.add_node("evaluate", EvaluateNode(model=self.model, n_evaluate=self.n_evaluate, dataset_name=self.dataset_name).invoke)
        self.add_node("prune", PruneNode(model=self.model, n_select=self.n_select, limit_depth=self.limit_depth, dataset_name=self.dataset_name).invoke)
        self.set_entry_point("expand")
        self.add_edge("expand", "evaluate")
        self.add_edge("evaluate", "prune")
        self.add_conditional_edge(
            "prune",
            self.should_continue,
            {
                "expand",
                END,
            },
        )
        app = self.compile(save_in="d_d_tree_of_thought_prompting_graph.png")
        result = app.invoke({"problem": prompt}, {"recursion_limit": 100})
        return result