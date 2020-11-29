import sys
import os
from glob import glob


def join_logs(log_folder):
    log_entries = []
    log_files = os.path.join(log_folder, "lamport_*.log")
    output = os.path.join(log_folder, "all.log")

    for item in glob(log_files):
        print(item)
        log_entries += [row for row in open(item, "r")]

    log_entries.sort(key=lambda row: int(row.split(" ")[2]))

    print("Saving all.log")
    with open(output, "w") as f:
        f.writelines(log_entries)


if __name__ == "__main__":
    try:
        log_folder = sys.argv[1]
        join_logs(log_folder)
    except IndexError:
        print("Log folder not specified")
        quit(1)