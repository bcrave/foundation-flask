from flask import Blueprint, abort, render_template, redirect, url_for, g
from foundation_server.db import get_db

bp = Blueprint("users", __name__, url_prefix="/users")


def get_user(id):
    user = get_db().execute("SELECT * FROM user WHERE id = ?", (id,)).fetchone()
    if user is None:
        abort(404, f"User id {id} does not exist.")

    return user


@bp.route("", methods=("GET", "POST"))
def index():
    users = (
        get_db()
        .execute(
            "SELECT u.id, first_name, last_name, team_id, t.name AS team_name"
            " FROM user u JOIN team t ON u.team_id = t.id"
            " WHERE u.team_id = t.id"
        )
        .fetchall()
    )
    return render_template("users/index.jinja", users=users)


@bp.route("/<int:id>")
def user(id):
    user = get_user(id)
    if g.user["id"] == id:
        return redirect(url_for("me.index"))

    return render_template("users/user.jinja", user=user)
