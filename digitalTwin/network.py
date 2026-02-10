class Network:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node):
        self.nodes[node.node_id] = node
        self.edges[node.node_id] = []

    def connect(self, from_id, to_id):
        if from_id in self.nodes and to_id in self.nodes:
            self.edges[from_id].append(to_id)

    def get_neighbors(self, node_id):
        return self.edges.get(node_id, [])
