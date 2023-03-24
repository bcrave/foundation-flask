from flask import Blueprint, session, render_template, redirect, url_for
from foundation_server.db import get_db

bp = Blueprint("teams", __name__, url_prefix="/teams")


@bp.route("", methods=("GET", "POST"))
def index():
    user_id = session.get("user_id")

    if user_id is not None:
        db = get_db()
        teams = db.execute(
            "SELECT t.id, name, created, creator_id"
            " FROM team t JOIN user u ON t.creator_id = u.id"
            " ORDER BY created DESC"
        ).fetchall()

        if len(teams) == 0:
            return "No teams created!"
        return render_template("teams/index.jinja", teams=teams)

    return redirect(url_for("auth.login"))
