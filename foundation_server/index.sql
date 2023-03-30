DROP INDEX IF EXISTS idx_username_email;
DROP INDEX IF EXISTS team_name;

CREATE INDEX IF NOT EXISTS idx_username_email ON user (first_name, last_name, username, email);
CREATE INDEX IF NOT EXISTS team_name ON team (name);