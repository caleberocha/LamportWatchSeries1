from threading import Thread
import socket
from time import perf_counter_ns
from network import create_socket


class Listener(Thread):
    def __init__(self, index, port, shared_clock):
        super().__init__()
        self.index = index
        self.port = int(port)
        self.shared_clock = shared_clock
        self.running = False
        self.socket = create_socket(1.0, self.port)

    def run(self):
        self.running = True
        while self.running:
            try:
                data = self.socket.recv(32)
                node, clock, callback_host, callback_port = data.decode("utf-8").split(
                    " "
                )
                self.socket.sendto(b"RECEIVED", (callback_host, int(callback_port)))

                self.shared_clock.set(max(self.shared_clock.get(), int(clock)) + 1)
                print(
                    f"""{perf_counter_ns() // 1000} {self.index} {self.shared_clock.get()} r {node} {clock}"""
                )
            except socket.timeout:
                pass

        self.socket.close()

    def stop(self):
        self.running = False
