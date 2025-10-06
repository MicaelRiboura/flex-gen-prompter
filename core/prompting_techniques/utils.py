from graphviz import Digraph
import json
# from pathlib import Path

def adjacency_to_tree(adj, root):
    """
    Cria um Digraph onde cada nó recebe um ID seguro (n0, n1, ...)
    e o texto original vai para label (com quebras de linha e aspas escapadas).
    """
    dot = Digraph('ExplicitIDsTree', format='pdf')
    dot.attr("node", shape="box", style="rounded,filled", fillcolor="white", fontsize="14", width="2")

    id_counter = 0
    def make_id():
        nonlocal id_counter
        nid = f"n{id_counter}"
        id_counter += 1
        return nid

    def safe_label(s):
        if not isinstance(s, str):
            s = str(s)
        # Normaliza quebras de linha e escapa aspas duplas para o DOT
        s = s.replace('\r\n', '\n').replace('\r', '\n')
        s = s.replace('"', '\\"')     # evita quebrar a string entre aspas
        s = s.replace('\n', r'\n')    # mantém quebras de linha para render
        return s

    def dfs(node, parent_id=None):
        node_id = make_id()
        label = safe_label(node)
        dot.node(node_id, label=label)   # ID seguro + label (texto grande)
        if parent_id is not None:
            dot.edge(parent_id, node_id)
        # itera filhos (se existirem)
        if node in adj and adj[node]:
            for child in adj[node]:
                dfs(child, node_id)

    dfs(root)
    return dot

def save_thoughts_graph(files=[]):

    for file in files:
        with open(file, 'r') as f:
            thoughts_graph = json.load(f)
            root = list(thoughts_graph.keys())[0]
            dot = adjacency_to_tree(thoughts_graph, root)
            dot.render(file.replace('.json', ''), view=True)

def save_tree_thoughts_graph(G, filename="tree_of_thoughts_graph"):
    dot = adjacency_to_tree(G, list(G.keys())[0])
    dot.render(directory="core/prompting_techniques/thoughts_graph/", filename=filename, format="pdf", view=True)


# filenames = []
# thoughts_directory = Path('./thoughts_graph/')
# for entry in thoughts_directory.iterdir():
#     if entry.is_file() and entry.suffix == '.json':
#         filenames.append(entry)
# save_thoughts_graph(files=[str(file).replace('\\', '/') for file in filenames])