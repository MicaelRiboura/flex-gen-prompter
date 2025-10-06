from langgraph.graph import END
from core.prompting_techniques.builder import WorkflowBuilder
from .nodes import AnswerNode


class ChainOfThoughtPromptingWorkflow(WorkflowBuilder):
    def __init__(self, state, model, dataset_name):
        super().__init__(state, model)
        self.dataset_name = dataset_name

    def run(self, prompt):
        super().__init__(self.state, self.model)
        
        self.add_node("chain_of_thought_answer", AnswerNode(model=self.model, dataset_name=self.dataset_name).invoke)
        self.set_entry_point("chain_of_thought_answer")
        self.add_edge("chain_of_thought_answer", END)
        app = self.compile(save_in="d_a_chain_of_thought_prompting_graph.png")
        result = app.invoke({"prompt": prompt})
        return result