# backend/models/news_model.py

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

class NewsSource(BaseModel):
    name: str
    reliability_score: float = Field(default=0.5, ge=0, le=1)
    url: Optional[HttpUrl]

class NewsData(BaseModel):
    title: str
    content: str
    summary: Optional[str]
    source: NewsSource
    published_at: datetime
    url: HttpUrl
    sentiment_score: Optional[float] = Field(default=None, ge=-1, le=1)
    impact_score: Optional[float] = Field(default=None, ge=-1, le=1)
    relevance_score: Optional[float] = Field(default=None, ge=0, le=1)
    keywords: List[str] = []

class NewsAnalysis(BaseModel):
    articles: List[NewsData]
    overall_sentiment: float = Field(default=0, ge=-1, le=1)
    overall_impact: float = Field(default=0, ge=-1, le=1)
    confidence: float = Field(default=0, ge=0, le=1)
    key_topics: List[str]
    analysis_timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "overall_sentiment": 0.65,
                "overall_impact": 0.8,
                "confidence": 0.9,
                "key_topics": ["earnings", "growth", "expansion"],
                "analysis_timestamp": "2024-03-13T14:30:00Z"
            }
        }