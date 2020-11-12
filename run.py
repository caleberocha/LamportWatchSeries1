import sys
from lamport_node import LamportNode
from config_parser import parse_config
from errors import InvalidNodeError


def lamport(config_file, node_index):
    nodes = parse_config(config_file)
    node = LamportNode(nodes, node_index)
    node.start()


if __name__ == "__main__":
    try:
        args = sys.argv[1], int(sys.argv[2])
    except IndexError:
        print("Usage: python3 run.py [config] [index]")
        quit(1)
    except ValueError:
        print(f"Error: Invalid index {sys.argv[2]}")
        quit(2)
    except InvalidNodeError as e:
        print(f"Error: {e}")
        quit(3)

    lamport(*args)
