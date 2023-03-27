from flask import (
    Blueprint,
    session,
    render_template,
    redirect,
    url_for,
    abort,
    g,
    request,
    flash,
)
from foundation_server.db import get_db
from foundation_server.auth import login_required

bp = Blueprint("teams", __name__, url_prefix="/teams")


def get_team(id):
    team = (
        get_db()
        .execute(
            "SELECT t.id, t.name, created, admin_id, u.first_name, u.last_name"
            " FROM team t JOIN user u ON t.admin_id = u.id"
            " WHERE t.id = ?",
            (id,),
        )
        .fetchone()
    )

    if team is None:
        abort(404, f"Team id {id} does not exist.")

    return team


@bp.route("", methods=("GET", "POST"))
def index():
    user_id = session.get("user_id")

    if user_id is not None:
        db = get_db()
        teams = db.execute(
            "SELECT t.id, t.name, created, admin_id, u.first_name, u.last_name, email"
            " FROM team t JOIN user u ON t.admin_id = u.id"
            " WHERE t.admin_id = ?"
            " OR t.id = ?"
            " ORDER BY created DESC",
            (g.user["id"], g.user["team_id"]),
        ).fetchall()

        return render_template("teams/index.jinja", teams=teams)

    return redirect(url_for("auth.login"))


@bp.route("/<int:id>", methods=("GET",))
def team(id):
    team = get_team(id)
    team_members = (
        get_db()
        .execute(
            "SELECT u.id, first_name, last_name"
            " FROM user u JOIN team t ON u.team_id = t.id"
            " WHERE u.team_id = ?",
            (id,),
        )
        .fetchall()
    )

    return render_template("teams/team.jinja", team=team, team_members=team_members)


@bp.route("/<int:id>/update", methods=("POST",))
@login_required
def update(id):
    name = request.form["team_name"]
    email = request.form["admin_email"]
    error = None
    db = get_db()
    new_admin = db.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()

    if not name:
        error = "Name is required"
    elif new_admin is None:
        error = "A user with this email does not exist."

    if error is not None:
        flash(error)
    else:
        db.execute(
            "UPDATE team SET name = ?, admin_id = ?" " WHERE id = ?",
            (
                name,
                new_admin["id"],
                id,
            ),
        )
        db.commit()

        return redirect(url_for("teams.index"))
