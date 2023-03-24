from flask import Blueprint, session
from foundation_server.db import get_db

bp = Blueprint("teams", __name__, "/teams")


@bp.route("", methods=("GET", "POST"))
def teams():
    user_id = session.get("user_id")

    if user_id is not None:
        db = get_db()
