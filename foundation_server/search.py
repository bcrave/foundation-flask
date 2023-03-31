from flask import Blueprint, request, render_template
from foundation_server.db import get_db

bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("", methods=("GET",))
def index():
    query = request.args
    db = get_db()
    results = db.execute(
        "SELECT u.id AS user_id, u.first_name, u.last_name, u.email, u.phone, u.username,"
        " GROUP_CONCAT(t.name, ',, ') AS team_names,"
        " GROUP_CONCAT(t.id, ',, ') AS team_ids,"
        " GROUP_CONCAT(t.owner_id, ',, ') AS owner_ids"
        " FROM user_team ut"
        " JOIN user u ON ut.user_id = u.id"
        " JOIN team t ON ut.team_id = t.id"
        " WHERE first_name LIKE ?"
        " OR last_name LIKE ?"
        " OR username LIKE ?"
        " OR email LIKE ?"
        " OR t.name LIKE ?"
        " GROUP BY u.id"
        " ORDER BY last_name",
        (
            f"%{query['term']}%",
            f"%{query['term']}%",
            f"%{query['term']}%",
            f"%{query['term']}%",
            f"%{query['term']}%",
        ),
    ).fetchall()

    return render_template("search.jinja", query=query, results=results)
