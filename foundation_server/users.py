from flask import Blueprint, abort, render_template, redirect, url_for
from foundation_server.db import get_db

bp = Blueprint("users", __name__, url_prefix="/users")


def get_user(id):
    user = get_db().execute("SELECT * FROM user WHERE id = ?", (id,)).fetchone()
    if user is None:
        abort(404, f"User id {id} does not exist.")

    return user


@bp.route("/<int:id>")
def user(id):
    user = get_user(id)
    if user["id"] == id:
        return redirect(url_for("me.index"))

    return render_template("users/user.jinja")
