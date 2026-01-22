from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .database import get_db
from .schemas import TopProduct, ChannelActivity, MessageSearchResult, VisualContentStats
from .crud import get_top_products, get_channel_activity, search_messages, get_visual_content_stats

app = FastAPI(title="Medical Analytics API")

# 1️⃣ Top Products Endpoint
@app.get("/api/reports/top-products", response_model=List[TopProduct])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    results = get_top_products(db, limit)
    if not results:
        raise HTTPException(status_code=404, detail="No products found")
    return results

# 2️⃣ Channel Activity Endpoint
@app.get("/api/channels/{channel_name}/activity", response_model=List[ChannelActivity])
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    results = get_channel_activity(db, channel_name)
    if not results:
        raise HTTPException(status_code=404, detail="Channel not found")
    return results

# 3️⃣ Message Search Endpoint
@app.get("/api/search/messages", response_model=List[MessageSearchResult])
def search_message(query: str, limit: int = 20, db: Session = Depends(get_db)):
    results = search_messages(db, query, limit)
    if not results:
        raise HTTPException(status_code=404, detail="No messages found")
    return results

# 4️⃣ Visual Content Stats Endpoint
@app.get("/api/reports/visual-content", response_model=List[VisualContentStats])
def visual_content(db: Session = Depends(get_db)):
    results = get_visual_content_stats(db)
    if not results:
        raise HTTPException(status_code=404, detail="No visual content found")
    return results
