from langgraph.graph import StateGraph

class WorkflowBuilder:
    """
    Classe base para construir workflows com LangGraph.
    """
    def __init__(self, state, model):
        self.state = state
        self.model = model
        self.workflow = StateGraph(state)

    def add_node(self, name: str, function):
        self.workflow.add_node(name, function)

    def set_entry_point(self, name: str):
        self.workflow.set_entry_point(name)

    def add_edge(self, from_node: str, to_node: str):
        self.workflow.add_edge(from_node, to_node)
    
    def add_conditional_edge(self, from_node: str, condition_function, options: dict):
        self.workflow.add_conditional_edges(
            from_node,
            condition_function,
            options,
        )
    
    def compile(self, save_in: str | None = None):
        app = self.workflow.compile()
        self._get_graph(app, filename=save_in)
        return app

    def _get_graph(self, app, filename: str | None):
        if filename and app:
            png_graph = app.get_graph().draw_mermaid_png()
            path_filename = f"core/prompting_techniques/graph_images/{filename}"
            with open(path_filename, "wb") as f:
                f.write(png_graph)