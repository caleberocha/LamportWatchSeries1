import socket
import pickle
from threading import Thread
from network import create_multicast_socket, create_multicast_socket_for_send
import constants


class Party(Thread):
    def __init__(self, nodes_count):
        super().__init__()
        self.socket = create_multicast_socket(1.0)
        self.nodes_count = nodes_count
        self.nodes = {}
        self.full = False
        self.running = False

    def run(self):
        self.running = True

        while not self.full:
            if not self.running:
                break

            try:
                data, addr = self.socket.recvfrom(1024)
                msg_type, msg_value = parse_data(data)
                if msg_type == "NODE":
                    self.add_node(msg_value, addr)
                elif msg_type == "NODES":
                    self.update_nodes(msg_value)
                else:
                    print("Unknown message")

                if len(self.nodes) == self.nodes_count:
                    self.full = True
            except socket.timeout:
                pass
            finally:
                print(
                    f"\rWaiting for nodes, {self.nodes_count - len(self.nodes)} left",
                    end="",
                )

        print(" " * 40, end="\r")

    def add_node(self, id_node, addr):
        self.nodes[id_node] = ":".join([str(n) for n in addr])
        self.send_nodes()

    def update_nodes(self, nodes):
        for i, n in nodes.items():
            self.nodes[i] = n

    def send_nodes(self):
        send_msg(("NODES", self.nodes))

    def enter(self, id_node):
        send_msg(("NODE", id_node))

    def stop(self):
        self.running = False


def send_msg(msg):
    sock = create_multicast_socket_for_send()
    sock.sendto(pickle.dumps(msg), (constants.MCAST_GROUP, constants.MCAST_PORT))


def parse_data(data):
    msg_type, msg_value = pickle.loads(data)
    return msg_type, msg_value
