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
                    score REAL,
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
    
def addmovie(title, image):
    try:
        with get_db_connection() as dbcon:
            cursor = dbcon.cursor()
            cursor.execute("""
                INSERT INTO movies (title, image)
                VALUES (?, ?)
            """, (title, image))
            dbcon.commit()
    except Exception as e:
        print("Error found:", e)
        
def getmovies():
    try:
        with get_db_connection() as dbcon:
            cursor = dbcon.cursor()
            cursor.execute("""
                SELECT * FROM movies
            """)
            return cursor.fetchall()
    except Exception as e:
        print("Error found:", e)
        return []
    
def getmovie(movie_id):
    try:
        with get_db_connection() as dbcon:
            cursor = dbcon.cursor()
            cursor.execute("""
                SELECT * FROM movies WHERE id = ?
            """, (movie_id,))
            return cursor.fetchone()
    except Exception as e:
        print("Error found:", e)
        return None
    
def getreviews(movie_id):
    try:
        with get_db_connection() as dbcon:
            cursor = dbcon.cursor()
            cursor.execute("""
                SELECT reviews.*, users.username
                FROM reviews
                INNER JOIN users ON reviews.user_id = users.id
                WHERE reviews.movie_id = ?
            """, (movie_id,))
            return cursor.fetchall()[::-1]
    except Exception as e:
        print("Error found:", e)
        return []
    
def getuserid(username):
    try:
        with get_db_connection() as dbcon:
            cursor = dbcon.cursor()
            cursor.execute("""
                SELECT id FROM users WHERE username = ?
            """, (username,))
            return cursor.fetchone()[0]
    except Exception as e:
        print("Error found:", e)
        return None
    
def addreview(movie_id, user_id, review, score):
    try:
        with get_db_connection() as dbcon:
            cursor = dbcon.cursor()
            cursor.execute("""
                INSERT INTO reviews (user_id, movie_id, review, score)
                VALUES (?, ?, ?, ?)
            """, (user_id, movie_id, review, score))
            dbcon.commit()
    except Exception as e:
        print("Error found:", e)
        
def getuser(user_id):
    try:
        with get_db_connection() as dbcon:
            cursor = dbcon.cursor()
            cursor.execute("""
                SELECT * FROM users WHERE id = ?
            """, (user_id,))
            return cursor.fetchone()
    except Exception as e:
        print("Error found:", e)
        return None
    
def getuserreviews(user_id):
    try:
        with get_db_connection() as dbcon:
            cursor = dbcon.cursor()
            cursor.execute("""
                SELECT reviews.*, movies.title
                FROM reviews
                INNER JOIN movies ON reviews.movie_id = movies.id
                WHERE reviews.user_id = ?
            """, (user_id,))
            return cursor.fetchall()[::-1]
    except Exception as e:
        print("Error found:", e)
        return []