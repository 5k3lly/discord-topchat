from selfcord import Client
# from selfcord.ext import commands
import logging
import sqlite3
from os import getenv
from dotenv import load_dotenv

DB_PATH = "/db/mydb.db"

load_dotenv()
TOKEN = getenv("TOKEN")

def connect_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}", file=sys.stderr)
        return None

client = Client()

@client.event
async def on_message(message):
    
    user = getattr(message.author, 'nick', None)
    if user is None:
        user = message.author.global_name

    text = message.content
    channel = message.channel.name

    print(f'User: {user} | Channel: {channel} | Text: {text})')

    try: 
        with connect_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO message ( user,msg,channel ) VALUES (?, ?, ?)", 
                (user, text, channel) 
            )

    except sqlite3.Error as e:
        print(f"error on insert: {e}", file=sys.stderr)
    
client.run(TOKEN)