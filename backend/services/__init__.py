# Services package initialization
# backend/services/__init__.py
from .news_service import NewsService
from .stock_service import StockService
from .recommendation_service import RecommendationService
from .email_service import EmailService

__all__ = [
    'NewsService',
    'StockService', 
    'RecommendationService',
    'EmailService'
]
