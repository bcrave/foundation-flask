import sqlite3
import click
from foundation_server.seed_data import users, teams
from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db(index=False):
    db = get_db()
    if not index:
        with current_app.open_resource("schema.sql") as f:
            db.executescript(f.read().decode("utf-8"))
    else:
        with current_app.open_resource("index.sql") as f:
            db.executescript(f.read().decode("utf-8"))


def seed_data():
    db = get_db()

    user_id = 1
    for user in users:
        db.execute(
            "INSERT INTO user (first_name, last_name, email, username, password, phone)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (
                user["first_name"],
                user["last_name"],
                user["email"],
                user["username"],
                generate_password_hash(user["password"]),
                user["phone"],
            ),
        )

        for team_id in user["collabs"]:
            db.execute(
                "INSERT INTO user_team (user_id, team_id) VALUES (?, ?)",
                (user_id, team_id),
            )

        user_id += 1

    for team in teams:
        db.execute(
            "INSERT INTO team (name, owner_id)" " VALUES (?, ?)",
            (
                team["name"],
                team["owner_id"],
            ),
        )

    db.commit()


@click.command("init-db")
def init_db_command():
    click.echo("Creating tables...")
    init_db()

    click.echo("Seeding data...")
    seed_data()

    click.echo("Indexing database...")
    init_db(index=True)

    click.echo("Initialized the database")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
