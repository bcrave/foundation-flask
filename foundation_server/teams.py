from flask import Blueprint, session, render_template, redirect, url_for, abort
from foundation_server.db import get_db

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
            "SELECT t.id, t.name, created, admin_id, u.first_name, u.last_name"
            " FROM team t JOIN user u ON t.admin_id = u.id"
            " ORDER BY created DESC"
        ).fetchall()

        for team in teams:
            print(team.keys())

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
