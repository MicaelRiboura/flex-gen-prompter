from core.prompting_techniques.builder import WorkflowBuilder
from langgraph.graph import END
from .nodes import FewShotAnswerNode

class FewShotPromptingWorkflow(WorkflowBuilder):
    def __init__(self, state):
        super().__init__(state)
    
    def run(self, prompt, examples):
        super().__init__(self.state)
        self.add_node("few_shot_answer", FewShotAnswerNode(examples=examples).invoke)
        self.set_entry_point("few_shot_answer")
        self.add_edge("few_shot_answer", END)
        app = self.compile(save_in="b_few_shot_prompting_graph.png")
        return app.invoke({"prompt": prompt})