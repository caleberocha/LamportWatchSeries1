from threading import Lock


class Clock:
    """Represents the logical clock. To avoid race condition between threads, it uses locks for acessing and setting the clock value."""

    def __init__(self, initial_value=0):
        self.clock = initial_value
        self.lock = Lock()

    def get(self):
        with self.lock:
            return self.clock

    def set(self, value):
        with self.lock:
            self.clock = value

    def increment(self, value=1):
        with self.lock:
            self.clock += value