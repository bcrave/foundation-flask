from flask import Blueprint, render_template

bp = Blueprint("me", __name__, url_prefix="/me")


@bp.route("")
def index():
    return render_template("me/profile.jinja")


@bp.route("/account")
def account():
    return render_template("me/account.jinja")
