# ML Models package initialization
# backend/models/__init__.py
#from .user import User
from .stock_recommendation import StockRecommendation
from .news_article import NewsArticle

__all__ = ['User', 'StockRecommendation', 'NewsArticle']
