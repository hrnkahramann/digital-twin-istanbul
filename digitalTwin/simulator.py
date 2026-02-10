import random
import time

class Simulator:
    def __init__(self, network):
        self.network = network
        self.time_step = 0

    def step(self):
        self.time_step += 1

        for node in self.network.nodes.values():
            if node.node_type == "traffic":
                current = node.state.get("traffic_density", random.randint(30, 70))
                new_value = max(0, min(100, current + random.randint(-5, 5)))
                node.update_state("traffic_density", new_value)

    def run(self, steps=1):
        for _ in range(steps):
            self.step()
            time.sleep(0.1)
