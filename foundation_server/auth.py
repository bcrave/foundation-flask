import functools
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    g,
)
from foundation_server.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None

        if email is None:
            error = "Email is required"
        elif password is None:
            error = "Password is required"

        if error is None:
            db = get_db()
            db.execute(
                "INSERT INTO user (email, password) VALUES (?, ?)",
                (email, generate_password_hash(password)),
            )
            db.commit()

            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.jinja")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None
        db = get_db()

        user = db.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()

        if user is None:
            error = "Incorrect email"
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.jinja")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@bp.before_app_request
def get_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view
