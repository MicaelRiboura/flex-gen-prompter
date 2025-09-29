from langgraph.graph import END
from core.prompting_techniques.builder import WorkflowBuilder
from .nodes import AnswerNode


class ZeroShotPromptingWorkflow(WorkflowBuilder):
    def __init__(self, state, model):
        super().__init__(state, model)

    def run(self, prompt):
        super().__init__(self.state, self.model)
        self.add_node("answer", AnswerNode(model=self.model).invoke)
        self.set_entry_point("answer")
        self.add_edge("answer", END)
        app = self.compile(save_in="a_zero_shot_prompting_graph.png")
        result = app.invoke({"prompt": prompt})
        return result