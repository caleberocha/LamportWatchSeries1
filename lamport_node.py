from time import sleep, perf_counter_ns
import random
import constants
from errors import InvalidNodeError, SocketTimeout
from listener import Listener
from clock import Clock
from network import create_socket, bind_random_port, wait_response
from logger import setup_logger


class LamportNode:
    def __init__(self, nodes, index):
        self.clock = Clock()

        self.index = index
        self.nodes = {i: n for i, n in nodes.items()}

        try:
            self.host = nodes[index]["host"]
            self.port = int(nodes[index]["port"])
            self.chance = float(nodes[index]["chance"])
        except KeyError:
            raise InvalidNodeError(f"Invalid node {index}")

        # Removes own node from the list to avoid sending messages to itself
        self.nodes.pop(self.index, None)

        self.running = False

        self.logger = setup_logger(self.index)

    def start(self):
        self.running = True
        conn_listener = Listener(self.index, self.port, self.clock)
        conn_listener.start()

        for i in range(constants.EVENTS_COUNT):
            if not self.running:
                break

            sleep(min(random.random() + 0.5, 1))
            self.clock.increment()
            if random.random() <= self.chance:
                # local
                self.logger.info(f"{perf_counter_ns() // 1000} {self.index} {self.clock.get()}{self.index} l")
            else:
                # remote
                idx, node = self.get_node()
                try:
                    self.send_message(idx, node)
                except SocketTimeout:
                    print(
                        f"""Error: Timeout sending message to node {idx} ({node["host"]}:{node["port"]})"""
                    )
                    break

        conn_listener.stop()

    def send_message(self, index, node):
        node_addr = (node["host"], node["port"])
        clock = self.clock.get()
        sock = create_socket()
        callback_port = bind_random_port(sock)

        sock.sendto(
            f"{self.index} {clock} {self.host} {callback_port}".encode("utf-8"),
            node_addr,
        )
        wait_response(sock, node_addr, 3.0)

        sock.close()

        self.logger.info(f"""{perf_counter_ns() // 1000} {self.index} {clock}{self.index} s {index}""")

    def get_node(self):
        index = random.choice(list(self.nodes.keys()))
        return index, self.nodes[index]

    def stop(self):
        self.running = False