# backend/services/news_service.py
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

class NewsService:
    def __init__(self):
        self.rss_feeds = {
            'latest': 'https://www.moneycontrol.com/rss/latestnews.xml',
            'business': 'https://www.moneycontrol.com/rss/business.xml',
            'markets': 'https://www.moneycontrol.com/rss/mcmarkets.xml',
            'tech': 'https://www.moneycontrol.com/rss/technology.xml'
        }
    
    def get_latest_news(self, limit=10):
        """For the homepage - existing method expected by routes"""
        return self.get_news('latest', limit)
    
    def get_news(self, category='latest', limit=15):
        """Get news from RSS feeds"""
        try:
            if category == 'all':
                return self.get_all_news(limit)
            
            feed_url = self.rss_feeds.get(category, self.rss_feeds['latest'])
            feed = feedparser.parse(feed_url)
            
            news_items = []
            
            for entry in feed.entries[:limit]:
                news_item = {
                    'id': entry.get('id', entry.link),
                    'title': entry.title,
                    'link': entry.link,
                    'summary': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': 'MoneyControl',
                    'category': category,
                    'scraped_at': datetime.now().isoformat()
                }
                news_items.append(news_item)
            
            return news_items
            
        except Exception as e:
            print(f"Error fetching news from {category}: {e}")
            return []
    
    def get_market_news(self, limit=10):
        """Get market-specific news"""
        return self.get_news(category='markets', limit=limit)
    
    def get_all_news(self, limit=20):
        """Get news from all categories"""
        all_news = []
        for category in self.rss_feeds.keys():
            news = self.get_news(category, limit=5)
            all_news.extend(news)
        
        # Sort by published date (newest first)
        all_news.sort(key=lambda x: x.get('published', ''), reverse=True)
        return all_news[:limit]
