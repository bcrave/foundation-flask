DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS user_team;

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  username TEXT,
  password TEXT NOT NULL,
  phone TEXT
);

CREATE TABLE IF NOT EXISTS team (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  owner_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name TEXT NOT NULL,
  FOREIGN KEY (owner_id) REFERENCES user (id)
);

CREATE TABLE IF NOT EXISTS user_team (
  user_id INTEGER,
  team_id INTEGER,
  user_role TEXT NOT NULL DEFAULT "user",
  PRIMARY KEY (user_id, team_id),
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (team_id) REFERENCES team (id)
);
