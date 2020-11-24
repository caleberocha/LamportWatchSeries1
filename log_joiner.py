import os
from glob import glob
import constants

log_entries = []
for item in glob(f"{constants.LOG_FOLDER}/lamport*.log"):
    print(item)
    with open(item, "r") as f:
        log_entries += f.readlines()

log_entries.sort(key=lambda row: int(row.split(" ")[2]))

with open(os.path.join(constants.LOG_FOLDER, "all.log"), "w") as f:
    f.writelines(log_entries)