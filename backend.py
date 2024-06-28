import sqlite3

DATABASE_PATH = "database.db"

def get_db_connection():
    return sqlite3.connect(DATABASE_PATH)

def initialize():
    try:
        with get_db_connection() as dbcon:
            cursor = dbcon.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    image BLOB
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    movie_id INTEGER,
                    review TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (movie_id) REFERENCES movies (id)
                )
            """)
            dbcon.commit()
    except Exception as e:
        print("Error found:", e)
        
def createuser(username, password):
    try:
        with get_db_connection() as dbcon:
            cursor = dbcon.cursor()
            cursor.execute("""
                INSERT INTO users (username, password)
                VALUES (?, ?)
            """, (username, password))
            dbcon.commit()
    except Exception as e:
        print("Error found:", e)
        
def login(username, password):
    try:
        with get_db_connection() as dbcon:
            cursor = dbcon.cursor()
            cursor.execute("""
                SELECT * FROM users WHERE username = ? AND password = ?
            """, (username, password))
            return cursor.fetchone() is not None
    except Exception as e:
        print("Error found:", e)
        return False
    
    