import psycopg2
from config import DB_CONFIG

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cur = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            )
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            )
        """)
        self.conn.commit()

    def get_user_id(self, username):
        self.cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
        self.cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        self.conn.commit()
        return self.cur.fetchone()[0]

    def save_session(self, user_id, score, level):
        self.cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
                         (user_id, score, level))
        self.conn.commit()

    def get_top_10(self):
        self.cur.execute("""
            SELECT p.username, g.score, g.level_reached, g.played_at
            FROM game_sessions g
            JOIN players p ON g.player_id = p.id
            ORDER BY g.score DESC LIMIT 10
        """)
        return self.cur.fetchall()

    def get_personal_best(self, user_id):
        self.cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s", (user_id,))
        row = self.cur.fetchone()
        return row[0] if row and row[0] else 0