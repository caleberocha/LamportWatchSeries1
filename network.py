import socket
import errno
import random
from time import perf_counter
from errors import SocketError, SocketTimeout


def create_socket(timeout=None, bind_port=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if bind_port is not None:
        sock.bind(("127.0.0.1", bind_port))
    sock.settimeout(timeout)

    return sock


def bind_random_port(sock):
    while True:
        port = random.randint(10000, 65535)
        try:
            sock.bind(("127.0.0.1", port))
            return port
        except socket.error as e:
            if not e.errno == errno.EADDRINUSE:
                raise SocketError(e)


def wait_response(sock, from_addr, timeout):
    sock.settimeout(0.2)
    start_time = perf_counter()

    while perf_counter() - start_time < timeout:
        try:
            data, addr = sock.recvfrom(32)
            if addr == from_addr and data == b"RECEIVED":
                return True
        except socket.timeout:
            pass

    raise SocketTimeout()