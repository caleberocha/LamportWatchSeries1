def parse_config(config_file):
    nodes = {}
    with open(config_file, "r") as f:
        for row in f.readlines():
            row = row.replace("\r", "").replace("\n", "").split(" ")
            nodes[int(row[0])] = {"host": row[1], "port": row[2], "chance": row[3]}
    return nodes