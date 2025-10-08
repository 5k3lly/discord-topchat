from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import sys
import sqlite3


app = FastAPI()


DB_PATH = "/db/mydb.db"

def connect_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}", file=sys.stderr)
        return None

"""
@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")
"""

@app.get("/test")
async def get_count():
    conn = connect_db()
    if not conn:
        return {"error": "Database failed."}
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM message")
        return {
            "message_count": cursor.fetchall()[0]
        }
    except: 
        print(f"Error on SELECT stmt")
    finally:
        conn.close()

@app.get("/api/users/frequency")
async def get_user_frequency(channels: str = None):
    conn = connect_db()
    if not conn:
        return {"error": "Database connection failed"}
    try:
        cursor = conn.cursor()
        if channels:
            channel_list = channels.split(",")
            placeholders = ",".join("?" for _ in channel_list)
            query = f"SELECT user, COUNT(*) as count FROM message WHERE channel IN ({placeholders}) GROUP BY user"
            cursor.execute(query, channel_list)
        else:
            cursor.execute("SELECT user, COUNT(*) as count FROM message GROUP BY user ORDER BY COUNT(*) DESC")
        rows = cursor.fetchall()
        frequencies = [{"user": row[0], "count": row[1]} for row in rows]
        return {"frequencies": frequencies}
    except sqlite3.Error as e:
        print(f"Error selecting user frequencies: {e}")
        return {"error": str(e)}
    finally:
        conn.close()

@app.get("/api/channels")
async def get_channels():
    conn = connect_db()
    if not conn:
        return {"error": "Database connection failed"}
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT channel FROM message")
        rows = cursor.fetchall()
        channels = [row[0] for row in rows]
        return {"channels": channels}
    except sqlite3.Error as e:
        print(f"Error selecting channels: {e}", file=sys.stderr)
        return {"error": str(e)}
    finally:
        conn.close()

app.mount("/", StaticFiles(directory="static"), name="static")
