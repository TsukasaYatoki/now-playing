import argparse
import os

from app import create_app

DEFAULT_INTERVAL = 1.0
DEFAULT_PORT = 3939
DEFAULT_WATCH_FILE = os.path.join(
    os.environ["LOCALAPPDATA"], "VirtualDJ", "History", "tracklist.txt"
)


def parse_args():
    parser = argparse.ArgumentParser(description="Now Playing Monitor")
    parser.add_argument("-t", "--time", type=float, default=DEFAULT_INTERVAL)
    parser.add_argument("-f", "--file", type=str, default=DEFAULT_WATCH_FILE)
    parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT)
    return parser.parse_args()


def main():
    args = parse_args()

    config = {"INTERVAL": args.time, "WATCH_FILE": os.path.abspath(args.file)}
    app = create_app(config)

    app.run(host="127.0.0.1", port=args.port, threaded=True)


if __name__ == "__main__":
    main()
