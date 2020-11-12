from time import sleep, perf_counter_ns
import random
import constants
from errors import InvalidNodeError
from listener import Listener
from clock import Clock


class LamportNode:
    def __init__(self, nodes, index):
        self.clock = Clock()

        self.index = index
        self.nodes = nodes

        try:
            self.host = nodes[index]["host"]
            self.port = nodes[index]["port"]
            self.chance = float(nodes[index]["chance"])
        except KeyError:
            raise InvalidNodeError(f"Invalid node {index}")

        # Removes own node from the list to avoid sending messages to itself
        self.nodes.pop(self.index, None)

    def start(self):
        conn_listener = Listener(self.index, self.port, self.clock)
        conn_listener.start()

        for i in range(constants.EVENTS_COUNT):
            sleep(min(random.random() + 0.5, 1))
            self.clock.increment()
            if random.random() <= self.chance:
                # local
                print(f"{self.get_time()} {self.index} {self.clock.get()} l")
            else:
                # remote
                idx, node = self.get_node()
                self.send_message(idx)

        conn_listener.stop()

    def send_message(self, index, node):
        # TODO send message
        print(f"""{self.get_time()} {self.index} {self.clock.get()} s {index}""")

    def get_node(self):
        index = random.choice(list(self.nodes.keys()))
        return index, self.nodes[index]

    def get_time(self):
        return perf_counter_ns() // 1000