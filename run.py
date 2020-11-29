import sys
from time import sleep
from lamport_node import LamportNode
from party import Party
from config_parser import parse_config
from logger import clean_log
from log_api import upload_log
from errors import InvalidNodeError


def lamport(config_file, node_index):
    nodes = parse_config(config_file)

    clean_log(node_index)

    node = LamportNode(nodes, node_index)
    party = Party(len(nodes))
    try:
        party.start()
        party.enter(node_index)
        while party.is_alive():
            sleep(0.1)

        node.start()

        print("Uploading log")
        upload_log(node_index)
        print("FIN")

    except KeyboardInterrupt:
        party.stop()
        node.stop()


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
