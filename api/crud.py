from sqlalchemy.orm import Session
from sqlalchemy import text

# 1️⃣ Top Products
def get_top_products(db: Session, limit: int = 10):
    query = text("""
        SELECT message_text AS product_name, COUNT(*) AS mentions
        FROM raw.telegram_messages
        GROUP BY message_text
        ORDER BY mentions DESC
        LIMIT :limit
    """)
    return db.execute(query, {"limit": limit}).fetchall()
# chnnel activity

def get_channel_activity(db: Session, channel_name: str):
    query = text("""
        SELECT DATE(message_date) AS date, COUNT(*) AS messages_count
        FROM raw.telegram_messages
        WHERE LOWER(channel_name) = LOWER(:channel_name)
        GROUP BY DATE(message_date)
        ORDER BY date
    """)
    result = db.execute(query, {"channel_name": channel_name}).fetchall()
    
    # Convert each row to a dict and make date a string
    return [{"date": str(row[0]), "messages_count": row[1]} for row in result]

    # Ensure we always return a list
    return [dict(row) for row in result] if result else []


# 3️⃣ Message Search
from sqlalchemy.orm import Session
from sqlalchemy import text

def search_messages(db: Session, keyword: str, limit: int = 20):
    query = text("""
        SELECT message_id,
               channel_name AS channel,
               message_text AS content,
               message_date AS timestamp
        FROM raw.telegram_messages
        WHERE message_text ILIKE '%' || :keyword || '%'
        LIMIT :limit
    """)
    result = db.execute(query, {"keyword": keyword, "limit": limit}).fetchall()
    
    # Convert SQLAlchemy rows to JSON-serializable dicts
    return [
        {
            "message_id": row[0],
            "channel": row[1],
            "content": row[2],
            "timestamp": str(row[3])  # datetime → string
        }
        for row in result
    ]


# 4️⃣ Visual Content Stats
from sqlalchemy.orm import Session
from sqlalchemy import text

def get_visual_content_stats(db: Session):
    query = text("""
        SELECT channel_name AS channel,
               detected_objects,
               COUNT(*) AS total
        FROM raw.yolo_detections
        GROUP BY channel_name, detected_objects
        ORDER BY channel_name, detected_objects
    """)
    result = db.execute(query).fetchall()
    
    # Convert to JSON-serializable dicts
    return [
        {
            "channel": row[0],
            "detected_objects": row[1] if row[1] is not None else "",
            "total": row[2]
        }
        for row in result
    ]


