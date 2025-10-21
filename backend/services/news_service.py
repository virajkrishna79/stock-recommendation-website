import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import time

class NewsService:
    def __init__(self):
        self.rss_feeds = {
            'latest': 'https://www.moneycontrol.com/rss/latestnews.xml',
            'business': 'https://www.moneycontrol.com/rss/business.xml',
            'markets': 'https://www.moneycontrol.com/rss/mcmarkets.xml',
            'tech': 'https://www.moneycontrol.com/rss/technology.xml',
            # New fallback sources
            'yahoo_finance': 'https://finance.yahoo.com/news/rssindex',
            'investing': 'https://news.google.com/rss/search?q=stocks+market+investing&hl=en-US&gl=US&ceid=US:en'
        }
    
    def get_latest_news(self, limit=10):
        """For the homepage - existing method expected by routes"""
        return self.get_news('latest', limit)
    
    def get_news(self, category='latest', limit=15):
        """Get news from RSS feeds - UPDATED with fallback"""
        try:
            # First try MoneyControl as before
            moneycontrol_news = self._get_moneycontrol_news(category, limit)
            
            # If we got good results, return them
            if moneycontrol_news and self._is_recent_news(moneycontrol_news):
                return moneycontrol_news
            
            # If MoneyControl fails or has old news, try fallback
            print(f"MoneyControl news outdated or empty, trying fallback sources...")
            fallback_news = self._get_fallback_news(limit)
            
            # Combine and deduplicate
            all_news = moneycontrol_news + fallback_news
            unique_news = self._remove_duplicates(all_news)
            
            return unique_news[:limit]
            
        except Exception as e:
            print(f"Error in get_news: {e}, using fallback")
            return self._get_fallback_news(limit)
    
    def _get_moneycontrol_news(self, category='latest', limit=15):
        """Your original MoneyControl logic"""
        try:
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
            print(f"Error fetching MoneyControl news from {category}: {e}")
            return []
    
    def _get_fallback_news(self, limit=10):
        """Fallback to other news sources if MoneyControl fails"""
        try:
            fallback_news = []
            
            # Try Yahoo Finance
            try:
                yahoo_feed = feedparser.parse(self.rss_feeds['yahoo_finance'])
                for entry in yahoo_feed.entries[:5]:
                    news_item = {
                        'id': entry.get('id', entry.link),
                        'title': entry.title,
                        'link': entry.link,
                        'summary': entry.get('summary', entry.title),
                        'published': entry.get('published', ''),
                        'source': 'Yahoo Finance',
                        'category': 'markets',
                        'scraped_at': datetime.now().isoformat()
                    }
                    fallback_news.append(news_item)
            except Exception as e:
                print(f"Yahoo Finance fallback failed: {e}")
            
            # Try Google News search for investing
            try:
                investing_feed = feedparser.parse(self.rss_feeds['investing'])
                for entry in investing_feed.entries[:5]:
                    news_item = {
                        'id': entry.get('id', entry.link),
                        'title': entry.title,
                        'link': entry.link,
                        'summary': entry.get('summary', 'Latest market updates'),
                        'published': entry.get('published', ''),
                        'source': 'Google News',
                        'category': 'markets',
                        'scraped_at': datetime.now().isoformat()
                    }
                    fallback_news.append(news_item)
            except Exception as e:
                print(f"Investing news fallback failed: {e}")
            
            return fallback_news[:limit]
            
        except Exception as e:
            print(f"All fallback sources failed: {e}")
            return []
    
    def _is_recent_news(self, news_items, max_hours_old=48):
        """Check if news is reasonably recent"""
        if not news_items:
            return False
        
        try:
            # Check the first few items for recency
            for item in news_items[:3]:
                published_str = item.get('published', '')
                if published_str:
                    # Simple check - if it contains today's or yesterday's date
                    today = datetime.now().strftime('%d %b')
                    yesterday = (datetime.now() - timedelta(days=1)).strftime('%d %b')
                    if today in published_str or yesterday in published_str:
                        return True
            return False
        except:
            return True  # If we can't determine, assume it's okay
    
    def _remove_duplicates(self, news_items):
        """Remove obvious duplicates"""
        seen_titles = set()
        unique_news = []
        
        for item in news_items:
            title_lower = item['title'].lower()
            if title_lower not in seen_titles:
                seen_titles.add(title_lower)
                unique_news.append(item)
        
        return unique_news
    
    # Keep all your existing methods exactly as they were
    def get_market_news(self, limit=10):
        """Get market-specific news"""
        return self.get_news(category='markets', limit=limit)
    
    def get_all_news(self, limit=20):
        """Get news from all categories"""
        all_news = []
        for category in ['latest', 'markets', 'business']:
            news = self.get_news(category, limit=5)
            all_news.extend(news)
        
        # Sort by published date (newest first)
        all_news.sort(key=lambda x: x.get('published', ''), reverse=True)
        return all_news[:limit]
