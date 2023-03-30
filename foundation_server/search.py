from flask import Blueprint, request, render_template
from foundation_server.db import get_db

bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("", methods=("GET",))
def index():
    query = request.args

    db = get_db()
    results = db.execute(
        "SELECT u.id AS user_id, u.first_name, u.last_name, u.email, u.phone, u.username, t.name AS team_name"
        " FROM user_team ut"
        " JOIN user u ON ut.user_id = u.id"
        " JOIN team t ON ut.team_id = t.id"
        f" WHERE first_name LIKE '%{query['term']}%'"
        f" OR last_name LIKE '%{query['term']}%'"
        f" OR username LIKE '%{query['term']}%'"
        f" OR email LIKE '%{query['term']}%'"
        f" OR team_name LIKE '%{query['term']}%'"
        " GROUP BY u.id"
        " ORDER BY last_name",
    ).fetchall()

    return render_template("search.jinja", query=query, results=results)
