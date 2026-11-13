import json
import os
import threading
import uuid

from datetime import datetime
from pathlib import Path

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for
)



BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "tasks.json"

DATA_LOCK = threading.Lock()

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key"
)


def read_database():

    DATA_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not DATA_FILE.exists():

        write_database({
            "tasks": []
        })

    try:

        with DATA_FILE.open(
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except (json.JSONDecodeError, OSError):

        data = {
            "tasks": []
        }

    if not isinstance(data, dict) or not isinstance(
        data.get("tasks"), list
    ):

        data = {
            "tasks": []
        }

    return data



def write_database(data):

    DATA_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temporary_file = DATA_FILE.with_suffix(".tmp")

    with temporary_file.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

    temporary_file.replace(DATA_FILE)


def get_tasks():

    with DATA_LOCK:

        return read_database()["tasks"]


def update_tasks(callback):

    with DATA_LOCK:

        data = read_database()

        result = callback(data["tasks"])

        write_database(data)

        return result


def find_task(tasks, task_id):

    return next(
        (
            task for task in tasks
            if task["id"] == task_id
        ),
        None
    )


@app.get("/")
def index():

    tasks = get_tasks()

    pending_tasks = [
        task for task in tasks
        if task["status"] == "pending"
    ]

    completed_tasks = [
        task for task in tasks
        if task["status"] == "completed"
    ]

    return render_template(
        "index.html",
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks
    )


@app.get("/admin")
def admin_panel():

    tasks = get_tasks()

    pending_tasks = [
        task for task in tasks
        if task["status"] == "pending"
    ]

    completed_tasks = [
        task for task in tasks
        if task["status"] == "completed"
    ]

    return render_template(
        "adminpanel.html",
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks
    )


@app.post("/admin/tasks")
def add_task():

    title = request.form.get(
        "title", ""
    ).strip()

    duration = request.form.get(
        "duration", ""
    ).strip()

    if not title or not duration:

        flash(
            "لطفاً عنوان و زمان انجام وظیفه را وارد کنید.",
            "danger"
        )

        return redirect(url_for("admin_panel"))

    task = {

        "id": uuid.uuid4().hex,

        "title": title,

        "duration": duration,

        "manager": "کاربر مدیر",

        "status": "pending",

        "completed_by": None,

        "created_at": datetime.now().isoformat(
            timespec="seconds"
        ),

        "completed_at": None

    }

    update_tasks(
        lambda tasks: tasks.append(task)
    )

    flash(
        "وظیفه با موفقیت ثبت شد.",
        "success"
    )

    return redirect(url_for("admin_panel"))


@app.post("/admin/tasks/<task_id>/edit")
def edit_task(task_id):

    title = request.form.get(
        "title", ""
    ).strip()

    duration = request.form.get(
        "duration", ""
    ).strip()

    if not title or not duration:

        flash(
            "عنوان و زمان انجام نمی‌توانند خالی باشند.",
            "danger"
        )

        return redirect(url_for("admin_panel"))

    def edit(tasks):

        task = find_task(tasks, task_id)

        if task is None or task["status"] != "pending":

            return False

        task["title"] = title

        task["duration"] = duration

        return True

    result = update_tasks(edit)

    if result:

        flash(
            "تغییرات وظیفه ذخیره شد.",
            "success"
        )

    else:
        flash(
            "وظیفه پیدا نشد یا قبلاً انجام شده است.",
            "warning"
        )

    return redirect(url_for("admin_panel"))

@app.post("/admin/tasks/<task_id>/delete")
def delete_task(task_id):

    def delete(tasks):

        before = len(tasks)

        tasks[:] = [
            task for task in tasks
            if task["id"] != task_id
        ]

        return len(tasks) < before
    
    result = update_tasks(delete)

    if result:

        flash(
            "وظیفه حذف شد.",
            "success"
        )

    else:

        flash(
            "وظیفه پیدا نشد.",
            "warning"
        )

    return redirect(url_for("admin_panel"))

@app.post("/tasks/<task_id>/complete")
def complete_task(task_id):

    completed_by = request.form.get(
        "completed_by",
        "کاربر مبین"
    ).strip() or "کاربر مبین"

    def complete(tasks):

        task = find_task(tasks, task_id)

        if task is None or task["status"] != "pending":

            return False

        task["status"] = "completed"

        task["completed_by"] = completed_by

        task["completed_at"] = datetime.now().isoformat(
            timespec="seconds"
        )

        return True

    result = update_tasks(complete)

    if result:

        flash(
            "انجام وظیفه با موفقیت ثبت شد.",
            "success"
        )

    else:
        flash(
            "این وظیفه وجود ندارد یا قبلاً تکمیل شده است.",
            "warning"
        )

    return redirect(url_for("index"))

@app.errorhandler(404)
def not_found(error):

    return "صفحه یا وظیفه موردنظر پیدا نشد.", 404

if __name__ == "__main__":

    app.run(debug=True)
