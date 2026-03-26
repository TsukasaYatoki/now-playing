import argparse
import os

from flask import Flask, Response, render_template, stream_with_context
from services.monitor import monitor_file

# Resolve frontend path relative to this backend directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
DATA_DIR = os.path.join(BASE_DIR, "data")
DEFAULT_WATCH_FILE = os.path.join(DATA_DIR, "output.txt")

# Initialize Flask, pointing to the frontend dir for templates and static files
app = Flask(
    __name__,
    template_folder=FRONTEND_DIR,
    static_folder=FRONTEND_DIR,
    static_url_path="/static",
)

# Global configs
WATCH_FILE = DEFAULT_WATCH_FILE
INTERVAL = 1.0
FADE_SPEED = 1000


@app.route("/")
def index():
    return render_template(
        "index.html", filename=os.path.basename(WATCH_FILE), speed=FADE_SPEED
    )


@app.route("/stream")
def stream():
    generator = monitor_file(WATCH_FILE, INTERVAL)
    return Response(stream_with_context(generator), mimetype="text/event-stream")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Web live monitor for new lines in a text file"
    )
    parser.add_argument(
        "-t", "--time", type=float, default=1.0, help="Read interval in seconds"
    )
    parser.add_argument(
        "-f", "--file", type=str, default=DEFAULT_WATCH_FILE, help="File to monitor"
    )
    parser.add_argument(
        "-s", "--speed", type=int, default=1000, help="Fade animation speed in ms"
    )
    parser.add_argument("-p", "--port", type=int, default=3900, help="Web server port")
    return parser.parse_args()


def main():
    global WATCH_FILE, INTERVAL, FADE_SPEED

    args = parse_args()

    WATCH_FILE = os.path.abspath(args.file)
    INTERVAL = args.time
    FADE_SPEED = args.speed

    # Ensure the data directory exists
    os.makedirs(os.path.dirname(WATCH_FILE), exist_ok=True)

    app.run(host="0.0.0.0", port=args.port, threaded=True)


if __name__ == "__main__":
    main()
