import os
import sys
import http.client
import re
import constants
from errors import DownloadError, UploadError


def upload_log(node_idx):
    with open(
        os.path.join(constants.LOG_FOLDER, constants.LOG_NAME_FORMAT.format(node_idx)),
        "r",
    ) as f:
        log = f.read()

    # if log == "":
    #     raise Exception("Nothing to upload")

    url_to_parse = f"{constants.LOG_UPLOAD_URL}{node_idx}"

    try:
        connclass, domain, url = parse_url(url_to_parse)
    except TypeError as e:
        raise UploadError("Error parsing upload URL")

    conn = connclass(domain)
    payload = f"text={log}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        conn.request("POST", url, payload, headers)
        res = conn.getresponse()
    except Exception as e:
        raise UploadError(e)

    data = res.read().decode("utf-8")
    if 400 <= res.status < 600:
        raise UploadError(f"{url_to_parse} returned status {res.status}: {data}")

    return True


def download_logs(nodes, target_dir):
    os.makedirs(target_dir, exist_ok=True)

    for n in nodes:
        outfile = os.path.join(target_dir, f"lamport_{n}.log")
        print(f"Downloading log {n} to {outfile}")
        log = download_log(n)
        with open(outfile, "w") as f:
            f.write(log)


def download_log(node_idx):
    url_to_parse = f"{constants.LOG_UPLOAD_URL}/{node_idx}.txt"

    try:
        connclass, domain, url = parse_url(url_to_parse)
    except TypeError as e:
        raise DownloadError("Error parsing URL")

    conn = connclass(domain)

    try:
        conn.request("GET", url)
        res = conn.getresponse()
    except Exception as e:
        raise DownloadError(e)

    data = res.read().decode("utf-8")
    if 400 <= res.status < 600:
        raise DownloadError(f"{url_to_parse} returned status {res.status}: {data}")

    return data


def parse_url(url):
    m = re.match("(http[s]?)://(.+?)(/.+)$", url)
    if m is None:
        return None

    return (
        http.client.HTTPSConnection
        if m.group(1) == "https"
        else http.client.HTTPConnection,
        m.group(2),
        m.group(3),
    )


if __name__ == "__main__":
    try:
        action = sys.argv[1]
        params = sys.argv[2:]

        if action == "upload":
            upload_log(params[0])
        elif action == "download":
            download_logs(params[1:], params[0])
    except IndexError:
        print("Incorrect parameters")
        quit(1)
