from pydantic import BaseModel
from typing import List

class TopProduct(BaseModel):
    product_name: str
    mentions: int

class ChannelActivity(BaseModel):
    date: str
    messages_count: int

class MessageSearchResult(BaseModel):
    message_id: int
    channel: str
    content: str
    timestamp: str

class VisualContentStats(BaseModel):
    channel: str
    detected_objects: str
    total: int
