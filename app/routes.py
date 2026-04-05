from flask import Blueprint, Response, current_app, render_template, stream_with_context

from .services import monitor_file

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/stream")
def stream():
    generator = monitor_file(
        current_app.config["WATCH_FILE"], current_app.config["INTERVAL"]
    )
    return Response(stream_with_context(generator), mimetype="text/event-stream")
