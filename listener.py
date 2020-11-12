from threading import Thread
import random
from time import sleep, perf_counter_ns


class Listener(Thread):
    def __init__(self, index, port, shared_clock):
        super().__init__()
        self.index = index
        self.port = port
        self.shared_clock = shared_clock
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            # Temporary message receiving simulation
            sleep(random.random() * 5)
            clock = random.randint(0, 10) + self.shared_clock.get()
            node = 0
            # TODO listen for messages

            self.shared_clock.set(clock + 1)
            print(
                f"""{self.get_time()} {self.index} {self.shared_clock.get()} r {node} {clock}"""
            )

    def stop(self):
        self.running = False

    def get_time(self):
        return perf_counter_ns() // 1000