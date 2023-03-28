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
            "SELECT t.id, t.name, created, owner_id, u.first_name, u.last_name"
            " FROM team t JOIN user u ON t.owner_id = u.id"
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
            "SELECT t.id, t.name, t.created, t.owner_id, u.first_name, u.last_name, u.email"
            " FROM user_team ut"
            " JOIN team t ON ut.team_id = t.id"
            " JOIN user u ON t.owner_id = u.id"
            " WHERE ut.user_id = ?"
            " ORDER BY created DESC",
            (g.user["id"],),
        ).fetchall()

        return render_template("teams/index.jinja", teams=teams)

    return redirect(url_for("auth.login"))


@bp.route("/<int:id>", methods=("GET",))
def team(id):
    team = get_team(id)
    team_members = (
        get_db()
        .execute(
            "SELECT u.id, u.first_name, u.last_name"
            " FROM user_team ut"
            " JOIN team t ON ut.team_id = t.id"
            " JOIN user u ON ut.user_id = u.id"
            " WHERE ut.team_id = ?",
            (id,),
        )
        .fetchall()
    )

    return render_template("teams/team.jinja", team=team, team_members=team_members)


@bp.route("/<int:id>/update", methods=("POST",))
@login_required
def update(id):
    team = get_team(id)
    name = request.form["team_name"]
    email = request.form["owner_email"]
    error = None
    db = get_db()
    new_owner = db.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()

    if not name:
        error = "Name is required"
    elif new_owner is None:
        error = "A user with this email does not exist."
    elif team["owner_id"] != g.user["id"]:
        error = "You are not authorized to make changes to this team."

    if error is not None:
        flash(error)
    else:
        db.execute(
            "UPDATE team SET name = ?, owner_id = ?" " WHERE id = ?",
            (
                name,
                new_owner["id"],
                id,
            ),
        )
        db.commit()

    return redirect(url_for("teams.index"))
