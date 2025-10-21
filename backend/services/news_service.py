import os
import requests
from datetime import datetime, timedelta
import time
import feedparser

class NewsService:
    def __init__(self):
        self.newsapi_key = os.getenv('NEWS_API_KEY', 'c9e369d1f1b34b6e9b4014f2fde08a2f')
        self.use_newsapi = bool(self.newsapi_key)
        
        # Fallback RSS feeds
        self.fallback_feeds = [
            'https://feeds.finance.yahoo.com/rss/2.0/headline?s=%5EGSPC,%5EDJI,%5EIXIC,AAPL,MSFT,GOOGL&region=US&lang=en-US',
            'https://www.investing.com/rss/news_25.rss',
            'https://feeds.content.dowjones.io/public/rss/mw_business'
        ]
        
        self.cache = {}
        self.cache_time = None
        self.cache_duration = 1800  # 30 minutes cache
    
    def get_latest_news(self, limit=15):
        """Get fresh news using NewsAPI with RSS fallback"""
        current_time = time.time()
        
        # Return cached news if still valid
        if (self.cache_time and 
            current_time - self.cache_time < self.cache_duration and 
            'news' in self.cache):
            return self.cache['news'][:limit]
        
        try:
            # Try NewsAPI first (paid, fresh news)
            if self.use_newsapi:
                newsapi_news = self._get_newsapi_news(limit)
                if newsapi_news:
                    self.cache['news'] = newsapi_news
                    self.cache_time = current_time
                    return newsapi_news[:limit]
            
            # Fallback to RSS feeds
            rss_news = self._get_rss_news(limit)
            if rss_news:
                self.cache['news'] = rss_news
                self.cache_time = current_time
                return rss_news[:limit]
            
            # Final fallback
            fallback_news = self._get_fallback_news()
            self.cache['news'] = fallback_news
            self.cache_time = current_time
            return fallback_news[:limit]
            
        except Exception as e:
            print(f"Error in get_latest_news: {e}")
            return self.cache.get('news', self._get_fallback_news())[:limit]
    
    def _get_newsapi_news(self, limit=15):
        """Get fresh news from NewsAPI (your paid service)"""
        try:
            # NewsAPI endpoint for business news
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                'category': 'business',
                'language': 'en',
                'pageSize': limit,
                'apiKey': self.newsapi_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'ok' and data['articles']:
                    return self._format_newsapi_articles(data['articles'])
                else:
                    print(f"NewsAPI returned no articles: {data.get('message', 'Unknown error')}")
            else:
                print(f"NewsAPI error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"NewsAPI request failed: {e}")
        
        return None
    
    def _format_newsapi_articles(self, articles):
        """Format NewsAPI articles to our standard format"""
        formatted_news = []
        
        for article in articles:
            # Only include articles from last 24 hours
            published_at = article.get('publishedAt', '')
            if published_at and not self._is_within_24_hours(published_at):
                continue
                
            formatted_article = {
                'id': f"newsapi_{hash(article['url'])}",
                'title': article.get('title', 'Financial News'),
                'link': article.get('url', '#'),
                'summary': article.get('description', 'Latest financial news update.'),
                'published': self._format_iso_date(published_at),
                'source': article.get('source', {}).get('name', 'NewsAPI'),
                'category': 'business',
                'scraped_at': datetime.now().isoformat(),
                'timestamp': time.time()
            }
            formatted_news.append(formatted_article)
        
        return formatted_news
    
    def _is_within_24_hours(self, iso_date_string):
        """Check if article is from last 24 hours"""
        try:
            article_date = datetime.fromisoformat(iso_date_string.replace('Z', '+00:00'))
            return (datetime.now() - article_date) < timedelta(hours=24)
        except:
            return True  # If we can't parse, include it
    
    def _format_iso_date(self, iso_date_string):
        """Convert ISO date to RSS format"""
        try:
            dt = datetime.fromisoformat(iso_date_string.replace('Z', '+00:00'))
            return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
        except:
            return datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    def _get_rss_news(self, limit=15):
        """Fallback to RSS feeds"""
        all_news = []
        
        for feed_url in self.fallback_feeds:
            if len(all_news) >= limit:
                break
                
            try:
                feed_news = self._fetch_rss_feed(feed_url, 5)
                if feed_news:
                    all_news.extend(feed_news)
                    time.sleep(0.5)
            except Exception as e:
                print(f"RSS feed error {feed_url}: {e}")
                continue
        
        return self._process_news(all_news, limit)
    
    def _fetch_rss_feed(self, feed_url, limit=5):
        """Fetch from RSS feed"""
        try:
            feed = feedparser.parse(feed_url)
            news_items = []
            
            for entry in feed.entries[:limit]:
                news_item = {
                    'id': f"rss_{hash(entry.link)}",
                    'title': entry.title,
                    'link': entry.link,
                    'summary': entry.get('summary', 'Financial market update'),
                    'published': entry.get('published', datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')),
                    'source': self._get_source_name(feed_url),
                    'category': 'markets',
                    'scraped_at': datetime.now().isoformat(),
                    'timestamp': time.time()
                }
                news_items.append(news_item)
            
            return news_items
        except Exception as e:
            print(f"Error parsing RSS {feed_url}: {e}")
            return []
    
    def _process_news(self, news_items, limit):
        """Remove duplicates and sort"""
        unique_news = []
        seen_titles = set()
        
        for item in news_items:
            title_key = item['title'].lower()[:40]
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_news.append(item)
        
        # Sort by timestamp (newest first)
        unique_news.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        return unique_news[:limit]
    
    def _get_source_name(self, feed_url):
        """Get source name from URL"""
        if 'yahoo' in feed_url:
            return 'Yahoo Finance'
        elif 'investing' in feed_url:
            return 'Investing.com'
        elif 'marketwatch' in feed_url:
            return 'MarketWatch'
        else:
            return 'Financial News'
    
    def _get_fallback_news(self):
        """Generate fallback news"""
        current_time = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        return [{
            'id': f"fallback_{i}",
            'title': f"Financial Market Update {i+1}",
            'link': '#',
            'summary': 'Latest financial news and market updates',
            'published': current_time,
            'source': 'Market News',
            'category': 'markets',
            'scraped_at': datetime.now().isoformat(),
            'timestamp': time.time()
        } for i in range(10)]
    
    # Keep existing method signatures
    def get_news(self, category='latest', limit=15):
        return self.get_latest_news(limit)
    
    def get_market_news(self, limit=10):
        return self.get_latest_news(limit)
    
    def get_all_news(self, limit=20):
        return self.get_latest_news(limit)
