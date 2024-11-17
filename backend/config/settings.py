# backend/config/settings.py

import os
from datetime import timedelta

class Config:
    # API Settings
    API_VERSION = "v1"
    API_PREFIX = f"/api/{API_VERSION}"
    
    # Database Settings
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./stock_trading.db")
    
    # Trading Settings
    MIN_PROFIT_THRESHOLD = 0.01  # 1%
    MAX_POSITION_SIZE = 0.1      # 10% of portfolio
    MAX_POSITIONS = 10
    
    # API Keys
    ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    
    # Email Settings
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USERNAME = os.getenv("EMAIL_USERNAME")
    SMTP_PASSWORD = os.getenv("EMAIL_PASSWORD")
    DEFAULT_RECIPIENT = "polis.srikanth@gmail.com"
    
    # WebSocket Settings
    WS_HEARTBEAT_INTERVAL = 30  # seconds
    
    # Cache Settings
    CACHE_TIMEOUT = timedelta(minutes=5)
    
    # Security Settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION = timedelta(days=1)

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "INFO"
    
    # Override with more secure settings
    JWT_EXPIRATION = timedelta(hours=12)
    CACHE_TIMEOUT = timedelta(minutes=1)

# Select config based on environment
env = os.getenv("ENVIRONMENT", "development")
config = ProductionConfig if env == "production" else DevelopmentConfig