from langgraph.graph import END
from core.prompting_techniques.builder import WorkflowBuilder
from .nodes import KnowledgeGeneratorNode, AnswerNode


class GenerateKnowledgePromptingWorkflow(WorkflowBuilder):
    def __init__(self, state):
        super().__init__(state)

    def run(self, prompt):
        super().__init__(self.state)
        
        self.add_node("knowledge_generator", KnowledgeGeneratorNode().invoke)
        self.set_entry_point("knowledge_generator")
        self.add_node("answer", AnswerNode().invoke)
        self.add_edge("knowledge_generator", "answer")
        self.add_edge("answer", END)
        app = self.compile(save_in="d_b_generate_knowledge_prompting_graph.png")
        result = app.invoke({"prompt": prompt})
        return result