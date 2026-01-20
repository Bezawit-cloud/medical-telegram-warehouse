import os
import json
import pandas as pd
import psycopg2
from pathlib import Path

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="medical_telegram_db",
    user="postgres",       # <-- change this
    password="beza091163"  # <-- change this
)
cur = conn.cursor()

# Path to your raw JSON files
RAW_DIR = Path(r"C:\Users\bezis\Downloads\medical-telegram-warehouse\data\raw\telegram_messages\2026-01-19")  # adjust path

for json_file in RAW_DIR.glob("*.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        messages = json.load(f)
    
    for msg in messages:
        cur.execute("""
            INSERT INTO raw.telegram_messages (
                message_id,
                channel_name,
                message_date,
                message_text,
                has_media,
                media_type,
                views,
                forwards
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (message_id) DO NOTHING;
        """, (
            msg.get("message_id"),
            json_file.stem,  # channel_name from filename
            msg.get("date"),
            msg.get("text"),
            msg.get("has_media"),
            msg.get("media_type"),
            msg.get("views"),
            msg.get("forwards")
        ))

conn.commit()
cur.close()
conn.close()

print("✅ JSON data loaded into PostgreSQL successfully!")
