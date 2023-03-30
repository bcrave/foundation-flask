from flask import Blueprint, render_template, g
from foundation_server.db import get_db

bp = Blueprint("me", __name__, url_prefix="/me")


@bp.route("")
def index():
    teams = (
        get_db()
        .execute(
            "SELECT t.id AS team_id, t.name AS team_name"
            " FROM user_team ut"
            " JOIN team t ON t.id = ut.team_id"
            " JOIN user u ON u.id = ut.user_id"
            " WHERE u.id = ?",
            (g.user["id"],),
        )
        .fetchall()
    )
    return render_template("me/profile.jinja", teams=teams)


@bp.route("/account")
def account():
    return render_template("me/account.jinja")
