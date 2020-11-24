from threading import Thread
import socket
from time import perf_counter_ns
from network import create_socket
from logger import setup_logger


class Listener(Thread):
    def __init__(self, index, port, shared_clock):
        super().__init__()
        self.index = index
        self.port = int(port)
        self.shared_clock = shared_clock
        self.running = False
        self.socket = create_socket(1.0, self.port)

        self.logger = setup_logger(self.index)

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
                self.logger.info(
                    f"""{perf_counter_ns() // 1000} {self.index} {self.shared_clock.get()}{node} r {node} {clock}{node}"""
                )
            except socket.timeout:
                pass

        self.socket.close()

    def stop(self):
        self.running = False
