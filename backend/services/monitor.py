import os
import time


def monitor_file(watch_file, interval=1.0):
    """Generator that yields new lines from log file."""
    if not os.path.exists(watch_file):
        yield f"data: [System] Waiting for file {watch_file} to be created...\n\n"
        while not os.path.exists(watch_file):
            time.sleep(interval)

    yield f"data: [System] Start monitoring {watch_file}...\n\n"

    with open(watch_file, "r", encoding="utf-8") as file:
        file.seek(0, os.SEEK_END)
        while True:
            line = file.readline()
            if not line:
                time.sleep(interval)
                continue
            yield f"data: {line.rstrip()}\n\n"
