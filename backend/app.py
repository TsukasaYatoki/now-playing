import argparse
import os

from flask import Flask, Response, render_template, stream_with_context
from services.monitor import monitor_file

# Resolve frontend path relative to this backend directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
DEFAULT_WATCH_FILE = "/tmp/output.txt"
DEFAULT_INTERVAL = 1.0
DEFAULT_PORT = 3939

# Initialize Flask, pointing to the frontend dir for templates and static files
app = Flask(
    __name__,
    template_folder=FRONTEND_DIR,
    static_folder=FRONTEND_DIR,
    static_url_path="/static",
)
app.config.update(WATCH_FILE=DEFAULT_WATCH_FILE, INTERVAL=DEFAULT_INTERVAL)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stream")
def stream():
    generator = monitor_file(app.config["WATCH_FILE"], app.config["INTERVAL"])
    return Response(stream_with_context(generator), mimetype="text/event-stream")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Web live monitor for new lines in a text file"
    )
    parser.add_argument(
        "-t",
        "--time",
        type=float,
        default=DEFAULT_INTERVAL,
        help="Read interval in seconds",
    )
    parser.add_argument(
        "-f", "--file", type=str, default=DEFAULT_WATCH_FILE, help="File to monitor"
    )
    parser.add_argument(
        "-p", "--port", type=int, default=DEFAULT_PORT, help="Web server port"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    app.config["WATCH_FILE"] = os.path.abspath(args.file)
    app.config["INTERVAL"] = args.time

    app.run(host="127.0.0.1", port=args.port, threaded=True)


if __name__ == "__main__":
    main()
