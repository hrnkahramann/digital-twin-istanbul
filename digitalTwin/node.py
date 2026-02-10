class Node:
    def __init__(self, node_id, name, node_type, lat=None, lon=None):
        self.node_id = node_id
        self.name = name
        self.node_type = node_type
        self.lat = lat
        self.lon = lon

        self.state = {}
        self.history = {
            "traffic_density": [],
        }

    def update_state(self, key, value):
        self.state[key] = value

        if key in self.history:
            self.history[key].append(value)

    def get_state(self):
        return self.state
