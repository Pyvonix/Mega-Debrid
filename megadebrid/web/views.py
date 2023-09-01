from megadebrid.worker.celery import app as celery_app
from flask import Blueprint, jsonify, request, render_template

from megadebrid.worker.tasks import (
    save_file,
    debrid_and_save_file,
    download_magnet,
    download_torrent,
)
from megadebrid.web.forms import (
    SaveFileForm,
    DebridAndSaveFileForm,
    DownloadMagnetForm,
    DownloadTorrentForm,
)


megaweb = Blueprint(
    "tasks",
    __name__,
)

TASKS_MAPPER = {
    "SaveFile": {"desc": "Save File", "form": SaveFileForm, "func": save_file},
    "DebridAndSaveFile": {
        "desc": "Debrid & Save File",
        "form": DebridAndSaveFileForm,
        "func": debrid_and_save_file,
    },
    "DownloadMagnet": {
        "desc": "Download Magnet",
        "form": DownloadMagnetForm,
        "func": download_magnet,
    },
    "DownloadTorrent": {
        "desc": "Download Torrent",
        "form": DownloadTorrentForm,
        "func": download_torrent,
    },
}


@megaweb.route("/", methods=["GET"])
async def home():
    return render_template("tasks/home.html", actions=TASKS_MAPPER)


@megaweb.route("/tasks", methods=["POST"])
async def run_task():
    post_json = request.get_json()

    if request.headers.get("Mega-Task") not in TASKS_MAPPER.keys():
        return (
            jsonify(
                {
                    "message": "Bad Request",
                    "error": "You need specify a valid value for the header Mega-Task. "
                    f"Allowed values are: { ', '.join(TASKS_MAPPER.keys()) }.",
                }
            ),
            400,
        )

    task_type = request.headers["Mega-Task"]
    task = TASKS_MAPPER[task_type]
    form = task["form"](**post_json)

    if form.validate():
        task = task["func"].delay(**post_json)
        return jsonify({"task_id": task.id}), 202

    return jsonify({"message": "Bad Request", "error": form.errors}), 400


@megaweb.route("/tasks/<task_id>", methods=["GET"])
async def get_status(task_id):
    task_result = celery_app.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
        if isinstance(task_result.result, str)
        else None,
    }
    return jsonify(result), 200
